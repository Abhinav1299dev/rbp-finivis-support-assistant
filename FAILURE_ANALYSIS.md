# Failure Analysis

This document describes five representative cases where the current RBP Support Assistant either cannot answer a customer’s question or does not correctly identify the customer’s intent. The analysis distinguishes between retrieval limitations and genuine knowledge gaps in the FAQ source.

## 1. General Pricing Inquiry

**Test question:**

> How much does it cost?

**Observed behavior:**
The assistant responds that the requested information is not available in the FAQ.

**Root cause:**
The FAQ includes partner commission tiers but does not define general product or service pricing. The assistant correctly avoids fabricating a price; however, it does not explicitly distinguish a general pricing inquiry from a partner commission-related question.

**Recommended improvement:**

* Add intent classification for general pricing and partner commission inquiries.
* Route general pricing questions to an approved pricing or sales-support workflow when such information becomes available.
* Continue refusing to provide unsupported prices rather than generating estimates.

**Expected outcome:**
The assistant should clearly explain whether the question concerns general pricing or partner commissions and provide information only from an approved source.

---

## 2. SDK Language Support Paraphrase

**Test question:**

> What programming languages can I use with your SDKs?

**Observed behavior:**
The assistant attempted to use the AI service instead of reliably retrieving the relevant SDK FAQ entry. Because the AI service was unavailable, it returned an AI-service-unavailable response.

**Root cause:**
The FAQ contains relevant information under the question:

> Which languages have SDKs?

However, the keyword-based retriever does not reliably recognize paraphrased questions. As a result, a question that should be answered from the FAQ may fail retrieval and incorrectly proceed to the AI-generation stage.

**Recommended improvement:**

* Replace keyword matching with embedding-based semantic retrieval.
* Store FAQ entries in a vector index and retrieve them using similarity search.
* Apply a similarity threshold before generating an answer.
* Keep the FAQ as the only authorized knowledge source.
* Add paraphrase-based regression tests for SDK-related questions.

**Expected outcome:**
Questions about supported SDK programming languages should retrieve the correct FAQ entry even when the wording differs substantially.

---

## 3. Identity and Business Verification Inquiry

**Test question:**

> How do I prove who I am and my business is legitimate?

**Observed behavior:**
The assistant responds that the information is not available in the FAQ.

**Root cause:**
The FAQ contains information about Know Your Customer (KYC) and the documents required for verification. However, the customer uses broader wording related to identity and business legitimacy, which does not sufficiently overlap with the current keyword-based retrieval terms.

**Recommended improvement:**

* Use semantic retrieval to associate identity-verification questions with KYC-related FAQ entries.
* Add approved synonyms and related concepts, such as identity verification, business verification, verification documents, and customer due diligence.
* Add test cases covering both direct and paraphrased KYC questions.

**Expected outcome:**
The assistant should retrieve the relevant KYC information when the customer asks about proving their identity or verifying their business.

---

## 4. Weekend Transfer Availability

**Test question:**

> Can I transfer money on Sundays?

**Observed behavior:**
The assistant responds that the information is not available in the FAQ.

**Root cause:**
The FAQ includes information about payment settlement times but does not explicitly state whether transfers are available on Sundays. Settlement timing and weekend transfer availability are related but distinct topics.

**Recommended improvement:**

* Preserve the refusal behavior when the FAQ does not contain an authoritative answer.
* Add an approved FAQ entry covering weekend and holiday transfer availability if the information is officially confirmed.
* Avoid inferring Sunday availability from settlement-time information alone.

**Expected outcome:**
Until authoritative information is added, the assistant should transparently state that weekend transfer availability is not specified in the available FAQ.

---

## 5. Delayed Payment Scenario

**Test question:**

> What happens if my payment is delayed?

**Observed behavior:**
The assistant responds that the information is not available in the FAQ.

**Root cause:**
The FAQ contains information about held transactions and payment settlement times, but it does not clearly describe the specific customer scenario of a delayed payment. Additionally, the keyword-based retriever may fail to connect terms such as “delayed” and “still processing” with related payment information.

**Recommended improvement:**

* Improve semantic retrieval for related payment-status terminology.
* Add an approved FAQ entry explaining delayed-payment scenarios, expected timelines, and appropriate next steps if that information is available.
* Escalate cases involving a specific failed, stuck, pending, or missing transaction according to the assistant’s deterministic escalation rules.
* Add tests for phrases such as “my payment is delayed,” “my payment is still processing,” and “the recipient has not received the funds.”

**Expected outcome:**
The assistant should either provide an authoritative explanation from the FAQ or clearly state that the information is unavailable. Specific transaction problems should continue to follow the human-escalation workflow.

---

## Summary of Findings

The five cases reveal two primary limitations:

1. **Knowledge coverage gaps:**
   Some questions cannot be answered because the FAQ does not contain the required information, such as general pricing or Sunday transfer availability.

2. **Retrieval limitations:**
   Some questions are answerable in principle, but keyword-based matching fails to recognize paraphrases, particularly for SDK support, KYC, and payment-related terminology.

The recommended next step is to introduce semantic retrieval with a confidence threshold while preserving the current safety controls:

* Deterministic escalation rules should run before answer generation.
* The FAQ should remain the sole knowledge source.
* Low-confidence or unsupported questions should receive an explicit refusal.
* Regression tests should cover direct questions, paraphrases, boundary conditions, and unrelated requests.
