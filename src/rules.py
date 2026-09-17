import re
from typing import Optional, Dict, Any


# Words that commonly indicate a complaint.
COMPLAINT_KEYWORDS = [
    "complaint",
    "complain",
    "unhappy",
    "dissatisfied",
    "not satisfied",
    "terrible service",
    "bad service",
    "poor service",
    "worst service",
    "file a complaint",
    "raise a complaint",
    "make a complaint",
    "report your service",
]


# Phrases that indicate a transaction or payment problem.
TRANSACTION_PROBLEM_PHRASES = [
    "transaction failed",
    "transaction has failed",
    "transaction is failed",
    "transaction stuck",
    "transaction is stuck",
    "transaction pending",
    "transaction is pending",
    "transaction declined",
    "transaction was declined",
    "transaction rejected",
    "transaction was rejected",
    "transaction reversed",
    "transaction was reversed",
    "transaction missing",
    "transaction is missing",

    "payment failed",
    "payment has failed",
    "payment is failed",
    "payment stuck",
    "payment is stuck",
    "payment pending",
    "payment is pending",
    "payment declined",
    "payment was declined",
    "payment rejected",
    "payment was rejected",
    "payment reversed",
    "payment was reversed",
    "payment missing",
    "payment is missing",

    "transfer failed",
    "transfer has failed",
    "transfer is failed",
    "transfer stuck",
    "transfer is stuck",
    "transfer pending",
    "transfer is pending",
    "transfer declined",
    "transfer was declined",
    "transfer rejected",
    "transfer was rejected",
    "transfer reversed",
    "transfer was reversed",
    "transfer missing",
    "transfer is missing",

    "payment not received",
    "payment has not arrived",
    "payment hasn't arrived",
    "money not received",
    "money has not arrived",
    "money hasn't arrived",
    "funds not received",
    "funds have not arrived",
    "transfer not received",
    "transfer has not arrived",
    "transfer hasn't arrived",
    "recipient did not receive",
    "recipient has not received",
    "recipient hasn't received",

    "hasn't gone through",
    "has not gone through",
    "didn't go through",
    "did not go through",
    "still processing",
    "stuck in processing",
]


def normalize_question(question: str) -> str:
    """
    Normalize the question for more reliable matching.
    """
    if not isinstance(question, str):
        return ""

    question = question.lower().strip()

    # Replace different apostrophe styles with a normal apostrophe.
    question = question.replace("’", "'")

    # Replace punctuation with spaces, except the dollar sign.
    question = re.sub(r"[^\w\s$']", " ", question)

    # Remove extra spaces.
    question = re.sub(r"\s+", " ", question)

    return question


def contains_complaint(question: str) -> bool:
    """
    Check whether the customer is making a complaint.
    """
    normalized = normalize_question(question)

    return any(
        keyword in normalized
        for keyword in COMPLAINT_KEYWORDS
    )


def contains_transaction_problem(question: str) -> bool:
    """
    Check whether the question describes a transaction problem.
    """
    normalized = normalize_question(question)

    return any(
        phrase in normalized
        for phrase in TRANSACTION_PROBLEM_PHRASES
    )


def extract_amount(question: str) -> Optional[float]:
    """
    Extract a monetary amount from a question.

    Supported examples:
        $75,000
        $ 75,000
        $75000.50
        75000 USD
        75,000 dollars
        75000
    """

    if not isinstance(question, str):
        return None

    patterns = [
        # Examples: $75,000 or $ 75,000.50
        r"\$\s*([\d,]+(?:\.\d{1,2})?)",

        # Examples: 75000 USD or 75,000 dollars
        r"([\d,]+(?:\.\d{1,2})?)\s*(?:usd|us dollars|dollars)",

        # Examples: transfer 75000 or send 75,000
        r"(?:transfer|send|move|deposit|withdraw)\s+(?:of\s+)?\$?\s*([\d,]+(?:\.\d{1,2})?)",
    ]

    for pattern in patterns:
        match = re.search(pattern, question, re.IGNORECASE)

        if not match:
            continue

        amount_text = match.group(1).replace(",", "")

        try:
            return float(amount_text)
        except ValueError:
            continue

    return None


def requires_large_amount_escalation(question: str) -> bool:
    """
    Escalate only when the amount is greater than $50,000.

    $50,000 exactly does not trigger escalation.
    """
    amount = extract_amount(question)

    return amount is not None and amount > 50000


def check_escalation(question: str) -> Dict[str, Any]:
    """
    Determine whether a question must be escalated.

    Returns:
        {
            "escalate": bool,
            "reason": str or None
        }
    """

    if not isinstance(question, str) or not question.strip():
        return {
            "escalate": False,
            "reason": None
        }

    if contains_complaint(question):
        return {
            "escalate": True,
            "reason": "Complaint requires human review."
        }

    if contains_transaction_problem(question):
        return {
            "escalate": True,
            "reason": "Specific transaction problem requires human review."
        }

    if requires_large_amount_escalation(question):
        return {
            "escalate": True,
            "reason": "Requests above $50,000 require human review."
        }

    return {
        "escalate": False,
        "reason": None
    }


if __name__ == "__main__":
    test_questions = [
        "I want to file a complaint.",
        "My payment is stuck.",
        "My transfer hasn't gone through.",
        "The recipient did not receive the money.",
        "I want to transfer $75,000.",
        "I want to transfer $50,000.",
        "Can I send 60,000 USD?",
        "What is KYC?",
        "Can I use RBP to buy a house?",
    ]

    for question in test_questions:
        result = check_escalation(question)

        print(f"\nQuestion: {question}")
        print(f"Extracted amount: {extract_amount(question)}")
        print(f"Escalate: {result['escalate']}")
        print(f"Reason: {result['reason']}")