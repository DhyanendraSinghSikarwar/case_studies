import numpy as np

# Pilot counts (measured, from the question)
alerts, overridden, acted = 1000, 700, 300
ev_over, ev_acted = 35, 90
assert overridden + acted == alerts
ev_all = ev_over + ev_acted
share_alerts_with_event = ev_all / alerts
share_events_in_acted = ev_acted / ev_all
rate_over, rate_acted = ev_over / overridden, ev_acted / acted
assert ev_all == 125 and share_alerts_with_event == 0.125
assert round(share_events_in_acted, 3) == 0.72
assert rate_over == 0.05 and rate_acted == 0.30
print("alerts followed by an event:", share_alerts_with_event)
print("events (among alerted) that were in acted-on alerts:", round(share_events_in_acted, 3))
print("event rate overridden / acted:", rate_over, rate_acted)

# Two-proportion z (large-sample): is 30% vs 5% a real gap? Yes, but it is not the question.
p = ev_all / alerts
se = np.sqrt(p * (1 - p) * (1 / overridden + 1 / acted))
z = (rate_acted - rate_over) / se
assert z > 10
print("z for acted vs overridden event rate:", round(float(z), 1))

# Why the gap does not say who is right: a simulation with an illustrative skilled clinician.
# Latent risk r; clinician sees r plus noise and acts if the signal is high; acting cuts events by 40%.
rng = np.random.default_rng(11)
n = 1000
r = rng.beta(2, 8, n)                      # latent true risk, mean 0.2
sees = r + rng.normal(0, 0.08, n)
act = sees > np.quantile(sees, 0.70)       # clinicians act on the top 30% by their own read
prevented = rng.random(n) < 0.40
event = (rng.random(n) < r) & ~(act & prevented)
print("sim: acted share", act.mean(), "event rate acted", round(float(event[act].mean()), 3),
      "overridden", round(float(event[~act].mean()), 3))
no_action_acted = (rng.random(n) < r)[act].mean()
print("sim: acted-group event rate had nobody acted (untreated risk):", round(float(no_action_acted), 3))
assert event[act].mean() > event[~act].mean()      # acted group looks worse even though clinicians are skilled
assert no_action_acted > event[act].mean()   # acting lowered events in the acted group
