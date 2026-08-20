# Failure Analysis

The following are five cases where the current assistant either cannot answer
or does not handle the customer's intent as well as it could.

## 1. "How much does it cost?"

**Observed behavior:**  
The assistant says that the information is not available in the FAQ.

**What went wrong:**  
The FAQ contains partner commission tiers, but it does not provide general
pricing information. The assistant correctly avoids inventing a price, but it
could be more helpful by recognizing that the question is broader than the
available pricing information.

**Improvement:**  
Add better intent detection so the assistant can distinguish between general
pricing questions and questions about the partner commission structure.

---

## 2. "What programming languages can I use with your SDKs?"

**Observed behavior:**  
The assistant attempted to use the AI service instead of directly identifying
the relevant SDK FAQ entry. With the current API unavailable, it returned an
AI-service-unavailable message.

**What went wrong:**  
The FAQ contains the answer, but the question is phrased differently from
the FAQ question "Which languages have SDKs?". The keyword-based retriever
did not recognize the paraphrase reliably.

**Improvement:**  
Replace the simple keyword retriever with an embedding-based semantic
retrieval approach, while keeping the FAQ as the only knowledge source.

---

## 3. "How do I prove who I am and my business is legitimate?"

**Observed behavior:**  
The assistant says that the information is not available in the FAQ.

**What went wrong:**  
The FAQ contains information about KYC and the documents required for
verification, but the customer's wording does not directly match the FAQ
question.

**Improvement:**  
Use semantic retrieval to connect questions about identity/business
verification with the KYC and required-documents entries.

---

## 4. "Can I transfer money on Sundays?"

**Observed behavior:**  
The assistant says that the information is not available in the FAQ.

**What went wrong:**  
The FAQ provides information about payment settlement times, but it does
not state whether transfers are available on Sundays. The assistant
therefore refuses instead of guessing.

**Improvement:**  
Keep the refusal behavior. If more product information were available,
additional FAQ content about weekend availability could be added.

---

## 5. "What happens if my payment is delayed?"

**Observed behavior:**  
The assistant says that the information is not available in the FAQ.

**What went wrong:**  
The FAQ contains information about held transactions and payment settlement
times, but it does not specifically explain what happens when a payment is
delayed. The current retriever does not confidently map the question to the
relevant payment information.

**Improvement:**  
Improve semantic retrieval and add clearer FAQ coverage for delayed-payment
scenarios if that information is officially available.