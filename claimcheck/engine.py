"""Deterministic rules engine. NO AI in this file.

Input: structured facts (from the AI extractor, or hand-written gold facts).
Output: a verdict per rejection ground, with the exact clause behind each step.

Verdicts:
  LIKELY_VALID    - the rules support the insurer's rejection
  LIKELY_INVALID  - the rules contradict the rejection -> worth a grievance
  NEEDS_HUMAN     - a judgment the code must not make (medical, fraud, missing facts)
"""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path

RULES = json.loads((Path(__file__).parent.parent / "knowledge" / "rules.json").read_text(encoding="utf-8"))

VALID, INVALID, HUMAN = "LIKELY_VALID", "LIKELY_INVALID", "NEEDS_HUMAN"


def d(s):
    return date.fromisoformat(s) if s else None


def months_between(a: date, b: date) -> int:
    """Completed months from a to b."""
    m = (b.year - a.year) * 12 + (b.month - a.month)
    if b.day < a.day:
        m -= 1
    return m


class Finding:
    def __init__(self, ground, verdict, reason, cites):
        self.ground, self.verdict, self.reason, self.cites = ground, verdict, reason, cites

    def as_dict(self):
        return {"ground": self.ground, "verdict": self.verdict, "reason": self.reason, "cites": self.cites}


def _is_ped(f, pol, inception):
    """Returns (True/False/None, explanation). None = cannot decide -> human."""
    lb = pol["ped_lookback_months"]
    cite = pol["ped_lookback_cite"]
    hits = []
    for label, key in (("diagnosed", "diagnosis_date"), ("treated/advised", "last_advice_or_treatment_before_inception")):
        x = d(f.get(key))
        if x and x <= inception and months_between(x, inception) <= lb:
            hits.append(f"{label} on {x} ({months_between(x, inception)} months before policy start; limit {lb})")
    if hits:
        return True, "; ".join(hits), cite
    if f.get("symptoms_before_inception"):
        return None, ("only symptoms are recorded before the policy start - no diagnosis or treatment. "
                      "Courts have held a PED must be diagnosed, not merely symptomatic; a doctor must review"), cite
    dx = d(f.get("diagnosis_date"))
    if dx and dx <= inception:
        # Absence of a treatment record is NOT evidence of no treatment (a chronic disease is usually treated).
        return None, (f"diagnosed {dx}, more than {lb} months before policy start; the documents do not say whether "
                      f"it was treated within {lb} months before the policy - medical history needed"), cite
    if dx and dx > inception and f.get("declared_at_proposal"):
        return None, (f"CONTRADICTION: diagnosis date {dx} is after policy start, but the schedule says the disease "
                      "was declared as pre-existing - the extracted date is probably of a complication"), cite
    if dx and dx > inception:
        return False, f"first diagnosed {dx}, after the policy start", cite
    # No usable date at all (missing, relative like '3 yrs back', or dropped by the quote guard) -> do not guess.
    return None, "no verifiable diagnosis date in the documents - cannot tell if the condition pre-dates the policy", cite


