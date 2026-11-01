# RAGAS-style metrics from scratch with MOCK components (word-overlap 'entailment', bag-of-words
# 'embedding'). Real Ragas uses an LLM for claim extraction and verdicts and a real embedding model.
import math, re
from collections import Counter

def words(s): return re.findall(r"[a-z0-9$]+", s.lower())
def supported(claim, context):                 # mock verdict: all content words appear in context
    stop = {"the", "is", "a", "of", "in", "to", "and"}
    cw = [w for w in words(claim) if w not in stop]
    return all(w in set(words(context)) for w in cw)

def faithfulness(claims, context):             # supported claims / total claims
    return sum(supported(c, context) for c in claims) / len(claims)

def cos(a, b):
    a, b = Counter(words(a)), Counter(words(b))
    dot = sum(a[w] * b[w] for w in a)
    return dot / (math.sqrt(sum(v*v for v in a.values())) * math.sqrt(sum(v*v for v in b.values())) or 1)

def answer_relevance(question, generated_questions):   # mean cosine(question, questions generated from the answer)
    return sum(cos(question, g) for g in generated_questions) / len(generated_questions)

ctx = "Einstein was born in Germany. The refund window is 30 days."
print("faithfulness, Einstein-style (1 of 2 claims supported):",
      faithfulness(["Einstein was born in Germany", "Einstein was born on 20 March 1879"], ctx))

# Faithful but wrong: the retriever returned an OLD policy; the answer is faithful to it.
stale = "The refund window is 14 days."
print("faithful to a stale doc:", faithfulness(["The refund window is 14 days"], stale), "(current policy: 30 days)")

# Faithful but incomplete: answers only restate one safe fact; relevance sees on-topic questions.
q = "What is the refund window and how do I request a refund?"
print("answer relevance, on-topic but partial answer:",
      round(answer_relevance(q, ["What is the refund window?", "How long is the refund window?"]), 2))
print("answer relevance, off-topic answer:",
      round(answer_relevance(q, ["Where was Einstein born?"]), 2))

# Mean 0.9 can still hide complaints: 10 SYNTHETIC answers (all numbers assumed)
faith    = [1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0.5]   # per-answer faithfulness (supported claims / claims)
resolved = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0]       # human: was the user's problem solved?
print("mean faithfulness:", round(sum(faith) / 10, 2), "| resolved rate:", sum(resolved) / 10)
print("answers with faithfulness 1.0 that were NOT resolved:",
      sum(1 for f, r in zip(faith, resolved) if f == 1 and r == 0), "of", sum(1 for f in faith if f == 1))
