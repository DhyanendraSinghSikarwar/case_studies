# Toy prioritisation for a RAG chatbot with tools. The ten names are the OWASP LLM Top 10 2025 list (as seen on genai.owasp.org).
# The likelihood/impact scores (1-5) are MY ASSUMPTIONS for this one design, not OWASP data. Point: test how robust the top 4 is.
import random
RISKS = {  # name: (likelihood, impact) for: RAG over internal docs + tools that can email and call internal APIs, hosted provider model
 "LLM01 Prompt Injection": (5, 4), "LLM02 Sensitive Information Disclosure": (4, 4), "LLM03 Supply Chain": (3, 3),
 "LLM04 Data and Model Poisoning": (3, 3), "LLM05 Improper Output Handling": (3, 4), "LLM06 Excessive Agency": (4, 5),
 "LLM07 System Prompt Leakage": (4, 2), "LLM08 Vector and Embedding Weaknesses": (3, 3), "LLM09 Misinformation": (4, 3),
 "LLM10 Unbounded Consumption": (3, 3)}
def top4(scores): return [n for n, _ in sorted(scores.items(), key=lambda kv: (-kv[1][0] * kv[1][1], kv[0]))[:4]]
print("base ranking (L x I):")
for n, (l, i) in sorted(RISKS.items(), key=lambda kv: -kv[1][0] * kv[1][1]): print(f"  {l * i:2d}  {n}")
random.seed(2)
counts = {n: 0 for n in RISKS}; N = 5000
for _ in range(N):   # each score wiggles by -1/0/+1 (clamped to 1..5): how stable is "my" top four?
    pert = {n: (min(5, max(1, l + random.choice((-1, 0, 1)))), min(5, max(1, i + random.choice((-1, 0, 1))))) for n, (l, i) in RISKS.items()}
    for n in top4(pert): counts[n] += 1
print(f"share of {N} perturbed scorings in which each risk lands in the top 4:")
for n, c in sorted(counts.items(), key=lambda kv: -kv[1]): print(f"  {c / N:5.1%}  {n}")
