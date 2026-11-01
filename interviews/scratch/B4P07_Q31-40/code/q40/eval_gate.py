"""CI gate for an LLM app. The model call is a STUB: no provider API is called here."""
import json, random, statistics, sys

BANNED = ["ignore previous instructions", "as an ai language model"]

def stub_model(prompt, seed):
    """Deterministic stand-in for the real call. Pretends to be a bit noisy on g3 only."""
    rnd = random.Random(f"{prompt}-{seed}")
    answer = {"Refund for order 118?": "You can request a refund within the window.",
              "Reset my password": "Use the reset link on the login page.",
              "Delivery time to Pune?": "Usually 3 to 5 days." if rnd.random() > 0.2 else "Soon.",
              "Cancel subscription": "You can cancel from Settings."}[prompt]
    return json.dumps({"answer": answer, "source": "faq"})

def stub_judge(prompt, output, seed):
    """Stand-in for LLM-as-judge: score 1-5 with noise. A real judge costs money and varies run to run."""
    base = 4.5 if "days" in output or "refund" in output.lower() or "reset" in output or "cancel" in output else 2.0
    return base + random.Random(f"j-{prompt}-{seed}").uniform(-0.4, 0.4)

def deterministic_checks(case, raw):
    fails = []
    try:
        obj = json.loads(raw)
    except ValueError:
        return ["not valid JSON"]
    for k in case["expect_json_keys"]:
        if k not in obj:
            fails.append(f"missing key {k}")
    text = str(obj.get("answer", "")).lower()
    fails += [f"missing '{w}'" for w in case["must_contain"] if w not in text]
    fails += [f"banned phrase '{b}'" for b in BANNED if b in text]
    return fails

def run_gate(cases, model=stub_model, judge=stub_judge, repeats=5,
             min_det_pass=0.9, min_judge_mean=4.0, tolerance=0.3, baseline_judge=4.4):
    problems, notes = [], []
    det_pass = 0
    judge_runs = []
    for r in range(repeats):                       # repeat: single judge scores are noisy
        scores = []
        for c in cases:
            out = model(c["input"], r)
            f = deterministic_checks(c, out)       # cheap, so run on every repeat
            det_pass += not f
            if f:
                notes.append(f"{c['id']} repeat {r}: " + "; ".join(f))
            scores.append(judge(c["input"], out, r))
        judge_runs.append(statistics.mean(scores))
    det_rate = det_pass / (len(cases) * repeats)
    jm = statistics.mean(judge_runs)
    if det_rate < min_det_pass:
        problems.append(f"deterministic pass rate {det_rate:.2f} < {min_det_pass}")
    if jm < min_judge_mean:
        problems.append(f"judge mean {jm:.2f} < floor {min_judge_mean}")
    if jm < baseline_judge - tolerance:
        problems.append(f"judge mean {jm:.2f} dropped more than tolerance {tolerance} from baseline {baseline_judge}")
    return {"det_rate": det_rate, "judge_mean": round(jm, 3), "judge_spread": round(max(judge_runs) - min(judge_runs), 3), "notes": notes}, problems

if __name__ == "__main__":
    cases = [json.loads(l) for l in open(sys.argv[1])]
    summary, problems = run_gate(cases)
    print({k: v for k, v in summary.items() if k != "notes"})
    for n in summary["notes"]:
        print("note:", n)
    for p in problems:
        print("FAIL:", p)
    print("GATE:", "FAIL" if problems else "PASS")
    sys.exit(1 if problems else 0)
