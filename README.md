# RBP Finivis Support Assistant

A small FAQ-based customer support assistant built for the RBP Finivis
Marketing & AI Operations Internship Round 1 task.

## What it does

The assistant:

- Answers customer questions using the supplied RBP FAQ.
- Avoids answering when the FAQ does not contain sufficient information.
- Escalates complaints.
- Escalates specific transaction problems.
- Escalates transfers above $50,000.
- Logs every customer interaction.
- Includes automated tests for key behaviors.

## Architecture

```text
Customer Question
       |
       v
Escalation Rules
       |
       +---- Escalation required ----> Human escalation
       |
       v
FAQ Retriever
       |
       +---- No relevant FAQ --------> "I don't know"
       |
       v
OpenAI Model
       |
       v
Answer
       |
       v
JSONL Logger