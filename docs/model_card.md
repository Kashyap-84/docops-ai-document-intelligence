# Model Card

## Model Type

Current MVP uses a rule-based OCR pipeline, not a trained neural model.

## Intended Use

Extract structured fields from receipts and simple scanned documents.

## Inputs

Image files: PNG, JPG, JPEG, TIFF, BMP.

## Outputs

Validated JSON containing vendor, invoice number, date, subtotal, tax, total, confidence, and review status.

## Limitations

- May fail on handwritten documents.
- May fail on heavily rotated or low-quality scans.
- Rule-based extraction may miss uncommon field labels.
- PDF support is planned but not enabled in the current API route.

## Responsible AI Notes

The system uses confidence thresholds and schema validation to route uncertain documents to review instead of silently returning unreliable outputs.
