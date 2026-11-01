# SYNTHETIC expected-vs-actual tool calls; no model. Shows the scoring logic.
cases = [
 # (id, expected calls, actual calls)   a call is (name, args)
 ("c1", [("get_order", {"order_id": "A1"})],                          [("get_order", {"order_id": "A1"})]),
 ("c2", [("get_order", {"order_id": "A1"})],                          [("get_order", {"order_id": "a1"})]),            # arg differs in case
 ("c3", [("get_weather", {"city": "Pune"})],                          [("search_web", {"q": "weather Pune"})]),        # wrong tool
 ("c4", [],                                                           []),                                             # no call needed: correct
 ("c5", [],                                                           [("get_order", {"order_id": "A1"})]),            # called when not needed
 ("c6", [("get_order", {"order_id": "A1"}), ("get_order", {"order_id": "B2"})],
        [("get_order", {"order_id": "B2"}), ("get_order", {"order_id": "A1"})]),                                         # parallel, order differs
 ("c7", [("get_order", {"order_id": "A1"})],
        [("get_order", {"order_id": "A1"}), ("get_order", {"order_id": "A1"}), ("get_order", {"order_id": "A1"})]),     # correct but wasteful
]

def norm(v): return v.strip().lower() if isinstance(v, str) else v

def key(call, lenient): 
    name, args = call
    return (name, tuple(sorted((k, norm(v) if lenient else v) for k, v in args.items())))

def score(cases, lenient=False):
    n = len(cases)
    sel = arg = exact = nocall_ok = nocall_n = extra = 0
    for _, exp, act in cases:
        if not exp:
            nocall_n += 1; nocall_ok += (not act)
        e_names, a_names = sorted(c[0] for c in exp), sorted(c[0] for c in act)
        sel += e_names == a_names
        arg += sorted(key(c, lenient) for c in exp) == sorted(key(c, lenient) for c in act)
        extra += max(0, len(act) - len(exp))
    return dict(tool_selection=f"{sel}/{n}", args_match=f"{arg}/{n}",
                no_call_correct=f"{nocall_ok}/{nocall_n}", extra_calls=extra,
                avg_calls_per_case=round(sum(len(a) for _, _, a in cases) / n, 2))

print("strict  :", score(cases))
print("lenient :", score(cases, lenient=True), " (case/whitespace-insensitive strings)")
