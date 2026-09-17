from src.assistant import answer_question
from src.retriever import retrieve_relevant_entries
from src.rules import (
    check_escalation,
    contains_complaint,
    contains_transaction_problem,
    extract_amount,
)


def test_complaint_is_escalated():
    result = check_escalation("I want to file a complaint.")

    assert result["escalate"] is True
    assert "complaint" in result["reason"].lower()


def test_dissatisfied_customer_is_escalated():
    result = check_escalation("I am dissatisfied with your service.")

    assert result["escalate"] is True


def test_transaction_problem_is_escalated():
    result = check_escalation("My payment is stuck.")

    assert result["escalate"] is True
    assert "transaction" in result["reason"].lower()


def test_transaction_paraphrase_is_escalated():
    result = check_escalation("My transfer hasn't gone through.")

    assert result["escalate"] is True


def test_recipient_not_receiving_money_is_escalated():
    result = check_escalation(
        "The recipient did not receive the money."
    )

    assert result["escalate"] is True


def test_large_transfer_is_escalated():
    result = check_escalation("I want to transfer $75,000.")

    assert result["escalate"] is True
    assert "50,000" in result["reason"]


def test_large_amount_with_usd_is_escalated():
    result = check_escalation("Can I transfer 60,000 USD?")

    assert result["escalate"] is True


def test_large_amount_with_dollars_is_escalated():
    result = check_escalation("Can I send 75,000 dollars?")

    assert result["escalate"] is True


def test_50000_dollar_transfer_is_not_escalated():
    result = check_escalation("I want to transfer $50,000.")

    assert result["escalate"] is False
    assert result["reason"] is None


def test_amount_below_threshold_is_not_escalated():
    result = check_escalation("I want to transfer $49,999.")

    assert result["escalate"] is False


def test_amount_extraction_with_commas():
    assert extract_amount("$75,000") == 75000.0


def test_amount_extraction_with_usd():
    assert extract_amount("75,000 USD") == 75000.0


def test_amount_extraction_with_dollars():
    assert extract_amount("75,000 dollars") == 75000.0


def test_amount_extraction_without_amount():
    assert extract_amount("What is KYC?") is None


def test_complaint_detection():
    assert contains_complaint("I am unhappy with the service.") is True


def test_transaction_problem_detection():
    assert contains_transaction_problem(
        "The transfer is still processing."
    ) is True


def test_normal_question_is_not_escalated():
    result = check_escalation("What is KYC?")

    assert result["escalate"] is False


def test_kyc_question_is_retrieved():
    results = retrieve_relevant_entries("What is KYC?")

    assert len(results) > 0

    questions = [
        entry["question"].lower()
        for entry in results
    ]

    assert any("what is kyc" in question for question in questions)


def test_unknown_question_does_not_use_ai():
    result = answer_question("Can I use RBP to buy a house?")

    assert result["escalated"] is False
    assert "don't have that information" in result["answer"].lower()


def test_empty_question_is_not_escalated():
    result = check_escalation("")

    assert result["escalate"] is False


def test_whitespace_question_is_not_escalated():
    result = check_escalation("   ")

    assert result["escalate"] is False