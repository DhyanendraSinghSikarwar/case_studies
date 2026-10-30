p_fraud, loss = 0.12, 80
gap, value = 0.92 - 0.84, 150
friction = gap * value
cost_decline = (1 - p_fraud) * friction
cost_allow = p_fraud * loss
print(f"friction per genuine decline {friction:.2f}; decline {cost_decline:.2f}; allow {cost_allow:.2f}; difference {cost_decline-cost_allow:+.2f}")
assert abs(friction - 12.0) < 1e-9 and abs(cost_decline - 10.56) < 1e-9 and abs(cost_allow - 9.60) < 1e-9
p_be = friction / (loss + friction)
print(f"break-even fraud share {p_be:.4f}")
assert abs(p_be - 12 / 92) < 1e-12 and p_fraud < p_be
gap_be = p_fraud * loss / ((1 - p_fraud) * value)
print(f"break-even retention gap {gap_be*100:.2f} points (observed 8)")
assert abs(gap_be - 9.6 / 132) < 1e-12 and gap_be < gap
# over 100,000 flagged transactions
print(f"per 100,000 flagged: decline {100_000*cost_decline:,.0f}; allow {100_000*cost_allow:,.0f}")
# add an assumed extra cost of allowing (chargeback fee 15 on the fraud) and see the flip
fee = 15
print(f"with a {fee} chargeback fee on allowed fraud: allow {p_fraud*(loss+fee):.2f}")
assert p_fraud * (loss + fee) > cost_decline
