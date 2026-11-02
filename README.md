# ClaimCheck – Is this health-insurance rejection valid?

Prototype for the Tresata take-home. Jurisdiction: **India (IRDAI)**. Scope: individual health policies,
rejections on **pre-existing disease (PED), non-disclosure, specified-disease waiting period, 30-day initial waiting**.
Knowledge base currently covers one product in two versions: Star Health *Family Health Optima* V.19 (2023) and V.26 (2026).

## How it works
```
 documents (schedule, rejection letter, discharge summary)
        │
        ▼
 [AI] extractor.py ── reads text → structured facts + a VERBATIM quote for each fact
        │                 any fact whose quote is not found in the documents is DROPPED
        ▼
 [CODE] engine.py ──── date maths + rules from knowledge/rules.json (every number has a clause + page)
        │                 outputs LIKELY_VALID / LIKELY_INVALID / NEEDS_HUMAN with citations
        ▼
 [CODE] template ───── draft grievance letter (only if LIKELY_INVALID)
        │
        ▼
 [HUMAN] policyholder / advisor reviews, edits, sends. Medical & fraud questions always go to a human.
```
The AI never decides the verdict. It only reads.

## Run
```bash
pip install requests
python run.py --eval                 # rules engine on hand-written facts (no key needed)
python run.py --case C06             # one case with full reasoning + draft letter
# full pipeline with the AI reading the documents:
export OPENROUTER_API_KEY=...        # free key: https://openrouter.ai
export OPENROUTER_MODEL=nvidia/nemotron-3.5-super-vl:free   # optional (this is the default)
python run.py --eval --mode llm
```
Outputs are saved in `outputs/`. The `outputs/` folder in this repo holds the final run: `*_gold.json` (engine on hand-written facts) and `*_llm.json` (full pipeline, AI reading the documents).

## Test cases (`cases/cases.json`) – ALL SYNTHETIC (made up; names and people are fictional)
| ID | What it tests | Expected |
|---|---|---|
| C01 | 30-day waiting, real illness | valid |
| C02 | 30-day waiting wrongly applied to accident | invalid |
| C03 | Declared PED, 36-month wait over (V26) | invalid |
| C04 | Same as C03 but old wording V19 (48 months) | valid |
| C05 | Undeclared hypertension, 13 months | valid |
| C06 | Non-disclosure after 67 months → moratorium | invalid |
| C07 | Only symptoms before policy | needs human |
| C08 | Cataract at 12 months (24-month list) | valid |
| C09 | Kidney stone at 27 months | invalid |
| C10 | Ported policy (credit) + no clause cited | invalid + flag |
| C11 | Unknown policy wording | needs human |
| C12 | Diagnosed 2012 but treated within 36 months | valid |
| C13 | HARD: OCR noise, relative date "3 yrs back", vague letter | needs human |
| C14 | HARD: key fact only in Hindi; old diagnosis, no treatment date | needs human |
| C15 | HARD: two admissions; must pick the claimed one | invalid |
| C16 | HARD: insurer cites wrong clause, but another exclusion applies | needs human |

## Results – final run (16 cases, after fixes): 16/16 verdicts, 0 dangerous errors
Model: `nvidia/nemotron-3.5-super-vl:free`. Two calls failed with network errors ("Response ended prematurely")
and were retried. The AI read the Hindi line in C14 correctly ("2019 से मधुमेह" → 2019).

