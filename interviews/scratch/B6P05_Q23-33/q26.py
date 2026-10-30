# Q26: LLM feature unit economics (illustrative prices)
tin, tout = 3000, 500
p_in, p_out = 2.00 / 1e6, 10.00 / 1e6
retr = 0.001
cpq = tin * p_in + tout * p_out + retr
print(f"cost per query: input {tin*p_in:.4f} + output {tout*p_out:.4f} + retrieval {retr:.4f} = {cpq:.4f}")
assert abs(cpq - 0.012) < 1e-12

price, fee = 3.00, 0.03
net_rev = price * (1 - fee)
light_q, heavy_q, f_heavy = 100, 1000, 0.05
m_light = net_rev - light_q * cpq
m_heavy = net_rev - heavy_q * cpq
blend = (1 - f_heavy) * m_light + f_heavy * m_heavy
print(f"net revenue per subscriber {net_rev:.2f}; light margin {m_light:.2f}; heavy margin {m_heavy:.2f}; blended {blend:.4f}")
assert abs(net_rev - 2.91) < 1e-9 and abs(m_light - 1.71) < 1e-9 and abs(m_heavy + 9.09) < 1e-9 and abs(blend - 1.17) < 1e-9

be_q = net_rev / cpq
print(f"break-even queries per subscriber per month: {be_q:.1f}")
assert abs(be_q - 242.5) < 1e-9

# share of cost from the 5% heavy users
cost_light = (1 - f_heavy) * light_q * cpq
cost_heavy = f_heavy * heavy_q * cpq
print(f"cost per average subscriber: light {cost_light:.3f}, heavy {cost_heavy:.3f}; heavy share {cost_heavy/(cost_light+cost_heavy)*100:.1f}% of cost from 5% of users")
assert abs(cost_heavy / (cost_light + cost_heavy) - 0.3448) < 1e-3

# control 1: cap at 200 queries a month (heavy users above 200 are throttled or pay overage)
cap = 200
m_heavy_cap = net_rev - cap * cpq
blend_cap = (1 - f_heavy) * m_light + f_heavy * m_heavy_cap
print(f"cap 200: heavy margin {m_heavy_cap:.2f}; blended {blend_cap:.4f}")
assert abs(m_heavy_cap - 0.51) < 1e-9 and abs(blend_cap - 1.65) < 1e-9
# control 2: cheaper path (here: shorter context, 3,000 -> 1,500 input tokens)
cpq2 = 1500 * p_in + tout * p_out + retr
blend2 = net_rev - ((1 - f_heavy) * light_q + f_heavy * heavy_q) * cpq2
print(f"shorter context: cost per query {cpq2:.4f}; blended margin without a cap {blend2:.4f}")
assert abs(cpq2 - 0.009) < 1e-12 and abs(blend2 - 1.605) < 1e-9
# follow-up: all token prices halve (retrieval cost unchanged)
cpq3 = tin * p_in / 2 + tout * p_out / 2 + retr
print(f"token prices halved: cost per query {cpq3:.4f}; heavy user cost {heavy_q*cpq3:.2f} vs net revenue {net_rev:.2f}")
assert abs(cpq3 - 0.0065) < 1e-12 and heavy_q * cpq3 > net_rev
