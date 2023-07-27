from pathlib import Path

import supervisely as sly

import sly_globals as g
from utils import pages_to_images_from_folder_or_file, download_project


def convert_pdf_to_images_on_agent(api: sly.Api):
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
    

@sly.timeit
def import_pdf_as_img(api: sly.Api, task_id: int):
    dir_info = api.file.list(g.TEAM_ID, g.INPUT_PATH)
    convert_pdf_to_images_on_agent(api)

    if len(dir_info) == 0:
        raise Exception(f"There are no files in selected directory: '{g.INPUT_PATH}'")

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

    if g.IS_ON_AGENT:
        sly.logger.info(f"Data will be downloaded: {g.INPUT_PATH}")
        download_project(api, g.INPUT_PATH)


if __name__ == "__main__":
    import_pdf_as_img(g.api, g.TASK_ID)