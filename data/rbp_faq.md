# RBP Finivis FAQ

## About the platform

**What is Royal Bank Pacific?** RBP is a financial infrastructure provider, not a bank. We provide the technology layer — account issuance, payment routing, compliance screening, treasury tools — that businesses use to run global money operations. All regulated banking services are delivered through licensed partner institutions.

**So RBP doesn't hold my money?** Correct. Client funds sit with our licensed banking partners in segregated accounts. RBP operates the software and the client relationship.

**Who is the platform for?** Financial institutions, fintech companies, international corporates, crypto and digital asset businesses, holding companies, enterprise merchants, and payment aggregators.

**Can an individual open an account?** No. RBP serves businesses only.

## Products

**What products are available?** Six modules: IBAN Infrastructure, Payment Gateway, Cross-Border Payments, Compliance, Merchant Infrastructure, and White-Label Banking.

**What is an IBAN?** An International Bank Account Number — the standard account identifier used across Europe and many other regions. Through RBP you can issue both virtual and dedicated IBANs.

**How many currencies are supported?** More than 40.

**What is White-Label Banking?** You launch a banking product under your own brand, running on RBP infrastructure. Your customers see your name; the accounts, cards, and payments run on our rails.

**Do you offer cards?** Yes — Visa or Mastercard corporate cards linked to a multi-currency account, with per-card spend limits, real-time controls, and instant freeze. Available under your brand or ours.

**Do you support crypto?** Yes, through partner crypto rails for on-ramp, off-ramp, and stablecoin settlement.

## Payments

**Which payment rails do you support?** SWIFT, Fedwire, SEPA, CHAPS, UPI, and crypto rails.

**How does routing work?** The platform selects a rail automatically based on currency, destination, and urgency. You can also specify a rail directly through the API.

**How fast are payments?** SEPA transfers settle in under ten seconds within the Eurozone. SWIFT transfers typically settle T+1. Domestic USD and GBP transfers settle same-day.

**Is there a maximum transfer size?** There is no fixed cap, but transfers above $500,000 are routed for human review before release.

**Can I track an international payment?** Yes, where the corridor supports SWIFT gpi tracking.

## Onboarding

**How long does onboarding take?** Applications are reviewed within 24 hours. Verification takes days two to four. Account activation and rail connection happens around days five to six, API access on days six to seven, and go-live typically between days seven and ten.

**What is KYC?** Know Your Customer — the identity and business verification we are legally required to complete before you can move money.

**What documents do I need?** Certificate of incorporation, proof of business address, identification for directors and beneficial owners, and a recent bank statement. Additional documents may be requested depending on your risk tier and jurisdiction.

**What is a risk tier?** A classification assigned during verification that determines how much additional checking your account requires. Low and medium tiers complete faster; high-risk cases require enhanced review.

**What happens if my application is rejected?** You will receive the reason in writing and may reapply once the issue is resolved.

## API and developers

**What does the API look like?** REST with webhooks, documented to OpenAPI 3.1. Requests are idempotent and webhooks are signed.

**Which languages have SDKs?** TypeScript, Go, Python, Java, Ruby, and .NET.

**Is there a sandbox?** Yes. The sandbox ships with seeded test data and signed responses, and upgrades to production keys in one step.

**How do I authenticate?** API keys issued at activation. Never share a key or commit it to source control. Keys can be rotated from the dashboard.

**What is a webhook?** An automatic message the platform sends to a URL you specify when something happens — a payment settling, a verification completing — so you don't have to keep asking.

## Compliance

**What screening runs on transactions?** Every transaction is screened against sanctions lists before release, alongside ongoing transaction monitoring.

**What is AML?** Anti-Money-Laundering — the controls that detect and prevent funds from illegal activity moving through the system.

**Why was my transaction held?** Transactions are held when screening flags a possible match, when the amount exceeds a review threshold, or when the pattern is unusual for your account. Held transactions are reviewed by a person.

**Is the platform certified?** Infrastructure practices are aligned to ISO 27001, and card handling is PCI-DSS compliant.

## Partners

**Is there a partner programme?** Yes. Partners earn commission on every transaction from every client they introduce, for the life of the account, with no cap.

**What are the commission tiers?** Standard at 0.15% per transaction, open to all partners. Silver at 0.25%, unlocking at five active client accounts. Gold at 0.40% at fifteen accounts. Platinum at 0.60% at twenty-five accounts.

**When are commissions paid?** Monthly, with real-time tracking available in the partner dashboard.

## Support

**How do I get help?** Through the contact form on the website or your account dashboard.

**What if I have a complaint?** Complaints are handled through a formal process and are always reviewed by a person.