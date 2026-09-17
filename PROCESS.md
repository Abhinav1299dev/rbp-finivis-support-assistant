# PROCESS.md

## 1. What was the hardest decision you made, and what did you choose?

The most difficult design decision was determining how the assistant should respond when the FAQ did not contain sufficient information to answer a customer’s question. I chose to prioritize reliability and safety over attempting to answer every question, so the assistant explicitly states, “I don’t have that information,” instead of generating an unsupported or potentially misleading response.

## 2. Where did you get stuck, and how did you get unstuck?

I encountered difficulties while testing the FAQ retrieval system. Some unrelated questions matched FAQ entries because of common keywords, while some paraphrased questions failed to retrieve relevant information. I investigated these cases individually, refined the matching logic, and added automated tests covering complaints, transaction issues, transfer-amount boundaries, FAQ retrieval, and unknown questions. After these changes, all six automated tests passed.

## 3. If you used AI tools to help build this, which ones and for what parts?

I used ChatGPT as a development assistant during the initial implementation, Python debugging, retrieval-logic improvements, automated test creation, and documentation preparation. I treated the generated suggestions as starting points rather than final solutions, reviewing the code, executing tests, investigating observed behavior, and making the necessary modifications myself.
