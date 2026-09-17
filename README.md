# RBP Finivis Support Assistant

A FAQ-based customer support assistant developed for the RBP Finivis Marketing & AI Operations

## Features

The assistant is designed to:

* Answer customer questions using the provided RBP FAQ.
* Avoid generating answers when the FAQ does not provide sufficient information.
* Escalate customer complaints.
* Escalate defined transaction-related issues.
* Escalate transfers exceeding $50,000.
* Log customer interactions in JSONL format.
* Include automated tests covering important assistant behaviors.

## Architecture

```text
Customer Question
       |
       v
Escalation Rules
       |
       +---- Escalation required ----> Human Escalation
       |
       v
FAQ Retriever
       |
       +---- No relevant FAQ --------> "I don't have that information"
       |
       v
OpenAI Model
       |
       v
Generated Answer
       |
       v
JSONL Logger
```
