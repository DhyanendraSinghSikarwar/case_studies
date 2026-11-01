# ILLUSTRATIVE calculator. ALL PRICES AND SPEEDS BELOW ARE ASSUMED, not any provider's.
# Units: currency units per 1M tokens. Replace with your provider's current price list.
ASSUMED = {
    "big":   dict(inp=3.00, out=15.00, cached_inp=0.30, tok_per_s=60),
    "small": dict(inp=0.25, out=1.25,  cached_inp=0.025, tok_per_s=150),
}

def request(model, in_tok, out_tok, cached_frac=0.0):
    p = ASSUMED[model]
    cost = ((in_tok * (1 - cached_frac)) * p["inp"] + (in_tok * cached_frac) * p["cached_inp"]
            + out_tok * p["out"]) / 1e6
    gen_s = out_tok / p["tok_per_s"]            # decode time only; ignores prefill/network
    return cost, gen_s

def show(label, **kw):
    c, s = request(**kw)
    print(f"{label:46s} cost/req {c*1000:8.4f} milli-units   decode {s:5.2f}s   per 1M req {c*1e6:9.0f}")

show("baseline: big, 3000 in, 400 out",            model="big", in_tok=3000, out_tok=400)
show("fewer examples: 1500 in",                    model="big", in_tok=1500, out_tok=400)
show("stable prefix cached (80% of input)",        model="big", in_tok=3000, out_tok=400, cached_frac=0.8)
show("concise output: 150 out",                    model="big", in_tok=3000, out_tok=150)
show("route to small model",                       model="small", in_tok=3000, out_tok=400)
show("all of: 1500 in, 80% cached, 150 out, small", model="small", in_tok=1500, out_tok=150, cached_frac=0.8)

# routing: 70% of traffic easy enough for the small model
easy = 0.7
cb, _ = request("big", 3000, 400); cs, _ = request("small", 3000, 400)
print(f"routing 70% to small: {easy*cs+(1-easy)*cb:.6f} vs all-big {cb:.6f} per request (assumes router is free and quality holds)")
