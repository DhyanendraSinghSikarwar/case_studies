# Illustrative numbers only. Exposure window, record counts (unique, not downloads x records), and the first-hour order.
import random
push_to_flag_min = 3 * 60
flag_to_revoke_min = 20                      # target: key disabled within 20 minutes of the flag
window = push_to_flag_min + flag_to_revoke_min
print('exposure window (push to revoke), minutes:', window)
assert window == 200
downloads, records = 14, 2_100_000
rate = downloads / (push_to_flag_min / 60)   # if all 14 happened before the flag (the log will say)
print('downloads per hour if all before the flag:', round(rate, 2), '; per extra 10 minutes of delay:', round(rate / 6, 2))
assert round(rate, 2) == 4.67
# WRONG way to count: downloads x records. RIGHT way: union of objects actually read.
naive = downloads * records
assert naive == 29_400_000 and naive > records            # impossible: only 2,100,000 records exist
# Illustrative bucket: 21 objects x 100,000 records. 14 download events listing which objects were read.
rnd = random.Random(35)
objects = {f'part-{i:02d}': 100_000 for i in range(21)}
assert sum(objects.values()) == records
events = [rnd.sample(sorted(objects), rnd.choice([1, 2, 3, 4])) for _ in range(downloads)]
touched = set(k for ev in events for k in ev)
unique_records = sum(objects[k] for k in touched)
print('objects touched:', len(touched), 'of', len(objects), '-> unique records exposed (upper bound for this log):', unique_records)
assert unique_records <= records and unique_records >= max(len(ev) for ev in events) * 100_000
# If any one event listed the whole bucket (21 objects), the bound is the whole bucket.
full_copy_events = sum(1 for ev in events if len(ev) == 21)
assert (full_copy_events > 0) == (unique_records == records)
print('events that read the whole bucket:', full_copy_events, '-> exposed records:', unique_records)
# Bytes check: total bytes downloaded divided by bucket size says how many full copies left.
bucket_gb, downloaded_gb = 2.1, 3.15
print('full-copy equivalents downloaded:', downloaded_gb / bucket_gb)
assert downloaded_gb / bucket_gb == 1.5
# First hour, ordered, with minute marks (illustrative). Each step has a deadline and an owner.
plan = [
    (0,  'declare incident (SEV1), page security on-call + privacy/legal contact; start a timeline doc'),
    (5,  'DISABLE the key (do not delete); preserve logs and the repo copy before any history rewrite'),
    (15, 'confirm the key no longer works; list what else the key could reach (IAM policy), check for new users/keys/roles'),
    (25, 'export access logs for the window: who, from where, which objects, how many bytes'),
    (40, 'lock the bucket path (deny by default except named roles); rotate related secrets in the same notebook/repo'),
    (50, 'take the notebook down or make the repo private; ask host to purge cached copies; scan history for other secrets'),
    (60, 'first written update to security, legal and the business: known, unknown, next update time'),
]
mins = [m for m, _ in plan]
assert mins == sorted(mins) and mins[-1] == 60 and mins[1] <= 5
for m, a in plan: print(f'{m:>3} min  {a}')
# Escalation rules (illustrative)
rules = {'unknown_ip_reads_personal_data': 'SEV1 now', 'any_write_or_delete_in_logs': 'SEV1 plus integrity review', 'cannot_disable_key_in_15_min': 'escalate to cloud account owner'}
assert rules['unknown_ip_reads_personal_data'] == 'SEV1 now'
