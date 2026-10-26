"""Parse scheduler FailedScheduling messages into a count of reasons per message and overall."""
import re, sys
from collections import Counter

def split_top(s):
    """Split on commas that are not inside braces (taints look like {key: value})."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        depth += ch == "{"
        depth -= ch == "}"
        if ch == "," and depth == 0:
            parts.append(cur.strip()); cur = ""
        else:
            cur += ch
    return parts + [cur.strip()] if cur.strip() else parts

def parse(msg):
    m = re.match(r"0/(\d+) nodes are available: (.*)", msg)
    total, rest = int(m.group(1)), m.group(2)
    rest = re.split(r"\.\s+preemption:", rest)[0].rstrip(".")      # drop the preemption tail
    counts = Counter()
    for part in split_top(rest):
        pm = re.match(r"(\d+) (.*)", part)
        if pm:
            counts[pm.group(2)] += int(pm.group(1))
        else:
            counts[part] += total                                   # no count prefix: applies to all
    return total, counts

HINTS = {
    "Insufficient": "no node has that much free; reduce requests, add nodes, or wait for autoscaler",
    "untolerated taint": "add a toleration, or this pod should not run on those nodes",
    "node affinity": "fix nodeSelector / affinity labels vs kubectl get nodes --show-labels",
    "unbound": "PVC is not bound: kubectl get pvc, check StorageClass and zone",
    "Too many pods": "node pod-count cap reached: more nodes or bigger max-pods",
}
def hint(reason):
    return next((h for k, h in HINTS.items() if k in reason), "read the full event")

if __name__ == "__main__":
    grand = Counter()
    for line in open(sys.argv[1]):
        total, counts = parse(line.strip())
        grand.update(counts)
        print(f"nodes={total}  sum_of_reasons={sum(counts.values())}")
        for r, n in counts.most_common():
            print(f"   {n} x {r}  -> {hint(r)}")
    print("\noverall:")
    for r, n in grand.most_common():
        print(f"  {n:2d}  {r}")
