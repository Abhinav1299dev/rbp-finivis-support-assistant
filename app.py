from flask import Flask, request, jsonify, render_template_string
from src.assistant import answer_question

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RBP Support Assistant</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 40px auto;
            padding: 20px;
            background: #f7f7f7;
        }

        .container {
            background: white;
            padding: 25px;
            border-radius: 10px;
        }

        .input-area {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            padding: 12px;
        }

        button {
            padding: 12px 20px;
            cursor: pointer;
        }

        #answer {
            margin-top: 25px;
            padding: 15px;
            background: #eeeeee;
            white-space: pre-wrap;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>RBP Support Assistant</h1>
        <p>Ask a question about RBP Finivis.</p>

        <div class="input-area">
            <input id="question" placeholder="Enter your question">
            <button id="askButton" onclick="askQuestion()">Ask</button>
        </div>

        <div id="answer"></div>
    </div>

    <script>
        async function askQuestion() {
            const question = document.getElementById("question").value.trim();
            const answerBox = document.getElementById("answer");
            const button = document.getElementById("askButton");

            if (!question) {
                answerBox.innerText = "Please enter a question.";
                return;
            }

            answerBox.innerText = "Thinking...";
            button.disabled = true;

            try {
                const response = await fetch("/ask", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ question: question })
                });

                const data = await response.json();

                if (!response.ok) {
                    answerBox.innerText = data.error || "An error occurred.";
                    return;
                }

                answerBox.innerText = data.answer || "No answer returned.";

            } catch (error) {
                answerBox.innerText = "Unable to connect to the assistant.";
            } finally {
                button.disabled = false;
            }
        }
    </script>
</body>
</html>
"""


def convert_to_text(result):
    """Convert any assistant response into readable text."""
    while isinstance(result, dict):
        if "answer" in result:
            result = result["answer"]
        elif "response" in result:
            result = result["response"]
        elif "message" in result:
            result = result["message"]
        else:
            result = str(result)
            break

    return str(result)


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please provide a question"}), 400

    try:
        result = answer_question(question)
        answer = convert_to_text(result)

        return jsonify({
            "question": question,
            "answer": answer
        })

    except Exception:
        return jsonify({
            "error": "An internal error occurred while processing your question."
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)