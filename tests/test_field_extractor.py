from src.extraction.field_extractor import extract_fields


def test_extract_fields_from_receipt_text():
    text = """
    ABC Market
    Receipt # R12345
    Date: 04/10/2026
    Subtotal: $20.00
    Tax: $1.50
    Total: $21.50
    """
    result = extract_fields(text)
    assert result["vendor_name"] == "ABC Market"
    assert result["invoice_number"] == "R12345"
    assert result["transaction_date"] == "2026-04-10"
    assert result["total"] == 21.50
