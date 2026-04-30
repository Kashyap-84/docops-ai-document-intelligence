import re
from datetime import datetime
from typing import Optional

MONEY_PATTERN = re.compile(r"(?:\$\s*)?(\d{1,6}(?:,\d{3})*(?:\.\d{2})?)")
DATE_PATTERNS = [
    "%m/%d/%Y",
    "%m/%d/%y",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d/%m/%Y",
]


def _to_float(value: str | None) -> Optional[float]:
    if not value:
        return None
    try:
        return float(value.replace(",", ""))
    except ValueError:
        return None


def _find_money_after(label: str, text: str) -> Optional[float]:
    pattern = re.compile(rf"{label}\s*[:\-]?\s*\$?\s*(\d{{1,6}}(?:,\d{{3}})*(?:\.\d{{2}})?)", re.I)
    match = pattern.search(text)
    return _to_float(match.group(1)) if match else None


def _find_date(text: str) -> Optional[str]:
    candidates = re.findall(r"\b\d{1,4}[/-]\d{1,2}[/-]\d{2,4}\b", text)
    for candidate in candidates:
        for fmt in DATE_PATTERNS:
            try:
                return datetime.strptime(candidate, fmt).date().isoformat()
            except ValueError:
                continue
    return None


def _find_invoice_number(text: str) -> Optional[str]:
    match = re.search(r"(?:invoice|inv|receipt)\s*(?:no|number|#)?\s*[:\-#]?\s*([A-Z0-9\-]{4,})", text, re.I)
    return match.group(1).strip() if match else None


def _guess_vendor(text: str) -> Optional[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None
    for line in lines[:5]:
        if len(line) >= 3 and not re.search(r"total|tax|subtotal|invoice", line, re.I):
            return line[:80]
    return lines[0][:80]


def _confidence(payload: dict) -> float:
    score = 0.15
    if payload.get("vendor_name"):
        score += 0.20
    if payload.get("transaction_date"):
        score += 0.15
    if payload.get("invoice_number"):
        score += 0.10
    if payload.get("subtotal") is not None:
        score += 0.10
    if payload.get("tax") is not None:
        score += 0.10
    if payload.get("total") is not None:
        score += 0.20
    return min(round(score, 2), 1.0)


def extract_fields(raw_text: str) -> dict:
    """Rule-based baseline field extraction.

    This is intentionally simple for the first MVP. Later we can replace or augment
    this module with LayoutLMv3, Donut, or a vision-language model.
    """
    subtotal = _find_money_after("subtotal", raw_text)
    tax = _find_money_after("tax", raw_text)
    total = _find_money_after("total|amount due|balance due|grand total", raw_text)

    if total is None:
        amounts = [_to_float(x) for x in MONEY_PATTERN.findall(raw_text)]
        amounts = [x for x in amounts if x is not None]
        total = max(amounts) if amounts else None

    payload = {
        "document_type": "receipt",
        "vendor_name": _guess_vendor(raw_text),
        "invoice_number": _find_invoice_number(raw_text),
        "transaction_date": _find_date(raw_text),
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "currency": "USD",
        "line_items": [],
        "raw_text": raw_text,
    }
    payload["confidence"] = _confidence(payload)
    return payload
