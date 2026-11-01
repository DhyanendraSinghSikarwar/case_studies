# ASSUMED accounting for a 7B-parameter policy; value and reward models assumed also 7B.
P = 7e9
GB = 1e9
bf16 = 2
weights_each = P * bf16 / GB
print(f"bf16 weights per model: {weights_each:.0f} GB")
frozen = 2 * weights_each                      # reference + reward, inference only
# trainable policy and value, mixed precision with Adam:
# bf16 weights (2) + bf16 grads (2) + fp32 master (4) + Adam m (4) + Adam v (4) = 16 B/param
train_bytes = 2 + 2 + 4 + 4 + 4
trainable = 2 * P * train_bytes / GB
print(f"frozen ref + reward: {frozen:.0f} GB")
print(f"policy + value with {train_bytes} B/param training state: {trainable:.0f} GB")
print(f"total before activations and KV cache: {frozen + trainable:.0f} GB")
print(f"80 GB GPUs needed at minimum if perfectly sharded: {(frozen + trainable)/80:.1f}")
# GRPO-style: no value model (critic), reference kept; reward is a rule or a small model
grpo = weights_each + P * train_bytes / GB + weights_each
print(f"GRPO-style (policy train + ref bf16 + reward as bf16 7B): {grpo:.0f} GB; with rule reward: {grpo - weights_each:.0f} GB")
