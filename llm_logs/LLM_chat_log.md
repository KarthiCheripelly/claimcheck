# LLM conversation log – ClaimCheck (Tresata take-home)
Tool: Claude Code (model: Claude Opus 5.5). Exported from the session transcript.
Tool calls are summarised in one line each; full raw transcript is in the .jsonl file.

## USER
go through the problem statement and explain me in simple words . this is hte placement releated so be careful

> _tool: PowerShell – List files in project folder_

> _tool: Read – C:\Users\spoor\OneDrive\Desktop\tresata\[EXTERNAL] TRESATA_TAKE HOME ASSIGNMENT.pdf_

## AI
I've read the whole PDF (3 pages). Here's what Tresata is asking for, in simple words.

## The big idea
Finance runs on documents: tax rules, regulations, audit papers, agreements. Experts still read and cross-check them by hand. Tresata wants to see whether you can **find one real problem in finance and design an AI solution that people can trust.**

They are mainly testing **how you think**, not how much code you write.

## What you have to do

**Step 1: Pick one problem**
- Choose any area of finance (tax, audit, regulation, cross-border trade, or something else).
- Describe one **simple, specific** problem: who has it, what task they do, how often, and what it costs them today.
- Explain why it matters and **why now**.
- Say what is **out of scope** (what you are *not* solving).
- ⚠️ **Don't reuse their two examples** (bank compliance teams reading regulator circulars, and small exporters missing out on trade-agreement tariff cuts). Find your own problem.

**Step 2: Design the solution (this matters most)**
Explain:
- **Input:** what data goes in
- **AI's job:** what the AI actually does
- **Output:** what comes out
- **Human review:** where a person has to check or approve
- **Mistakes:** how the system deals with uncertainty and errors
- **Why AI:** why a simple rule-based or non-AI approach wouldn't be enough

**Step 3: Build a small proof (optional)**
- This can be a tiny prototype, a notebook, or a clickable mock.
- Test it on **at least 10 examples you create yourself**.
- **Report honestly where it fails.** They value that honesty.

## What they care about most: architecture
They say plainly that **a simple design with sharp reasoning beats a complex one you can't defend.** Be ready to answer:
- Is one LLM call enough, or do you need retrieval (searching source documents), a rules engine, a calculator, or several agents? Why?
- Which parts **must be exact** (like a tax amount or a cited clause) and which can be "AI guesses"? How do you keep the two separate?
- Where does the knowledge live (in the model, in a document index, in code, or with a human)? What happens when a rule changes?
- Can every output be **traced back to its source** so an auditor can check it?
- What is the **weakest point** of your design?
- What options did you **consider and reject**, and why?

## The "beyond the AI" appendix (1 page, required)
They expect you to use AI tools. They want to see **your own thinking**:
1. **Where AI helped**, including 2–3 of your key prompts
2. **What AI got wrong** and you corrected, and how you knew it was wrong
3. **What came from you**: decisions, insights or risks the AI didn't suggest
4. **One part you could defend live with no tools**

## What you submit
1. **Written brief, 4 pages max.** It should cover:
   - the area you explored and what surprised you
   - your problem statement
   - what you added beyond the AI
   - your solution with an **architecture diagram** showing where the human acts and where the AI acts, plus the alternatives you rejected
   - risks: wrong answers, outdated rules, confidential data, and legal liability
   - what you would think about before spending more time on it
2. **Prototype or mock (optional).** If you share a link, it **must be publicly accessible** and have a README covering how to run it, the examples you tested, and which model you used.
3. **LLM chat logs as a zip.** They will read your AI conversations, **including this one**. Make sure the logs show your own thinking, not just you copying answers.

## Rules to follow
- **Only public or made-up data.** No real client or personal financial data. Say clearly which examples you made up.
- **Pick a country or jurisdiction** (India is fine) and say what would change for another country.
- **No finance background needed.** They are testing how fast you learn, so show your learning in the brief.
- **A free model is fine** (OpenRouter's free tier). Note which model you used.
- **Legal and tax advice is a real constraint.** Say who is accountable for the output and where a qualified human (like a CA or lawyer) must approve.

## My advice
- **Choose a narrow problem.** "Helping everyone with taxes" is too broad. "Checking whether a vendor invoice correctly applies TDS under one specific section" is the right size.
- **Keep exact things out of the AI.** Do the math with code, and have the AI cite the exact clause it relied on.
- **Do the problem choice and the trade-offs yourself.** That's what the appendix and the chat logs will show.

Do you want me to help you brainstorm a few problem ideas next? You'd make the final choice.

## USER
yes lets brainstor

## AI
Here are 6 ideas, mostly set in India since that's easiest for you to research. Each one is narrow, uses public data, and has a clear place where a human has to sign off.

### 1. GST input tax credit mismatch explainer
- **Who:** Accountants at small businesses, every month.
- **Problem:** The GST credit a business claims in its books often doesn't match what appears in GSTR-2B, the auto-generated statement of credit available to it. Matching the numbers is mechanical, but working out *why* they differ is not. Was the invoice filed late, did the supplier enter the wrong GSTIN (the business's GST number), or is this credit blocked under Section 17(5)?
- **AI's role:** Reads the invoice and the CGST Act rules, and suggests the likely reason for each mismatch with the clause cited.
- **Exact part:** Matching and amounts are done in code. The AI only explains the reason.
- **Why it's strong:** It splits cleanly into an exact part and an AI part, which is exactly the separation the brief asks you to show.

### 2. TDS section classifier for vendor payments
- **Who:** Accounts payable teams paying vendors.
- **Problem:** For each payment, deciding which TDS section applies (194C contracts, 194J professional fees, 194I rent, 194Q purchase of goods) depends on what the invoice actually describes. Getting it wrong means interest and penalties.
- **AI's role:** Reads the invoice description, picks the section, and cites the clause. Code applies the rate and thresholds.
- **Hard case:** Something like "software support and maintenance" could fall under 194C or 194J. That ambiguity is a good place to show human review.

