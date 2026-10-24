# Diagnostic over a toy SFT batch: masked fraction, label shift, trainable params, suspicious-value flags. Toy model, no library.
import torch, torch.nn as nn
IGNORE = -100
def diagnose(model, input_ids, labels, eos_id, adapter_prefix="lora_"):
    flags = []
    valid = labels != IGNORE
    masked_frac = 1 - valid.float().mean().item()
    # label shift: in a correct HF-style batch, labels == input_ids at unmasked positions (the model shifts internally).
    same = (labels[valid] == input_ids[valid]).float().mean().item() if valid.any() else float("nan")
    # if labels were already shifted by the user, label[t] == input[t+1] and the double shift trains the wrong target
    shifted_match = (labels[:, :-1][labels[:, :-1] != IGNORE] == input_ids[:, 1:][labels[:, :-1] != IGNORE]).float().mean().item() \
        if (labels[:, :-1] != IGNORE).any() else float("nan")
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    adapters = sum(p.numel() for n, p in model.named_parameters() if adapter_prefix in n and p.requires_grad)
    last_has_eos = (input_ids[:, -1] == eos_id).float().mean().item()
    if masked_frac == 0: flags.append("no masking: prompt tokens are in the loss")
    if masked_frac > 0.95: flags.append("almost everything masked: few or no supervised tokens")
    if (~valid).all(): flags.append("ALL labels ignored: loss will be NaN/0")
    if shifted_match > same and shifted_match > 0.9: flags.append("labels look pre-shifted: double shift")
    if trainable == 0: flags.append("no trainable parameters")
    if adapter_prefix and adapters == 0: flags.append("no trainable adapter parameters (adapter not attached or frozen)")
    if trainable / total > 0.5 and adapter_prefix: flags.append("most params trainable: expected adapter-only?")
    if last_has_eos < 0.5: flags.append("EOS missing at sequence end")
    if not model.training: flags.append("model in eval mode: dropout off")
    print(f"masked {masked_frac:.1%} | labels==inputs {same:.2f} | labels==next-input {shifted_match:.2f} | "
          f"trainable {trainable}/{total} (adapter {adapters}) | EOS-final {last_has_eos:.0%}")
    print("FLAGS:", flags or "none")

class Tiny(nn.Module):
    def __init__(self, lora=True):
        super().__init__()
        self.emb = nn.Embedding(50, 8); self.base = nn.Linear(8, 8)
        self.lora_A = nn.Parameter(torch.zeros(2, 8)); self.lora_B = nn.Parameter(torch.zeros(8, 2))
        for p in list(self.emb.parameters()) + list(self.base.parameters()): p.requires_grad = False
        if not lora: self.lora_A.requires_grad = self.lora_B.requires_grad = False

EOS = 2
ids = torch.tensor([[5, 6, 7, 8, 9, EOS], [5, 6, 10, 11, 12, EOS]])
good = ids.clone(); good[:, :3] = IGNORE                       # prompt masked, answer supervised
print("== healthy batch"); diagnose(Tiny(), ids, good, EOS)
print("== bad: no masking, adapter frozen, no EOS, eval mode")
noeos = ids.clone(); noeos[:, -1] = 0
m = Tiny(lora=False).eval()
diagnose(m, noeos, noeos.clone(), EOS)
print("== bad: labels pre-shifted by the user")
pre = torch.full_like(ids, IGNORE); pre[:, 2:-1] = ids[:, 3:]     # label[t] = input[t+1]
diagnose(Tiny(), ids, pre, EOS)
print("== bad: everything masked")
diagnose(Tiny(), ids, torch.full_like(ids, IGNORE), EOS)