def evaluate(f: dict) -> dict:
    out = {"facts_used": f, "findings": [], "flags": []}
    pol = RULES["policies"].get(f.get("policy_uin") or "")
    reg = RULES["regulation"]
    if not pol:
        out["findings"].append(Finding("any", HUMAN, f"Policy UIN '{f.get('policy_uin')}' is not in the knowledge base; "
                                       "cannot apply its wording. Add the wording before judging.", []).as_dict())
        return _finish(out)

    inception, adm = d(f.get("first_inception_date")), d(f.get("admission_date"))
    if not inception or not adm:
        out["findings"].append(Finding("any", HUMAN, "Policy start or admission date missing/unverified.", []).as_dict())
        return _finish(out)
    prior = int(f.get("prior_continuous_coverage_months") or 0)
    cov = months_between(inception, adm) + prior
    days = (adm - inception).days
    out["computed"] = {"policy": pol["name"], "months_continuous_coverage": cov,
                       "days_since_inception": days, "portability_credit_months": prior}
    accident = bool(f.get("accident"))

    if not f.get("clause_cited"):
        out["flags"].append({"issue": "Rejection letter cites no specific policy clause", "cite": reg["specific_reason_cite"]})

    for g in f.get("rejection_grounds") or []:
        if g == "initial_waiting":
            c = [pol["initial_waiting_cite"]]
            if accident:
                out["findings"].append(Finding(g, INVALID, "30-day exclusion does not apply to accidents.", c).as_dict())
            elif prior > 0:
                out["findings"].append(Finding(g, HUMAN, f"Ported policy with {prior} months prior cover; check whether initial waiting was waived.", c).as_dict())
            elif days < pol["initial_waiting_days"]:
                out["findings"].append(Finding(g, VALID, f"Admitted {days} days after policy start (< {pol['initial_waiting_days']}).", c).as_dict())
            else:
                out["findings"].append(Finding(g, INVALID, f"Admitted {days} days after policy start; 30-day period was over.", c).as_dict())

        elif g == "specified_waiting":
            c = [pol["specified_waiting_cite"]]
            if accident:
                out["findings"].append(Finding(g, INVALID, "Specified-disease waiting period does not apply to accidents.", c).as_dict())
            elif f.get("specified_disease_category") is None:
                out["findings"].append(Finding(g, HUMAN, f"Could not confirm '{f.get('condition')}' is on the Excl 02 list.", c).as_dict())
            elif not f["specified_disease_category"]:
                out["findings"].append(Finding(g, INVALID, f"'{f.get('condition')}' is not on the Excl 02 list.", c).as_dict())
            elif cov < pol["specified_waiting_months"]:
                out["findings"].append(Finding(g, VALID, f"{cov} months of cover < {pol['specified_waiting_months']} required.", c).as_dict())
            else:
                out["findings"].append(Finding(g, INVALID, f"{cov} months of cover >= {pol['specified_waiting_months']}; waiting period over.", c).as_dict())

        elif g in ("ped", "non_disclosure"):
            is_ped, why, lcite = _is_ped(f, pol, inception)
            c = [lcite, pol["ped_waiting_cite"]]
            if is_ped is None:
                out["findings"].append(Finding(g, HUMAN, why, c).as_dict())
                continue
            if not is_ped:
                out["findings"].append(Finding(g, INVALID, f"Condition does not meet the PED definition: {why}.", c).as_dict())
                continue
            declared = f.get("declared_at_proposal")
            if cov >= reg["moratorium_months"]:
                out["findings"].append(Finding(g, INVALID,
                    f"PED ({why}), but {cov} months of continuous cover >= {reg['moratorium_months']}: moratorium bars "
                    "non-disclosure grounds unless fraud is established (fraud = human decision).",
                    c + [reg["moratorium_cite"]]).as_dict())
            elif declared is None:
                out["findings"].append(Finding(g, HUMAN, f"PED ({why}); proposal form not available to check if declared.", c).as_dict())
            elif not declared:
                out["findings"].append(Finding(g, VALID, f"PED ({why}) not declared at proposal and cover is {cov} months (< 60 moratorium).", c).as_dict())
            elif cov >= pol["ped_waiting_months"]:
                out["findings"].append(Finding(g, INVALID, f"PED ({why}) was declared and {cov} months >= {pol['ped_waiting_months']} waiting period.", c).as_dict())
            else:
                out["findings"].append(Finding(g, VALID, f"PED ({why}); {cov} months < {pol['ped_waiting_months']} waiting period.", c).as_dict())
        else:
            out["findings"].append(Finding(g, HUMAN, f"Ground '{g}' is outside this tool's scope.", []).as_dict())

    if not out["findings"]:
        out["findings"].append(Finding("any", HUMAN, "No rejection ground identified.", []).as_dict())
    res = _finish(out)
    # Wrong-clause check: if the cited grounds fail, would a ground the insurer did NOT cite still exclude the claim?
    # Telling a user to fight a rejection the insurer can simply re-issue under another clause would mislead them.
    if res["verdict"] == INVALID and not f.get("_no_recheck"):
        others = [g for g in ("initial_waiting", "specified_waiting") if g not in (f.get("rejection_grounds") or [])]
        alt = evaluate({**f, "rejection_grounds": others, "_no_recheck": True, "clause_cited": "x"}) if others else None
        hits = [x for x in (alt or {}).get("findings", []) if x["verdict"] == VALID]
        if hits:
            res["findings"].append(Finding(hits[0]["ground"], HUMAN,
                "Cited reason looks wrong, BUT this exclusion (not cited by insurer) appears to apply: "
                + hits[0]["reason"], hits[0]["cites"]).as_dict())
            res = _finish(res)
    return res


def _finish(out):
    vs = [x["verdict"] for x in out["findings"]]
    # A rejection stands if ANY ground holds. Only call it invalid if EVERY ground fails.
    out["verdict"] = VALID if VALID in vs else HUMAN if HUMAN in vs else INVALID
    return out
