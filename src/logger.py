import json
from datetime import datetime, timezone
from pathlib import Path


LOG_PATH = Path(__file__).parent.parent / "logs" / "exchanges.jsonl"


def log_exchange(question, answer, escalated):
    """Save one customer interaction to the JSONL log."""

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    exchange = {
        "question": question,
        "answer": answer,
        "escalated": escalated,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(exchange) + "\n")