# Q21: list ARG/ENV scope per stage: which ARGs are build-only, which become runtime ENV, and the ARG-before-FROM gotcha.
import re, sys
text = open(sys.argv[1]).read().replace("\\\n", " ")
global_args, stage, stages = {}, None, []
for ln in text.splitlines():
    ln = ln.strip()
    m = re.match(r"(ARG|ENV|FROM)\s+(.*)", ln, re.I)
    if not m: 
        if stage is not None and re.match(r"RUN|CMD|LABEL", ln): stage["uses"] |= set(re.findall(r"\$\{?(\w+)", ln))
        continue
    k, rest = m.group(1).upper(), m.group(2)
    if k == "ARG" and stage is None:
        n = rest.split("=")[0]; global_args[n] = rest.split("=", 1)[1] if "=" in rest else None
    elif k == "FROM":
        stage = {"from": rest, "args": {}, "env": {}, "uses": set()}; stages.append(stage)
    elif k == "ARG":
        n = rest.split("=")[0]; stage["args"][n] = rest.split("=", 1)[1] if "=" in rest else None
    elif k == "ENV":
        for n, v in re.findall(r"(\w+)=(\S+)", rest): stage["env"][n] = v; stage["uses"] |= set(re.findall(r"\$\{?(\w+)", v))
print("global ARGs (before first FROM):", list(global_args), "-> usable ONLY in FROM lines unless redeclared")
for i, s in enumerate(stages):
    print(f"\nstage {i}: FROM {s['from']}")
    for n in s["args"]:
        in_env = n in s["env"] or any(f"${{{n}}}" in v or f"${n}" in v for v in s["env"].values())
        redeclared = n in global_args
        status = "build-only (gone at runtime)"
        extra = " (redeclared: value inherited from global default)" if redeclared and s["args"][n] is None else ""
        print(f"  ARG {n:14} {status}{extra}; value baked into an ENV: {in_env}")
    for n, v in s["env"].items(): print(f"  ENV {n:14} runtime (visible in docker inspect/ps env): {v}")
    for u in sorted(s["uses"]):
        if u not in s["args"] and u not in s["env"]: print(f"  WARNING: ${u} used but not declared in this stage (empty at build time)")
