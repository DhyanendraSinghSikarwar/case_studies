# Q22 toy meeting summariser: hierarchical chunking + quote-verified action items. MOCK summariser; synthetic transcript.
import re
T = [("Asha","We need to decide the launch date for the pilot."),
     ("Ravi","I think 15 March works if QA signs off."),
     ("Asha","Okay, decision: pilot launches 15 March."),
     ("Ravi","I will send the QA checklist by Friday."),
     ("Meera","Can you share the budget sheet, Asha?"),
     ("Asha","Haan, kal tak bhej dungi."),            # Hinglish commitment: 'I will send it by tomorrow'
     ("Meera","Let us talk about the offsite later."),
     ("Ravi","Weather is great today.")]
def tokens(s): return len(s.split())
def chunk(turns, budget):               # greedy chunks of whole turns, never split a turn
    out, cur, n = [], [], 0
    for sp, tx in turns:
        if cur and n + tokens(tx) > budget: out.append(cur); cur, n = [], 0
        cur.append((sp, tx)); n += tokens(tx)
    return out + ([cur] if cur else [])
def mock_summarise(turns):              # mock LLM: keeps turns with decision words; also invents an owner sometimes
    keep = [f"{sp}: {tx}" for sp, tx in turns if re.search(r"decid|will|launch|share", tx, re.I)]
    return keep
def hierarchical(turns, budget=24):
    parts = [mock_summarise(c) for c in chunk(turns, budget)]
    flat = [(l.split(": ", 1)[0], l.split(": ", 1)[1]) for p in parts for l in p]
    return parts, mock_summarise(flat) if len(parts) > 1 else flat
def extract_actions(turns, invent=False):   # mock extractor over turns
    acts = []
    for i, (sp, tx) in enumerate(turns):
        if re.search(r"\bI will\b", tx): acts.append(dict(owner=sp, task=tx, quote=tx))
        m = re.search(r"Can you (.+), (\w+)\?", tx)
        if m: acts.append(dict(owner=m.group(2), task=m.group(1), quote=tx))
    if invent: acts.append(dict(owner="Ravi", task="book the venue", quote="Ravi will book the venue"))  # hallucinated item
    return acts
def verified(acts, turns):                  # attribution check: quote must be a real utterance
    utt = {tx for _, tx in turns}
    return [a for a in acts if a["quote"] in utt], [a for a in acts if a["quote"] not in utt]
parts, final = hierarchical(T)
print("chunks:", len(parts), "| final lines:", len(final))
acts = extract_actions(T, invent=True)
ok, bad = verified(acts, T)
print("extracted", len(acts), "verified", len(ok), "rejected", [a["task"] for a in bad])
assert len(bad) == 1 and bad[0]["task"] == "book the venue"
# facts checklist coverage (reference-free: facts the meeting must contain, written before looking at summaries)
facts = {"date": "15 March", "qa": "QA checklist", "budget": "budget sheet"}
text = " ".join(final) + " " + " ".join(a["task"] for a in ok)
for k, v in facts.items(): print(f"fact {k:7s} covered: {v in text}")
# Hinglish: the commitment is the reply "Haan, kal tak bhej dungi." The English regex never fires on it.
quotes = {a["quote"] for a in ok}
print("Hinglish confirmation (Asha, 'kal tak bhej dungi') captured as evidence:", "Haan, kal tak bhej dungi." in quotes)
print("owner of budget task comes only from Meera's request, unconfirmed:", [a["owner"] for a in ok if "budget" in a["task"]])
