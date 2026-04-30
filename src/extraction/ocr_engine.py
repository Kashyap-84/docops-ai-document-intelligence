from pathlib import Path
from PIL import Image
import pytesseract

from src.preprocessing.image_cleaner import clean_image


def extract_text_from_image(image_path: str | Path, clean: bool = True) -> str:
    image: Image.Image
    if clean:
        image = clean_image(image_path)
    else:
        image = Image.open(image_path)

    text = pytesseract.image_to_string(image)
    return text.strip()


def extract_text_from_pil(image: Image.Image) -> str:
    return pytesseract.image_to_string(image).strip()
