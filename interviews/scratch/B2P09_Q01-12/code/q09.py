# Hallucination checks on a MOCK knowledge setting (synthetic). Lexical 'entailment' stands in for an NLI model/LLM.
import random, re
random.seed(2)
SOURCE = "Acme was founded in 1998 in Pune. Its CEO is Rao. It has 400 employees."
def words(s): return set(re.findall(r"[a-z0-9]+", s.lower()))
def entailed(claim, src=SOURCE): return words(claim) <= words(src) | {"is", "was", "the", "a", "it"}

answer_claims = ["Acme was founded in 1998", "Acme was founded in Pune", "Acme has 900 employees", "Its CEO is Rao"]
flags = [entailed(c) for c in answer_claims]
print("claim decomposition + entailment:", list(zip(answer_claims, flags)))
print("grounded-claim rate:", sum(flags) / len(flags))

# citation verification: each claim cites a sentence index; check the cited sentence supports it
sentences = [s.strip() for s in SOURCE.split(".") if s.strip()]
cites = [(answer_claims[0], 0), (answer_claims[3], 1), (answer_claims[2], 2)]
for c, i in cites:
    print(f"citation [{i}] supports '{c}':", entailed(c, sentences[i]))

# sampling consistency (SelfCheck-style): sample 5 answers to 'how many employees?' from a mock model
def mock_sampler(kind):
    if kind == "unsure":   return random.choice(["400", "900", "150", "1200", "60"])
    if kind == "confident_wrong": return "900"     # consistently wrong
for kind in ("unsure", "confident_wrong"):
    s = [mock_sampler(kind) for _ in range(5)]
    top = max(set(s), key=s.count)
    print(f"{kind:16s} samples={s} agreement={s.count(top)/5:.1f} answer={top} (truth 400)")

# abstention rate on unanswerable questions (synthetic 10 cases, 4 unanswerable)
unanswerable = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
abstained    = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
ab_rate = sum(a for a, u in zip(abstained, unanswerable) if u) / sum(unanswerable)
print("abstention on unanswerable:", ab_rate, "| false abstention on answerable:",
      sum(a for a, u in zip(abstained, unanswerable) if not u) / unanswerable.count(0))
