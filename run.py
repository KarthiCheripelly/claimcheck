"""ClaimCheck CLI.

  python run.py --case C02              # one case, gold facts (no AI, no key needed)
  python run.py --case C02 --mode llm   # one case, AI reads the documents
  python run.py --eval                  # all cases, gold facts  -> tests the rules engine
  python run.py --eval --mode llm       # all cases, AI extraction -> tests the whole pipeline
"""
import argparse, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from claimcheck.engine import evaluate, INVALID, HUMAN  # noqa: E402
from claimcheck import extractor  # noqa: E402

CASES = json.loads((Path(__file__).parent / "cases" / "cases.json").read_text(encoding="utf-8"))
OUT = Path(__file__).parent / "outputs"


def get_facts(case, mode):
    if mode == "gold":
        return case["gold_facts"], None
    ex = extractor.extract(case["documents"])
    return ex["facts"], ex


def draft_grievance(case, res):
    """Template, not LLM: the letter only repeats verified findings + citations."""
    bad = [f for f in res["findings"] if f["verdict"] == INVALID]
    if res["verdict"] != INVALID:
        return None
    lines = ["To: Grievance Redressal Officer", "",
             "Subject: Request for review of repudiated claim", "",
             "I request a review of the rejection of my claim for the following reasons:"]
    for i, f in enumerate(bad, 1):
        lines.append(f"{i}. Ground '{f['ground']}': {f['reason']} [Ref: {'; '.join(f['cites'])}]")
    for fl in res["flags"]:
        lines.append(f"- Also: {fl['issue']} [Ref: {fl['cite']}]")
    lines += ["", "If not resolved within the timeline, I may approach the Insurance Ombudsman.",
              "", "[DRAFT - to be reviewed, edited and sent by the policyholder. Not legal advice.]"]
    return "\n".join(lines)


def show(case, res, ex):
    print(f"\n=== {case['id']}: {case['tests']}")
    if ex:
        print(f"  AI model: {ex['model']} | facts dropped (quote not found): {ex['dropped_unverified'] or 'none'}")
    if "computed" in res:
        c = res["computed"]
        print(f"  Policy: {c['policy']} | continuous cover: {c['months_continuous_coverage']} months")
    for f in res["findings"]:
        print(f"  [{f['verdict']}] {f['ground']}: {f['reason']}")
        for ci in f["cites"]:
            print(f"        cite: {ci}")
    for fl in res["flags"]:
        print(f"  [FLAG] {fl['issue']} ({fl['cite']})")
    print(f"  VERDICT: {res['verdict']}   (expected {case['expected']})")
    g = draft_grievance(case, res)
    if g:
        print("  --- draft grievance ---\n    " + g.replace("\n", "\n    "))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case")
    ap.add_argument("--eval", action="store_true")
    ap.add_argument("--mode", choices=["gold", "llm"], default="gold")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    cases = [c for c in CASES if not a.case or c["id"] == a.case]
    if not cases:
        sys.exit(f"No case {a.case}")
    OUT.mkdir(exist_ok=True)
    rows = []
    for c in cases:
        try:
            facts, ex = get_facts(c, a.mode)
            res = evaluate(facts)
        except Exception as e:  # an AI failure must never become a verdict
            ex, res = None, {"verdict": "ERROR", "findings": [], "flags": [], "error": str(e)}
        (OUT / f"{c['id']}_{a.mode}.json").write_text(json.dumps({"case": c["id"], "extraction": ex, "result": res}, indent=1), encoding="utf-8")
        if not a.quiet or not a.eval:
            show(c, res, ex) if res["verdict"] != "ERROR" else print(f"\n=== {c['id']} ERROR: {res['error']}")
        rows.append((c["id"], c["expected"], res["verdict"]))
        if a.mode == "llm":
            time.sleep(4)  # free-tier rate limits
    if a.eval:
        ok = sum(e == g for _, e, g in rows)
        print(f"\n{'case':5} {'expected':15} {'got':15}")
        for i, e, g in rows:
            print(f"{i:5} {e:15} {g:15} {'OK' if e == g else '<-- MISMATCH'}")
        dangerous = [i for i, e, g in rows if e != INVALID and g == INVALID]
        print(f"\nAccuracy: {ok}/{len(rows)} | dangerous errors (told user to fight a valid rejection): {dangerous or 'none'}")


if __name__ == "__main__":
    main()
