# Architecture

```mermaid
flowchart TD
    A[User uploads document image] --> B[FastAPI upload endpoint]
    B --> C[Image preprocessing]
    C --> D[Tesseract OCR]
    D --> E[Rule-based field extraction]
    E --> F[Pydantic schema validation]
    F --> G{Review required?}
    G -- Yes --> H[Human review queue JSONL]
    G -- No --> I[Return structured JSON]
    H --> I
    I --> J[Streamlit UI]
```

## MVP Design

This first version focuses on a transparent baseline:

- OCR using Tesseract
- Rule-based field extraction
- Pydantic validation
- Review queue for low-confidence or incomplete outputs
- FastAPI backend
- Streamlit frontend

## Future Enhancements

- LayoutLMv3 for layout-aware extraction
- Donut for OCR-free document parsing
- Qwen2.5-VL for visual question answering and JSON extraction
- MLflow experiment tracking
- Evidently monitoring
- Human correction feedback loop
