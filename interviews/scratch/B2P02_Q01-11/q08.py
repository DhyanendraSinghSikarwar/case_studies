N = 7e9
for name, tokens in [("pretrain from scratch, 2T tokens", 2e12), ("continued pretrain, 50B tokens", 50e9), ("full fine-tune, 50k ex x 500 tok", 50_000*500)]:
    print(f"{name:36s} tokens {tokens:.1e}  FLOPs ~6ND = {6*N*tokens:.2e}")
