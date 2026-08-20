import os

from dotenv import load_dotenv
from openai import APIError, OpenAI, RateLimitError

from src.logger import log_exchange
from src.retriever import retrieve_relevant_entries
from src.rules import check_escalation


# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. "
        "Add it to your .env file."
    )

client = OpenAI(api_key=api_key)


SYSTEM_PROMPT = """
You are the RBP Finivis customer support assistant.

You have access to a provided FAQ.

STRICT RULES:

1. Answer using ONLY the FAQ information provided to you.
2. Never use outside knowledge.
3. Never guess or invent information.
4. If the FAQ does not contain enough information to answer the question,
   say that you don't have that information in the provided FAQ.
5. Keep answers concise and clear.
6. Do not claim that you performed an action unless the FAQ explicitly
   supports that claim.
"""


def generate_answer(question, faq_entries):
    """Generate an answer using only the retrieved FAQ information."""

    if not faq_entries:
        return (
            "I don't have that information in the provided FAQ. "
            "I can escalate this to a human for further assistance."
        )

    # Build the FAQ context.
    context_parts = []

    for entry in faq_entries:
        context_parts.append(
            f"Category: {entry['category']}\n"
            f"Question: {entry['question']}\n"
            f"Answer: {entry['answer']}"
        )

    context = "\n\n".join(context_parts)

    user_prompt = f"""
FAQ INFORMATION:

{context}

CUSTOMER QUESTION:

{question}

Answer the customer's question using only the FAQ information above.

If the FAQ does not provide enough information, say that you don't know
and offer escalation to a human.
"""

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            instructions=SYSTEM_PROMPT,
            input=user_prompt
        )

        return response.output_text.strip()

    except RateLimitError:
        return (
            "The AI service is currently unavailable. "
            "I cannot safely provide an answer right now, "
            "so this should be escalated to a human."
        )

    except APIError:
        return (
            "The AI service is currently unavailable. "
            "I cannot safely provide an answer right now, "
            "so this should be escalated to a human."
        )


def answer_question(question):
    """Process a customer question."""

    # ---------------------------------------------------------
    # STEP 1: Check mandatory escalation rules first.
    # ---------------------------------------------------------

    escalation = check_escalation(question)

    if escalation["escalate"]:
        return {
            "answer": (
                "I'll escalate this to a human because "
                + escalation["reason"]
            ),
            "escalated": True,
            "reason": escalation["reason"]
        }

    # ---------------------------------------------------------
    # STEP 2: Retrieve relevant information from the FAQ.
    # ---------------------------------------------------------

    faq_entries = retrieve_relevant_entries(question)

    # ---------------------------------------------------------
    # STEP 3: If nothing relevant was found, DO NOT call AI.
    # This prevents the assistant from guessing.
    # ---------------------------------------------------------

    if not faq_entries:
        return {
            "answer": (
                "I don't have that information in the provided FAQ. "
                "I can escalate this to a human for further assistance."
            ),
            "escalated": False,
            "reason": None
        }

    # ---------------------------------------------------------
    # STEP 4: Generate answer using only the FAQ.
    # ---------------------------------------------------------

    answer = generate_answer(question, faq_entries)

    return {
        "answer": answer,
        "escalated": False,
        "reason": None
    }


def main():
    """Run the command-line support assistant."""

    print("RBP Finivis Support Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Customer: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        result = answer_question(question)

        # Log every exchange.
        log_exchange(
            question=question,
            answer=result["answer"],
            escalated=result["escalated"]
        )

        print(f"\nAssistant: {result['answer']}")

        if result["escalated"]:
            print(f"Escalation: {result['reason']}")

        print()


if __name__ == "__main__":
    main()