### What failed along the way, and the fix (iteration log)
| # | Failure found | Type | Fix |
|---|---|---|---|
| 1 | C03: AI invented a treatment date backed by a real but dateless quote | AI reading | Guard 2: a date must be visible *inside* its quote |
| 2 | C01: "PED declared: None" read as declared = true | AI reading | Guard 2: a "true" with nil/none/no in the quote is dropped |
| 3 | C13 (gold facts): no diagnosis date → engine said "not PED" → **told user to fight** | **Rule design** | Missing date now → NEEDS_HUMAN, never "not PED" |
| 4 | C14 design: old diagnosis + no treatment record would have been "not PED" | Rule design | Absence of a treatment record ≠ no treatment → NEEDS_HUMAN |
| 5 | C16: wrong clause cited → engine would say "fight", but Excl 02 applies anyway | Rule design | Engine re-checks exclusions the insurer did *not* cite |
| 6 | C04 (LLM): AI took the date of the *complication* (ketoacidosis, 2026) not the *disease* (diabetes, 2021) → **told user to fight a valid rejection**. C03 had the same misreading but got the right answer by luck. | AI reading | Prompt clarified + engine contradiction check: "declared as PED" but "diagnosed after policy" → NEEDS_HUMAN |

**Key lesson:** the most dangerous errors (3, 6) were not hallucinated text – they were real facts used wrongly.
The design answer was to make "I don't know" the default whenever facts are missing or contradict each other.

### First run (12 cases, before fixes) – kept for honesty
- **Gold facts (engine only): 12/12.** This only proves the code matches *my* reading of the clauses – I wrote both.
- **LLM mode (full pipeline): 12/12 verdicts correct.** Models: `google/gemma-4-31b-it:free` (C01, C03) and
  `nvidia/nemotron-3.5-super-vl:free` (C02, C04–C12) – switched because Gemma's free tier kept returning HTTP 429.
- **Field-level check: 6 of 144 extracted facts differ from my gold facts.** Verdicts were right, but the reading was not perfect:
  | Case | Field | Gold | AI | Harm |
  |---|---|---|---|---|
  | C01 | declared_at_proposal | not stated | **true** (schedule said "declared: None") | Misread "None" as yes. Harmless here, dangerous in a PED case. |
  | C03 | last treatment before inception | none | **2023-01-09 (invented)** | Date not in documents; the quote check passed because the *quote* ("on oral hypoglycaemics") was real – the *date* was inferred. |
  | C05 | last treatment before inception | 2024-12-01 | none | My gold value was itself an inference. Verdict still held via diagnosis date. |
  | C02, C09, C11 | clause_cited | "Code Excl 03" | "Excl 03" | Formatting only. |
- **Lesson:** the verbatim-quote guard stops invented quotes, but NOT a wrong interpretation of a real quote. Next fix:
  dates must appear in the quote itself, and yes/no fields need the quote to contain the value.
- **Caveat:** these 12 cases are clean, typed, and written by the same person who wrote the rules. Real letters
  (scanned, Hindi/regional language, multiple admissions) will be much harder. This is a proof of idea, not an accuracy claim.
- Hallucination guard test: a fabricated diagnosis date was dropped and the case routed to NEEDS_HUMAN.

## Known limitations (honest)
- 16/16 is on cases I wrote myself, after fixing what they exposed – it is NOT an accuracy estimate.
  New unseen cases are needed for that.
- Only one product, two versions. Any other UIN → NEEDS_HUMAN.
- Exact dates: "since June 2021" is stored as 2021-06-01. Edge cases near a boundary month can flip.
- Medical judgment (is this a "direct complication" of a PED?) is not checked – taken from the letter.
- Whether a condition is on the Excl 02 list is decided by the AI – a possible error point.
- The circular and two policy PDFs were downloaded from third-party mirrors; verify against irdai.gov.in / insurer site.

## Source documents
The public PDFs (IRDAI circular, policy wordings, Ombudsman award books, court judgments) are not committed –
see `SOURCES.md` for download links. `knowledge/rules.json` records the clause and page used from each.

## API key
Either set `OPENROUTER_API_KEY` in your environment, or create a file `.env` next to `run.py` containing
`OPENROUTER_API_KEY=...`. `.env` is git-ignored – never commit it.

## LLM logs
`llm_logs/LLM_chat_log.md` is the readable conversation with the LLM (Claude Code) used to research, design and build this, with tool calls summarised. `llm_logs/LLM_raw_transcript.jsonl` is the raw session transcript.
