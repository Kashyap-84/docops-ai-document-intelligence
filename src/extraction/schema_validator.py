from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class LineItem(BaseModel):
    description: str = Field(default="unknown")
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


class ExtractedDocument(BaseModel):
    document_type: str = Field(default="receipt")
    vendor_name: Optional[str] = None
    invoice_number: Optional[str] = None
    transaction_date: Optional[date] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: str = Field(default="USD")
    line_items: List[LineItem] = Field(default_factory=list)
    raw_text: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    review_required: bool = Field(default=True)
    review_reasons: List[str] = Field(default_factory=list)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper().strip() if value else "USD"


def validate_extraction(payload: dict) -> ExtractedDocument:
    doc = ExtractedDocument(**payload)
    reasons = []

    if not doc.vendor_name:
        reasons.append("Missing vendor_name")
    if doc.total is None:
        reasons.append("Missing total")
    if doc.confidence < 0.70:
        reasons.append("Low extraction confidence")
    if doc.total is not None and doc.total < 0:
        reasons.append("Invalid negative total")

    doc.review_reasons = reasons
    doc.review_required = len(reasons) > 0
    return doc
