import fitz
from typing import Tuple
from pathlib import Path
from logging import Logger


def pages_to_images(
    doc_path: Path,
    save_path: Path,
    dpi: int,
    logger: Logger,
    filetype: str = "pdf",
):
    name, is_pdf = get_file_name_and_check_type(doc_path, filetype)

    if not is_pdf:
        logger.warning(f"The file type for document {name} is wrong or it lacks a format.")
        logger.warning("Trying to read as PDF.")
    
    doc = fitz.Document(filename=doc_path, filetype=filetype)
    
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        pix_save_path = save_path / f"{name}_page_{page.number}.png"
        pix.save(pix_save_path)


def get_file_name_and_check_type(doc_path: Path, filetype: str = "pdf") -> Tuple[str, bool]:
    name = doc_path.name
    name_parts = name.split('.')

    if name_parts[-1] == filetype:
        return ".".join(name_parts[:-1]), True
    else:
        return name, False
