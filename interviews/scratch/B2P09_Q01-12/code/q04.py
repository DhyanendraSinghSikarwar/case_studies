# MOCK judges on SYNTHETIC answer qualities. Noise levels are ASSUMED, so the comparison
# shows the mechanics, not a measured property of any real judge.
import random
random.seed(3)
N = 20000
def pointwise(q):                      # 1-5 score = round(quality + noise), clipped
    return max(1, min(5, round(q + random.gauss(0, 0.9))))
def pairwise(qa, qb):                  # picks the answer whose noisy impression is higher
    return "A" if qa + random.gauss(0, 0.9) > qb + random.gauss(0, 0.9) else "B"

# true qualities on a 1-5 scale; B is better than A by `gap`
for gap in (0.3, 1.0):
    ok_pw = tie_pw = ok_pair = 0
    for _ in range(N):
        qa = random.uniform(1.5, 3.5); qb = qa + gap
        sa, sb = pointwise(qa), pointwise(qb)
        if sa == sb: tie_pw += 1
        elif sb > sa: ok_pw += 1
        ok_pair += pairwise(qa, qb) == "B"
    print(f"gap {gap}: pointwise picks better {ok_pw/N:.2f}, ties {tie_pw/N:.2f} | pairwise picks better {ok_pair/N:.2f}")

# Reference-based: the judge checks the answer against a reference. If the reference is wrong,
# a correct answer is marked wrong. (Deterministic toy: judge = does the answer match the reference?)
facts = {"capital of Australia": "Canberra"}
def ref_judge(answer, reference): return answer == reference
print("good reference, correct answer judged right:", ref_judge("Canberra", facts["capital of Australia"]))
bad_ref = "Sydney"
print("bad reference,  correct answer judged right:", ref_judge("Canberra", bad_ref))
