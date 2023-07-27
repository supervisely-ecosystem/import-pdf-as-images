import fitz
from typing import Tuple, Union
from pathlib import Path
from logging import Logger

import supervisely as sly

import sly_globals as g


def pages_to_images_from_folder_or_file(
    folder_or_file_path: Union[Path, str],
    save_path: Union[Path, str],
    dpi: int,
    logger: Logger,
    filetype: str = "pdf",
):
    folder_or_file_path = Path(folder_or_file_path)
    if folder_or_file_path.is_file():
        pages_to_images(folder_or_file_path, save_path, dpi, logger, filetype)
    else:
        for doc_path in folder_or_file_path.iterdir():
            pages_to_images(doc_path, save_path, dpi, logger, filetype)


def pages_to_images(
    doc_path: Union[Path, str],
    save_path: Union[Path, str],
    dpi: int,
    logger: Logger,
    filetype: str = "pdf",
):
    doc_path = Path(doc_path)
    save_path = Path(save_path)

    name, is_pdf = get_file_name_and_check_type(doc_path, filetype)

    if not is_pdf:
        logger.warning(f"The file extention for document {name} is wrong or there is no extension founded.")
        logger.warning("Trying to read as PDF.")
    
    doc = fitz.Document(filename=doc_path, filetype=filetype)
    
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        pix_save_path = save_path / f"{name}_page_{page.number}.png"
        pix.save(pix_save_path)


def get_file_name_and_check_type(doc_path: Path, filetype: str = "pdf") -> Tuple[str, bool]:
    suffix = doc_path.suffix
    if len(suffix) > 0:
        suffix = suffix[1:]

    if suffix == filetype:
        return doc_path.stem, True
    else:
        return doc_path.name, False


def download_project(api: sly.Api, input_path: Union[str, Path]) -> Path:
    remote_proj_dir = input_path

    if api.file.is_on_agent(str(input_path)):
        _, path_on_agent = api.file.parse_agent_id_and_path(str(input_path))
    else:
        path_on_agent = (
            remote_proj_dir
            if not remote_proj_dir.startswith("/")
            else remote_proj_dir[1:]
        )

    local_save_dir = Path(g.STORAGE_DIR) / str(path_on_agent)
    local_save_dir.resolve().absolute()

    api.file.download_directory(
        g.TEAM_ID,
        remote_path=str(remote_proj_dir),
        local_save_path=str(local_save_dir)
    )
    return local_save_dir
