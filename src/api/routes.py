from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.extraction.ocr_engine import extract_text_from_image
from src.extraction.field_extractor import extract_fields
from src.extraction.schema_validator import ExtractedDocument, validate_extraction
from src.review.review_queue import add_to_review_queue

router = APIRouter(prefix="/api/v1", tags=["document-intelligence"])

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "docops-ai"}


@router.post("/extract", response_model=ExtractedDocument)
async def extract_document(file: UploadFile = File(...)) -> ExtractedDocument:
    suffix = Path(file.filename or "uploaded_file").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only image files are supported in this MVP: png, jpg, jpeg, tiff, bmp.",
        )

    try:
        content = await file.read()
        with NamedTemporaryFile(delete=True, suffix=suffix) as tmp:
            tmp.write(content)
            tmp.flush()
            raw_text = extract_text_from_image(tmp.name)

        extracted_payload = extract_fields(raw_text)
        validated_doc = validate_extraction(extracted_payload)

        if validated_doc.review_required:
            add_to_review_queue(validated_doc)

        return validated_doc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
