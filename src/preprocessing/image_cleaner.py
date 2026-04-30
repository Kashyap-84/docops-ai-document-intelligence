from pathlib import Path
import cv2
import numpy as np
from PIL import Image


def clean_image(image_path: str | Path) -> Image.Image:
    """Basic document image cleanup for OCR.

    Steps:
    1. Read image.
    2. Convert to grayscale.
    3. Denoise.
    4. Apply adaptive thresholding.
    """
    path = str(image_path)
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Unable to read image: {path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    thresholded = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2,
    )
    return Image.fromarray(thresholded.astype(np.uint8))
