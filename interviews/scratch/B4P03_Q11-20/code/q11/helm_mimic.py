"""Helm mimic (teaching illustration, NOT helm): value merging + a tiny `helm template`.
Render supports ONLY what the chart uses: {{ .Values.a.b }}, {{ .Release.Name }}, {{ .Chart.Name }},
| quote, include "modelserver.fullname", and {{- if .Values.x }} ... {{- end }}.
Usage: helm_mimic.py values | helm_mimic.py CHART [-f file] [--set a.b=c] [--release name]"""
import re, sys, glob, os, copy
import yaml

import copy

def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in over.items():
        if v is None:                       # null in an override deletes the key
            out.pop(k, None)
        elif isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)  # maps merge key by key
        else:
            out[k] = copy.deepcopy(v)       # scalars AND lists are replaced whole
    return out

def typed(s):
    """--set value typing: true/false/null/integers are converted, the rest stay strings."""
    if s.lower() == "true": return True
    if s.lower() == "false": return False
    if s.lower() == "null": return None
    if s.isdigit() and not (len(s) > 1 and s[0] == "0"): return int(s)
    return s

def parse_set(expr):
    path, _, raw = expr.partition("=")
    tree = cur = {}
    keys = path.split(".")
    for k in keys[:-1]:
        cur[k] = {}
        cur = cur[k]
    cur[keys[-1]] = typed(raw)
    return tree

def compute_values(defaults, files=(), sets=()):
    vals = defaults
    for f in files:
        vals = deep_merge(vals, f)
    for s in sets:
        vals = deep_merge(vals, parse_set(s))
    return vals


TOKEN = re.compile(r"(\s*)\{\{(-?)\s*(.*?)\s*\}\}")

def lookup(ctx, path):
    cur = ctx
    for part in path.strip(".").split("."):
        cur = cur[part]
    return cur

def scalar(v):
    if v is True: return "true"
    if v is False: return "false"
    return str(v)

def evaluate(expr, ctx):
    quote = False
    if "|" in expr:
        expr, filt = [x.strip() for x in expr.split("|", 1)]
        assert filt == "quote", filt
        quote = True
    if expr.startswith("include"):
        assert '"modelserver.fullname"' in expr
        val = f'{ctx["Release"]["Name"]}-{ctx["Chart"]["Name"]}'
    else:
        val = scalar(lookup(ctx, expr))
    return f'"{val}"' if quote else val

def render(text, ctx):
    out, pos, stack = [], 0, []          # stack of "is this branch active"
    for m in TOKEN.finditer(text):
        ws, trim, expr = m.group(1), m.group(2), m.group(3)
        active = all(stack)
        if active:
            out.append(text[pos:m.start()])
            if not trim:
                out.append(ws)           # '{{-' removes the whitespace before it
        pos = m.end()
        if expr.startswith("define") or expr == "end" and stack == []:
            continue
        if expr.startswith("if "):
            stack.append(bool(lookup(ctx, expr[3:])))
        elif expr == "end":
            stack.pop()
        elif active:
            out.append(evaluate(expr, ctx))
    if all(stack):
        out.append(text[pos:])
    return "".join(out)

def values_demo():
    defaults = yaml.safe_load(open("chart/modelserver/values.yaml"))
    prod = yaml.safe_load(open("prod.yaml"))
    v = compute_values(defaults, [prod], ["image.tag=1.4.2", "replicaCount=5"])
    print("replicaCount :", v["replicaCount"], "(default 2, prod.yaml 3, --set 5 wins)")
    print("limits       :", v["resources"]["limits"], "(prod.yaml replaced memory)")
    print("requests kept:", v["resources"]["requests"], "(maps merge, untouched keys survive)")
    print("gpu          :", v["gpu"])
    print("--set typing :", {k: parse_set(k + "=" + s)[k] for k, s in [("a", "20260101"), ("b", "true"), ("c", "1.10"), ("d", "007")]})
    print("list replace :", compute_values({"args": ["--a", "--b"]}, [{"args": ["--c"]}]))
    print("null deletes :", compute_values({"gpu": {"enabled": True}, "x": 1}, [{"x": None}]))

def main(argv):
    if argv[1] == 'values':
        return values_demo()
    chart = argv[1]
    files, sets, release = [], [], "release-name"
    i = 2
    while i < len(argv):
        if argv[i] == "-f": files.append(yaml.safe_load(open(argv[i+1]))); i += 2
        elif argv[i] == "--set": sets.append(argv[i+1]); i += 2
        elif argv[i] == "--release": release = argv[i+1]; i += 2
        else: raise SystemExit("unknown arg " + argv[i])
    meta = yaml.safe_load(open(f"{chart}/Chart.yaml"))
    defaults = yaml.safe_load(open(f"{chart}/values.yaml"))
    ctx = {"Values": compute_values(defaults, files, sets),
           "Release": {"Name": release}, "Chart": {"Name": meta["name"]}}
    docs = []
    for path in sorted(glob.glob(f"{chart}/templates/*.yaml")):
        docs.append(f"---\n# Source: {meta['name']}/templates/{os.path.basename(path)}\n"
                    + render(open(path).read(), ctx).strip() + "\n")
    print("".join(docs), end="")

if __name__ == "__main__":
    main(sys.argv)
