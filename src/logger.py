import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "exchanges.jsonl"

logger = logging.getLogger(__name__)


def log_exchange(
    question: str,
    answer: str,
    escalated: bool,
) -> bool:
    """
    Store one customer interaction in JSONL format.

    Each interaction is saved as a separate JSON object on a new line.

    Args:
        question: The customer's question.
        answer: The assistant's response.
        escalated: Whether the interaction was escalated to a human.

    Returns:
        True if the exchange was logged successfully, otherwise False.
    """

    exchange: dict[str, Any] = {
        "question": question.strip(),
        "answer": answer.strip(),
        "escalated": bool(escalated),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

        with LOG_PATH.open("a", encoding="utf-8") as file:
            json.dump(exchange, file, ensure_ascii=False)
            file.write("\n")
            file.flush()

        return True

    except (OSError, TypeError, ValueError) as error:
        logger.exception("Failed to log customer exchange: %s", error)
        return False