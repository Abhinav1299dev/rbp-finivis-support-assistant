# PROCESS.md

## 1. What was the hardest decision you made, and what did you choose?

The hardest decision was deciding how to handle questions when the FAQ did not clearly contain the answer. I chose to prioritize safety over trying to make the assistant answer every question, so the system returns an explicit "I don't have that information" response instead of guessing.

## 2. Where did you get stuck, and how did you get unstuck?

I got stuck while testing the FAQ retrieval because unrelated questions could match FAQ entries through common keywords, and paraphrased questions could be missed. I debugged the retrieval behavior with individual test questions, tightened the matching logic, and added automated tests for both relevant and unknown questions until all six tests passed.

## 3. If you used AI tools to help build this, which ones and for what parts?

I used ChatGPT to help with the initial implementation, debugging Python errors, improving the FAQ retrieval logic, creating automated tests, and structuring the project documentation. I reviewed and tested the generated code myself and made changes based on the behavior observed during testing.