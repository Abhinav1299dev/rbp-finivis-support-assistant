# RBP Finivis Support Assistant

A FAQ-based customer support assistant developed for the RBP Finivis Marketing & AI Operations Internship — Round 1 task.

## Features

The assistant is designed to:

* Answer customer questions using the provided RBP FAQ.
* Avoid generating answers when the FAQ does not provide sufficient information.
* Escalate customer complaints.
* Escalate defined transaction-related issues.
* Escalate transfers exceeding $50,000.
* Log customer interactions in JSONL format.
* Include automated tests covering important assistant behaviors.

## Demo

The assistant is available through a simple web interface where users can enter a question and receive a response.

![RBP Support Assistant Demo](docs/demo.png)

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

## Project Structure

```text
rbp-support-assistant/
├── app.py
├── data/
│   └── rbp_faq.md
├── src/
│   ├── assistant.py
│   ├── retriever.py
│   ├── rules.py
│   └── logger.py
├── tests/
│   └── test_assistant.py
├── docs/
│   └── demo.png
├── PROCESS.md
├── FAILURE_ANALYSIS.md
├── README.md
└── requirements.txt
```

## Running the Application

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask application:

```bash
python app.py
```

The application will be available locally at:

```text
http://localhost:5000
```

## Testing

Run the automated tests with:

```bash
pytest -q
```
