"""AI step: read messy documents -> structured facts, each backed by a VERBATIM quote.

The LLM never decides the verdict. It only reads. Any fact whose quote cannot be
found word-for-word in the documents is thrown away (set to null), which pushes
the engine toward NEEDS_HUMAN instead of a confident wrong answer.
"""
from __future__ import annotations
import json, os, re
import requests

MODEL = os.environ.get("OPENROUTER_MODEL", "nvidia/nemotron-3.5-super-vl:free")
URL = "https://openrouter.ai/api/v1/chat/completions"

FIELDS = {
    "policy_uin": "UIN printed on the policy schedule, e.g. SHAHLIP26046V092526",
    "first_inception_date": "YYYY-MM-DD first policy start date with this insurer",
    "prior_continuous_coverage_months": "integer months of prior cover ported from another insurer, 0 if none",
    "admission_date": "YYYY-MM-DD hospital admission date",
    "accident": "true if hospitalisation was caused by an accident",
    "condition": "condition treated, short text",
    "specified_disease_category": "true if condition is one of: cataract/eye, ENT, thyroid, benign breast, benign lumps/cysts, joint/bone/ligament (non-accident), spine/disc, gall bladder/pancreas/kidney stones, hernia, hydrocele, piles/fistula, uterus/fibroids, prostate, varicose veins; false otherwise; null if unsure",
    "diagnosis_date": "YYYY-MM-DD first documented diagnosis of the UNDERLYING disease the insurer calls pre-existing (e.g. diabetes, not its complication ketoacidosis); use 01 for unknown day; null if not stated",
    "last_advice_or_treatment_before_inception": "YYYY-MM-DD most recent treatment/medication/advice for this condition BEFORE the policy start; null if none",
    "symptoms_before_inception": "true if only symptoms (no diagnosis/treatment) are mentioned before policy start",
    "declared_at_proposal": "true/false if the documents say whether it was declared in the proposal form; null if not stated",
    "rejection_grounds": "list from: initial_waiting, specified_waiting, ped, non_disclosure, other",
    "clause_cited": "clause/exclusion code the rejection letter cites, null if none",
}

PROMPT = """You extract facts from Indian health insurance claim documents. Do NOT judge the claim.
Return ONLY a JSON object with two keys:
"facts": an object with exactly these keys:
{fields}
"evidence": an object mapping each non-null fact key to a SHORT quote copied VERBATIM from the documents that supports it.
If a fact is not stated, use null. Never guess dates.

DOCUMENTS:
{docs}"""


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def _load_key():
    """Key comes from env var, or from a private .env file next to run.py (never committed, never printed)."""
    key = os.environ.get("OPENROUTER_API_KEY")
    env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if not key and os.path.exists(env):
        for line in open(env, encoding="utf-8-sig"):
            if line.strip().startswith("OPENROUTER_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    return key


def call_llm(prompt: str) -> str:
    key = _load_key()
    if not key:
        raise RuntimeError("Set OPENROUTER_API_KEY (free key from https://openrouter.ai) or run with --mode gold")
    import time
    for attempt in range(6):
        r = requests.post(URL, timeout=180, headers={"Authorization": f"Bearer {key}"}, json={
            "model": MODEL, "temperature": 0,
            "messages": [{"role": "user", "content": prompt}],
        })
        if r.status_code in (429, 502, 503):  # free-tier rate limit / busy: wait and retry
            time.sleep(15 * (attempt + 1))
            continue
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    r.raise_for_status()


def parse_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("LLM returned no JSON")
    return json.loads(m.group(0))


DATE_FIELDS = ("first_inception_date", "admission_date", "diagnosis_date", "last_advice_or_treatment_before_inception")
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def _value_supported(k, v, quote) -> bool:
    """Second guard (added after test run 1): a real quote is not enough - the VALUE must be visible in it.
    Catches the C03 failure where a real quote ('on oral hypoglycaemics') was used to back an invented date."""
    q = quote.lower()
    if k in DATE_FIELDS:
        try:
            y, m, _ = str(v).split("-")
        except ValueError:
            return False
        yy = y[2:]
        has_year = y in q or re.search(rf"[/\-.]{yy}\b", q)
        has_month = MONTHS[int(m) - 1] in q or re.search(rf"\b0?{int(m)}[/\-.]", q)
        return bool(has_year and has_month) or (bool(has_year) and k == "diagnosis_date" and int(m) == 1)
    if k == "declared_at_proposal" and v is True:
        return not re.search(r"\b(nil|none|no)\b", q)  # C01: "declared: None" was read as True
    return True


def extract(documents: dict, llm=call_llm) -> dict:
    docs = "\n\n".join(f"--- {k.upper()} ---\n{v}" for k, v in documents.items())
    raw = parse_json(llm(PROMPT.format(fields=json.dumps(FIELDS, indent=1), docs=docs)))
    facts, ev = raw.get("facts", {}), raw.get("evidence", {}) or {}
    corpus = _norm(docs)
    dropped = []
    for k, v in list(facts.items()):
        if k not in FIELDS:
            facts.pop(k); continue
        if v in (None, False, 0, [], "") or k in ("prior_continuous_coverage_months",):
            continue
        q = ev.get(k)
        if not q or _norm(str(q)) not in corpus or not _value_supported(k, v, str(q)):
            dropped.append(k)
            facts[k] = None
    return {"facts": facts, "evidence": ev, "dropped_unverified": dropped, "model": MODEL}
