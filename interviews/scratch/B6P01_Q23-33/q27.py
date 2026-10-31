# Q27 sanity check: how big would the segment loss have to be? (illustrative numbers)
total_dau = 10_000_000
ios_dau = 4_000_000
latest_os_dau = 1_200_000        # iOS users on the newest OS, before the drop

# reading A: total DAU is down 5% and all of it sits in the latest-OS segment
lost_A = 0.05 * total_dau
seg_drop_A = lost_A / latest_os_dau
# reading B: iOS DAU down 5%, all of it in the segment
lost_B = 0.05 * ios_dau
seg_drop_B = lost_B / latest_os_dau
# reading C: the segment itself is down 5%
lost_C = 0.05 * latest_os_dau
print("A lost users:", lost_A, " implied segment drop:", round(seg_drop_A, 3))
print("B lost users:", lost_B, " implied segment drop:", round(seg_drop_B, 3))
print("C lost users:", lost_C, " share of total DAU:", lost_C / total_dau)
assert lost_A == 500_000 and round(seg_drop_A, 3) == 0.417
assert lost_B == 200_000 and round(seg_drop_B, 3) == 0.167
assert lost_C == 60_000 and lost_C / total_dau == 0.006

# cross-check with a second source: backend active users (any authenticated API call) in the same segment
client_event_dau_before, client_event_dau_after = 1_200_000, 1_140_000   # app-open event
backend_dau_before, backend_dau_after = 1_260_000, 1_257_000             # server logs
ratio_before = client_event_dau_before / backend_dau_before
ratio_after = client_event_dau_after / backend_dau_after
print("client/backend ratio before:", round(ratio_before, 3), " after:", round(ratio_after, 3))
print("client DAU change:", round(client_event_dau_after / client_event_dau_before - 1, 3),
      " backend DAU change:", round(backend_dau_after / backend_dau_before - 1, 4))
assert round(ratio_before, 3) == 0.952 and round(ratio_after, 3) == 0.907
assert round(client_event_dau_after / client_event_dau_before - 1, 3) == -0.05
assert round(backend_dau_after / backend_dau_before - 1, 4) == -0.0024
# a falling client/backend ratio with flat backend points to lost events, not lost users
