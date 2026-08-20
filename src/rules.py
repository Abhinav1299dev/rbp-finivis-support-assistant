import re


def contains_complaint(question):
    """Check whether the customer is making a complaint."""
    complaint_keywords = [
        "complaint",
        "complain",
        "unhappy",
        "dissatisfied",
        "terrible service",
        "bad service",
        "poor service",
        "file a complaint",
    ]

    question_lower = question.lower()

    return any(
        keyword in question_lower
        for keyword in complaint_keywords
    )


def contains_transaction_problem(question):
    """Check whether the question describes a specific transaction problem."""

    transaction_phrases = [
        "transaction failed",
        "transaction is failed",
        "transaction stuck",
        "transaction is stuck",
        "transaction pending",
        "transaction is pending",

        "payment failed",
        "payment is failed",
        "payment stuck",
        "payment is stuck",
        "payment pending",
        "payment is pending",
        "payment missing",
        "payment is missing",
        "payment not received",
        "payment hasn't arrived",
        "payment has not arrived",

        "money not received",
        "money hasn't arrived",
        "money has not arrived",

        "transfer failed",
        "transfer is failed",
        "transfer stuck",
        "transfer is stuck",
        "transfer pending",
        "transfer is pending",
        "transfer missing",
        "transfer is missing",
        "transfer not received",
        "transfer hasn't arrived",
        "transfer has not arrived",
    ]

    question_lower = question.lower().strip()

    return any(
        phrase in question_lower
        for phrase in transaction_phrases
    )


def extract_amount(question):
    """Extract a dollar amount from the question."""
    patterns = [
        r"\$\s*([\d,]+(?:\.\d+)?)",
        r"([\d,]+(?:\.\d+)?)\s*(?:USD|dollars)",
    ]

    for pattern in patterns:
        match = re.search(pattern, question, re.IGNORECASE)

        if match:
            amount_text = match.group(1).replace(",", "")

            try:
                return float(amount_text)
            except ValueError:
                return None

    return None


def requires_large_amount_escalation(question):
    """Check whether the request involves more than $50,000."""
    amount = extract_amount(question)

    return amount is not None and amount > 50000


def check_escalation(question):
    """
    Determine whether a question must be escalated.

    Returns:
        {
            "escalate": bool,
            "reason": str
        }
    """

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
        "I want to transfer $75,000.",
        "What is KYC?",
    ]

    for question in test_questions:
        result = check_escalation(question)

        print(f"\nQuestion: {question}")
        print(f"Escalate: {result['escalate']}")
        print(f"Reason: {result['reason']}")
