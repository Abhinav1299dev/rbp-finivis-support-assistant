# Development Process

## Approach

I treated the task as a small retrieval-augmented customer support system.

The implementation was divided into:

1. FAQ loading and parsing
2. FAQ retrieval
3. Mandatory escalation rules
4. AI answer generation
5. Unknown-question handling
6. Conversation logging
7. Automated testing
8. Failure analysis

## Design Decisions

### FAQ as the source of truth

The assistant receives retrieved FAQ information as context and is instructed
not to use outside knowledge.

This reduces the risk of unsupported answers.

### Rules before AI

Mandatory escalation checks happen before the AI call.

This ensures that complaints, transaction problems and high-value transfers
are handled deterministically.

### Retrieval before AI

The assistant first checks whether the FAQ contains relevant information.

If no relevant FAQ entry is found, the assistant does not call the AI and
instead tells the customer that it does not have the information.

### Logging

Every exchange is written to a JSONL file containing the question, answer,
escalation status and timestamp.

## Testing

I created automated tests for:

- Complaint escalation
- Transaction-problem escalation
- Transfer amount above $50,000
- Exactly $50,000 boundary behavior
- KYC retrieval
- Unknown-question handling

The final automated test suite passes all six tests.

## AI Usage

AI tools were used during development for implementation assistance,
debugging and code review.

I reviewed and tested the generated implementation and made changes based
on observed failures.

## Known Limitations

The current retrieval implementation is intentionally lightweight and
keyword-based. It can fail on questions that use substantially different
wording from the FAQ.

This was identified through manual testing and documented separately in
`FAILURE_ANALYSIS.md`.

## What I Would Improve

Given additional time, I would replace the keyword retriever with semantic
retrieval using embeddings.

I would also add a retrieval confidence threshold and evaluate the system
against a larger set of paraphrased and adversarial customer questions.

The safety behavior would remain unchanged: if the system cannot establish
that the FAQ supports an answer, it should not guess.