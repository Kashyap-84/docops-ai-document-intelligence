from pathlib import Path
from typing import List
from pdf2image import convert_from_path
from PIL import Image


def pdf_to_images(pdf_path: str | Path, dpi: int = 200) -> List[Image.Image]:
    """Convert a PDF into page images.

    Requires poppler installed locally.
    macOS: brew install poppler
    Ubuntu: sudo apt-get install poppler-utils
    """
    return convert_from_path(str(pdf_path), dpi=dpi)