### 3. Tax notice triage for individuals
- **Who:** Salaried taxpayers who receive an Income Tax notice (for example under Section 143(1) or 139(9)) and panic.
- **AI's role:** Identifies the type of notice, the deadline, what the department is asking for, and which documents to gather. It routes the case to a CA, never decides it.
- **Advantage:** Sample notice formats are publicly available.
- **Risk:** It sits close to giving legal advice, so the accountability design has to be very clear.

### 4. Audit evidence ↔ claim checker
- **Who:** Junior auditors.
- **Problem:** Checking that a figure in a company's annual report notes, such as a related-party transaction, is supported by the disclosure elsewhere and meets the relevant accounting standard (Ind AS 24 for related parties).
- **AI's role:** Cross-references the sections of the report and flags inconsistencies.
- **Data:** Public annual reports from NSE/BSE.

### 5. Loan agreement covenant tracker
- **Who:** Finance teams at mid-size companies.
- **Problem:** Loan agreements contain covenants, conditions the company must keep, such as keeping its debt-to-equity ratio below 2 or reporting every quarter. Nobody tracks them until a breach happens.
- **AI's role:** Extracts each covenant into a structured rule. Code then checks the rules against the quarterly numbers.
- **Data:** Sample credit agreements are public, for example in SEC filings.

### 6. DTAA treaty benefit checker for freelancers
- **Who:** Indian freelancers paid by foreign clients.
- **Problem:** Clients wrongly withhold tax because nobody checks the Double Taxation Avoidance Agreement (DTAA) between the two countries and the Form 10F / Tax Residency Certificate requirements.
- **Caution:** This is similar to their "unclaimed benefit" example (small exporters missing tariff cuts), so it's slightly riskier to pick.

### My picks
- **#1 (GST)** or **#2 (TDS)**: very concrete, frequent, the cost is measurable, and the exact and AI parts separate cleanly.
- **#5 (covenants)**: if you want something less common that other candidates are unlikely to pick.

### Before you choose, ask yourself
1. Which of these could you **explain to an interviewer from your own understanding**?
2. Do you know anyone who does this work, such as a CA, an accountant or a family business? Even one conversation gives you an insight the AI didn't give you, and that's what the appendix asks for.
3. Can you find **real public documents** for it this week?

Tell me which 1–2 interest you, or a problem you've seen yourself, and we'll stress-test it together.

## USER
give me some niche ideas

## AI
These are less obvious, so fewer other candidates are likely to pick them. Each still uses public data and has a clear human sign-off point.

### 1. Gold loan pledge receipt checker
- **Who:** RBI-regulated lenders (NBFCs and banks) that give loans against gold jewellery.
- **Problem:** RBI has repeatedly flagged problems with gold loans, including the loan amount exceeding the allowed loan-to-value ratio (LTV) and wrong purity values on the pledge receipt.
- **AI's role:** Reads the handwritten or scanned receipt and extracts weight, purity, value and loan amount.
- **Exact part:** Code checks those values against the RBI LTV limit.
- **Why niche:** It's a messy-document problem with a very sharp rule behind it.

### 2. Crypto TDS (Section 194S) for peer-to-peer trades
- **Problem:** Since 2022, India deducts 1% TDS on crypto transfers. P2P traders and small exchanges often get it wrong.
- **AI's role:** Classifies whether a transaction is a VDA (virtual digital asset) transfer.
- **Exact part:** Code computes the TDS amount.
- **Why niche:** The law is new and changing, which lets you answer the brief's question about outdated knowledge.

### 3. Agricultural income exemption check
- **Problem:** Agricultural income is exempt from tax under Section 10(1), but this is heavily misused. The Income Tax department scrutinises big claims, and the test of what counts as agricultural (for example, nursery income or processed produce) is legally subtle.
- **AI's role:** Reads land records and sale bills, then maps them to case-law tests.
- **Why niche:** Hardly anyone builds for this.

### 4. Bank charge refund detector for MSMEs
- **Problem:** Small businesses get charged penal interest, minimum-balance fees and similar charges that break the bank's own published schedule of charges or RBI's 2023–24 penal charges circular.
- **AI's role:** Reads bank statement narrations and maps each charge to the right rule.
- **Exact part:** Code recomputes what the charge should have been.
- **Output:** A draft complaint for the RBI ombudsman, which a human reviews before sending.

### 5. Insurance claim rejection vs. policy wording
- **Problem:** Health insurance claims get rejected citing exclusion clauses ("pre-existing disease", "waiting period"). Policyholders can't tell whether the rejection is valid.
- **AI's role:** Matches the rejection letter to the exact policy clause and to IRDAI rules.
- **Fit:** This is in the insurance part of finance and very relatable.

### 6. Startup ESOP perquisite tax deferral (Section 192)
- **Problem:** Employees of eligible startups can defer tax on ESOPs, but eligibility depends on DPIIT recognition, the Section 80-IAC certificate, and the timing of the event that triggers the tax. Payroll teams often get this wrong.
- **Why niche:** It's very specific, and the "why now" story around Indian startup IPOs is strong.

### 7. Charitable trust 85% application rule
- **Problem:** NGOs registered under Section 12A must spend 85% of their income each year or lose the tax exemption. The accounts they work from are messy.
- **AI's role:** Classifies expenses as application of income or not. Code tracks the 85% rule.

### 8. Transfer pricing comparable rejection reasons
- **Problem:** In transfer pricing studies, analysts screen hundreds of companies from databases and must write down *why* each one is rejected as a comparable (for example, a different function or related-party transactions above 25%).
- **AI's role:** Reads the company descriptions from annual reports and drafts the rejection reason with the evidence it relied on.
- **Fit:** Very niche, and an audit-trail-heavy problem, which the brief emphasises.

### My niche picks
- **#4 (bank charges):** Relatable, uses public RBI circulars and bank charge schedules, has a clear calculator part, and has a clear human step (sending the complaint).
- **#8 (transfer pricing):** Truly uncommon and shows domain depth, but needs more learning time.
- **#5 (insurance):** Easy to make up realistic test cases, and the human-review design is natural.

Which ones catch your eye? Pick 1–2 and I'll help you check each against the brief's requirements: why now, what's out of scope, which parts are exact vs. AI, and its weakest point.

