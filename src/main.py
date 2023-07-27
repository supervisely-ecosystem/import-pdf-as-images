from pathlib import Path

import supervisely as sly

import sly_globals as g
from utils import pages_to_images_from_folder_or_file, download_project


def convert_pdf_to_images_on_agent(api: sly.Api) -> Path:
    local_project_path = download_project(api, g.INPUT_PATH)

    for folder_or_file in local_project_path.iterdir():
        if folder_or_file.is_file():
            dataset_name = g.DEFAULT_DATASET_NAME
        else:
            dataset_name = folder_or_file.name

        local_path = g.CONVERTED_LOCAL_DIR / dataset_name
        local_path.mkdir(parents=True, exist_ok=True)
        pages_to_images_from_folder_or_file(
            folder_or_file,
            local_path,
            g.DPI,
            api.logger
        )
    return local_project_path


@sly.timeit
def import_pdf_as_img(api: sly.Api, task_id: int):
    dir_info = api.file.list(g.TEAM_ID, g.INPUT_PATH)
    if len(dir_info) == 0:
        raise Exception(f"There are no files in selected directory: '{g.INPUT_PATH}'")

    local_pdf_dir = convert_pdf_to_images_on_agent(api)

    if g.PROJECT_ID is None:
        project_name = (
            Path(g.INPUT_PATH).name
            if len(g.OUTPUT_PROJECT_NAME) == 0
            else g.OUTPUT_PROJECT_NAME
        )
        project = api.project.create(
            workspace_id=g.WORKSPACE_ID,
            name=project_name,
            change_name_if_conflict=True
        )
    else:
        project = api.project.get_info_by_id(g.PROJECT_ID)

    if g.DATASET_ID is not None:
        dataset_info = api.dataset.get_info_by_id(g.DATASET_ID)

    for dataset_path in g.CONVERTED_LOCAL_DIR.iterdir():
        if g.DATASET_ID is None:
            dataset_info = api.dataset.create(
                project_id=project.id,
                name=dataset_path.name,
                change_name_if_conflict=True,
            )

        img_paths = list(dataset_path.iterdir())
        img_names = [p.name for p in img_paths]

        batch_size = 10
        total = len(img_names)
        progress = sly.Progress(
            f"Uploading images to dataset {dataset_info.name}",
            total_cnt=total
        )

        for pos, (batch_names, batch_paths) in enumerate(zip(
            sly.batched(seq=img_names, batch_size=batch_size),
            sly.batched(seq=img_paths, batch_size=batch_size),
        ), start=1):
            batch_names = [str(bn) for bn in batch_names]
            api.image.upload_paths(
                dataset_id=dataset_info.id,
                names=batch_names,
                paths=batch_paths,
            )
            current = min(pos * batch_size, total)
            progress.set(current, total, report=True)

        progress.set_current_value(total, True)

    sly.fs.remove_dir(dir_=str(g.CONVERTED_LOCAL_DIR))
    sly.fs.remove_dir(dir_=str(local_pdf_dir))

    if g.REMOVE_SOURCE and not g.IS_ON_AGENT:
        api.file.remove(team_id=g.TEAM_ID, path=g.INPUT_PATH)
        source_dir_name = Path(g.INPUT_PATH).parent.name
        api.logger.info(msg=f"Source directory: '{source_dir_name}' was successfully removed.")

    api.task.set_output_project(task_id=task_id, project_id=project.id, project_name=project.name)


if __name__ == "__main__":
    import_pdf_as_img(g.api, g.TASK_ID)