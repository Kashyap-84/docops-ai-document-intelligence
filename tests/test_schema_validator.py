from src.extraction.schema_validator import validate_extraction


def test_review_required_when_total_missing():
    doc = validate_extraction(
        {
            "document_type": "receipt",
            "vendor_name": "ABC Market",
            "total": None,
            "raw_text": "ABC Market",
            "confidence": 0.5,
        }
    )
    assert doc.review_required is True
    assert "Missing total" in doc.review_reasons
