# Judge prompt builder + strict output parser, exercised with a MOCK judge that returns canned text.
import json, re

RUBRIC = """You are grading ONE criterion: FAITHFULNESS.
PASS only if every factual claim in the ANSWER is supported by the CONTEXT.
FAIL if any claim is unsupported or contradicted. Ignore style, length and helpfulness.
Examples:
CONTEXT: The fee is $5. ANSWER: The fee is $5. -> {"reasoning": "fee matches", "verdict": "PASS"}
CONTEXT: The fee is $5. ANSWER: The fee is $7. -> {"reasoning": "fee differs", "verdict": "FAIL"}
Think first, then decide. Reply with JSON only, keys in this order: reasoning, verdict (PASS or FAIL)."""

def build_prompt(context, answer):
    return f"{RUBRIC}\n\nCONTEXT: {context}\nANSWER: {answer}\n"

def parse(text):
    """Strict: valid JSON, keys in order reasoning->verdict, verdict in {PASS, FAIL}. Else None."""
    try:
        obj = json.loads(text)
    except ValueError:
        m = re.search(r"\{.*\}", text, re.S)           # tolerate prose around the JSON, nothing more
        if not m: return None
        try: obj = json.loads(m.group(0))
        except ValueError: return None
    if list(obj.keys()) != ["reasoning", "verdict"]: return None
    return obj["verdict"] if obj["verdict"] in ("PASS", "FAIL") else None

outputs = {                               # canned judge replies (what a model might return)
    "clean":              '{"reasoning": "fee matches", "verdict": "PASS"}',
    "prose around json":  'Sure! {"reasoning": "fee differs", "verdict": "FAIL"} Hope that helps.',
    "verdict first":      '{"verdict": "PASS", "reasoning": "looks fine"}',
    "scale drift":        '{"reasoning": "mostly ok", "verdict": "4/5"}',
    "broken json":        '{"reasoning": "fee differs", "verdict": FAIL',
}
for k, v in outputs.items():
    print(f"{k:18s} -> {parse(v)}")
print("prompt length (chars):", len(build_prompt("The fee is $5.", "The fee is $5.")))

# One criterion per judge: three binary judges beat one 1-5 'overall' for debugging
verdicts = {"faithfulness": "PASS", "relevance": "PASS", "tone": "FAIL"}
print("per-criterion report:", verdicts, "-> failing:", [k for k, v in verdicts.items() if v == "FAIL"])
