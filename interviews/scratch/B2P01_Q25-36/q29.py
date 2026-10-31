import torch
def window_mask(T, w, sinks=0):
    i = torch.arange(T)[:, None]; j = torch.arange(T)[None, :]
    causal = j <= i
    local = (i - j) < w                 # last w tokens incl. itself
    sink = j < sinks                    # first few tokens always visible
    return causal & (local | sink)
print(window_mask(8, 3).int())
print(window_mask(8, 3, sinks=1).int())
T,w,s=100_000,4096,4
print("kv slots kept sliding+sinks:", w+s, "vs full", T)