## USER
go to reddit or any opensource and give me real world problems lets select from their

> _tool: ToolSearch – select:WebSearch,WebFetch_

> _tool: WebSearch – reddit IndiaTax GST notice mismatch frustrated small business_

> _tool: WebSearch – reddit CAIndia articleship most tedious manual work audit_

> _tool: WebSearch – reddit accounting most tedious manual task AI could automate reconciliation_

> _tool: WebSearch – reddit IndiaInvestments AIS mismatch income tax notice 143(1) adjustment_

> _tool: WebSearch – site:reddit.com r/IndiaTax help notice confused_

> _tool: WebSearch – site:reddit.com r/Accounting "I hate" manual task every month_

> _tool: WebFetch – https://www.reddit.com/r/IndiaTax/top.json?t=year&limit=50_

> _tool: WebSearch – RBI Ombudsman annual report 2024-25 top complaint categories grounds_

> _tool: WebSearch – Insurance Ombudsman annual report health claim rejection complaints share_

> _tool: WebSearch – GST appeals pending number ITC denial Section 16(4) litigation small taxpayers_

## AI
I couldn't get into Reddit: it blocks my fetch tool, and search engines didn't return Reddit threads. So I used **official ombudsman reports and court-case trackers** instead. These are actually stronger evidence for your brief than Reddit posts, because they show the problem is real and give you numbers. Please also browse r/IndiaTax, r/CAIndia and r/IndiaInvestments yourself for 20 minutes. Quotes you find yourself count as "what came from you" in the appendix.

## Real problems, with evidence

### 1. Health insurance claim rejections
- **Evidence:** About **95% of health insurance complaints** to the Insurance Ombudsman in FY24 were about claims being rejected fully or partly. Health complaints rose ~22% that year, to 31,490.
- **Why the AI matters:** Policyholders win about **55%** of these cases at the ombudsman. That suggests many rejections are weak, but most people never challenge them.
- **Problem framing:** A policyholder gets a rejection letter citing a clause. The AI checks it against the actual policy wording and the IRDAI rules, and drafts a grievance with citations. The person reviews it and submits it.
- **Data:** Public policy wordings, IRDAI master circulars, and ombudsman awards are all public.

### 2. Loan and credit card complaints to banks
- **Evidence:** The RBI Ombudsman received ~**13.3 lakh complaints in FY25, up 13.5%**. Loans and credit cards are the top categories.
- **Problem framing:** Check charges and practices on a statement against the RBI circulars and the bank's own published schedule of charges, then draft a complaint.

### 3. Income tax notices from AIS mismatches (Section 143(1)(a))
- **Evidence:** These notices are **fully automated, with no human officer involved**. They trigger when your return doesn't match the AIS (Annual Information Statement) or Form 26AS. The AIS pulls data from banks, employers and brokers, and that third-party data is often wrong.
- **Problem framing:** Before filing, compare each AIS entry against your own documents and flag likely mismatches with an explanation. Code does the matching. The AI explains the source of each mismatch and suggests whether to give AIS feedback or correct your return.

### 4. GST credit denied for missing the deadline (Sections 16(4) and 16(5))
- **Evidence:** High Courts (Madras, Kerala) are repeatedly **quashing orders by GST officers** that wrongly denied input tax credit. The officers missed the retrospective relief added in Section 16(5).
- **Why it's interesting:** The officers making the decisions get it wrong, not just taxpayers. That makes it a "knowledge goes stale" problem, which the brief explicitly asks about.
- **Problem framing:** Given a denial order, check whether Section 16(5) relief applies. The dates are checked in code, and the AI points to the relevant case law.

### 5. GSTR-1 vs GSTR-3B mismatch notices
- **Evidence (from vendor blogs, so weaker):** The portal automatically compares the two returns. A gap of more than about 5% reportedly triggers a DRC-01B notice. Most notices to small businesses come from bookkeeping timing errors.
- **Downside:** This is crowded, since Tally, ClearTax and others already sell tools for it.

## My honest ranking for Tresata
1. **#1 Insurance rejections:** The best evidence (official numbers, high win rate), a clear human in the loop, easy to make up 10 test cases, and less crowded.
2. **#4 GST Section 16(5):** Sharp and niche, with a great answer to the "outdated rules" question. It needs more legal reading.
3. **#3 AIS mismatch:** Relatable and clean to split into exact vs. AI parts, but more competitors exist.

Pick one or two, and I'll help you test each against the brief: who has the problem, how often, the cost, what's out of scope, and its weakest point.

