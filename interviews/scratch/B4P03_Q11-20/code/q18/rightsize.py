"""Turn observed memory samples into a request recommendation: daily peak -> percentile -> headroom -> round up.
A simplified model of what a recommender does, not the VPA algorithm itself."""
import math, statistics

MIB = 1
def percentile(xs, p):
    xs = sorted(xs); k = math.ceil(p / 100 * len(xs)) - 1
    return xs[max(k, 0)]

# 7 days of memory samples (MiB) for one scorer pod; day 5 had a big batch request
days = {
  "d1": [900, 950, 1010, 980, 1040], "d2": [910, 960, 1000, 1020, 990],
  "d3": [930, 970, 1050, 1000, 1030], "d4": [900, 940, 1020, 1060, 1010],
  "d5": [920, 980, 1500, 1620, 1100], "d6": [915, 955, 1005, 1035, 995],
  "d7": [925, 965, 1015, 1045, 1000],
}
all_samples = [s for v in days.values() for s in v]
peaks = [max(v) for v in days.values()]
avg = statistics.mean(all_samples)
p90_peak = percentile(peaks, 90)
rec = math.ceil(p90_peak * 1.15 / 64) * 64      # 15% headroom, rounded up to 64 MiB steps
print(f"mean of all samples : {avg:7.1f} MiB   <- the tempting, wrong number")
print(f"daily peaks         : {peaks}")
print(f"p90 of daily peaks  : {p90_peak} MiB   (only 7 peaks, so p90 is the max; with more days a rare spike drops out)")
print(f"recommended request : {rec} MiB (p90 peak + 15% headroom, rounded up to 64)")
print(f"max ever seen       : {max(all_samples)} MiB -> a request/limit at the mean would OOM on day 5: {math.floor(avg) < max(all_samples)}")
print(f"limit = request is the safe habit for memory: limit {rec} MiB")

# The VPA CRD is not in the bundled Kubernetes schemas, so check the few fields that matter by hand.
import yaml
vpa = yaml.safe_load(open("vpa.yaml"))
mode = vpa["spec"]["updatePolicy"]["updateMode"]
print(f"vpa.yaml parses; updateMode={mode!r}; valid mode: {mode in ('Off', 'Initial', 'Recreate', 'Auto')}; recommend-only: {mode == 'Off'}")
