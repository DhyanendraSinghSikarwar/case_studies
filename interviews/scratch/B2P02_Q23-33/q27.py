import torch
x = torch.tensor(70000.0)
print("fp16(70000):", x.half().item(), "| bf16(70000):", x.bfloat16().item())
print("max fp16:", torch.finfo(torch.float16).max, "max bf16:", torch.finfo(torch.bfloat16).max)
print("eps fp16:", torch.finfo(torch.float16).eps, "eps bf16:", torch.finfo(torch.bfloat16).eps)
print("fp16(1e-8):", torch.tensor(1e-8).half().item(), "bf16(1e-8):", torch.tensor(1e-8).bfloat16().item())
for dt in (torch.float16, torch.bfloat16, torch.float32):
    w = torch.tensor(1.0, dtype=dt)
    for _ in range(1000): w = w + torch.tensor(1e-4, dtype=dt)
    print(dt, "1.0 + 1000 x 1e-4 =", w.item())
