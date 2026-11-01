import torch

# ---------- BUGGY (as an LLM might write it) ----------
def buggy_sample(logits, temperature=0.8, top_p=0.9):      # logits: (B, V)
    probs = torch.softmax(logits, dim=-1)                   # BUG 2: softmax BEFORE temperature
    probs = probs / temperature                             #   (dividing probabilities, not logits)
    sorted_p, idx = torch.sort(probs, descending=True)
    cum = torch.cumsum(sorted_p, dim=-1)
    cutoff = int((cum < top_p).sum())                       # BUG 5: whole-batch count, ignores batch dim
    sorted_p[:, cutoff:] = 0                                # BUG 1: drops the token that crosses top_p
                                                            # BUG 3: no renormalisation
    logits[:] = 0                                           # BUG 4: mutates caller's tensor
    return idx[:, 0]                                        # (placeholder)

# ---------- FIXED ----------
def sample_top_p(logits, temperature=0.8, top_p=0.9, generator=None):
    """logits: (B, V) float tensor. Returns (B,) token ids. Does not modify `logits`."""
    scaled = logits / temperature                           # temperature on logits, out-of-place
    probs = torch.softmax(scaled, dim=-1)
    sorted_p, idx = torch.sort(probs, dim=-1, descending=True)
    cum = torch.cumsum(sorted_p, dim=-1)
    keep = (cum - sorted_p) < top_p                         # keep token if mass BEFORE it < top_p
    keep[:, 0] = True                                       # always keep the top token
    sorted_p = sorted_p * keep                              # per row
    sorted_p = sorted_p / sorted_p.sum(dim=-1, keepdim=True)  # renormalise
    choice = torch.multinomial(sorted_p, 1, generator=generator)
    return idx.gather(-1, choice).squeeze(-1)

def nucleus_probs_ref(logits_row, temperature, top_p):
    """Independent reference: plain python loop on one row, float64."""
    z = [float(v) / temperature for v in logits_row]
    m = max(z); e = [torch.exp(torch.tensor(v - m, dtype=torch.float64)).item() for v in z]
    s = sum(e); p = [v / s for v in e]
    order = sorted(range(len(p)), key=lambda i: -p[i])
    kept, mass = [], 0.0
    for i in order:
        kept.append(i); mass += p[i]
        if mass >= top_p: break                             # smallest set with mass >= top_p
    q = [0.0] * len(p); tot = sum(p[i] for i in kept)
    for i in kept: q[i] = p[i] / tot
    return q

if __name__ == "__main__":
    torch.manual_seed(0)
    # --- isolated demonstrations of each bug on tiny hand-made cases ---
    l = torch.log(torch.tensor([[0.5, 0.3, 0.15, 0.05]]))
    p = torch.softmax(l, -1)
    cum = torch.cumsum(p, -1)
    print("probs", p.tolist(), "cum", cum.tolist())
    n_below = int((cum < 0.7).sum())
    print("Bug1: top_p=0.7, buggy keeps", n_below, "token(s) via cum<p count; token crossing threshold dropped.",
          "Correct nucleus = 2 tokens (0.5+0.3=0.8>=0.7)")
    # bug 2
    t = 0.5
    right = torch.softmax(l / t, -1); wrong = torch.softmax(l, -1) / t
    print("Bug2: right", [round(v, 4) for v in right[0].tolist()], "sum", round(right.sum().item(), 4))
    print("      wrong", [round(v, 4) for v in wrong[0].tolist()], "sum", round(wrong.sum().item(), 4))
    # bug 3
    kept = torch.tensor([[0.5, 0.3, 0.0, 0.0]])
    print("Bug3: truncated probs sum", kept.sum().item(), "-> renormalised", (kept / kept.sum()).tolist())
    # bug 4
    x = torch.randn(2, 5); x0 = x.clone(); buggy_sample(x)
    print("Bug4: caller logits changed by buggy fn:", not torch.equal(x, x0))
    x = torch.randn(2, 5); x0 = x.clone(); sample_top_p(x)
    print("      fixed fn leaves logits unchanged:", torch.equal(x, x0))
    # bug 5
    b = torch.tensor([[3.0, 0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0, 1.0]])
    pr = torch.softmax(b, -1); sp, _ = torch.sort(pr, descending=True); cm = torch.cumsum(sp, -1)
    print("Bug5: per-row counts of cum<0.9:", (cm < 0.9).sum(-1).tolist(), "buggy uses single scalar", int((cm < 0.9).sum()))

    # --- verify fixed function against reference: empirical frequencies, 3 rows ---
    B, V = 3, 8
    logits = torch.randn(B, V) * 2
    g = torch.Generator().manual_seed(1)
    N = 40000
    counts = torch.zeros(B, V)
    big = logits.repeat(N, 1)                              # (N*B, V), row j%B
    s = sample_top_p(big, 0.8, 0.9, generator=g).view(N, B)
    for r in range(B):
        counts[r] = torch.bincount(s[:, r], minlength=V).float() / N
    for r in range(B):
        ref = torch.tensor(nucleus_probs_ref(logits[r].tolist(), 0.8, 0.9))
        print(f"row {r}: max |empirical - reference| = {(counts[r]-ref).abs().max():.4f};",
              "tokens outside nucleus ever sampled:", bool(((counts[r] > 0) & (ref == 0)).any()))
