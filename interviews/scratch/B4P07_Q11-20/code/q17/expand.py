"""Expand a GitHub Actions strategy.matrix (axes + exclude + include) and count jobs."""
import itertools, sys, yaml


def expand(matrix):
    m = dict(matrix)
    include = m.pop("include", [])
    exclude = m.pop("exclude", [])
    axes = list(m)
    combos = [dict(zip(axes, vals)) for vals in itertools.product(*[m[a] for a in axes])] if axes else []
    combos = [c for c in combos if not any(all(c.get(k) == v for k, v in e.items()) for e in exclude)]
    for inc in include:
        # simplified include rule: an entry whose axis values match existing combos adds its extra keys to them
        matched = [c for c in combos if all(c[k] == v for k, v in inc.items() if k in axes)]
        if matched:
            for c in matched:
                c.update({k: v for k, v in inc.items() if k not in axes})
        else:
            combos.append(dict(inc))          # no combo matched: becomes its own new job
    return combos


def show(title, matrix):
    jobs = expand(matrix)
    print(f"== {title}: {len(jobs)} jobs")
    for j in jobs:
        print("  ", j)


if __name__ == "__main__":
    wf = yaml.safe_load(open(sys.argv[1]))
    mx = wf["jobs"]["test"]["strategy"]["matrix"]
    show("as written", mx)
    more = dict(mx); more["numpy"] = ["1.26", "2.1"]
    show("add one axis (numpy x2)", more)
