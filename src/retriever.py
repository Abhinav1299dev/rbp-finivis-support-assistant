from pathlib import Path
import re


FAQ_PATH = Path(__file__).parent.parent / "data" / "rbp_faq.md"


STOP_WORDS = {
    "what", "which", "who", "how", "when", "where", "why",
    "can", "could", "would", "should", "does", "do",
    "is", "are", "the", "a", "an",
    "i", "me", "my", "we", "you", "your",
    "to", "of", "in", "on", "for", "and", "or",
    "it", "this", "that", "have", "has", "be",
    "with", "from", "use", "using", "rbp",
}


def load_faq():
    """Load the FAQ document."""

    if not FAQ_PATH.exists():
        raise FileNotFoundError(
            f"FAQ file not found: {FAQ_PATH}"
        )

    return FAQ_PATH.read_text(encoding="utf-8")


def split_into_entries(faq_text):
    """Split the FAQ into individual question-answer entries."""

    entries = []
    current_category = None

    for line in faq_text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("## "):
            current_category = line[3:].strip()

        elif line.startswith("**") and "**" in line[2:]:
            parts = line.split("**", 2)

            if len(parts) >= 3:
                question = parts[1].strip()
                answer = parts[2].strip()

                entries.append({
                    "category": current_category,
                    "question": question,
                    "answer": answer
                })

    return entries


def get_faq_entries():
    """Load and parse the FAQ."""

    return split_into_entries(load_faq())


def tokenize(text):
    """Extract meaningful lowercase words."""

    words = re.findall(r"[a-zA-Z0-9]+", text.lower())

    return {
        word
        for word in words
        if len(word) > 2 and word not in STOP_WORDS
    }


def retrieve_relevant_entries(question, top_k=3):
    """
    Retrieve FAQ entries using keyword overlap.

    Returns only sufficiently relevant FAQ questions.
    """

    entries = get_faq_entries()
    question_words = tokenize(question)

    if not question_words:
        return []

    scored_entries = []

    for entry in entries:

        faq_question_words = tokenize(entry["question"])

        matching_words = (
            question_words.intersection(faq_question_words)
        )

        if not matching_words:
            continue

        similarity = (
            len(matching_words) / len(question_words)
        )

        score = len(matching_words)

        scored_entries.append(
            (similarity, score, entry)
        )

    scored_entries.sort(
        key=lambda item: (item[0], item[1]),
        reverse=True
    )

    results = []

    for similarity, score, entry in scored_entries:

        # Accept:
        # 1. Two or more meaningful matching words
        # OR
        # 2. A single match when it represents the entire question.
        if score >= 2 or similarity >= 1.0:
            results.append(entry)

        if len(results) >= top_k:
            break

    return results


if __name__ == "__main__":

    question = input("Ask a question: ")

    results = retrieve_relevant_entries(question)

    if not results:
        print("\nNo relevant FAQ information found.")

    else:
        print("\nRelevant FAQ information:\n")

        for entry in results:
            print(f"[{entry['category']}]")
            print(f"Q: {entry['question']}")
            print(f"A: {entry['answer']}")
            print()