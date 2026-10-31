W, E = 20.0, 4.0
def cost(ans, acc, w=W, e=E):
    wrong = ans*(1-acc)
    return wrong*w + (1-ans)*e, wrong
c7, w7 = cost(0.80, 0.92)
c9, w9 = cost(0.55, 0.97)
print(f"threshold 0.7: wrong {w7:.4f}, expected cost {c7:.4f}")
print(f"threshold 0.9: wrong {w9:.4f}, expected cost {c9:.4f}")
assert abs(w7-0.064) < 1e-12 and abs(c7-2.08) < 1e-12
assert abs(w9-0.0165) < 1e-12 and abs(c9-2.13) < 1e-12
# break-even wrong-answer cost: 0.064 w + 0.8 = 0.0165 w + 1.8
be = (1.8-0.8)/(0.064-0.0165)
print(f"break-even wrong-answer cost = {be:.2f}")
assert abs(be - 21.0526) < 1e-3
for w in (10, 15, 20, 21.05, 22, 30, 40):
    a, _ = cost(0.80, 0.92, w); b, _ = cost(0.55, 0.97, w)
    print(f"wrong-answer cost {w:>5}: t=0.7 {a:.3f}, t=0.9 {b:.3f}, cheaper: {'0.7' if a<b else '0.9'}")
assert cost(0.80,0.92,20)[0] < cost(0.55,0.97,20)[0] and cost(0.80,0.92,22)[0] > cost(0.55,0.97,22)[0]
# marginal band: questions answered at 0.7 but not at 0.9
band = 0.80-0.55
wrong_band = w7-w9
print(f"band share {band:.2f}, wrong in band {wrong_band:.4f} = {wrong_band/band:.1%} of band answers")
assert abs(wrong_band/band - 0.19) < 1e-12
print(f"answering is worth it when wrong rate < escalation/wrong cost = {E/W:.0%} (at cost 20); 4/0.19 = {4/0.19:.2f}")
assert abs(4/0.19 - be) < 1e-9
# sensitivity to accuracy at threshold 0.7: 91% instead of 92%
c7b, _ = cost(0.80, 0.91)
print(f"if accuracy at 0.7 is really 91%: cost {c7b:.3f} vs 0.9 option {c9:.3f}")
assert c7b > c9
# answer-all and escalate-all references
print(f"answer all at 92% accuracy: {cost(1.0,0.92)[0]:.2f}; escalate all: {E:.2f}")
assert abs(cost(1.0,0.92)[0]-1.6) < 1e-12
