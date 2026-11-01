# Q16: dashboard first, model only when a decision needs it (illustrative)
dash_w, model_w = 2, 10
print("model/dashboard effort ratio", model_w / dash_w, "extra weeks", model_w - dash_w)
assert model_w / dash_w == 5
# when would a model pay? invented: 100,000 customers, 3% churn a month, offer costs 2 per contact,
# 20% of churners contacted are saved, a saved customer is worth 200
cust, churn, offer_cost, save_rate, value = 100_000, 0.03, 2, 0.20, 200
churners = cust * churn
# no model: contact everyone
blanket_cost = cust * offer_cost
blanket_gain = churners * save_rate * value
print("blanket: cost", blanket_cost, "gain", blanket_gain, "net", blanket_gain - blanket_cost)
assert (blanket_cost, blanket_gain) == (200_000, 120_000)
# a model whose top 10% holds 40% of churners (lift 4)
top, capture = 0.10, 0.40
m_cost = cust * top * offer_cost
m_gain = churners * capture * save_rate * value
print("model top 10%: cost", m_cost, "gain", m_gain, "net", m_gain - m_cost)
assert (m_cost, m_gain) == (20_000, 48_000)
# the dashboard alone changes nothing unless someone acts on the segment; model net per month 28,000
net = m_gain - m_cost
print("model net per month", net)
assert net == 28_000
# if offer only works at 5% save rate, the model does not pay
m_gain_low = churners * capture * 0.05 * value
print("at 5% save rate: gain", m_gain_low, "net", m_gain_low - m_cost)
assert m_gain_low - m_cost < 0