Sources:
- [Outlook Money – 95% of health insurance complaints concern claim rejections](https://www.outlookmoney.com/personal-finance/why-95-per-cent-of-health-insurance-complaints-concern-claim-rejections)
- [Cafemutual – 55% of health complaints resolved in favour of policyholders](https://cafemutual.com/news/insurance/34181-55-of-health-insurance-complaints-are-resolved-in-favour-of-policyholders)
- [Cafemutual – fewer policyholders winning rejection cases](https://cafemutual.com/news/insurance/38665-fewer-policyholders-are-winning-claim-rejection-cases)
- [RBI – Annual Report of Ombudsman Scheme 2024-25](https://website.rbi.org.in/web/rbi/-/publications/annual-report-of-ombudsman-scheme-2024-25)
- [CAalley – RBI ombudsman complaints rise 13.6% in FY25](https://caalley.com/news-updates/indian-news/rbi-ombudsman-complaints-rise-13-6-in-fy25-led-by-loan-and-card-issues)
- [TaxBuddy – Section 143(1)(a) adjustments](https://www.taxbuddy.com/blog/section-143-1-a-adjustments)
- [Business Today – 10 AIS mistakes](https://www.businesstoday.in/amp/personal-finance/tax/story/net-interest-skipped-rent-these-10-ais-mistakes-could-trigger-i-t-scrutiny-this-year-493462-2025-09-11)
- [Taxscan – Madras HC quashes ITC rejection u/s 16(4)](https://www.taxscan.in/gst/gst-s-165-madras-hc-quashes-order-rejecting-itc-us-164-orders-defreezing-of-clubs-bank-account-read-order)
- [Taxscan – Kerala HC on Section 16(5)](https://www.taxscan.in/top-stories/kerala-hc-quashes-order-denying-gst-input-tax-credit-directs-reconsideration-in-light-of-section-165-of-cgst-act-1447376)
- [Patron Accounting – bookkeeping errors and GST notices](https://www.patronaccounting.com/blog/signs-bookkeeping-wrong-gst-notices)

## USER
#1 Insurance rejections: The best evidence (official numbers, high win rate), a clear human in the loop, easy to make up 10 test cases, and less crowded. can i do this with the tresata requirement

## AI
Yes, this fits Tresata's requirements well. Here's how it maps to each requirement, plus the things to watch for.

## Does it count as "finance"?
Yes. Insurance is part of financial services in India and is regulated by IRDAI. The brief says *"tax, audit, regulation… or something else"*, and your problem is about regulation and contracts. Add one line in the brief explaining why you chose insurance.

## Requirement by requirement

| Tresata asks for | How your idea answers it |
|---|---|
| **Who, what task, how often, cost** | Policyholders, and the insurers' own grievance teams. 31,490 health complaints reached the ombudsman in a year, ~95% of them about rejections. A wrongly rejected claim can cost a family lakhs. |
| **Why now** | IRDAI's 2024 health insurance master circular reportedly shortened the moratorium (the period after which a claim can't be rejected for non-disclosure) from 8 to 5 years, and capped pre-existing disease waiting periods at 3 years. Old policy wordings and insurer habits may not have caught up. *Check these figures in the circular itself before you write them.* |
| **Out of scope** | Keep it narrow. For example: only individual health policies, only rejections for pre-existing disease (PED) or waiting periods, and only India. Exclude fraud cases, cashless pre-authorisation, and life or motor insurance. |
| **Exact vs. probabilistic** | **Exact (code):** policy start date, waiting-period math, whether the 5-year moratorium applies, claim amount vs. sum insured, and the deadline for a grievance or ombudsman complaint. **AI:** reading the rejection letter, finding the clause it cites, and judging whether the diagnosis in the discharge summary really is the pre-existing disease. |
| **Traceability** | Every output cites the exact policy clause and the IRDAI circular paragraph. No citation means no claim. |
| **Where knowledge lives** | Policy wordings and circulars sit in a retrieval index, with version dates. Date rules are in code. Medical judgment stays with a human. |
| **Human in the loop** | The policyholder or a licensed advisor reviews the draft grievance before anything is sent. The tool never says "you will win". |
| **Why AI** | Rejection letters, policy wordings and discharge summaries are unstructured and every insurer words them differently, so fixed rules alone can't read them. |
| **Weakest point** | Medical ambiguity. For example, was the patient's diabetes "pre-existing" if it was never diagnosed? The AI can be confidently wrong here, so this is exactly where the design forces a human to decide. |
| **10 test cases** | Easy to create: a realistic synthetic rejection letter, a policy excerpt and a discharge summary for each, with known correct answers. |

## Risks to handle carefully
1. **Medical data is sensitive.** Use only synthetic patients, and state this clearly.
2. **Legal advice.** Present the tool as helping someone *understand and draft* their complaint, not as representing them. The policyholder files it and is accountable for it. That mirrors how the ombudsman process works anyway: you don't need a lawyer.
3. **Policy versions.** Each insurer's wording changes over time. Your design must match the *version that was active on the policy date*. This is a good point to show sharp thinking.
4. **One-sidedness.** Interviewers may ask "isn't this just anti-insurer?" A good answer: an insurer's own grievance team could use the same tool to catch weak rejections *before* they reach the ombudsman, which saves them money.

## Verdict
It's a strong choice. The narrow scope (PED and waiting-period rejections) gives you the "simple problem, sharp reasoning" that the brief says it rewards.

## Next steps (your own work, which the appendix rewards)
1. Download 2–3 real health policy wordings from insurer websites, plus the IRDAI 2024 health master circular.
2. Read 3–5 real Insurance Ombudsman awards (published on cioins.co.in). Note *why* policyholders won or lost.
3. If possible, talk to anyone who has had a claim rejected, or to an insurance agent.

Want me to draft the problem statement and an architecture outline next? You'd edit them with what you learn in those steps.

## USER
download and keep the folder i will check

## AI
I'll find the official PDFs and download them into a `research` folder.

> _tool: WebSearch – IRDAI Master Circular on Health Insurance Business 2024 PDF irdai.gov.in_

> _tool: WebSearch – Star Health Family Health Optima policy wording PDF_

> _tool: WebSearch – Insurance Ombudsman award health pre-existing disease rejection PDF cioins.co.in_

> _tool: WebFetch – https://stableinvestor.com/2024/05/irda-master-circular-2024-pdf-download.html_

> _tool: Bash – Download research PDFs into organized folders_

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\research\README.md_

## AI
I downloaded 9 PDFs into `C:\Users\spoor\OneDrive\Desktop\tresata\research\`. All 9 are complete, valid PDFs.

```
research/
├── README.md                 ← index of every file: what it is, its source link, and cautions
├── 1_regulation/
│   └── IRDAI_Master_Circular_Health_2024-05-29.pdf
├── 2_policy_wordings/
│   ├── StarHealth_FamilyHealthOptima_wording_V26.pdf     (current, 44 pages)
│   ├── StarHealth_FamilyHealthOptima_wording_V19_2023_old.pdf  (older version)
│   └── StarHealth_FamilyHealthOptima_prospectus.pdf
├── 3_ombudsman_awards/       (official, from cioins.co.in)
│   ├── CIO_Mediclaim_Book14.pdf   (308 pages of real cases)
│   ├── CIO_Mediclaim_Book11.pdf
│   └── CIO_GroupMediclaim_Book14.pdf
└── 4_court_judgments/
    ├── PH_HC_PED_must_be_diagnosed_not_symptomatic.pdf
    └── PH_HC_no_inferential_PED_denial.pdf
```

**Before you cite anything:**
- **The IRDAI circular, the newer policy wording and both court judgments come from third-party websites, not official ones.** Check each against irdai.gov.in, starhealth.in or the court's own site before quoting it in your brief.
- **The ombudsman award books are older, from before the 2024 rule changes.** They're good for learning *how* rejections get argued, but the specific rules in them may be out of date.
- **Having an old and a new version of the same policy is useful.** Comparing them shows the "rules change over time" problem that Tresata asks about.

**Still missing:** the Insurance Ombudsman Rules (they set the deadline to complain and the maximum award) and recent 2024–26 awards from cioins.co.in. Both are listed in the README for you to fetch.

**Suggested reading order:** the circular's sections on pre-existing disease and waiting periods, then the exclusions in the policy wording, then 3–5 awards that mention "pre-existing", then the two short court judgments. Write down what surprises you as you read. Tresata asks for that in the brief.

## USER
i have zero knowledge on this. can you please explain this in simple words.

## AI
No problem. Here it is from the very beginning, with no jargon.

## 1. What is health insurance?
You pay a company a fixed amount every year, called the **premium** (say ₹15,000). If you get sick and go to hospital, the company pays the hospital bill, up to a limit called the **sum insured** (say ₹5 lakh).

It's like a deal: *"I pay you a little every year, and you pay my big hospital bills when they happen."*

## 2. What is a "claim"?
When you're in hospital and ask the insurance company to pay, that request is a **claim**. The company can:
- **Approve** it and pay,
- **Partly pay** it (pay only some of the bill), or
- **Reject** it and pay nothing.

## 3. Why do companies reject claims?
The most common reason is **"pre-existing disease" (PED)**.

**A simple example:**
- Ramesh already has diabetes when he buys insurance in 2024.
- Diabetes is a **pre-existing disease**, an illness he had *before* buying the policy.
- If he's hospitalised for diabetes in 2025, the company says: *"You already had this before you joined. We won't pay yet."*

Why? Otherwise people would buy insurance only *after* falling sick, and the company would lose money.

## 4. Waiting period
The company doesn't refuse pre-existing diseases forever. It says: *"Wait a few years first."*
- That gap is the **waiting period**. After it ends, your old disease is covered.
- IRDAI's 2024 rules reportedly limit this waiting period to a maximum of **3 years**. *Confirm this in the circular in your folder.*

There's also usually a **30-day initial waiting period**: claims for illnesses in the first month are not covered, except accidents.

## 5. Moratorium period
After you've held the policy continuously for **5 years**, the company **cannot reject a claim saying "you hid a disease"**, except in proven fraud. This protects long-time customers. *Also confirm this figure in the circular.*

## 6. The problem: wrong rejections
Companies sometimes reject claims **wrongly**. For example:
- They call something "pre-existing" when it was never actually **diagnosed** before. The court judgments in your folder say exactly this: having symptoms is not the same as having a diagnosis.
- They ignore that the waiting period has already ended.
- They apply an **old version** of the policy rules.

The customer gets a confusing letter: *"Claim rejected under Clause 4.1."* They don't understand it and usually just give up.

## 7. Who is IRDAI?
The **government regulator** for insurance, like a referee. It writes the rules every insurance company must follow. The **Master Circular** in your folder is its rulebook for health insurance.

## 8. What is the Insurance Ombudsman?
A **free complaint office** set up for customers. If your claim is rejected and the company's own complaint team doesn't help, you can complain to the ombudsman. No lawyer is needed.
- Real data shows customers win about **half** of these cases. That means many rejections were wrong.
- The **award books** in your folder are records of real cases: who complained, what happened, and who won.

## 9. Your project idea in one line
> **A tool that reads a claim rejection letter, checks it against the policy rules and IRDAI rules, tells the customer whether the rejection looks valid, and helps them write a complaint. A human always makes the final decision.**

**How it would work:**

| Step | Who does it |
|---|---|
| Read the rejection letter and find which clause was used | **AI** (letters are messy and every company writes them differently) |
| Calculate: is the waiting period over? Has the policy run for 5+ years? | **Code** (simple date math, always exact) |
| Find the matching rule in the policy wording and the IRDAI circular | **AI + search over documents** |
| Judge whether the disease was truly "pre-existing" | **Human** (a medical judgment, too risky to leave to AI) |
| Draft a complaint letter with clause references | **AI** |
| Check the draft and submit it | **Human** (the customer) |

## 10. Why Tresata will like this
- **Real problem:** official ombudsman numbers prove it.
- **Clear split:** code for exact things (dates, amounts), AI for reading messy text, a human for final judgment. That is exactly what their brief asks you to show.
- **Rules change over time** (the old vs. new policy in your folder), which answers their *"what if the knowledge becomes outdated?"* question.

## Words to remember

| Word | Meaning |
|---|---|
| Premium | The yearly amount you pay |
| Sum insured | The maximum the company will pay |
| Claim | Asking the company to pay |
| Pre-existing disease (PED) | An illness you had before buying the policy |
| Waiting period | Time before an old illness gets covered |
| Moratorium | After 5 years, the company can't reject for "hidden disease" |
| Policy wording | The full contract document |
| IRDAI | The government referee for insurance |
| Ombudsman | A free complaint office for customers |

**Your homework:** open the policy wording (V26) and search for "pre-existing" (Ctrl+F). Read just that part. Then come back and tell me in your own words what it says. Explaining it back is how you'll learn it, and it's good material for your appendix.

## USER
ok lets start building

## AI
I'll check what's installed first, then read the actual rules in the PDFs so the code uses real clauses rather than guesses.

> _tool: Bash – Check Python, pip, and libraries_

> _tool: Bash – Extract PDF text and search circular for key rules_

> _tool: Bash – Read moratorium clause and claim rules in circular_

> _tool: Bash – Read repudiation rule and policy PED clauses_

> _tool: Bash – Read PED definition and exclusions in V26 and V19_

> _tool: Bash – Read V19 exclusions and initial waiting clause_

## AI
I have the real clause numbers I need. Let me get page numbers so every citation can be checked by hand.

> _tool: Bash – Locate PDF page numbers for each clause_

> _tool: Bash – Get remaining V19 page numbers_

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\knowledge\rules.json_

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\engine.py_

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\extractor.py_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\engine.py_

## AI
Now the 12 test cases. All are synthetic, made up by me, and each one tests a specific rule.

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\cases\cases.json_

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\run.py_

> _tool: Bash – Run evaluation on all cases with gold facts_

> _tool: Bash – Test that a fabricated AI fact gets dropped_

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\README.md_

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\requirements.txt_

## AI
The first working version of the prototype is built in `C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\`. The rules part passes all 12 test cases, but the AI reading step hasn't been run yet because it needs a free API key.

## How it works
- **The AI only reads the documents.** It turns the rejection letter, discharge summary and policy schedule into structured facts, and must copy an exact quote from the documents as proof for each fact.
- **Plain code makes the decision.** It does the date math and applies the policy rules. Every rule comes from the real PDFs, with a page number.
- **The output is one of three answers:** the rejection looks valid, it looks wrong, or a human must decide. Each comes with citations.
- **If the rejection looks wrong, it drafts a complaint letter.** The policyholder reviews and sends it.

## What I found in the real documents
- **The old policy (V19) makes you wait 48 months for pre-existing diseases. The new one (V26) makes you wait 36 months.** Test cases C03 and C04 have identical facts and opposite answers, purely because of the policy version.
- **The IRDAI circular confirms the 5-year (60-month) rule.** After 60 months, an insurer can't reject a claim for "you hid a disease" unless fraud is proven (para 13, p.8).
- **The circular also says every rejection must cite a specific policy clause** (para 17(b), p.9). The tool flags letters that don't.

## Results so far
- **Rules engine: 12/12 correct.** This only shows the code matches my reading of the clauses, since I wrote both the cases and the rules. Don't present it as real accuracy.
- **Hallucination guard: works.** When the AI invented a diagnosis date that wasn't in the documents, the tool dropped that fact and sent the case to a human. Without the guard, it would have wrongly told the person the rejection was fine.
- **AI reading step: not tested yet.** This is the real test.

## What I need from you
A **free OpenRouter API key**:
1. Sign up at https://openrouter.ai and create a key.
2. In this prompt, run: `! $env:OPENROUTER_API_KEY="your-key"; python run.py --eval --mode llm`

The key never gets written into the files. After that run, we'll write up honestly where the AI got things wrong.

**Before your interview:** run `python run.py --case C06` and read the output line by line. If you can explain why C06's answer is "the rejection is wrong", you can defend the core of this project live.

## USER
do i need ot paste key here

## AI
No, don't paste it here. This chat becomes part of the LLM logs you submit to Tresata, so a key pasted here would be visible to anyone who reads them. The `!` command I suggested would also put it in the log. Sorry, I should have pointed that out.

Instead, I'll make the tool read the key from a private file that only you create.

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\extractor.py_

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\.gitignore_

## AI
The tool can now read your key from a private file, so it never has to appear in this chat or your logs.

**Steps:**
1. Open **Notepad**.
2. Type one line, with your real key after the `=`:
   ```
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxx
   ```
3. Save it as `C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\.env`
   - In the Save dialog, set **"Save as type" to "All Files"**. Otherwise Notepad saves it as `.env.txt` and the tool won't find it.
4. Come back here and type **"done"**. I'll run the test.

**Why this is safe:**
- I never see the key. The code reads it from the file and doesn't print it.
- `.env` is listed in `.gitignore`, so it won't be uploaded if you put this project on GitHub.
- Don't include the `.env` file in the zip you submit to Tresata.

## USER
i pasted direcrtly in extractor.py file

## AI
A key inside `extractor.py` is risky. That file is code you'll submit to Tresata and maybe put on GitHub, so the key would leak with it. I'll move it to the private `.env` file without displaying it, so it stays out of this chat and your logs.

> _tool: Bash – Move API key into .env, show masked location_

> _tool: Bash – Restore code line and run AI evaluation_

> _tool: Bash – Show the error message from first case_

## AI
The key is fine. The model name I picked no longer exists on OpenRouter. I'll check which free models are available right now.

> _tool: Bash – List currently available free OpenRouter models_

> _tool: Bash – Switch to an available free model and rerun AI evaluation_

> _tool: Bash – Check new error and model setting_

## AI
The model now works, but the free tier is rate-limiting us (error 429: too many requests). I'll add automatic retry with waiting.

> _tool: Read – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\extractor.py_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\extractor.py_

> _tool: Bash – Try one case with the AI, with retries_

## AI
Working. Now running all 12 cases with the AI. This takes a few minutes on the free tier.

> _tool: Bash – Run full AI evaluation on all 12 cases_

## AI
The full run is still going in the background. The free tier is slow, so I'll report the results when it finishes.

So far:
- **Your key is safe.** It's now only in the private `.env` file. I checked and it's no longer in `extractor.py`, and it was never printed in this chat.
- **Two problems are fixed.** The model name I'd picked had been retired, so I switched to Google's free `gemma-4-31b-it`. I also added automatic retries for when the free tier says "too many requests".
- **The first AI test passed.** On C07, the tricky case where only symptoms existed before the policy, the AI read the documents correctly and the tool rightly sent the case to a human.

**Going forward:** when you need to change a key or password, put it in `.env`, never in a `.py` file.

> _tool: Bash – Read results saved before the run was stopped_

## AI
The full test run didn't finish, and it produced no usable AI results.

- **Claude Code stopped it** because your computer was running low on memory. That wasn't caused by the script.
- **The free tier was also refusing most requests.** Cases C03 to C07 all failed with "Too Many Requests", even with the automatic retries.
- **The only AI result so far is C07**, from the earlier single-case test, and it was correct.

I won't restart it on my own. When you're ready, you have two options:

1. **Run it yourself**, which is easiest on memory. Close other apps (browser tabs especially), then type:
   ```
   ! python run.py --eval --mode llm --quiet
   ```
   It needs about 10–15 minutes.
2. **I run it in small batches** (a few cases at a time with longer pauses), which is gentler on the rate limit. Just say "run in batches".

The free tier will keep rejecting requests if we hit it too fast. That's fine to mention honestly in your README as a limitation of testing on free models.

## USER
GO HEAD

## AI
I'll run one case per call so each finishes well within the time limit and memory stays low.

> _tool: Bash – Run AI evaluation on cases C01-C03_

## AI
C01 is correct. C02 hit the rate limit again, so this Gemma model is overloaded on the free tier. C03 is still running in the background. When it finishes, I'll switch the remaining cases to a less busy free model, NVIDIA's Nemotron.

> _tool: Bash – Check C03 result and try C02 with Nemotron_

## AI
Nemotron is responding quickly. Running the rest:

> _tool: Bash – Run AI evaluation on C04-C07 with Nemotron_

> _tool: Bash – Run AI evaluation on C08-C12 with Nemotron_

## AI
All 12 cases pass with the AI reading the documents. Before celebrating, I'll check field by field whether the AI read each fact correctly. A right verdict can hide a wrong fact.

> _tool: Bash – Compare AI-extracted facts against gold facts_

> _tool: Read – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\README.md_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\README.md_

## AI
The full test is done. **All 12 verdicts are correct with the AI reading the documents**, and I've written the results into the README.

**I found real mistakes.** When I compared every fact the AI pulled out against my answer key, **6 of 144 facts were wrong**:

| Mistake | Why it matters |
|---|---|
| C01: the schedule said "declared: **None**" and the AI read it as "declared = **yes**" | Harmless in this case. In a pre-existing disease case it could flip the verdict. |
| C03: the AI **invented a treatment date** (09/01/2023) that isn't in the documents | My guard missed it. The quote ("on oral hypoglycaemics") was real, but the date was the AI's guess. |
| C05: the AI missed a treatment date | My own answer-key date was also an assumption, so this one is partly my error. |
| 3 cases: "Excl 03" instead of "Code Excl 03" | Formatting only, harmless. |

**This matters for Tresata because they explicitly asked you to "report honestly where it fails".** The C03 finding is the most useful thing to write about. It shows that checking whether a quote is real isn't enough; you also have to check that the AI's reading of the quote is right. Write it up in your own words. It shows you understand where your design is weak.

**Be honest about the limits:**
- The 12 cases are clean, typed text, written by the same person who wrote the rules, so 12/12 overstates how well it would do on real scanned letters.
- Two different free models were used, because the first kept getting rate-limited. The README says which case used which model.

**Next steps, you choose:**
1. **Fix the weakness:** require any date the AI reports to appear in its quote. That closes the C03 gap.
2. **Add 3–4 harder, messier cases** (typos, a Hindi line, two admissions) to find more failures.
3. **Start the 4-page written brief and the architecture diagram.** That is where most of your marks are.

I'd recommend **3**, then come back to 1 if there's time.

## USER
add now go head

## AI
I'll do both: fix the weakness, then add 4 harder test cases.

> _tool: Read – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\extractor.py_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\extractor.py_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\extractor.py_

> _tool: Read – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\engine.py_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\engine.py_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\engine.py_

## AI
Now the 4 harder cases:

> _tool: Bash – Add 4 hard cases and rerun gold evaluation_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\claimcheck\engine.py_

> _tool: Bash – Rerun gold evaluation after fix_

## AI
Now the full AI run on all 16 cases with the stricter guard, one case at a time:

> _tool: Bash – Run AI evaluation on C01-C08_

## AI
C04 is now wrong, and it's a dangerous error: the tool said "fight" when the insurer was right. Checking why:

> _tool: Bash – Inspect C04 AI extraction and findings_

> _tool: Bash – Fix prompt and add contradiction check, retest C03-C04_

## AI
Fixed. Now the remaining cases, including the 4 hard ones:

> _tool: Bash – Run AI evaluation on remaining and hard cases_

> _tool: Bash – Rerun C15 and recheck changed cases, inspect hard cases_

> _tool: Bash – Retry C06 after network error_

## AI
All 16 pass. Updating the README with what failed and how each failure was fixed.

> _tool: Read – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\README.md_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\README.md_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\README.md_

## AI
I added 4 hard test cases and they exposed 4 new problems, including two dangerous ones. All are fixed, and **all 16 cases now give the right answer, with zero "fight a valid rejection" errors.**

## The 4 hard cases
| Case | What makes it hard | Result |
|---|---|---|
| C13 | Typos from a bad scan, "diagnosed **3 yrs back**" with no actual date, and a vague letter | Correctly sent to a human |
| C14 | The key fact is only in **Hindi** ("मरीज़ को 2019 से मधुमेह है", "the patient has had diabetes since 2019") | The AI read it correctly; sent to a human |
| C15 | **Two hospital admissions**, and picking the wrong date flips the answer | The AI picked the right one |
| C16 | The insurer **cited the wrong clause**, but a different exclusion still applies | Correctly sent to a human instead of saying "fight" |

## What broke and how it was fixed
1. **Missing date taken as "not pre-existing" (C13).** With no date to check, the engine concluded "not pre-existing" and told the person to fight. **Fix:** a missing date now means "I don't know", and a human decides.
2. **AI took the wrong date (C04).** It read the date of the *complication* (diabetic ketoacidosis, 2026) instead of the *disease* behind it (diabetes, since 2021). **Fix:** a clearer prompt, plus a contradiction check. If the schedule says the disease was declared before the policy but the diagnosis date is after the policy start, the case goes to a human.
   - C03 had the same misreading earlier but got the right answer **by luck**. That's worth mentioning in your brief.
3. **Invented date with a real quote (C03, earlier).** **Fix:** any date the AI reports must now appear inside its quote.
4. **Wrong clause cited (C16).** **Fix:** the engine now also checks exclusions the insurer *didn't* cite before telling anyone to fight.

## Most important lesson for your brief
The dangerous errors weren't the AI inventing things. **They were real facts used wrongly.** The design answer was to make "I don't know, ask a human" the default whenever facts are missing or contradict each other.

**Be honest about this:** 16/16 is on cases I wrote and then fixed the system against, so it is **not** a real accuracy number. The README says so.

Everything, including the full list of failures and fixes, is in `C:\Users\spoor\OneDrive\Desktop\tresata\claimcheck\README.md`.

**Next:** the 4-page written brief and the architecture diagram, which carry most of the marks. Want to start? I'll draft the structure and you fill in your own learnings, since the appendix must show your own thinking.

## USER
ok go head

## AI
I'll write it as an editable draft in the project folder. Places marked **[YOU]** need your own words. Tresata will read your chat logs, so those parts must genuinely come from you.

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\BRIEF_DRAFT.md_

> _tool: Edit – C:\Users\spoor\OneDrive\Desktop\tresata\BRIEF_DRAFT.md_

## AI
I've written a first draft of the brief: `C:\Users\spoor\OneDrive\Desktop\tresata\BRIEF_DRAFT.md`. I haven't checked its length against the 4-page limit yet; I'll do that when we make the PDF.

**What it covers (matching Tresata's checklist):**
1. **The area and what surprised you:** the ombudsman numbers, and the same product having 48- vs 36-month rules in different versions.
2. **Problem statement:** who, what task, how often, what it costs today, why now, and what's in and out of scope.
3. **Solution design:**
   - an architecture diagram showing where the AI, the code and the human each act
   - which parts must be exact and which can be AI
   - where the knowledge lives and what happens when it goes out of date
   - how mistakes are handled
   - why AI is needed
   - 5 rejected alternatives
   - who is accountable, given that this touches legal advice
4. **Prototype results:** stated honestly, including the 6 failures and the "real facts used wrongly" lesson.
5. **Risks, the weakest point, and what to do next.**
6. **Appendix:** a skeleton only. You must write this part.

**What you must do yourself (marked [YOU]):**
- **Write the appendix in your own words.** Tresata will compare it with your chat logs.
- **Pick what genuinely surprised you.** Delete my suggestions if they didn't surprise you.
- **Add one alternative you thought of yourself.**
- **Check every number and source:** the ombudsman figures, the court judgments (they came from unofficial websites), and the data protection law point. I corrected one mistake of my own there: I'd wrongly called health data "sensitive" under the DPDP Act.
- **Practise explaining the C03 vs C04 example out loud.** That's your "defend without AI" answer.

**Remaining steps:**
1. You edit the [YOU] parts.
2. I turn it into a clean 4-page PDF with a proper diagram, plus a 1-page appendix.
3. We put the code on GitHub with a public link, without the `.env` file.
4. You export these chats as your LLM logs.

Tell me when your edits are done, or if you want any section rewritten first.

## USER
write the appindix also i simple words.

## AI
I'll write it in simple words, based only on what actually happened in our conversation. Tresata will compare this appendix with your chat logs, so it can't claim things you didn't do. Where the true answer is thin, I'll leave a gap for you to fill rather than invent something.

> _tool: Read – C:\Users\spoor\OneDrive\Desktop\tresata\BRIEF_DRAFT.md_

> _tool: Bash – Find appendix section line numbers_

> _tool: Bash – Replace appendix section with simple-words version_

## AI
The appendix is now in `C:\Users\spoor\OneDrive\Desktop\tresata\BRIEF_DRAFT.md`, in simple words, in four parts:

1. **Where AI helped:** what you used it for, plus 3 of your real prompts quoted exactly from this chat.
2. **What you rejected or corrected:** the meaningless first "12/12", the AI's own mistakes (retired model name, unsafe API-key advice, the wrong data-protection law claim), and unreliable web sources.
3. **What came from you:** choosing the problem, asking for real-world evidence, insisting on simple explanations.
4. **What you'd defend without AI:** the C03 vs C04 example, explained step by step.

**Some of this is thinner than it should be, and you should fix that before submitting:**
- **Part 2:** I warned you the tax-treaty idea was too close to Tresata's example, and I suggested the harder test cases. Your role was choosing and approving. If an interviewer asks, say exactly that: "the AI flagged it, I agreed."
- **Part 3 is the weakest.** Right now your own contribution is mostly *choices*, not *insights*. Tresata values insights most. The fastest way to add one:
  1. Open `research\3_ombudsman_awards\CIO_Mediclaim_Book14.pdf` and press **Ctrl+F** to search for "pre-existing".
  2. Read **2–3 cases** (about 20 minutes).
  3. For each, write one line: what was rejected, who won, and why.
  
  That gives you a genuine "I learned this from a real document" point, which is exactly what they ask for.
- **Fill the three ✎ lines.** If you have nothing for one, delete it rather than make something up.

**Practise part 4 out loud once:** "38 months of cover, the old rule needs 48, the new rule needs 36, so the same claim gets opposite answers." If you can say that without notes, you're ready for that question.

When you've read the awards and filled the ✎ lines, tell me and I'll turn the whole brief into a clean PDF.

## USER
do and give me required things to submit

## AI
I'll make all three submission items. First, checking what's available for building the PDF:

> _tool: Bash – Check PDF tools and transcript location_

## AI
Chrome is installed, so I'll lay out the brief as a print-ready page and save it to PDF. I'm also tightening the text to fit the 4-page limit.

> _tool: Write – C:\Users\spoor\OneDrive\Desktop\tresata\submission\brief.html_

> _tool: Bash – Render brief to PDF with Chrome and count pages_

## AI
3 pages of brief plus a 1-page appendix, within the limit. Checking how it looks:

> _tool: Read – C:\Users\spoor\OneDrive\Desktop\tresata\submission\ClaimCheck_Brief.pdf_

> _tool: Bash – Screenshot top of brief to check layout_

> _tool: Read – C:\Users\spoor\AppData\Local\Temp\claude\C--Users-spoor-OneDrive-Desktop-tresata\105e8494-f22f-43ab-91cb-47140ffbb9bb\sc_

## AI
The layout looks clean. Now the prototype repo and the LLM logs. First, safety checks that your API key isn't anywhere it shouldn't be:

> _tool: Bash – Check for leaked API key and GitHub login_

> _tool: Bash – Initialize local git repo and check tracked files_

> _tool: Bash – Add sources file and key instructions, check git identity_

## AI
This computer's git is set up for a different person (KarthiCheripelly), so I'll set your name only for this project. That way the commit is credited to you:

> _tool: Bash – Commit locally with user's identity for this repo only_
