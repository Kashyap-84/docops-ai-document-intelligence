from pathlib import Path
import json
from datetime import datetime
from src.extraction.schema_validator import ExtractedDocument

QUEUE_PATH = Path("data/processed/review_queue.jsonl")


def add_to_review_queue(document: ExtractedDocument) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = document.model_dump(mode="json")
    record["queued_at"] = datetime.utcnow().isoformat()
    with QUEUE_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")
