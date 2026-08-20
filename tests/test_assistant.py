from src.assistant import answer_question
from src.retriever import retrieve_relevant_entries
from src.rules import check_escalation


def test_complaint_is_escalated():
    result = check_escalation(
        "I want to file a complaint."
    )

    assert result["escalate"] is True


def test_transaction_problem_is_escalated():
    result = check_escalation(
        "My payment is stuck."
    )

    assert result["escalate"] is True


def test_large_transfer_is_escalated():
    result = check_escalation(
        "I want to transfer $75,000."
    )

    assert result["escalate"] is True


def test_50000_dollar_transfer_is_not_escalated():
    result = check_escalation(
        "I want to transfer $50,000."
    )

    assert result["escalate"] is False


def test_kyc_question_is_retrieved():
    results = retrieve_relevant_entries(
        "What is KYC?"
    )

    assert len(results) > 0

    questions = [
        entry["question"].lower()
        for entry in results
    ]

    assert any("what is kyc" in question for question in questions)


def test_unknown_question_does_not_use_ai():
    result = answer_question(
        "Can I use RBP to buy a house?"
    )

    assert result["escalated"] is False
    assert "don't have that information" in result["answer"].lower()