# Book 1 - Part 08: Deep Learning (Question List)

- **Topic:** Neural net basics, backprop, activations, losses, optimizers (SGD/Adam/AdamW), initialization, norm layers, dropout, gradient problems, CNN/RNN/LSTM basics, training diagnostics, PyTorch from scratch
- **Target:** 50 questions | **Actual:** 58 (⭐⭐⭐ 16, ⭐⭐ 30, ⭐ 12)
- **Date:** 2026-10-20
- Scope: transformer-agnostic DL only; transformers/CV architectures in Part 9, LLM internals in Book 2.
- Status: questions only; answers pending (Wave B).

> Dedupe pass: removed 1 cross-part duplicate(s); renumbered Q1–Q58.

---

### Q1 ⭐⭐⭐ 🟢 Explain backpropagation in simple terms. How does the chain rule give gradients for each layer?
**Asked at:** Product cos, GCCs, MLE loops (OpenAI-style onsite reports)
**Say this first (1 line):** Backprop is just the chain rule applied layer by layer from the loss backwards, reusing each layer's saved forward values, so one backward pass gives the gradient for every weight.

**Then explain:**
- Forward pass: compute and **cache** activations layer by layer, then compute the loss.
- Backward pass: start with dLoss/dOutput. For each layer, the gradient flowing in (`dout`) gives three things: gradient for its weights, gradient for its bias, and gradient to pass to the previous layer.
- Chain rule: if `L = f(g(h(x)))`, then `dL/dx = f' * g' * h'`. Each layer multiplies the incoming gradient by its **local** derivative.
- For a linear layer `z = xW + b`: `dW = xᵀ·dz`, `db = sum(dz)`, `dx = dz·Wᵀ`. For an activation `a = σ(z)`: `dz = da * σ'(z)`.
- Cost is about 2x a forward pass, not one pass per weight. That efficiency is why deep nets are trainable.

**Example:** Net `x -> tanh(xW1) -> W2 -> MSE`. I compute `dp` from the loss, `dW2 = hᵀ dp`, `dh = dp W2ᵀ`, `dz = dh * (1 - h²)` (tanh derivative), `dW1 = xᵀ dz`.

**Code:** (run; I verify with a numeric gradient check, which is how you should test any hand-written backward)
```python
import numpy as np
rng = np.random.default_rng(0)
X = rng.normal(size=(4, 3)); y = rng.normal(size=(4, 1))
W1 = rng.normal(size=(3, 5)) * .5; W2 = rng.normal(size=(5, 1)) * .5
loss = lambda W1, W2: ((np.tanh(X @ W1) @ W2 - y) ** 2).mean()

h = np.tanh(X @ W1); p = h @ W2                  # forward (cache h)
dp = 2 * (p - y) / len(y)                        # dL/dp
dW2 = h.T @ dp; dh = dp @ W2.T
dz = dh * (1 - h ** 2); dW1 = X.T @ dz           # backward

eps = 1e-6; W1b = W1.copy(); W1b[0, 0] += eps
print(dW1[0, 0], (loss(W1b, W2) - loss(W1, W2)) / eps)
# -0.05437033519105147 -0.05437028338661776  -> match
```

**Follow-ups:**
- *Why not compute gradients numerically?* One extra forward per weight: O(#params) passes. Backprop needs one backward pass.
- *Why cache activations?* The backward formulas need them (`h` above). This is why training uses much more memory than inference.

**Common mistakes:** Saying backprop is "the optimizer" (it only computes gradients; SGD/Adam use them). Forgetting the activation derivative term. Mixing up the shapes of `dW` and `dx`.

### Q2 ⭐⭐⭐ 🟢 Why do neural networks need non-linear activation functions? Compare sigmoid, tanh and ReLU.
**Asked at:** Product cos, GCCs, fintech
**Say this first (1 line):** Without a non-linearity, stacked linear layers collapse into a single linear layer, so depth adds nothing. Activations let the network model curves and interactions; ReLU is the default today.

**Then explain:**
- `W2(W1 x) = (W2 W1) x`: two linear layers equal one. Non-linearity between them breaks that.
- Comparison:

| | Range | Pros | Cons |
|---|---|---|---|
| Sigmoid | (0,1) | Probability-like output, good for the final binary head | Saturates (gradient max 0.25, near 0 at the tails), not zero-centred |
| Tanh | (-1,1) | Zero-centred, so better than sigmoid inside | Still saturates, so vanishing gradients |
| ReLU `max(0,x)` | [0,∞) | Cheap, gradient 1 for x>0, no saturation, sparse activations | "Dead ReLU": a neuron stuck at x<0 gets zero gradient forever |

- Rule: ReLU (or GELU/Leaky variants) in hidden layers, sigmoid/softmax only at the output.

**Example:** XOR cannot be solved by any linear model but a 2-unit ReLU hidden layer solves it. With sigmoid, ten layers multiply gradients by at most `0.25¹⁰ ≈ 1e-6`: the early layers barely learn.

**Follow-ups:**
- *Why is zero-centred output nice?* Gradients for the next layer's weights don't all share the same sign, so updates zig-zag less.
- *Fix for dead ReLU?* Leaky ReLU/ELU/GELU, a smaller learning rate, good init.

**Common mistakes:** Claiming sigmoid is "bad everywhere" (it is right for output probabilities). Not knowing why ReLU helps (non-saturating gradient, not just speed).

### Q3 ⭐⭐⭐ 🟢 What is overfitting in a neural network and which regularization techniques do you know (L2, dropout, early stopping, augmentation)?
**Asked at:** Walmart-type GCCs, product cos
**Say this first (1 line):** Overfitting is when the network memorises training data, so train loss keeps falling while validation loss rises. I fight it with more data/augmentation, weight decay, dropout, early stopping and a smaller model.

**Then explain:**
- Sign: big gap between train and validation metric.
- Techniques, in the order I try them:
  1. **More data / augmentation** (flips, crops, noise, text paraphrase): most effective.
  2. **Early stopping**: stop when validation loss stops improving, keep the best checkpoint.
  3. **L2 / weight decay**: penalises large weights, giving smoother functions.
  4. **Dropout**: randomly zero units in training, so units cannot co-adapt (acts like an ensemble).
  5. **Smaller model / fewer epochs / batch norm / label smoothing**.
- Always tune on a validation set, never the test set.

**Example (illustrative, not a run):** 2k-row tabular data, 3-layer net with 512 units shows a train AUC far above validation AUC. Cutting to 64 units, adding dropout 0.3 and weight decay 1e-2 typically lowers train AUC a bit, narrows the gap and often lifts validation.

**Follow-ups:**
- *Dropout and BatchNorm together?* Works, but the order and variance shift can hurt; many modern nets use one or the other.
- *Is a big gap always overfitting?* No, check for leakage or a train/val distribution shift first.

**Common mistakes:** Using the test set to pick the early-stopping epoch. Applying dropout at inference. Listing techniques without saying which you would try first and why.

### Q4 ⭐⭐⭐ 🟢 How does dropout work, and what changes between training and inference (inverted dropout scaling)?
**Asked at:** Walmart Bengaluru (Glassdoor), product cos
**Say this first (1 line):** Dropout randomly zeroes each unit with probability p during training; in inference all units are on. "Inverted" dropout rescales by 1/(1-p) during training so no scaling is needed at inference.

**Then explain:**
- Train: `mask ~ Bernoulli(1-p)`, `out = x * mask / (1-p)`.
- Why divide: the expected value of `x*mask` is `(1-p)x`. Dividing keeps `E[out] = x`, so activation scale is the same in train and eval.
- Eval: dropout is the identity. In PyTorch this needs `model.eval()`.
- Why it works: forces redundancy; like averaging many thinned sub-networks.
- Gradient flows only through kept units.

**Example:** p = 0.2, the kept units are scaled by 1.25. I checked with NumPy: the mean of a ones-vector after dropout is about 0.998, close to 1.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
a = np.ones(100000); p = 0.2
mask = (rng.random(a.shape) >= p) / (1 - p)     # inverted dropout
print((a * mask).mean())   # 0.9984125  (~1, as expected)
# inference: out = a   (no mask, no scaling)
```

**Follow-ups:**
- *Typical p?* 0.1–0.5; lower for conv layers and transformers, higher for big dense layers.
- *Monte-Carlo dropout?* Keep dropout on at inference and average several passes for an uncertainty estimate.

**Common mistakes:** Forgetting `model.eval()`. Scaling at both train and test (double scaling). Thinking dropout drops *weights* (that's DropConnect).

### Q5 ⭐⭐⭐ 🟢 Batch, mini-batch and stochastic gradient descent: differences, and what does momentum add?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** Batch GD uses all data per step, SGD uses one sample, mini-batch uses a small chunk (32–512); mini-batch is the standard. Momentum adds a running average of past gradients so updates keep direction and smooth out noise.

**Then explain:**

| | Data per step | Gradient | Cost per step |
|---|---|---|---|
| Batch | all N | exact, smooth | high, one update per epoch |
| SGD | 1 | very noisy | tiny, hardware-inefficient |
| Mini-batch | B | slightly noisy | GPU-friendly, many updates per epoch |

- The noise from small batches is not all bad: it helps escape sharp minima and regularises.
- Momentum: `v = β v + g`, `w = w - lr * v` (β≈0.9). Consistent gradient directions accumulate (faster along valleys), oscillating ones cancel (less zig-zag).
- Nesterov momentum computes the gradient at the "looked-ahead" point, a small improvement.

**Example (qualitative picture, not a run):** In a long narrow valley with steep sides, plain SGD bounces side to side while advancing slowly along the floor. Momentum cancels the side-to-side part and builds up speed along the floor. With β=0.9, the effective step along a steady gradient is up to 10x larger (1/(1-β)).

**Follow-ups:**
- *Why shuffle every epoch?* Avoids batches in a fixed order biasing the updates.
- *Does momentum need a smaller lr?* Yes, since effective step grows ~1/(1-β).

**Common mistakes:** Saying "SGD" while meaning mini-batch (fine, but be clear). Believing a larger batch is always better. Not knowing momentum's effect on effective step size.

### Q6 ⭐⭐⭐ 🟢 In PyTorch, why do you call optimizer.zero_grad()? What do model.train(), model.eval() and torch.no_grad() each do?
**Asked at:** MLE loops, product cos
**Say this first (1 line):** PyTorch **accumulates** gradients into `.grad`, so you must clear them each step with `zero_grad()`. `model.train()/eval()` switch layer behaviour (dropout, batch norm); `torch.no_grad()` turns off gradient tracking to save memory and time.

**Then explain:**
- `loss.backward()` does `p.grad += new_grad`, not `=`. Without `zero_grad()` the gradients of all previous batches pile up and your step is wrong.
- This accumulation is a feature: gradient accumulation (several `backward()` calls, one `step()`) simulates a larger batch.
- `model.train()`: dropout active, batch norm uses batch stats and updates running stats.
- `model.eval()`: dropout off, batch norm uses running stats. It does **not** stop gradients.
- `torch.no_grad()`: no graph is built, so less memory and faster. It does **not** change dropout/BN behaviour. For validation use both.

**Example / Code:** (run)
```python
import torch, torch.nn as nn
m = nn.Linear(1, 1, bias=False); nn.init.constant_(m.weight, 1.0)
x = torch.tensor([[2.0]])
for _ in range(2): m(x).sum().backward()
print(m.weight.grad.item())        # 4.0  (2 + 2: accumulated)
m.zero_grad(); print(m.weight.grad)  # None (PyTorch 2.x sets to None by default)

d = nn.Dropout(0.5); d.train(); print(d(torch.ones(6)))   # random zeros, survivors = 2.0 (output varies per run)
d.eval();  print(d(torch.ones(6)))                         # tensor([1., 1., 1., 1., 1., 1.])
with torch.no_grad(): print(m(x).requires_grad)           # False
```

**Follow-ups:**
- *Where do you call zero_grad?* Anywhere before `backward()`; usually the start of the step. `set_to_none=True` (the default now) is slightly faster than filling zeros.
- *`eval()` without `no_grad()`?* Correct predictions but wasted memory.

**Common mistakes:** Forgetting `zero_grad()` (loss behaves strangely). Thinking `eval()` disables gradients. Forgetting to switch back to `train()` after validation.

### Q7 ⭐⭐⭐ 🟡 What are vanishing and exploding gradients? Why do they happen and how do you fix them?
**Asked at:** Walmart Bangalore, Snapchat MLE, product cos
**Say this first (1 line):** Gradients are a product of many per-layer factors; if those factors are mostly below 1 the product vanishes, if above 1 it explodes. I fix it with ReLU-type activations, good initialization, normalization, residual connections and gradient clipping.

**Then explain:**
- Backprop multiplies one Jacobian per layer (or per time-step in RNNs). A product of 50 numbers like 0.25 is about 1e-30; a product of 50 numbers like 1.5 is about 6e8.
- **Vanishing**: early layers stop learning, loss plateaus. Causes: sigmoid/tanh saturation (sigmoid derivative ≤ 0.25), bad init, very deep nets, long RNNs.
- **Exploding**: loss/weights become inf or NaN, sudden spikes. Causes: large weights, high lr, RNNs.
- Fixes:

| Problem | Fix |
|---|---|
| Vanishing | ReLU/GELU, He/Xavier init, BatchNorm/LayerNorm, residual connections, LSTM/GRU gates |
| Exploding | Gradient clipping (by norm), lower lr, better init, normalization |

- Diagnose: log the per-layer gradient norm; a steep drop from last to first layer means vanishing.

**Example:** A 10-layer sigmoid MLP: the bound on the gradient is `0.25¹⁰ ≈ 1e-6` times the weights' scale, so layer 1 barely moves. Swap to ReLU + He init + BN and all layers get similar gradient norms.

**Follow-ups:**
- *Why do RNNs suffer most?* The same recurrent matrix is multiplied at every time step, so its largest eigenvalue decides explode vs vanish.
- *Does Adam fix vanishing?* Partly: it rescales per-parameter, but a gradient that is numerically ~0 stays useless.

**Common mistakes:** Saying "use ReLU" only. Confusing dead ReLU with vanishing gradients. Proposing clipping for vanishing gradients (it only caps big ones).

### Q8 ⭐⭐⭐ 🟡 Compare MSE, binary cross-entropy and categorical cross-entropy. Why is cross-entropy preferred for classification?
**Asked at:** Product cos, fintech, GCCs
**Say this first (1 line):** MSE is for regression, binary cross-entropy for two classes/multi-label, categorical cross-entropy for one-of-K classes. Cross-entropy is preferred for classification because it is the likelihood of a probability model and gives strong gradients when the model is wrong.

**Then explain:**
- MSE: `mean((y - ŷ)²)`. Assumes Gaussian noise. Sensitive to outliers.
- BCE: `-[y log p + (1-y) log(1-p)]`, `p = sigmoid(logit)`.
- CCE: `-log p_true_class`, with `p = softmax(logits)`.
- Why not MSE for classification: with sigmoid + MSE the gradient is `(p - y) * p(1-p)`. When the model is confidently wrong (p near 0, y=1) the `p(1-p)` factor kills the gradient and learning stalls. With sigmoid + BCE the gradient on the logit is simply `p - y`: big when wrong.
- Cross-entropy = negative log-likelihood = penalises confident wrong answers very hard (`-log 0.01 = 4.6`). It is also a proper scoring rule, so the probabilities are meaningful.

**Example:** True label 1, model says p=0.01. BCE loss = 4.6 and logit gradient = -0.99. MSE with sigmoid: loss = 0.98 and the gradient is about `-0.99 * 0.0099 * 2 ≈ -0.02`, roughly 50x smaller.

**Follow-ups:**
- *Multi-label problem?* Sigmoid per class + BCE, not softmax.
- *Which PyTorch loss?* `BCEWithLogitsLoss` and `CrossEntropyLoss`: both take **logits**.

**Common mistakes:** Applying softmax/sigmoid before a loss that already does it. Using MSE on class probabilities. Not knowing CE equals log-loss (same thing as MLE).

### Q9 ⭐⭐⭐ 🟡 Compare batch norm and layer norm: how each is computed, when each works, trade-offs.
**Asked at:** Snapchat MLE (prep site, Feb 2026), product cos
**Say this first (1 line):** BatchNorm normalizes each feature across the batch; LayerNorm normalizes across the features of each single sample. BN is the CNN default; LN is the default for transformers and RNNs because it doesn't depend on batch size.

**Then explain:**
- Both compute `(x - mean) / sqrt(var + eps)` then apply learned scale `γ` and shift `β`. Only the axis differs.
- **BatchNorm**: mean/var over the batch (and spatial dims) per channel. Training uses batch stats, inference uses running averages. Needs a reasonably large batch.
- **LayerNorm**: mean/var over the feature dim per sample. Same maths in train and eval; works with batch size 1 and variable-length sequences.
- Benefits: stable gradients, allows higher learning rates, mild regularisation (BN, via batch noise).

| | BN | LN |
|---|---|---|
| Normalizes over | batch (per feature) | features (per sample) |
| Train vs eval | differ | same |
| Small batch | unstable | fine |
| Typical use | CNNs | Transformers, RNNs |

**Example / Code:** (run)
```python
import torch, torch.nn as nn
torch.manual_seed(0)
x = torch.randn(8, 4) * 3 + 5
print(nn.BatchNorm1d(4)(x).mean(0))   # ~0 for every feature column
print(nn.LayerNorm(4)(x).mean(1))     # ~0 for every sample row
```

**Follow-ups:**
- *BN with batch size 2?* Noisy stats; use GroupNorm or LayerNorm.
- *Why BN breaks in sequence models?* Padding and varying lengths make batch statistics messy.

**Common mistakes:** Mixing up the axes. Forgetting BN's eval-mode running stats. Putting BN after the final output layer.

### Q10 ⭐⭐⭐ 🟡 Explain how Adam works. Why is it the default and when would you prefer SGD with momentum?
**Asked at:** Product cos, MLE loops, Europe tech
**Say this first (1 line):** Adam keeps a running mean of gradients (momentum) and a running mean of squared gradients (per-parameter scale) and steps by `m / sqrt(v)`, so each weight gets its own adaptive step size. It works well with little tuning; I choose SGD+momentum when I want the best final generalization, usually for CNNs with a tuned schedule.

**Then explain:**
- Update (β1=0.9, β2=0.999, lr 1e-3 default):
  - `m = β1 m + (1-β1) g`, `v = β2 v + (1-β2) g²`
  - bias-correct: `m̂ = m/(1-β1ᵗ)`, `v̂ = v/(1-β2ᵗ)`
  - `w -= lr * m̂ / (sqrt(v̂) + eps)`
- Parameters with big/noisy gradients get smaller steps, rare/small ones get larger. That helps sparse features and badly scaled problems.
- Default because it is robust to lr choice, fast early, and works for transformers/embeddings.
- SGD+momentum: less memory (one buffer vs two), often generalizes slightly better on vision with lr schedule; needs more lr tuning.
- Use **AdamW** (decoupled weight decay) rather than Adam+L2.

**Example:** Embedding rows for rare words get gradients seldom. Adam's small `v` for them gives larger steps when they do appear; plain SGD would move them very little.

**Follow-ups:**
- *Memory cost?* Adam stores 2 extra tensors per parameter, so about 3x parameter memory plus gradients (before mixed-precision tricks).
- *What is eps for?* Numerical stability when `v̂` is near 0.

**Common mistakes:** Forgetting bias correction (see Q50). Saying Adam "always beats SGD". Using Adam with L2 `weight_decay` and expecting real weight decay (see Q15).

### Q11 ⭐⭐⭐ 🟡 Write a clean PyTorch training loop from scratch (zero_grad, forward, loss, backward, step) with validation.
**Asked at:** MLE loops, OpenAI-style phone screens, Zalando (framework skills)
**Say this first (1 line):** Loop: for each batch, `zero_grad` -> forward -> loss -> `backward` -> `step`; then validate with `eval()` and `no_grad()`, and keep the best model.

**Then explain:**
- Move model and each batch to the same device.
- Train mode for training, eval mode and no_grad for validation.
- Use `loss.item()` for logging (not the tensor, or you keep the graph alive).
- Pass **logits** to `BCEWithLogitsLoss`/`CrossEntropyLoss`.
- Keep a scheduler/early stopping outside the batch loop if needed.

**Example:** On the synthetic 1,000-row set below (800 train, 200 val, CPU), validation accuracy goes from 0.85 after epoch 0 to about 0.95 after epoch 4, with train and val loss falling together (both about 0.12 at the end), so no overfitting yet.

**Code:** (run on synthetic data, CPU)
```python
import torch, torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split
torch.manual_seed(0)
X = torch.randn(1000, 10); w = torch.randn(10)
y = (X @ w + 0.5 * torch.randn(1000) > 0).float()
tr, va = random_split(TensorDataset(X, y), [800, 200], generator=torch.Generator().manual_seed(0))
tl = DataLoader(tr, batch_size=64, shuffle=True); vl = DataLoader(va, batch_size=256)
dev = "cuda" if torch.cuda.is_available() else "cpu"
model = nn.Sequential(nn.Linear(10, 32), nn.ReLU(), nn.Dropout(0.2), nn.Linear(32, 1)).to(dev)
opt = torch.optim.AdamW(model.parameters(), lr=1e-2, weight_decay=1e-2)
lossf = nn.BCEWithLogitsLoss()
for ep in range(5):
    model.train(); tot = 0
    for xb, yb in tl:
        xb, yb = xb.to(dev), yb.to(dev)
        opt.zero_grad()
        loss = lossf(model(xb).squeeze(1), yb)
        loss.backward(); opt.step()
        tot += loss.item() * len(xb)
    model.eval(); vt = ok = 0
    with torch.no_grad():
        for xb, yb in vl:
            xb, yb = xb.to(dev), yb.to(dev); lo = model(xb).squeeze(1)
            vt += lossf(lo, yb).item() * len(xb); ok += ((lo > 0).float() == yb).sum().item()
    print(f"ep{ep} train {tot/len(tr):.3f} val {vt/len(va):.3f} acc {ok/len(va):.3f}")
# ep0 train 0.588 val 0.464 acc 0.850 ... ep4 train 0.121 val 0.121 acc 0.950
```

**Follow-ups:**
- *Add GPU/AMP?* Wrap forward in `torch.autocast`, use `GradScaler` for fp16.
- *Add scheduler?* `sched.step()` per epoch (or per batch for OneCycle/warmup).

**Common mistakes:** Missing `zero_grad`. No `eval()`/`no_grad()` in validation. Averaging loss per batch without weighting by batch size. Calling `sigmoid` before `BCEWithLogitsLoss`.

### Q12 ⭐⭐⭐ 🟡 How do you initialize weights? Explain Xavier/Glorot vs He initialization and why zero init fails.
**Asked at:** Product cos, GCCs
**Say this first (1 line):** Init must keep the signal and gradient variance roughly constant across layers. Xavier/Glorot (variance `2/(fan_in+fan_out)`, or `1/fan_in`) suits tanh/sigmoid; He (variance `2/fan_in`) suits ReLU. Zero init fails because all neurons stay identical.

**Then explain:**
- If weights are too big, activations/gradients explode; too small, they vanish. Both grow exponentially with depth.
- Xavier: keeps variance for roughly linear/tanh units. He: ReLU zeros half the inputs, so the variance needs a factor of 2.
- Zero (or any constant) init: every neuron in a layer computes the same thing and gets the same gradient, so they never differ (symmetry; see Q17). Biases may start at 0.
- PyTorch defaults: `nn.Linear` uses a Kaiming-uniform variant; `nn.init.kaiming_normal_(w, nonlinearity='relu')` for explicit He.

**Example / Code:** (run: 20-layer, width 256 net; std of final activations)
```python
import numpy as np
rng = np.random.default_rng(0)
for name, sc in [("N(0,1)", lambda n: 1.0), ("Xavier", lambda n: np.sqrt(1/n)), ("He", lambda n: np.sqrt(2/n))]:
    for act in ("tanh", "relu"):
        x = rng.normal(size=(512, 256))
        for _ in range(20):
            x = x @ (rng.normal(size=(256, 256)) * sc(256))
            x = np.tanh(x) if act == "tanh" else np.maximum(x, 0)
        print(name, act, "%.2e" % x.std())
# N(0,1) relu 1.25e+21 (explodes) | Xavier relu 8.88e-04 (vanishes) | He relu 7.19e-01 (stable)
# Xavier tanh 1.6e-01, He tanh 5.5e-01, N(0,1) tanh 0.97 (saturated at +-1)
```

**Follow-ups:**
- *Why does Xavier fail for ReLU?* It ignores that ReLU halves the variance each layer; you lose a factor 2 per layer.
- *Init with BatchNorm?* Less sensitive, but still matters.

**Common mistakes:** Using zero init for weights. Using N(0,1) with no scaling. Not matching init to the activation.

### Q13 ⭐⭐⭐ 🟡 Your training loss is not decreasing. How do you debug it, step by step?
**Asked at:** Product cos, MLE loops, Europe tech
**Say this first (1 line):** I shrink the problem: first prove the pipeline can overfit a tiny batch, then check data/labels, loss, learning rate, gradients and architecture one at a time.

**Then explain (in order):**
1. **Overfit one small batch** (e.g. 8-32 samples). If loss doesn't go near 0, there is a code bug, not a modeling problem.
2. **Check data**: labels aligned with inputs, normalization, shuffling, no NaNs, quick look at a few samples and the class balance.
3. **Check loss/outputs**: initial loss should be about `ln(K)` for K classes (`0.69` for binary). Logits into the loss (no extra softmax). Right loss for the task.
4. **Check the training step**: `zero_grad` present, `optimizer.step()` called, parameters actually in the optimizer, `model.train()`, no `.detach()` that cuts the graph, no `no_grad` around training.
5. **Learning rate**: try 10x up and down. Too high gives spikes/NaN; too low gives a flat curve.
6. **Gradients**: log grad norm per layer. Zero = dead/disconnected; huge = exploding.
7. **Simplify**: remove regularization, augmentation, schedulers; try a tiny model, then add things back.
8. Only then: init, normalization, architecture, capacity.

**Example:** Initial loss 2.3 for 10 classes is fine (`ln 10 = 2.30`); initial loss 12 means badly scaled outputs or wrong loss. Loss stuck at 2.30 forever means the model predicts the prior, so look at the lr, gradients or label mismatch.

**Follow-ups:**
- *Loss falls but accuracy doesn't?* Metric bug, class imbalance, or the wrong threshold.
- *Loss decreases on train but not on val?* See Q16.

**Common mistakes:** Changing the architecture first. Tuning many things at once. Not testing the overfit-one-batch sanity check.

### Q14 ⭐⭐⭐ 🟡 How does learning rate affect training? Explain schedulers (step, cosine, warmup) and how you would choose one.
**Asked at:** Product cos, MLE loops
**Say this first (1 line):** The learning rate is the most important hyperparameter: too high diverges or oscillates, too low is slow and gets stuck. A schedule starts with a bigger lr for speed and decays it for fine convergence; warmup avoids early instability.

**Then explain:**
- **Step decay**: multiply lr by 0.1 every N epochs. Simple, classic for CNNs.
- **Cosine annealing**: smooth decay from lr_max to ~0 following a cosine. Strong default, no extra knobs.
- **Warmup**: ramp lr linearly from ~0 over the first few hundred or thousand steps. Needed for Adam/transformers because early `v` estimates and random weights make big steps risky.
- **OneCycle**: warmup up, then anneal down (see Q47).
- **ReduceLROnPlateau**: drop lr when validation stops improving; reactive, good when you don't know the length.
- Choosing: start with Adam(W) 1e-3 (or 3e-4 for transformers) + warmup + cosine; for CNNs with SGD use 0.1 + step/cosine. Do a quick lr sweep on a log scale.

**Example / Code:** (run) 10 steps of the lr under two schedules
```python
import torch
p = torch.nn.Parameter(torch.zeros(1))
def trace(make):
    o = torch.optim.SGD([p], lr=0.1); s = make(o); out = []
    for _ in range(10): o.step(); out.append(round(o.param_groups[0]["lr"], 4)); s.step()
    return out
print(trace(lambda o: torch.optim.lr_scheduler.OneCycleLR(o, max_lr=0.1, total_steps=10)))
# [0.004, 0.052, 0.1, 0.095, 0.0812, 0.0611, 0.0389, 0.0188, 0.005, 0.0]
print(trace(lambda o: torch.optim.lr_scheduler.CosineAnnealingLR(o, T_max=10)))
# [0.1, 0.0976, 0.0905, 0.0794, 0.0655, 0.05, 0.0345, 0.0206, 0.0095, 0.0024]
```

**Follow-ups:**
- *Why does warmup help?* Adam's second-moment estimate is poor at the start and the weights are random, so full-size steps can wreck early training.
- *Scheduler step per epoch or batch?* Match how you defined it; warmup and OneCycle are per batch.

**Common mistakes:** Forgetting to call `scheduler.step()`. Calling it before `optimizer.step()`. No warmup on a transformer.

### Q15 ⭐⭐⭐ 🟡 What is the difference between Adam and AdamW? Why is decoupled weight decay better than L2 inside Adam?
**Asked at:** Product cos, LLM-adjacent teams
**Say this first (1 line):** AdamW applies weight decay directly to the weights, separately from the adaptive gradient step. Adam with L2 adds `λw` to the gradient, which then gets rescaled by `1/sqrt(v)`, so the regularization strength becomes tied to the gradient history.

**Then explain:**
- Adam + L2: `g' = g + λw` then `w -= lr * m̂(g') / sqrt(v̂(g'))`. Weights with large gradients get their decay divided down; weights with tiny gradients get decayed hard. Not uniform shrinkage.
- AdamW: `w -= lr * (m̂/sqrt(v̂) + λ w)`. The decay `lr * λ * w` is independent of the gradient scale, like true weight decay in SGD.
- Result: easier tuning (lr and λ decouple), better generalization; AdamW is the standard for transformers/LLMs.
- In SGD the two are the same thing (see Q31); in Adam they are not.

**Example / Code:** (run) zero loss gradient, only decay, lr 0.1, wd 0.1, 50 steps
```python
import torch
def final(cls):
    w = torch.nn.Parameter(torch.tensor([1.0, 1.0])); o = cls([w], lr=0.1, weight_decay=0.1)
    for _ in range(50):
        o.zero_grad(); (w.sum() * 0).backward(); o.step()   # loss gradient = 0
    return w.detach()
print(final(torch.optim.Adam))    # tensor([-0.0048, -0.0048]) : L2 gradient gets normalized -> step ~ lr, collapses
print(final(torch.optim.AdamW))   # tensor([0.6050, 0.6050]) = (1 - 0.1*0.1)^50 : plain multiplicative decay
```
This is a contrived case to show the mechanism: in Adam the decay term is normalized away from its true size (here it even overshoots), in AdamW it is exactly `lr*λ`.

**Follow-ups:**
- *Typical weight decay?* 0.01-0.1 for AdamW; no decay on biases/LayerNorm params.
- *Paper?* Loshchilov & Hutter, "Decoupled Weight Decay Regularization".

**Common mistakes:** Using `Adam(weight_decay=...)` and calling it weight decay. Applying decay to biases and norm layers. Reusing an L2 value tuned for SGD.

### Q16 ⭐⭐⭐ 🟡 How do you read training vs validation loss curves to diagnose overfitting, underfitting or a bug?
**Asked at:** Product cos, GCCs, Europe tech
**Say this first (1 line):** I compare the shape of train and validation curves: both high = underfitting, train low and validation high or rising = overfitting, and weird patterns (val better than train, flat, spiky) point to bugs, leakage or lr problems.

**Then explain:**

| Curves | Diagnosis | What I do |
|---|---|---|
| Train and val both high, converging | Underfit (high bias) | Bigger model, train longer, higher lr, less regularization, better features |
| Train falling, val falls then rises | Overfit | Early stop, dropout/weight decay, more data/augmentation, smaller model |
| Train low, val flat/high from start | Overfit or distribution mismatch/leakage in train | Check split, data drift |
| Val **lower** than train | Dropout/augmentation active only in train, or leakage | Check eval mode, reporting order |
| Both flat from step 1 | Bug or lr far too low, dead net | See Q13 |
| Spiky / NaN | lr too high, bad batch, exploding grads | Lower lr, clip, check data |
| Val much noisier than train | Small val set | Bigger val set, smoother metric |

- Always plot loss **and** the real metric (AUC, F1): they can disagree.
- Compare epoch-wise on the same scale; log lr too.

**Example:** Train loss 0.2, val loss 0.6 and growing after epoch 8: classic overfitting; restore the epoch-8 checkpoint, add dropout and weight decay.

**Follow-ups:**
- *Val loss rising but accuracy still improving?* Model gets more confident on wrong examples (overconfidence), so calibration worsens before accuracy does.
- *Is a gap always bad?* A small gap is normal.

**Common mistakes:** Judging only by accuracy. Not noticing the training-only dropout effect. Calling noisy curves "overfitting" when the val set is tiny.

### Q17 ⭐⭐ 🟢 Why should you never initialize all weights to the same value (symmetry breaking)?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** If all weights in a layer start equal, every neuron computes the same output and receives the same gradient, so they stay identical forever. Random init breaks the symmetry so neurons learn different features.

**Then explain:**
- Same weights -> same activations -> same incoming gradient -> same update. Ten hidden units behave like one.
- The network's effective width collapses to 1 unit per layer.
- Random small values (properly scaled: Xavier/He) give each neuron a different starting point.
- Biases can be zero: the weights already break symmetry. Zero-init of **all** weights is the failure; also constant non-zero init fails in the same way.

**Example:** Two hidden units, both with weights (0.5, 0.5) and the same output weights. For any input they give the same output, and their gradients are identical, so after each step they remain equal.

**Code:** (run)
```python
import torch, torch.nn as nn
torch.manual_seed(0)
net = nn.Sequential(nn.Linear(3, 4), nn.Tanh(), nn.Linear(4, 1))
for p in net.parameters(): nn.init.constant_(p, 0.5)
net(torch.randn(8, 3)).sum().backward()
print(net[0].weight.grad)   # all 4 rows identical (-0.0431, 0.0550, -0.1013) -> units never diverge
```

**Follow-ups:**
- *Does symmetry matter for a single-layer linear/logistic model?* No: one output neuron and a convex loss, so zero init is fine.
- *Same issue with dropout?* Dropout adds noise but the key fix is random init.

**Common mistakes:** Saying "zero init just learns slowly" (it never differentiates). Confusing this with the vanishing-gradient problem.

### Q18 ⭐⭐ 🟢 How do you save and load PyTorch models (state_dict vs full model) and resume training?
**Asked at:** MLE loops
**Say this first (1 line):** Save the `state_dict` (just the weights), not the whole pickled model. To resume training, also save the optimizer state, scheduler, epoch and RNG state in a checkpoint dict.

**Then explain:**
- `state_dict()` is an ordered dict of tensors. Loading needs the model class defined and a new instance: `model.load_state_dict(sd)`.
- Full-model `torch.save(model)` pickles the class by path: it breaks when code moves, and unpickling arbitrary files is a security risk.
- Resume: save `model`, `optimizer`, `scheduler`, `epoch`, best metric. Optimizer state matters for Adam (moments) so training continues smoothly.
- Use `map_location="cpu"` to load a GPU checkpoint on a CPU box; `model.eval()` before inference.
- `torch.load(..., weights_only=True)` is safer (the default in recent PyTorch).

**Example:** A job dies after epoch 4 (counting from 0). I reload the checkpoint, restore the model and Adam state, and carry on from epoch 5; the check below confirms the restored weights equal the saved ones.

**Code:** (run)
```python
import torch, torch.nn as nn, os, tempfile
f = os.path.join(tempfile.gettempdir(), "ck.pt")
mm = nn.Linear(3, 2); oo = torch.optim.Adam(mm.parameters())
torch.save({"model": mm.state_dict(), "opt": oo.state_dict(), "epoch": 4}, f)

ck = torch.load(f, weights_only=True, map_location="cpu")
m2 = nn.Linear(3, 2); m2.load_state_dict(ck["model"])
oo2 = torch.optim.Adam(m2.parameters()); oo2.load_state_dict(ck["opt"])
print("resume at epoch", ck["epoch"] + 1, torch.equal(m2.weight, mm.weight))  # resume at epoch 5 True
```

**Follow-ups:**
- *Load into a different architecture?* `strict=False` ignores missing/unexpected keys; useful for fine-tuning.
- *Model trained with DataParallel?* Keys have a `module.` prefix; strip it.

**Common mistakes:** Saving the whole model. Not saving optimizer state when resuming. Forgetting `model.eval()` after loading.

### Q19 ⭐⭐ 🟡 What is the softmax function and why is it computed with the log-sum-exp trick? Why feed logits to CrossEntropyLoss?
**Asked at:** Product cos, MLE loops
**Say this first (1 line):** Softmax turns logits into probabilities that sum to 1: `exp(z_i) / Σ exp(z_j)`. The log-sum-exp trick subtracts the max logit first to avoid overflow, and CrossEntropyLoss takes raw logits because it fuses log-softmax with the loss in a numerically stable way.

**Then explain:**
- Softmax is invariant to adding a constant to all logits, so `softmax(z) = softmax(z - max z)`. That keeps `exp` arguments ≤ 0 (no overflow).
- `log softmax(z)_i = z_i - logsumexp(z)`, with `logsumexp(z) = m + log Σ exp(z - m)`. No `log(0)` problem.
- `nn.CrossEntropyLoss` = `LogSoftmax` + `NLLLoss`. If you softmax first, you lose precision and effectively squash twice.
- Also: you often need only the argmax at inference, which equals the argmax of the logits.

**Example / Code:** (run) logits around 1000
```python
import numpy as np, torch
z = np.array([1000., 1001., 1002.])
with np.errstate(all="ignore"): print(np.exp(z) / np.exp(z).sum())   # [nan nan nan]
m = z.max(); e = np.exp(z - m); print(e / e.sum())                  # [0.09   0.2447 0.6652]
print(m + np.log(e.sum()))                                          # 1002.4076...
zt = torch.tensor([[1000., 1001., 1002.]])
print(torch.nn.CrossEntropyLoss()(zt, torch.tensor([2])))           # tensor(0.4076)
```

**Follow-ups:**
- *Softmax temperature?* `softmax(z/T)`: T>1 flatter, T<1 sharper.
- *Binary case?* `BCEWithLogitsLoss` uses the same stability idea.

**Common mistakes:** Applying `softmax` then `CrossEntropyLoss`. Implementing softmax without subtracting the max. Treating softmax outputs as calibrated probabilities.

### Q20 ⭐⭐ 🟡 Write a custom PyTorch Dataset and DataLoader for tabular or text data. What do num_workers, collate_fn and shuffle do?
**Asked at:** MLE loops, Zalando, product cos
**Say this first (1 line):** A `Dataset` defines `__len__` and `__getitem__` (one sample); a `DataLoader` wraps it to batch, shuffle and load in parallel. `shuffle` randomizes order each epoch, `num_workers` loads batches in background processes, and `collate_fn` controls how samples are merged into a batch.

**Then explain:**
- Keep `__getitem__` light: index, convert to tensor, return `(x, y)`.
- `shuffle=True` for training only (not validation/test).
- `num_workers=N`: N subprocesses prefetch. 0 = main process. Use >0 for heavy loading/augmentation; add `pin_memory=True` for GPU. On Windows/macOS put the entry point under `if __name__ == "__main__":`.
- `collate_fn`: needed for variable-length data (pad sequences) or custom batch structures. Default stacks tensors of the same shape.
- For tabular data, loading everything as tensors in memory and using `TensorDataset` is often enough.

**Example:** 10 rows with batch size 4 give batches of 4, 4 and 2 rows (the last one is smaller unless `drop_last=True`). Three sequences of lengths 2, 5 and 3 are padded by `collate_fn` to one `(3, 5)` tensor, with the true lengths kept alongside.

**Code:** (run)
```python
import torch, torch.nn as nn
from torch.utils.data import Dataset, DataLoader

class Tab(Dataset):
    def __init__(self, X, y):
        self.X = torch.as_tensor(X, dtype=torch.float32); self.y = torch.as_tensor(y, dtype=torch.float32)
    def __len__(self): return len(self.X)
    def __getitem__(self, i): return self.X[i], self.y[i]

dl = DataLoader(Tab(torch.randn(10, 3).numpy(), torch.arange(10)), batch_size=4, shuffle=False)
print([b[0].shape for b in dl])   # [torch.Size([4, 3]), torch.Size([4, 3]), torch.Size([2, 3])]

def collate(batch):                      # variable-length text/sequence batch
    xs = [b[0] for b in batch]
    return nn.utils.rnn.pad_sequence(xs, batch_first=True), torch.tensor([len(x) for x in xs])
dl = DataLoader([(torch.ones(n), 0) for n in (2, 5, 3)], batch_size=3, collate_fn=collate)
xb, L = next(iter(dl)); print(xb.shape, L)   # torch.Size([3, 5]) tensor([2, 5, 3])
```

**Follow-ups:**
- *Map-style vs iterable dataset?* Iterable for streams that don't fit in memory.
- *Last small batch?* `drop_last=True` if shapes or BatchNorm need full batches.

**Common mistakes:** Shuffling the validation set (harmless but pointless) or **not** shuffling train. Doing heavy preprocessing in the main process. Applying augmentation to validation data.

### Q21 ⭐⭐ 🟡 Write a custom nn.Module. What do __init__ vs forward do, and how are parameters registered?
**Asked at:** MLE loops, TORC-style hands-on rounds
**Say this first (1 line):** Subclass `nn.Module`; define layers in `__init__` (assigning them as attributes registers their parameters) and the computation in `forward`. Call the model as `model(x)`, not `model.forward(x)`.

**Then explain:**
- `__init__`: call `super().__init__()`, create submodules (`nn.Linear`, ...). Attributes that are `nn.Module` or `nn.Parameter` are auto-registered, so they appear in `parameters()`, move with `.to(device)`, and are saved in `state_dict()`.
- `forward`: how input becomes output. Autograd records it automatically.
- Plain tensors you want saved but not trained: `register_buffer` (e.g. BN running mean).
- Lists of layers must be `nn.ModuleList` / `nn.Sequential` or the layers are **not** registered.

**Example:** A 4-input, 8-hidden, 2-output MLP has 130 parameters (hand check below). If I stored a layer in a plain Python list it would silently be missing from `parameters()`, so the optimizer would never train it.

**Code:** (run)
```python
import torch, torch.nn as nn
class MLP(nn.Module):
    def __init__(self, i, h, o):
        super().__init__()
        self.fc1 = nn.Linear(i, h); self.fc2 = nn.Linear(h, o)
        self.drop = nn.Dropout(0.1)
        self.skip = nn.ModuleList([nn.Linear(h, h)])      # registered
        self.bad = [nn.Linear(1, 1)]                      # plain list: NOT registered
    def forward(self, x):
        return self.fc2(self.drop(torch.relu(self.fc1(x))))
m = MLP(4, 8, 2)
print([n for n, _ in m.named_parameters()], sum(p.numel() for p in m.parameters()))
# ['fc1.weight', 'fc1.bias', 'fc2.weight', 'fc2.bias', 'skip.0.weight', 'skip.0.bias'] 130  (self.bad is missing)
```
(`4*8+8` + `8*8+8` + `8*2+2` = 40 + 72 + 18 = 130.)

**Follow-ups:**
- *Why not call `forward` directly?* `__call__` runs hooks and bookkeeping.
- *Count trainable params?* `sum(p.numel() for p in m.parameters() if p.requires_grad)`.

**Common mistakes:** Plain Python list of layers. Forgetting `super().__init__()`. Putting an `nn.Softmax` before `CrossEntropyLoss`. Using `x = x.to(device)` inside `forward` for tensors that should already be on the right device.

### Q22 ⭐⭐ 🟡 Explain CNNs: convolution, stride, padding, pooling, parameter sharing. Why do they suit images?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** A CNN slides small learned filters over an image, so the same weights detect the same pattern everywhere (parameter sharing) and it builds from edges to textures to objects. This uses far fewer parameters than a dense layer and exploits locality and translation structure in images.

**Then explain:**
- **Convolution**: each filter (e.g. 3x3xC) is dotted with local patches, producing a feature map. Many filters give many channels.
- **Stride**: step size of the slide; stride 2 halves the resolution.
- **Padding**: zeros around the border; "same" padding keeps the size, "valid" shrinks it.
- **Pooling**: downsample (max or average) for small shift-invariance and less compute.
- **Parameter sharing + local connectivity**: a 3x3 conv with 64 filters on 3 channels has `64*(3*9+1) = 1792` parameters regardless of the image size.
- Receptive field grows with depth: deeper units "see" larger regions.
- Why images: neighbouring pixels are correlated and a cat is a cat anywhere in the frame (translation equivariance).

**Example:** A fully connected layer from a 224x224x3 image (150k inputs) to 1000 units needs 150M weights. A 7x7 conv with 64 filters needs 9,472 (see Q23) and works at every position.

**Follow-ups:**
- *Equivariant vs invariant?* Convolution is translation-equivariant (shift in, shift out); pooling/global pooling adds approximate invariance.
- *Do CNNs handle rotation/scale?* Not by design; use augmentation.

**Common mistakes:** Saying conv layers share weights across channels (they share across **positions**, not channels). Forgetting the bias in parameter counts. Confusing equivariance and invariance.

### Q23 ⭐⭐ 🟡 Given an input shape and layer config, compute the output shape and parameter count of a conv layer.
**Asked at:** Pen-and-paper rounds (TORC Robotics), product cos
**Say this first (1 line):** Output size = `floor((H + 2P - K)/S) + 1` per spatial dim, channels = number of filters; parameters = `C_out * (C_in * K * K + 1)`.

**Then explain:**
- Each filter has `K*K*C_in` weights + 1 bias. Multiply by `C_out`.
- Parameters do not depend on the input height/width.
- Pooling layers have no parameters; stride/kernel give the same size formula (`P=0`).
- Compute (multiply-accumulates, ignoring bias) = `C_out * C_in * K² * H_out * W_out`: each weight is used once per output position.

**Example:** Input 3x224x224, Conv(64 filters, 7x7, stride 2, padding 3):
- H_out = floor((224 + 6 - 7)/2) + 1 = floor(111.5) + 1 = **112**
- Output 64x112x112; params = 64 * (3*49 + 1) = **9,472**.

Second: input 16x32x32, Conv(32, 3x3, stride 1, padding 1): output 32x32x32, params = 32*(16*9+1) = **4,640**.

**Code:** (run)
```python
import torch, torch.nn as nn
def conv(H, W, Cin, Cout, k, s=1, p=0):
    return (H + 2*p - k)//s + 1, (W + 2*p - k)//s + 1, Cout * (Cin*k*k + 1)
print(conv(224, 224, 3, 64, 7, 2, 3), conv(32, 32, 16, 32, 3, 1, 1))  # (112,112,9472) (32,32,4640)
c = nn.Conv2d(3, 64, 7, stride=2, padding=3)
print(c(torch.zeros(1, 3, 224, 224)).shape, sum(p.numel() for p in c.parameters()))
# torch.Size([1, 64, 112, 112]) 9472
```

**Follow-ups:**
- *Dilation?* Effective kernel `d*(K-1)+1` replaces K in the formula.
- *Transposed conv output?* `(H-1)*S - 2P + K`.

**Common mistakes:** Forgetting the bias, using `C_out` instead of `C_in` in the weight count, forgetting `floor`, forgetting that padding applies on both sides (`2P`).

### Q24 ⭐⭐ 🟡 How do RNNs work and what is backpropagation through time? Why do they struggle with long sequences?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** An RNN reads a sequence one step at a time, updating a hidden state `h_t = tanh(W_x x_t + W_h h_{t-1} + b)` with the same weights at every step. Backprop through time (BPTT) unrolls the network over the steps and backpropagates through all of them, which makes gradients vanish or explode on long sequences.

**Then explain:**
- The hidden state is the memory: it summarizes everything seen so far.
- Weights are shared across time, so the model handles any length.
- **BPTT**: treat the unrolled net as a very deep feed-forward net with tied weights; sum the weight gradients over time steps. Truncated BPTT limits the unroll length (e.g. 100 steps) to save memory.
- Long sequences: the gradient from step T to step t includes a product of `T-t` Jacobians `W_hᵀ diag(tanh')`. If the largest singular value is below 1 it vanishes (model forgets early information); above 1 it explodes (use clipping).
- Also: sequential computation, so no parallelism over time.

**Example:** Predict the next word in "I grew up in France... I speak fluent ___". The key clue is many steps back; a vanilla RNN's gradient from "France" has shrunk to almost nothing by then.

**Follow-ups:**
- *Fixes?* LSTM/GRU (gates, Q25), gradient clipping, attention/Transformers (Part 9).
- *Bidirectional RNN?* Reads both directions; only for offline tasks where the entire sequence is known.

**Common mistakes:** Thinking an RNN has different weights per step. Saying clipping fixes vanishing. Forgetting to detach the hidden state between truncated chunks.

### Q25 ⭐⭐ 🟡 Explain LSTM gates and how they mitigate vanishing gradients. How does GRU differ?
**Asked at:** Product cos, Amazon-type loops, GCCs
**Say this first (1 line):** An LSTM adds a cell state with three gates (forget, input, output) that control what to erase, write and expose; the cell state is updated additively, which gives gradients a near-linear path through time. GRU merges this into two gates (update, reset) with no separate cell state.

**Then explain:**
- Gates are sigmoids (0 to 1) computed from `x_t` and `h_{t-1}`:
  - Forget `f`: how much old memory to keep.
  - Input `i` with candidate `g = tanh(...)`: what new info to write.
  - Output `o`: how much of the cell to reveal as `h_t = o * tanh(c_t)`.
- Cell update: `c_t = f * c_{t-1} + i * g`. The path `c_{t-1} -> c_t` is an elementwise multiply by `f`, with no repeated matrix multiplication and no squashing. If `f ≈ 1`, the gradient flows back almost unchanged: that is how it mitigates vanishing (see Q57).
- GRU: update gate `z` blends old and new state `h_t = (1-z) h_{t-1} + z h̃`; reset gate `r` controls how much of the past feeds the candidate. Fewer parameters (3 weight sets vs 4), faster, often equal accuracy.
- LSTM vs GRU: LSTM for very long dependencies and when data is large; GRU for speed or small data. In practice, try both.

**Example:** Language modeling: the forget gate can stay near 1 for a subject noun across many words, then drop to 0 when the sentence ends.

**Follow-ups:**
- *Does LSTM fully solve vanishing gradients?* No; it helps a lot but very long ranges still struggle; attention does better.
- *Parameter count of an LSTM layer?* `4 * (input*hidden + hidden*hidden + hidden)` for one bias set (PyTorch has two bias vectors).

**Common mistakes:** Calling the hidden state and cell state the same thing. Saying gates are the "reason" without mentioning the additive cell path. Forgetting that gradient clipping is still used.

### Q26 ⭐⭐ 🟡 What are residual (skip) connections and why do they let you train much deeper networks?
**Asked at:** Product cos, MLE loops
**Say this first (1 line):** A residual connection adds the input to the layer's output: `y = x + F(x)`. The layers only need to learn a correction, and the identity path lets gradients flow straight back, so very deep nets (ResNet-152, Transformers) become trainable.

**Then explain:**
- Backprop: `dy/dx = 1 + dF/dx`. The "1" guarantees a gradient path that does not vanish, however deep the net.
- Easier optimization: if the best block is "do nothing", the net just pushes `F` toward 0 instead of learning an identity through nonlinear layers.
- Plain nets that are made much deeper can get **worse** training error, not just worse test error (the degradation problem); ResNets fixed that (He et al. 2015).
- If dimensions change, use a 1x1 conv (or a linear projection) on the shortcut.
- Used everywhere: ResNet, Transformers, U-Net variants (DenseNet concatenates instead).

**Example / Code:** (run) gradient of the first layer for a deep tanh stack with and without skips
```python
import torch, torch.nn as nn
torch.manual_seed(0)
def grad_first(skip, depth=30):
    layers = nn.ModuleList(nn.Linear(16, 16) for _ in range(depth))
    x = torch.randn(32, 16); h = x
    for l in layers: h = (h + torch.tanh(l(h))) if skip else torch.tanh(l(h))
    h.pow(2).mean().backward()
    return layers[0].weight.grad.norm().item()
print("plain", grad_first(False), "residual", grad_first(True))
# plain 3.9e-10   residual 6.43
```
The plain 30-layer tanh stack has a first-layer gradient about ten orders of magnitude smaller; the residual one stays usable.

**Follow-ups:**
- *Pre-norm vs post-norm?* Pre-norm (norm before the block) trains deeper transformers more stably.
- *Why does it help generalization?* Smoother loss landscape (Li et al., 2018 visualizations).

**Common mistakes:** Saying skips "add parameters". Forgetting the projection when shapes differ. Calling it only a "vanishing gradient fix": it also improves optimization.

### Q27 ⭐⭐ 🟡 What is gradient clipping, when do you need it, and norm vs value clipping?
**Asked at:** Product cos, MLE loops
**Say this first (1 line):** Gradient clipping caps the size of the gradient before the optimizer step so one huge gradient can't blow up training. Norm clipping rescales the whole gradient vector if its L2 norm exceeds a threshold (keeps direction); value clipping clamps each element (changes direction).

**Then explain:**
- Needed for: RNNs/LSTMs, transformers, RL, noisy or heavy-tailed data, high learning rates. Symptom: loss spikes, NaN.
- **Norm clipping**: `g = g * min(1, c / ||g||)`; typical c = 1.0. Preserves direction. Default choice.
- **Value clipping**: `g = clamp(g, -c, c)`; simple but distorts direction.
- Order: `backward()` -> **unscale** (if using AMP GradScaler) -> `clip_grad_norm_` -> `step()`.
- It handles exploding gradients, not vanishing.
- Log the pre-clip norm: if it's clipped most of the time, c is too small or lr too high.

**Example:** One huge input (all 100s) gives a gradient with L2 norm about 173. With `max_norm=1.0` the whole gradient is scaled down by 173x, so the direction is unchanged and the norm becomes exactly 1.

**Code:** (run)
```python
import torch, torch.nn as nn
m = nn.Linear(3, 1)
m(torch.ones(1, 3) * 100).sum().backward()
pre = torch.nn.utils.clip_grad_norm_(m.parameters(), max_norm=1.0)   # returns the norm BEFORE clipping
post = torch.sqrt(sum((p.grad ** 2).sum() for p in m.parameters()))
print(pre.item(), post.item())   # 173.2079620361328 1.0
# value clipping alternative: torch.nn.utils.clip_grad_value_(m.parameters(), 0.5)
```

**Follow-ups:**
- *Global vs per-layer norm?* `clip_grad_norm_` uses the global norm over all parameters (preferred).
- *How to choose c?* Look at the typical gradient-norm distribution; clip around its 90-99th percentile.

**Common mistakes:** Clipping before unscaling under AMP. Clipping after `optimizer.step()`. Using clipping to hide a too-high lr.

### Q28 ⭐⭐ 🟡 How does batch size affect convergence and generalization? What is the linear learning-rate scaling rule?
**Asked at:** Product cos, MLE loops
**Say this first (1 line):** Larger batches give less noisy gradients and better hardware efficiency but fewer updates per epoch and often slightly worse generalization; small batches are noisier, which acts as regularisation. The linear scaling rule says: multiply the learning rate by k when you multiply the batch size by k.

**Then explain:**
- Gradient noise scales like `1/sqrt(B)`. Small B: noisy, many updates, can escape sharp minima. Large B: smooth, closer to full-batch.
- Large-batch training often hits a "generalization gap" and needs retuning (higher lr, warmup, more epochs).
- **Linear scaling rule** (Goyal et al. 2017, ImageNet batch 8k in 1 hour): `lr_new = lr_base * (B_new / B_base)`, plus a warmup of a few epochs. Works for SGD up to a point; for Adam, `sqrt` scaling is often used instead.
- Beyond a "critical batch size" returns diminish: more samples per step stop helping.
- Practical limits: GPU memory (use gradient accumulation), BN needs enough samples per device.

**Example:** Baseline: batch 256, lr 0.1. Move to batch 1024 (4x): lr 0.4 with 5 warmup epochs. Per-epoch steps drop 4x, but each step uses 4x the data, so wall-clock per epoch is shorter on enough GPUs.

**Follow-ups:**
- *Why warmup with big lr?* Early gradients are unreliable, a big lr can diverge.
- *Memory too small for a big batch?* Gradient accumulation: `loss/accum_steps`, `backward()` each micro-batch, `step()` every `accum_steps`.

**Common mistakes:** Increasing batch size without touching lr. Claiming bigger batch is always better. Forgetting BN statistics depend on per-device batch size.

### Q29 ⭐⭐ 🟡 How would you handle class imbalance in a neural network (weighted loss, focal loss, sampling)?
**Asked at:** Fintech (PhonePe/Klarna-type), product cos
**Say this first (1 line):** I first fix the evaluation (use PR-AUC/F1 and threshold tuning, not accuracy), then use class-weighted loss, resampling or focal loss; I try the simplest (weights/threshold) first.

**Then explain:**
- **Weighted loss**: weight the rare class more, e.g. `pos_weight = n_neg / n_pos` in `BCEWithLogitsLoss`, or `weight=` in `CrossEntropyLoss`. Easy, no data change.
- **Focal loss**: `-(1-p_t)^γ log p_t` down-weights easy, confident examples so training focuses on hard ones (γ≈2). Popular in detection (RetinaNet) with extreme imbalance.
- **Sampling**: oversample the minority (or undersample the majority) with `WeightedRandomSampler`; SMOTE is less useful for deep nets/embeddings. Oversampling can overfit duplicates: add augmentation.
- **Threshold moving**: train normally, then pick the decision threshold from the PR curve to meet the business cost.
- Keep the validation set at the **real** class ratio.
- Weighted loss/sampling distort probabilities: recalibrate if you need real probabilities.

**Example / Code:** (run) 1 positive in 6, `pos_weight=5`
```python
import torch, torch.nn as nn
torch.manual_seed(0)
logits = torch.randn(6, 1); tgt = torch.tensor([0, 0, 0, 0, 0, 1.]).unsqueeze(1)
print(nn.BCEWithLogitsLoss(pos_weight=torch.tensor(5.0))(logits, tgt).item())   # 1.9673880338668823 (random logits, so only the mechanism matters)
# focal loss for binary logits
def focal(logits, y, gamma=2.0):
    bce = nn.functional.binary_cross_entropy_with_logits(logits, y, reduction="none")
    p_t = torch.exp(-bce)
    return ((1 - p_t) ** gamma * bce).mean()
```

**Follow-ups:**
- *Fraud at 0.1% positives?* Weighted loss or mild undersampling + PR-AUC + cost-based threshold + calibration.
- *Why not just accuracy?* A model that predicts "all negative" gets 99.9%.

**Common mistakes:** Evaluating with accuracy. Resampling before the train/validation split (leakage). Oversampling then reporting probabilities as if calibrated.

### Q30 ⭐⭐ 🟡 What is early stopping and how do you implement it with checkpointing in PyTorch?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** Early stopping watches the validation loss and stops training when it has not improved for N epochs ("patience"); you save the best weights as a checkpoint and reload them at the end.

**Then explain:**
- It is regularisation by limiting training time: past some epoch, train loss keeps falling but validation loss rises (overfitting).
- Three moving parts: **monitor** (val loss or metric), **patience** (epochs to wait, e.g. 5-10), **min_delta** (smallest change that counts as improvement).
- Always keep the **best** state, not the last one. The last epoch is `patience` epochs past the best.
- Use a validation set, never the test set. If you also use a LR scheduler, keep its patience shorter than the early-stop patience.
- Save `state_dict` (not the whole model); for resuming, also save optimizer and epoch.

**Example:** (run) The val loss bottoms out, the loop stops at epoch 31 with patience 10, and we reload the best weights (val loss 0.3816).

**Code:** (run, seeded)
```python
import torch, torch.nn as nn, copy
torch.manual_seed(0)
X = torch.randn(200, 5); y = (X[:, 0] + 0.5 * torch.randn(200) > 0).float().unsqueeze(1)
Xtr, ytr, Xva, yva = X[:100], y[:100], X[100:], y[100:]
model = nn.Sequential(nn.Linear(5, 64), nn.ReLU(), nn.Linear(64, 1))
opt = torch.optim.Adam(model.parameters(), 1e-2); lossf = nn.BCEWithLogitsLoss()
best, bad, patience = float("inf"), 0, 10
for ep in range(200):
    model.train(); opt.zero_grad(); lossf(model(Xtr), ytr).backward(); opt.step()
    model.eval()
    with torch.no_grad(): v = lossf(model(Xva), yva).item()
    if v < best - 1e-4:                       # improved
        best, bad = v, 0
        torch.save(copy.deepcopy(model.state_dict()), "best.pt")
    else:
        bad += 1
        if bad >= patience:
            print("stop at", ep, "best val", round(best, 4)); break   # stop at 31 best val 0.3816
model.load_state_dict(torch.load("best.pt"))  # restore best weights
```

**Follow-ups:**
- *Why deepcopy the state_dict?* `state_dict()` returns references to the live tensors; without a copy, later updates overwrite your "best" snapshot (here `torch.save` writes immediately, but if you keep it in memory you need the copy).
- *Does early stopping bias the validation score?* Slightly, since you picked the epoch using it. Report final numbers on a separate test set.
- *Noisy val loss?* Raise patience, or smooth the metric.

**Common mistakes:** Returning the last model instead of the best. Stopping on training loss. Early-stopping on the test set. Patience of 1-2 on a noisy metric.

### Q31 ⭐⭐ 🟡 Explain L2 regularization vs weight decay, and when they are equivalent.
**Asked at:** Product cos, MLE loops
**Say this first (1 line):** L2 regularization adds `(λ/2)·||w||²` to the loss; weight decay shrinks the weights directly in the update step. For plain SGD they are the same thing, but for adaptive optimizers like Adam they are not.

**Then explain:**
- L2: loss' = loss + `(λ/2)||w||²`, so the gradient gets an extra `λw`. SGD update: `w ← w − lr(g + λw) = (1 − lr·λ)w − lr·g`. That is exactly weight decay with factor `1 − lr·λ`. Equivalent.
- Adam divides the gradient by `sqrt(v)`. With L2 the `λw` term goes *through* that division, so weights with large historical gradients get *less* decay and weights with small gradients get more. Regularization strength gets tangled up with gradient scale.
- **AdamW** applies the decay directly, `w ← w − lr·λ·w`, outside the adaptive scaling. Uniform shrink, and λ tunes independently of gradient scale.
- Note `torch.optim.SGD(weight_decay=...)` and `Adam(weight_decay=...)` are both implemented as L2 (added to the gradient). Only `AdamW` is truly decoupled.
- Usually no decay on biases and norm parameters.

**Example:** (run) zero data gradient, `w=1.0`, `lr=0.1`, `wd=0.1`, 3 steps. SGD gives 0.9703 (matches `(1−0.01)³`), AdamW 0.9703, but Adam-with-L2 gives 0.7016, because the normalized step is about `lr` regardless of the gradient size.

**Code:** (run)
```python
import torch
def run(cls, **kw):
    w = torch.tensor([1.0], requires_grad=True); o = cls([w], **kw)
    for _ in range(3):
        o.zero_grad(); (w * 0).sum().backward(); o.step()
    return w.item()
print(run(torch.optim.SGD, lr=0.1, weight_decay=0.1))    # 0.97029900
print(run(torch.optim.Adam, lr=0.1, weight_decay=0.1))   # 0.70158625
print(run(torch.optim.AdamW, lr=0.1, weight_decay=0.1))  # 0.97029907
```

**Follow-ups:**
- *Is the effective L2 penalty the same as λ?* Only with the `(λ/2)||w||²` convention; with `λ||w||²` the decay constant is `2λ`.
- *Why does it matter for transformers?* AdamW is the standard because a decay value tuned for SGD does not transfer under Adam.

**Common mistakes:** Saying "they are always the same". Using `Adam(weight_decay=...)` and believing it is decoupled. Decaying biases and LayerNorm scales.

### Q32 ⭐⭐ 🟡 Sigmoid vs softmax output heads: binary, multi-class and multi-label setups and matching losses.
**Asked at:** Product cos, fintech
**Say this first (1 line):** Use sigmoid when each output is an independent yes/no, softmax when exactly one class is correct; and match the loss: `BCEWithLogitsLoss` for sigmoid, `CrossEntropyLoss` for softmax, both fed raw logits.

**Then explain:**

| Task | Output units | Activation | Loss | Target |
|---|---|---|---|---|
| Binary | 1 | sigmoid | `BCEWithLogitsLoss` | float 0/1, shape (N,1) |
| Multi-class (one label) | K | softmax | `CrossEntropyLoss` | int class index, shape (N,) |
| Multi-label (many labels) | K | sigmoid per unit | `BCEWithLogitsLoss` | float multi-hot (N,K) |

- Softmax outputs compete and sum to 1; sigmoid outputs are independent and can all be high.
- Binary can also be done as a 2-way softmax, but one sigmoid unit is simpler and equivalent.
- Do not apply sigmoid/softmax inside the model when using these losses; they fuse it for numerical stability (log-sum-exp).
- Multi-label: threshold each class separately (tune per class); evaluate with per-class PR-AUC or macro-F1.

**Example:** (run) logits `[2.0, 0.5, -1.0]`: softmax = `[0.786, 0.175, 0.039]` (sums to 1). Sigmoid = `[0.881, 0.623, 0.269]` (sums to 1.77: fine for multi-label, wrong for single-label).

**Code:** (run)
```python
import torch, torch.nn as nn
lg = torch.tensor([[2.0, 0.5, -1.0]])
print(nn.CrossEntropyLoss()(lg, torch.tensor([0])).item())                 # 0.2413
print(nn.BCEWithLogitsLoss()(lg, torch.tensor([[1., 1., 0.]])).item())     # 0.3048
```

**Follow-ups:**
- *Tags like "sports" and "politics" on an article?* Multi-label: sigmoid + BCE.
- *Class imbalance in multi-label?* A `pos_weight` vector, one entry per class.
- *Want a "none of the above" option with softmax?* Add an extra class, or use all-sigmoid with a threshold.

**Common mistakes:** Softmax for multi-label. `CrossEntropyLoss` fed probabilities after a softmax. `BCELoss` after a manual sigmoid (unstable). Target shape or dtype mismatch, `(N,)` vs `(N,1)`, int vs float.

### Q33 ⭐⭐ 🟡 What is the dead ReLU problem? Compare Leaky ReLU, ELU, GELU and Swish.
**Asked at:** Product cos, MLE loops
**Say this first (1 line):** A dead ReLU is a neuron whose input is always negative, so its output and gradient are always 0 and it never recovers; Leaky ReLU, ELU, GELU and Swish keep a small non-zero response for negative inputs to avoid this.

**Then explain:**
- ReLU = `max(0, x)`. The gradient is 0 for `x<0`. If a big update or a high learning rate pushes a neuron's bias very negative, it outputs 0 for all inputs and stops learning.
- Causes: high LR, bad init, large negative bias, unnormalized inputs. Fixes: lower LR, He init, batch norm, or a leaky variant.

| Activation | Negative side | Notes |
|---|---|---|
| Leaky ReLU | `0.01x` | Cheap, no dead neurons |
| ELU | `α(eˣ−1)`, saturates at −α | Smooth, mean closer to 0, costs an exp |
| GELU | `x·Φ(x)` | Smooth, slight dip below 0; used in BERT/GPT |
| Swish/SiLU | `x·sigmoid(x)` | Smooth, non-monotonic; used in EfficientNet, and in SwiGLU of LLaMA-style models |

- For CNNs/MLPs ReLU is still a fine default. For transformers, GELU/SiLU variants are the norm.

**Example:** (run) outputs at x = [-3, -1, 0, 1, 3]: ReLU `[0,0,0,1,3]`; Leaky `[-0.03,-0.01,0,1,3]`; ELU `[-0.95,-0.632,0,1,3]`; GELU `[-0.004,-0.159,0,0.841,2.996]`; SiLU `[-0.142,-0.269,0,0.731,2.858]`.

**Code:** (run)
```python
import torch, torch.nn as nn
x = torch.tensor([-3., -1., 0., 1., 3.])
for f in [nn.ReLU(), nn.LeakyReLU(0.01), nn.ELU(), nn.GELU(), nn.SiLU()]:
    print(type(f).__name__, [round(v, 3) for v in f(x).tolist()])
```

**Follow-ups:**
- *How do you detect dead neurons?* Track the fraction of activations that are exactly 0 per layer over a batch.
- *Is Leaky ReLU always better?* Not necessarily; gains are small and task-dependent.

**Common mistakes:** Blaming dead ReLU for slow training when the LR is the issue. Saying GELU is "just ReLU". Mixing up sigmoid-style saturation (vanishing gradient, both sides) with dead ReLU (zero gradient, one side).

### Q34 ⭐⭐ 🟡 Your loss becomes NaN or spikes mid-training. What are the likely causes and fixes?
**Asked at:** MLE loops, product cos
**Say this first (1 line):** NaN or a loss spike almost always means a numerical blow-up: too high a learning rate, exploding gradients, `log(0)` or divide-by-zero, or bad input data; I find the first step where it appears and then fix that cause.

**Then explain (likely causes and fixes):**

| Cause | Symptom | Fix |
|---|---|---|
| LR too high | Loss rises then NaN within a few steps | Lower LR, add warmup |
| Exploding gradients | Grad norm spikes, then inf | `clip_grad_norm_(params, 1.0)`, better init, norm layers |
| `log(0)`, `0/0`, `sqrt(0)` | NaN from step 1 | Use `BCEWithLogits`/`CrossEntropy` on logits, add `eps`, clamp |
| Bad data | NaN/inf in features or labels, or a corrupt batch | Check `torch.isfinite(x).all()`, fix preprocessing |
| Unnormalized inputs or huge targets | Huge activations | Standardize inputs, scale targets |
| fp16 overflow | inf above 65504 | Use bf16 or GradScaler, keep loss and softmax in fp32 |
| Bad batch / rare outlier | One-off spike, then recovers | Clip gradients, skip bad step, inspect that batch |

- Debug order: (1) check data for NaN/inf, (2) overfit one small batch, (3) log the loss and grad norm every step, (4) `torch.autograd.set_detect_anomaly(True)` to find the op that first produced NaN (slow, debug only), (5) lower LR 10x.
- Once weights become NaN they stay NaN, so find the *first* bad step, not the last.

**Example:** (run) `torch.log(torch.tensor(0.))` gives `-inf`, and `torch.exp(torch.tensor(100.))` gives `inf`; `inf - inf` or `0 * inf` then gives NaN. Adding `1e-8` inside the log gives `-18.42` instead.

**Code:** (run, the pieces)
```python
import torch
print(torch.log(torch.tensor(0.)))                  # tensor(-inf)
print(torch.log(torch.tensor(0.) + 1e-8))           # tensor(-18.4207)
print(torch.exp(torch.tensor(100.)))                # tensor(inf)
# in a training loop:
# torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
# if not torch.isfinite(loss): print("bad batch"); continue
```

**Follow-ups:**
- *Spike but recovers?* Typical with Adam on rare outlier batches; clipping and a lower peak LR help.
- *NaN only with fp16?* Overflow or underflow; switch to bf16 or use loss scaling.
- *NaN in eval but not training?* Check BatchNorm running stats and empty batches.

**Common mistakes:** Hand-written `log(softmax(x))` instead of fused losses. Only lowering LR without checking the data. Ignoring grad-norm logging. Leaving `detect_anomaly` on in production training.

### Q35 ⭐⭐ 🟡 When would you use a neural net versus gradient-boosted trees for tabular data?
**Asked at:** Product cos, fintech, Europe tech
**Say this first (1 line):** For typical tabular data, gradient-boosted trees (XGBoost/LightGBM/CatBoost) are the strong default; I reach for a neural net when I have lots of data, multi-modal inputs (text, images, sequences), learned embeddings, multi-task learning, or need end-to-end training.

**Then explain:**
- **Why trees win on tabular:** they handle mixed types, missing values, skewed features and irregular decision boundaries with little tuning, they are robust on small-to-medium data, and they are fast to train. A well-known benchmark (Grinsztajn, Oyallon and Varoquaux, NeurIPS 2022, "Why do tree-based models still outperform deep learning on typical tabular data?", 45 datasets) found trees still ahead on medium-sized data (about 10k samples), even before counting their speed.
- **Where NNs make sense:**
  - Very large data (millions of rows) with high-cardinality categoricals, via embeddings.
  - Mixing tabular with text/image/sequence features in one model.
  - Multi-task or multi-output learning; shared representations.
  - Online/incremental learning; differentiable pipelines; pretraining or transfer.
  - Smooth targets where extrapolation matters (trees cannot extrapolate beyond training range).
- **Costs of NNs:** more preprocessing (scaling, encoding, imputation), more hyperparameters, seed sensitivity, slower, harder to explain.
- Newer tabular models (TabNet, FT-Transformer, TabPFN) are competitive in some settings but are not a default replacement.

**Example:** A bank's 200k-row credit table with 40 mixed features: LightGBM trains in minutes with little tuning and is a hard baseline to beat. If you add transaction text and a 90-day sequence of events, a NN (or a NN on top of GBM-style features, or stacking) becomes attractive.

**Follow-ups:**
- *What would you do in practice?* Start with a GBM baseline, then try a NN only if there is a reason, and consider blending both (often +small gain).
- *Which is easier to serve/monitor?* GBMs: small, fast, and SHAP is cheap.

**Common mistakes:** Assuming deep learning always wins. Comparing a tuned NN with an untuned GBM (or the reverse). Forgetting to scale inputs for the NN. Not counting maintenance and explainability cost.

### Q36 ⭐⭐ 🟡 How do embedding layers work for high-cardinality categorical features in tabular deep learning?
**Asked at:** Flipkart/Swiggy-type recsys-adjacent teams, Zalando
**Say this first (1 line):** An embedding layer is a learnable lookup table that maps each category ID to a small dense vector, so a 10,000-value category becomes, say, 16-50 numbers learned jointly with the rest of the network, instead of a 10,000-wide one-hot.

**Then explain:**
- `nn.Embedding(num_categories, dim)` holds a `(num_categories, dim)` weight matrix; input is integer IDs, output is the matching rows. It equals one-hot times a matrix, without building the one-hot.
- Similar categories (similar users, items, zip codes) end up with nearby vectors, which the net can reuse. Embeddings can also be extracted and reused downstream.
- **Size rule of thumb:** `dim = min(50, round(1.6 * cardinality**0.56))` (fastai heuristic); or `cardinality**0.25`. Tune it.
- **Rare and unseen categories:** reserve index 0 for "unknown", map rare categories (below a count threshold) to it, and apply dropout to categories during training so unknown behaves sensibly. Hashing is an alternative for huge vocabularies.
- Concatenate the embeddings with the scaled numeric features, then feed an MLP.
- Parameter cost: 10,000 x 16 = 160,000 weights for one feature, so very large vocabularies need hashing, smaller dims, or sparse updates.

**Example:** (run) A `user_id` with 10,000 values and a `country` with 50 values, plus 3 numeric features, gives the model below; the 10,000-value feature gets a 50-dim embedding by the heuristic (160,000 params at dim 16).

**Code:** (run)
```python
import torch, torch.nn as nn
torch.manual_seed(0)
class Tab(nn.Module):
    def __init__(s, cards, n_num):
        super().__init__()
        s.embs = nn.ModuleList([nn.Embedding(c, min(50, round(1.6 * c ** 0.56))) for c in cards])
        d = sum(e.embedding_dim for e in s.embs) + n_num
        s.mlp = nn.Sequential(nn.Linear(d, 64), nn.ReLU(), nn.Linear(64, 1))
    def forward(s, xc, xn):                       # xc: (N, n_cat) int64, xn: (N, n_num) float
        return s.mlp(torch.cat([e(xc[:, i]) for i, e in enumerate(s.embs)] + [xn], 1))
m = Tab([10000, 50], 3)
print(m(torch.randint(0, 50, (4, 2)), torch.randn(4, 3)).shape)   # torch.Size([4, 1])
print(sum(p.numel() for p in nn.Embedding(10000, 16).parameters()))  # 160000
```

**Follow-ups:**
- *Cold start for new IDs?* Fall back to the "unknown" vector, or use content features instead of the ID.
- *Why not one-hot or target encoding?* One-hot is huge and sparse; target encoding leaks without careful out-of-fold handling and loses multi-dimensional similarity.
- *Same idea elsewhere?* Word embeddings, recommender user/item embeddings.

**Common mistakes:** No handling for unseen categories. Feeding raw IDs as numeric features. Embedding dims much too large for rare categories (overfits). Index out of range because the vocabulary was built on a different split.

### Q37 ⭐⭐ 🟡 How do you tune hyperparameters for a neural net (random vs grid vs Bayesian), and which matter most?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** I use random search (or Bayesian optimisation such as Optuna) over log-scaled ranges, not grid search, and I tune the learning rate first because it matters most.

**Then explain:**
- **Grid search:** tries every combination; cost explodes with dimensions and wastes trials on unimportant parameters.
- **Random search:** same budget, but each trial tests a *new* value of every parameter, so it covers the important ones better (Bergstra and Bengio 2012). Strong baseline.
- **Bayesian / TPE (Optuna, Hyperopt):** builds a model of "which configs did well" and proposes promising ones; plus pruning (Hyperband/ASHA) to kill bad trials early. Best when each trial is expensive.
- **What matters most (rough order):** learning rate (by far), batch size and schedule/warmup, weight decay and dropout, then width/depth, optimizer betas.
- Sample scale-free parameters on a **log scale** (`lr` in 1e-5..1e-2, `wd` in 1e-6..1e-2); use linear for dropout.
- Use a fixed validation split, same seed policy, check variance across seeds, and finally retrain on the best config and evaluate once on the test set.

**Example:** (run) the three seeded configs below have `lr` = 0.000814, 0.002753, 0.001543, sampled as `10 ** uniform(-5, -2)`; every trial gets a different LR, which is the point.

**Code:** (run)
```python
import numpy as np
rng = np.random.default_rng(0)
cfgs = [{"lr": 10 ** rng.uniform(-5, -2), "wd": 10 ** rng.uniform(-6, -2),
         "dropout": rng.uniform(0, 0.5), "width": int(rng.choice([64, 128, 256]))} for _ in range(3)]
for c in cfgs: print(c)
# for each cfg: train with early stopping, record best val metric, keep the top one
```

**Follow-ups:**
- *Budget of 20 trials?* Random search with a coarse LR sweep first, then a narrower search around the best.
- *Tuned on validation, reporting the same score?* It is optimistic; confirm on held-out test or nested CV.
- *Early pruning?* Hyperband/ASHA stops weak runs after a few epochs.

**Common mistakes:** Grid over linear LR values. Tuning many parameters but not the learning rate. Single-seed comparisons of tiny differences. Tuning on the test set.

### Q38 ⭐⭐ 🟡 How do you make PyTorch experiments reproducible (seeds, determinism, DataLoader workers)?
**Asked at:** MLE loops, Europe tech
**Say this first (1 line):** Seed every random number generator (Python, NumPy, PyTorch), make DataLoader shuffling and worker seeding explicit, and turn on deterministic algorithms; and accept that bit-exact results across different hardware or library versions are not guaranteed.

**Then explain:**
- **Seeds:** `random.seed`, `np.random.seed`, `torch.manual_seed` (this also seeds CUDA in recent versions; `torch.cuda.manual_seed_all` is harmless).
- **DataLoader:** pass `generator=torch.Generator().manual_seed(s)` for shuffling, and a `worker_init_fn` so NumPy/Python RNGs inside workers are seeded (PyTorch seeds torch per worker, but not NumPy in older setups).
- **Deterministic ops:** `torch.use_deterministic_algorithms(True)` raises an error on non-deterministic ops; on GPU set `CUBLAS_WORKSPACE_CONFIG=:4096:8`, and `torch.backends.cudnn.benchmark=False` (and `cudnn.deterministic=True`). Slower.
- **Remaining sources of drift:** different GPU model, CUDA/cuDNN or PyTorch version, atomic-add ops (scatter, index_add), changing `num_workers`, multi-GPU reduction order.
- Also log the seed, library versions, config and data version. For comparing models, run several seeds and report mean and std instead of chasing one exact number.

**Example:** (run) with the same seed, two draws of `torch.randn(2)` are identical, and a seeded generator gives the same shuffle order every run.

**Code:** (run)
```python
import random, numpy as np, torch
def seed_all(s=42):
    random.seed(s); np.random.seed(s); torch.manual_seed(s)
    torch.use_deterministic_algorithms(True)
def seed_worker(wid):
    np.random.seed(torch.initial_seed() % 2**32)
def f(): seed_all(); return torch.randn(2).tolist()
print(f() == f())                                                 # True
g = torch.Generator().manual_seed(0)
dl = torch.utils.data.DataLoader(torch.arange(8.).unsqueeze(1), batch_size=4, shuffle=True,
                                 generator=g, worker_init_fn=seed_worker)
print([b.flatten().tolist() for b in dl])   # [[5.0, 3.0, 1.0, 7.0], [2.0, 6.0, 4.0, 0.0]]
```

**Follow-ups:**
- *Why not set deterministic always?* Some ops get slower or have no deterministic version.
- *Same seed, different result on another machine?* Hardware, library versions or floating-point reduction order differ.

**Common mistakes:** Seeding only `torch`. Forgetting worker seeds when augmentation uses NumPy or `random`. Calling the seed function after the model is already built. Believing a single-seed gain of 0.2% is real.

### Q39 ⭐⭐ 🟡 Explain transfer learning and fine-tuning: which layers do you freeze and what learning rates do you use?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** Transfer learning reuses a model pretrained on a large dataset; you replace the head, first train just the head with the backbone frozen, then optionally unfreeze some top layers and fine-tune them with a much smaller learning rate.

**Then explain:**
- Early layers learn generic features (edges, basic word patterns); later layers are task-specific. So freeze early layers, adapt late ones.
- **Rule of thumb by data size and similarity:**

| Your data | Target close to pretraining | Target different |
|---|---|---|
| Small | Freeze backbone, train new head only (feature extraction) | Freeze early, fine-tune a few top layers lightly |
| Large | Fine-tune the whole net with a small LR | Fine-tune all, maybe longer |

- **Learning rates:** new head about `1e-3`; pretrained layers about `1e-5` to `1e-4` (10-100x smaller). Use *discriminative LRs* via optimizer param groups, with lower LR for earlier layers.
- Warmup helps. Keep norm layers in sensible mode (BatchNorm with small batches: often keep it in eval mode / frozen statistics).
- Use the same preprocessing/normalization the pretrained model expects.
- For LLMs the same idea appears as LoRA/adapters: freeze the base and train small added matrices.

**Example:** (run) freeze first layer, give the head 1e-3 and the frozen/low layer group 1e-5; only the last layer's weights and bias stay trainable.

**Code:** (run)
```python
import torch.nn as nn, torch
net = nn.Sequential(nn.Linear(10, 8), nn.ReLU(), nn.Linear(8, 2))   # stand-in: backbone + head
for p in net[0].parameters(): p.requires_grad = False                 # freeze backbone
print([(n, p.requires_grad) for n, p in net.named_parameters()])
# [('0.weight', False), ('0.bias', False), ('2.weight', True), ('2.bias', True)]
# later, unfreeze and use two LRs:
opt = torch.optim.AdamW([{"params": net[0].parameters(), "lr": 1e-5},
                         {"params": net[2].parameters(), "lr": 1e-3}])
```

**Follow-ups:**
- *Why a small LR for pretrained layers?* A big LR destroys the useful features ("catastrophic forgetting").
- *Frozen model: `eval()` or `no_grad`?* Frozen layers still need `eval()` if they have BatchNorm/Dropout, otherwise statistics keep updating.
- *How many layers to unfreeze?* Treat it as a hyperparameter; unfreeze gradually and watch validation.

**Common mistakes:** Fine-tuning everything at a large default LR such as 1e-3. Freezing layers with `requires_grad=False` but then calling `model.train()`, which puts frozen BatchNorm layers back in train mode so their running statistics keep changing (put them in `eval()`). Unfreezing layers later without adding them to the optimizer (new parameter group). Wrong input normalization for the pretrained model.

### Q40 ⭐⭐ 🟡 Explain mixed precision training and common reasons for GPU out-of-memory errors; how do you reduce memory?
**Asked at:** MLE loops, product cos
**Say this first (1 line):** Mixed precision runs most math in 16-bit (fp16 or bf16) and keeps a few sensitive parts in fp32, which cuts memory and speeds training on modern GPUs; GPU out-of-memory errors come mostly from activations and batch size, and I fix them by shrinking the batch, accumulating gradients, using mixed precision, or checkpointing activations.

**Then explain:**
- **Mixed precision:** weights are kept in fp32 (master copy); forward and backward matmuls and convs run in 16-bit via `torch.autocast`. Memory for activations roughly halves, and tensor cores speed up matmuls.
- **fp16 vs bf16:** fp16 has more precision but a small range (max 65504), so gradients can underflow and you need **loss scaling** (`GradScaler`). bf16 has the fp32 range with less precision, so no scaler needed (A100/H100/TPU/newer cards).
- Autocast keeps unstable ops (softmax, losses, norms, reductions) in fp32.
- **Memory = weights + gradients + optimizer states (Adam: 2 more copies) + activations.** Activations grow with batch size and sequence length.
- **Reduce memory:** smaller batch plus gradient accumulation; mixed precision; gradient checkpointing; shorter sequences; smaller model or LoRA; 8-bit optimizers; `torch.no_grad()` in eval; do not keep graphs (`loss.item()` not `loss` when logging); free cache between runs.

**Example:** Adam in fp32, 1B params: weights 4 GB + grads 4 GB + Adam states 8 GB = 16 GB before activations (hand-computed).

**Code:** (the CPU bf16 autocast part was run; the CUDA GradScaler loop was not executed: no GPU here)
```python
import torch
x = torch.randn(4, 4)
with torch.autocast("cpu", dtype=torch.bfloat16):
    print((x @ x).dtype)                         # torch.bfloat16   (run)

# not executed: needs CUDA
# scaler = torch.amp.GradScaler("cuda")
# for xb, yb in loader:
#     opt.zero_grad()
#     with torch.autocast("cuda", dtype=torch.float16):
#         loss = lossf(model(xb.cuda()), yb.cuda())
#     scaler.scale(loss).backward()
#     scaler.unscale_(opt); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
#     scaler.step(opt); scaler.update()
```

**Follow-ups:**
- *Why does fp16 need loss scaling?* Small gradients underflow to 0 in fp16 (`1e-8` becomes 0); scaling the loss up shifts them into range, and they are unscaled before the step.
- *OOM only at some steps?* Variable-length batches; the longest batch decides the peak. Cap length or sort into buckets.

**Common mistakes:** Calling `.half()` on the whole model instead of autocast. Skipping the scaler with fp16. Accumulating `loss` tensors (keeps the graph) in a list. Assuming OOM is always the model: often it is the batch or a leak.

### Q41 ⭐⭐ 🟡 Here is LLM-generated PyTorch training code. Find the bugs (missing zero_grad, eval mode, softmax before CE, data leakage, wrong device).
**Asked at:** AI-era code-review rounds, product cos
**Say this first (1 line):** I read it like a code review: check the data split, the loss/logits contract, the train/eval modes, the gradient reset, and the device placement; LLM-written training code often gets one of these wrong while still "running".

**Example:** The buggy snippet below is the kind of code an assistant produces: it looks reasonable, and some of it even runs, but it has seven problems. I would walk through it in the order of the numbered comments.

**Buggy snippet (LLM-style):** (not executed: intentionally buggy; it also assumes `X`, `y` and the imports already exist)
```python
X = StandardScaler().fit_transform(X)                     # (1)
Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=0.2)  # (2)
model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Dropout(0.2),
                      nn.Linear(32, 2), nn.Softmax(dim=1)).to("cuda")      # (3)
opt = torch.optim.Adam(model.parameters(), 1e-2); lossf = nn.CrossEntropyLoss()
for ep in range(30):
    loss = lossf(model(Xtr), ytr)                          # (4) (5)
    loss.backward(); opt.step()                            # (6)
acc = (model(Xva).argmax(1) == yva).float().mean()         # (7)
```

**Bugs:**
1. **Data leakage:** scaler fitted on all data before the split; validation statistics leak into training. Fit on train only.
2. **Unseeded, unstratified split:** not reproducible (set `random_state`, `stratify=y` if classes are imbalanced).
3. **Softmax before `CrossEntropyLoss`:** the loss applies log-softmax itself; double softmax squashes gradients. Output raw logits.
4. **Wrong device and types:** the model is hard-coded to `cuda` while the inputs are CPU data (and here still NumPy arrays, not tensors), so this errors. Convert to tensors and move batches with `.to(dev)`.
5. **No explicit `model.train()`:** harmless in this exact snippet (modules start in train mode), but once an `eval()` call is added for validation, nothing switches back and dropout stays off for later epochs. Always call `model.train()` at the top of each training epoch.
6. **Missing `opt.zero_grad()`:** gradients accumulate across steps, so each step uses the sum of all past gradients.
7. **No `model.eval()` / `torch.no_grad()`** at validation: dropout still active, graph built, memory wasted. Also `.mean()` returns a tensor on GPU; use `.item()`.

**Fixed code:** (run on CPU on a synthetic `make_classification` set; val acc 0.825 for this small 30-step demo, the point is the structure, not the score)
```python
import numpy as np, torch, torch.nn as nn
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
torch.manual_seed(0)
X, y = make_classification(1000, 6, n_informative=4, random_state=0)
Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
sc = StandardScaler().fit(Xtr)                                   # fit on train only
Xtr, Xva = [torch.tensor(sc.transform(a), dtype=torch.float32) for a in (Xtr, Xva)]
ytr, yva = torch.tensor(ytr), torch.tensor(yva)                  # int64 labels for CE
dev = "cuda" if torch.cuda.is_available() else "cpu"
model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Dropout(0.2), nn.Linear(32, 2)).to(dev)  # logits
opt = torch.optim.Adam(model.parameters(), 1e-2); lossf = nn.CrossEntropyLoss()
for ep in range(30):
    model.train(); opt.zero_grad()
    loss = lossf(model(Xtr.to(dev)), ytr.to(dev)); loss.backward(); opt.step()
model.eval()
with torch.no_grad():
    acc = (model(Xva.to(dev)).argmax(1).cpu() == yva).float().mean().item()
```

**Follow-ups:**
- *Other things to check?* Label dtype (`int64` for CE), shuffling, learning rate, metric on imbalanced data, test set touched, loss logged as `.item()`.
- *How to use an LLM for this safely?* Treat output as a draft: ask for tests, run an overfit-one-batch check, verify shapes and data flow yourself.

**Common mistakes:** Trusting that code which runs is correct. Spotting only the obvious bug (softmax) and missing the leakage. Not checking where preprocessing is fitted.

### Q42 ⭐⭐ 🟡 What does universal approximation say, and why do we still use deep rather than wide networks?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** The universal approximation theorem says a network with one hidden layer and enough neurons can approximate any continuous function on a compact set to any accuracy, but it says nothing about how many neurons, whether training will find the weights, or whether it will generalize; in practice depth is far more efficient than width.

**Then explain:**
- **What it guarantees:** *existence* of a good approximator (Cybenko 1989, Hornik 1991) for non-polynomial activations, on a compact domain.
- **What it does not say:** the needed width can be exponentially large; gradient descent may not find it; it gives no generalization or sample-complexity bound.
- **Why deep beats wide:**
  - Some functions need exponentially many units with one hidden layer, but only polynomially many with depth (depth-separation results, e.g. Telgarsky 2016).
  - Depth builds **hierarchical features**: edges, then parts, then objects. Composition reuses features, so it is parameter-efficient.
  - Deep nets of the same parameter count often generalize better and train well with residuals and normalization.
- Width still matters (wide nets are easier to optimize; very wide nets approach kernel-like behavior), but real architectures balance both.

**Example:** Parity of n bits: a shallow net needs about `2^n` hidden units, while a deep net with O(n) layers of constant width computes it by chaining XORs (standard textbook example).

**Follow-ups:**
- *Does it justify using a huge single layer?* No; existence is not trainability.
- *Is there a theorem for depth?* Yes, approximation results for deep ReLU nets show they represent piecewise-linear functions with exponentially more linear regions per parameter than shallow ones.

**Common mistakes:** Saying "one hidden layer is enough in practice". Forgetting that the theorem is about representation, not learning. Mixing it up with generalization.

### Q43 ⭐⭐ 🔴 Implement a 2-layer MLP with forward and backward pass in NumPy (no frameworks).
**Asked at:** Product cos, GCCs, from-scratch rounds
**Say this first (1 line):** Forward pass: `z1 = XW1 + b1`, `a1 = ReLU(z1)`, `z2 = a1W2 + b2`, sigmoid, loss. Backward pass: apply the chain rule layer by layer from the output back, and verify with a numerical gradient check.

**Then explain (shapes for N samples, D inputs, H hidden):**
- Forward: `z1 (N,H) = X (N,D) @ W1 (D,H) + b1`; `a1 = max(0, z1)`; `z2 (N,1) = a1 @ W2 (H,1) + b2`; `p = sigmoid(z2)`; `L = mean BCE`.
- Backward (sigmoid + BCE collapses to a clean term): `dz2 = (p - y)/N`; `dW2 = a1.T @ dz2`; `db2 = dz2.sum(0)`.
- Push back through the layer: `da1 = dz2 @ W2.T`; ReLU gate: `dz1 = da1 * (z1 > 0)`; `dW1 = X.T @ dz1`; `db1 = dz1.sum(0)`.
- Each gradient has the same shape as its parameter: a quick sanity check.
- Check against finite differences `(L(w+e) - L(w-e)) / 2e`.

**Example:** (run) 8 samples, 3 features, 5 hidden units. Analytic and numeric gradients agree: `dW1[0,0] = -0.111809` vs numeric `-0.111809`; `dW2[1,0] = -0.035633` vs `-0.035633`. After 300 plain gradient-descent steps (lr 0.5) the loss goes from 1.0162 to 0.0016 (tiny set, so it memorizes).

**Code:** (run, seeded)
```python
import numpy as np
rng = np.random.default_rng(0)
N, D, H = 8, 3, 5
X = rng.normal(size=(N, D)); y = (X[:, 0] > 0).astype(float)[:, None]
W1 = rng.normal(size=(D, H)) * np.sqrt(2 / D); b1 = np.zeros(H)
W2 = rng.normal(size=(H, 1)) * np.sqrt(1 / H); b2 = np.zeros(1)
def fwd(W1, b1, W2, b2):
    z1 = X @ W1 + b1; a1 = np.maximum(0, z1); z2 = a1 @ W2 + b2; p = 1 / (1 + np.exp(-z2))
    return z1, a1, p, -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
z1, a1, p, loss = fwd(W1, b1, W2, b2)
dz2 = (p - y) / N; dW2 = a1.T @ dz2; db2 = dz2.sum(0)
dz1 = (dz2 @ W2.T) * (z1 > 0); dW1 = X.T @ dz1; db1 = dz1.sum(0)
def num(arr, i, e=1e-6):                      # numerical gradient of one entry
    o = arr[i]; arr[i] = o + e; l1 = fwd(W1, b1, W2, b2)[3]
    arr[i] = o - e; l2 = fwd(W1, b1, W2, b2)[3]; arr[i] = o; return (l1 - l2) / (2 * e)
print(dW1[0, 0], num(W1, (0, 0)))             # -0.11180890035 vs -0.11180890036
print(dW2[1, 0], num(W2, (1, 0)))             # -0.03563260418 vs -0.03563260420
for t in range(300):
    z1, a1, p, loss = fwd(W1, b1, W2, b2)
    dz2 = (p - y) / N; dW2 = a1.T @ dz2; db2 = dz2.sum(0)
    dz1 = (dz2 @ W2.T) * (z1 > 0); dW1 = X.T @ dz1; db1 = dz1.sum(0)
    W1 -= .5 * dW1; b1 -= .5 * db1; W2 -= .5 * dW2; b2 -= .5 * db2
print(round(loss, 4))                          # 0.0016
```

**Follow-ups:**
- *Why divide by N?* The loss is a mean, so its gradient is too.
- *Softmax multi-class version?* Same code with `dz2 = (softmax - onehot)/N` (see Q46).
- *Why `* (z1 > 0)`?* ReLU derivative is 1 where the input was positive, else 0.

**Common mistakes:** Wrong shapes (missing transpose). Forgetting the `1/N`. Using the post-activation instead of `z1` for the ReLU mask (equivalent for ReLU, but not for others). Skipping the gradient check.

### Q44 ⭐⭐ 🔴 How does PyTorch autograd work? Explain the computational graph, requires_grad, detach and retain_graph.
**Asked at:** OpenAI-style autograd rounds, MLE loops
**Say this first (1 line):** PyTorch records every operation on tensors that need gradients into a dynamic computational graph during the forward pass, and `.backward()` walks that graph in reverse applying the chain rule, accumulating results in each leaf's `.grad`.

**Then explain:**
- **Graph:** nodes are operations (`grad_fn`, e.g. `AddBackward0`), edges are tensors. It is built on the fly each forward pass ("define by run"), so Python control flow works.
- **`requires_grad=True`:** marks a *leaf* tensor to track (parameters do this by default). Any result computed from it also tracks and has a `grad_fn`.
- **`.backward()`:** computes d(loss)/d(leaf) for all leaves; gradients are **accumulated** (added) into `.grad`, which is why you need `zero_grad()`.
- **`retain_graph`:** by default the graph's saved buffers are freed after `backward()` to save memory; a second backward through it raises an error unless the first used `retain_graph=True` (needed e.g. for multiple losses over a shared graph).
- **`detach()`:** returns a tensor sharing data but cut off from the graph (no gradient flows through it), e.g. for target networks or logging. `torch.no_grad()` disables graph building altogether.
- Backward is vector-Jacobian products: reverse mode costs about the same order as one forward pass, regardless of the number of parameters.

**Example:** (run) `y = x**2 + 3x` at `x=2`: `dy/dx = 2x+3 = 7`. Calling `backward` twice (first with `retain_graph=True`) leaves `x.grad = 14`, showing accumulation.

**Code:** (run)
```python
import torch
x = torch.tensor(2.0, requires_grad=True); y = x ** 2 + 3 * x
print(y.grad_fn.name(), y.is_leaf, x.is_leaf)   # AddBackward0 False True
y.backward(retain_graph=True); print(x.grad)     # 7.0
y.backward(); print(x.grad)                      # 14.0 (accumulated)
print((x * 3).detach().requires_grad)            # False
y2 = x ** 2; y2.backward()
# y2.backward()  -> RuntimeError: Trying to backward through the graph a second time
with torch.no_grad(): print((x * 2).requires_grad)  # False
```

**Follow-ups:**
- *Why dynamic graphs matter?* Variable-length inputs, conditionals and loops in the model are just Python.
- *`loss.item()` vs `loss`?* `item()` gives a Python float and drops the graph; appending `loss` to a list keeps all graphs alive (memory leak).
- *In-place ops?* Can break autograd if they overwrite a value needed for backward; PyTorch raises a version-counter error.

**Common mistakes:** Forgetting `zero_grad()`. Thinking `no_grad` and `eval()` are the same. Calling `backward()` on a non-scalar without a gradient argument. Detaching by accident in the middle of a model so earlier layers get no gradient.

### Q45 ⭐⭐ 🔴 What is the difference between DataParallel and DistributedDataParallel, and when do you need multi-GPU training?
**Asked at:** MLE loops, product cos
**Say this first (1 line):** DataParallel is a single-process, multi-thread wrapper that is easy but slow and unbalanced; DistributedDataParallel (DDP) runs one process per GPU, syncs gradients with an efficient all-reduce, and is the recommended way, including across machines.

**Then explain:**

| | `DataParallel` | `DistributedDataParallel` |
|---|---|---|
| Processes | 1 process, multi-thread | 1 process per GPU |
| Python GIL | Bottleneck | None |
| Model copy | Re-replicated every forward | Replicated once at start |
| Gradient sync | Gather to GPU 0, then scatter | All-reduce, overlapped with backward |
| Load | GPU 0 overloaded | Balanced |
| Multi-node | No | Yes |

- **How DDP works:** every process holds a full model copy and sees a different data shard (`DistributedSampler`). After backward, gradients are averaged with all-reduce (in buckets, overlapped with computation), so each replica applies the same update and stays identical.
- **Effective batch** = per-GPU batch x number of GPUs; adjust LR (Q28).
- **When you need multi-GPU:** the data or time is too large for one GPU (data parallelism speeds training), or the model does not fit in one GPU's memory (needs model/pipeline/tensor parallelism or sharding such as FSDP/DeepSpeed ZeRO; DDP alone does not solve this).
- Try cheaper first: mixed precision, gradient accumulation, a bigger single GPU.

**Example:** 4 GPUs, per-GPU batch 64: effective batch 256; with near-linear scaling, an epoch takes about a quarter of the time (ideal case; communication overhead cuts this).

**Code:** (sketch, not executed: needs multiple GPUs; `model`, `dataset`, `E` are placeholders; launched with `torchrun --nproc_per_node=4 train.py`)
```python
import os, torch, torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler
dist.init_process_group("nccl"); rank = int(os.environ["LOCAL_RANK"])
torch.cuda.set_device(rank)
model = DDP(model.to(rank), device_ids=[rank])
sampler = DistributedSampler(dataset)
loader = torch.utils.data.DataLoader(dataset, batch_size=64, sampler=sampler)
for epoch in range(E):
    sampler.set_epoch(epoch)          # different shuffle each epoch
    ...                               # usual loop; save checkpoints on rank 0 only
```

**Follow-ups:**
- *What about BatchNorm?* Each GPU sees its own batch; use `SyncBatchNorm` if per-GPU batches are small.
- *Model too big for one GPU?* FSDP/ZeRO shard parameters, gradients and optimizer states.
- *Why `set_epoch`?* Otherwise every epoch uses the same shuffle order.

**Common mistakes:** Recommending `DataParallel` for new code. Forgetting `DistributedSampler` (every GPU sees the same data). Logging or saving from all ranks. Assuming DDP lets you train a model larger than one GPU's memory.

### Q46 ⭐⭐ 🔴 Derive the gradient of softmax followed by cross-entropy with respect to the logits.
**Asked at:** Product cos, from-scratch rounds
**Say this first (1 line):** For softmax followed by cross-entropy, the gradient with respect to the logits is simply `p - y`: predicted probabilities minus the one-hot target.

**Then explain (derivation):**
- Softmax: `p_i = e^{z_i} / Σ_k e^{z_k}`. Loss with true class `c`: `L = -log p_c = -z_c + log Σ_k e^{z_k}`.
- Differentiate w.r.t. `z_i`:
  - `∂(-z_c)/∂z_i = -1` if `i = c`, else `0` (that is `-y_i` for one-hot `y`).
  - `∂ log Σ_k e^{z_k} / ∂z_i = e^{z_i} / Σ_k e^{z_k} = p_i`.
- So `∂L/∂z_i = p_i - y_i`.
- Why it is nice: the gradient is bounded in `[-1, 1]` and large when the model is confidently wrong. The `log` cancels the `exp`, so no vanishing gradient from saturation (unlike MSE on softmax). The gradient sums to zero across classes.
- For a batch mean, divide by N: `∂L/∂Z = (P - Y)/N`. It is the first step of backprop in Q43.
- (Via the Jacobian: `∂p_i/∂z_j = p_i(δ_ij - p_j)`, then `Σ_i (-y_i/p_i) · p_i(δ_ij - p_j) = p_j - y_j`: same answer.)

**Example:** (run) 4 logits drawn at random, true class 2. The analytic gradient `p - y` is `[0.226, 0.1746, -0.6219, 0.2213]` and matches a numerical finite-difference gradient. Note it sums to 0 and only the true class is negative.

**Code:** (run, seeded)
```python
import numpy as np
rng = np.random.default_rng(0)
z = rng.normal(size=4); c = 2
sm = lambda z: np.exp(z - z.max()) / np.exp(z - z.max()).sum()
L = lambda z: -np.log(sm(z)[c])
g = sm(z); g[c] -= 1                                     # p - y
e = 1e-6; ng = [(L(z + e * np.eye(4)[i]) - L(z - e * np.eye(4)[i])) / (2 * e) for i in range(4)]
print(np.allclose(g, ng, atol=1e-6), np.round(g, 4))     # True [ 0.226   0.1746 -0.6219  0.2213]
```

**Follow-ups:**
- *Same for sigmoid + BCE?* Yes: `∂L/∂z = p - y`.
- *Label smoothing?* Replace one-hot `y` with a smoothed target; gradient is still `p - y_smooth`.
- *Why subtract `z.max()`?* Numerical stability; it does not change softmax (Q19).

**Common mistakes:** Forgetting the `i = c` term. Applying `softmax` and then `log` separately (instability). Leaving out the `1/N` for batch means. Confusing the Jacobian of softmax with the loss gradient.

### Q47 ⭐ 🟡 What are one-cycle and cosine annealing schedules and how do you find a good learning rate (LR range test)?
**Asked at:** Senior MLE loops
**Say this first (1 line):** Cosine annealing decays the learning rate smoothly from a max to near zero along a half-cosine; one-cycle ramps the LR up to a high peak and then anneals it far below the start in a single cycle; and the LR range test finds a good max LR by sweeping the LR upward and watching the loss.

**Then explain:**
- **Cosine annealing:** `lr_t = lr_min + 0.5(lr_max - lr_min)(1 + cos(πt/T))`. Slow at the start and end, fast in the middle. Often used with warmup; "warm restarts" reset the cycle.
- **One-cycle (Leslie Smith):** warm up from `max_lr/25` to `max_lr` (about 30% of steps), then cosine-anneal to a tiny value (PyTorch default: start `max_lr/25`, end at that start value divided by 1e4). Momentum is cycled inversely. A big LR mid-training acts as regularisation and trains fast ("super-convergence").
- **LR range test:** start with a tiny LR (1e-7), increase it exponentially every step, record the loss. Loss falls, then flattens, then explodes. Pick a max LR roughly an order of magnitude below the blow-up point (or where loss falls fastest).
- Set the scheduler step per *batch* for OneCycle, per epoch for many others; know the total steps in advance.

**Example:** (run) `OneCycleLR(max_lr=1.0, total_steps=10)` gives: `0.04, 0.52, 1.0, 0.95, 0.812, 0.611, 0.389, 0.188, 0.05, 0.0`. Cosine with `T_max=4` from 1.0: `1.0, 0.854, 0.5, 0.146, 0.0`.

**Code:** (run)
```python
import torch, torch.nn as nn
m = nn.Linear(2, 1); opt = torch.optim.SGD(m.parameters(), 0.1, momentum=0.9)
sch = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=1.0, total_steps=10)
lrs = []
for _ in range(10):
    opt.step(); lrs.append(round(opt.param_groups[0]["lr"], 3)); sch.step()
print(lrs)   # [0.04, 0.52, 1.0, 0.95, 0.812, 0.611, 0.389, 0.188, 0.05, 0.0]
# LR range test (sketch): for lr in np.geomspace(1e-7, 1, 100): set lr, train 1 batch, log loss; plot loss vs lr
```

**Follow-ups:**
- *Do you still need warmup with one-cycle?* It is built in.
- *Cosine vs step decay?* Cosine has no hyperparameters to pick milestones and usually matches or beats step decay.
- *Does it work with Adam?* Yes; common for transformers (warmup + cosine/linear decay).

**Common mistakes:** Stepping a per-batch scheduler once per epoch. Choosing the LR at the loss minimum of the range test (too high, it is right at the edge of divergence). Not knowing the total number of steps. Using a range test with a model in a different state (dropout, BN) from real training.

### Q48 ⭐ 🟡 A GenAI assistant suggests a huge architecture for a 5k-row tabular problem. How do you decide model size and sanity-check the suggestion?
**Asked at:** AI-era judgment questions, GCCs
**Say this first (1 line):** With 5k rows I would start from a simple, strong baseline (regularized linear model or small gradient-boosted trees), size any neural net by the data (a few thousand parameters, not millions), and let cross-validated results decide, not the assistant's confidence.

**Then explain:**
- **Parameters vs data:** a net with millions of weights on 5,000 rows memorizes noise. Rough guide: far fewer parameters than rows, or strong regularisation; 5k rows supports maybe one or two hidden layers of 16-64 units.
- **Sanity checks on the suggestion:**
  1. Count parameters (`sum(p.numel() for p in model.parameters())`) and compare with N.
  2. Run a baseline first (logistic/ridge, LightGBM). If the big net does not beat it under cross-validation with a margin larger than the seed noise, drop it.
  3. Overfit-one-batch test, then look at train vs validation gap.
  4. Learning curve: does more data help? If val is flat and the gap large, the model is too big.
  5. Repeat across several seeds and folds; check leakage.
- **Cost view:** training, serving, explainability and maintenance cost matter as much as a tiny metric gain.
- **If a net is justified:** small, with weight decay, dropout, early stopping, ensembles of several seeds. Or use pretrained/tabular foundation models, or fine-tune a pretrained model if the data is text/images.

**Example:** (hand-computed) A 3-hidden-layer MLP with 512 units on 50 features has about `50*512 + 512*512*2 + 512 ≈ 550k` parameters: 110 parameters per training row. A 2-layer MLP with 32 units has about `50*32 + 32*32 + 32 ≈ 2.7k`, still comparable to the row count, and a GBM with depth-4 trees is simpler again.

**Follow-ups:**
- *"But big models generalize well anyway"?* Double descent and large pretrained models need huge data or good priors; on 5k rows noise dominates.
- *How to verify the code itself?* Run it, read it, check shapes and data leakage; do not trust "should work".

**Common mistakes:** Accepting a big architecture because it sounds modern. Comparing against no baseline. Judging by one train/validation split. Ignoring the variance across seeds.

### Q49 ⭐ 🔴 Why might Adam generalize worse than SGD with momentum? Discuss sharp vs flat minima.
**Asked at:** Senior MLE, research-leaning teams
**Say this first (1 line):** Adam often reaches low training loss faster but, on some tasks (notably image classification with CNNs), converges to solutions that generalize slightly worse than SGD with momentum; a popular explanation is that SGD's noisier, less adaptive steps favour flatter minima.

**Then explain:**
- **Sharp vs flat minima:** a flat minimum has low loss in a wide neighbourhood, so small shifts between the train and test loss surfaces cost little; a sharp one rises quickly, so it generalizes worse (Hochreiter and Schmidhuber 1997; Keskar et al. 2017 on large batches).
- **Why SGD may find flatter ones:** gradient noise (scaled by lr/batch size) helps it escape sharp basins. Adam normalizes per-parameter step sizes, which reduces that noise-driven exploration and can bias towards sharper or different solutions. Wilson et al. 2017 showed cases where adaptive methods generalize worse.
- **Honest caveat:** the evidence is mixed. Sharpness depends on parametrization (a rescaled net can have different sharpness with the same function), and with tuning, proper decay (AdamW) and schedules the gap often vanishes. Transformers/LLMs are trained with AdamW because SGD works poorly there.
- **Practical mitigations:** use AdamW (decoupled decay), tune LR/schedule, longer training, SAM (sharpness-aware minimization), or switch to SGD for the final phase.

**Example:** ResNet on CIFAR/ImageNet: SGD+momentum with step or cosine decay is the classic best-practice recipe; Adam often trains faster early but can end slightly behind on such tasks unless tuned; the size of the gap varies by setup and is often closed with tuning (Wilson et al. 2017 report gaps in some settings), so treat it as a tendency, not a rule.

**Follow-ups:**
- *Does batch size relate?* Larger batch means less noise and a larger generalization gap (Q28); the same logic.
- *Which do you choose?* Adam/AdamW by default for speed and robustness; SGD+momentum for CNN vision if I can afford tuning.

**Common mistakes:** Stating "Adam always generalizes worse". Claiming flat minima always generalize (sharpness is not reparametrization-invariant). Comparing untuned Adam with tuned SGD (or vice versa).

### Q50 ⭐ 🔴 Explain bias correction in Adam and why the first steps would be off without it.
**Asked at:** Senior MLE loops
**Say this first (1 line):** Adam's moving averages start at zero, so early on they are biased towards zero; dividing by `1 - β^t` corrects that, so the first steps have the right size instead of being badly scaled.

**Then explain:**
- `m_t = β1 m_{t-1} + (1-β1) g_t`, `v_t = β2 v_{t-1} + (1-β2) g_t²`, with `m_0 = v_0 = 0`.
- With a constant gradient `g`, `m_t = (1 - β1^t) g`, so at `t=1` `m` is only `0.1 g` (it should be `g`). `v` is even more biased: `v_1 = 0.001 g²` with `β2 = 0.999`.
- Correction: `m̂ = m/(1-β1^t)`, `v̂ = v/(1-β2^t)`. These are unbiased estimates of the mean and uncentered second moment; the bias shrinks as `t` grows.
- Without it, the step `m / sqrt(v)` is wrong in the early steps. Since `v` is under-estimated more than `m`, the uncorrected ratio is too large, so the first steps would be too big (`~3.2x` the intended size at t=1 here).
- The effect lasts roughly `1/(1-β2)` ≈ 1000 steps for `v`, which is why warmup is often used with Adam too.

**Example:** (run) constant gradient `g = 1`, `β1=0.9`, `β2=0.999`:

| t | m | v | raw step m/√v | corrected step |
|---|---|---|---|---|
| 1 | 0.1 | 0.001 | 3.162 | 1.0 |
| 2 | 0.19 | 0.001999 | 4.25 | 1.0 |
| 3 | 0.271 | 0.002997 | 4.95 | 1.0 |

The corrected step equals 1 (as it should for a constant gradient), while the raw step is 3 to 5 times too large.

**Code:** (run)
```python
import numpy as np
g, b1, b2 = 1.0, 0.9, 0.999; m = v = 0
for t in range(1, 4):
    m = b1 * m + (1 - b1) * g; v = b2 * v + (1 - b2) * g * g
    print(t, round(m / np.sqrt(v), 3), round((m / (1 - b1 ** t)) / np.sqrt(v / (1 - b2 ** t)), 3))
# 1 3.162 1.0 / 2 4.25 1.0 / 3 4.95 1.0
```

**Follow-ups:**
- *Does it matter late in training?* No: `1 - β^t → 1`.
- *What about eps?* It is added to `sqrt(v̂)` for stability; tiny values can amplify noise when `v̂` is near zero.

**Common mistakes:** Saying bias correction is only about `m`. Saying the uncorrected step is too *small* (with `v` biased more than `m`, it is too large). Ignoring that this is why Adam without warmup can be unstable early.

### Q51 ⭐ 🔴 Implement a tiny autograd engine (micrograd-style) with add, multiply, tanh and a backward pass.
**Asked at:** OpenAI-style autograd rounds, senior MLE
**Say this first (1 line):** An autograd engine stores each value with its parents and a small function that knows how to pass gradients back; `backward()` sorts the graph topologically and runs those functions in reverse, accumulating (`+=`) into each node's gradient.

**Then explain:**
- Each node holds `data`, `grad`, its children (inputs), and a `_backward` closure.
- **add:** `d(a+b)/da = 1`, `d/db = 1`, so pass the output gradient to both.
- **multiply:** `d(a*b)/da = b`, `d/db = a`.
- **tanh:** `d tanh(x)/dx = 1 - tanh(x)²`.
- Use `+=` so a node used several times (e.g. `a*a`) gets the sum of contributions (multivariate chain rule).
- Topological order guarantees a node's gradient is complete before it is pushed to its inputs.

**Example:** (run) `y = tanh(x*w + b)` with `x=0.5, w=-1.0, b=0.3`: `y = -0.1974`; `dy/dx = -0.961`, `dy/dw = 0.4805`, `dy/db = 0.961`. A numeric derivative of `w` gives `0.4805`. For `a*a` with `a=3`, grad is `6.0`.

**Code:** (run)
```python
import math
class V:
    def __init__(s, d, ch=()): s.d = d; s.g = 0.0; s._ch = ch; s._bw = lambda: None
    def __add__(s, o):
        o = o if isinstance(o, V) else V(o); out = V(s.d + o.d, (s, o))
        def bw(): s.g += out.g; o.g += out.g
        out._bw = bw; return out
    def __mul__(s, o):
        o = o if isinstance(o, V) else V(o); out = V(s.d * o.d, (s, o))
        def bw(): s.g += o.d * out.g; o.g += s.d * out.g
        out._bw = bw; return out
    def tanh(s):
        t = math.tanh(s.d); out = V(t, (s,))
        def bw(): s.g += (1 - t * t) * out.g
        out._bw = bw; return out
    def backward(s):
        order, seen = [], set()
        def topo(v):
            if v not in seen:
                seen.add(v); [topo(c) for c in v._ch]; order.append(v)
        topo(s); s.g = 1.0
        for v in reversed(order): v._bw()
x, w, b = V(0.5), V(-1.0), V(0.3)
y = (x * w + b).tanh(); y.backward()
print(round(y.d, 4), round(x.g, 4), round(w.g, 4), round(b.g, 4))   # -0.1974 -0.961 0.4805 0.961
a = V(3.0); (a * a).backward(); print(a.g)                          # 6.0
```

**Follow-ups:**
- *Why `+=` and not `=`?* A node feeding several outputs must collect all gradients; `=` would drop contributions.
- *What to add for a real engine?* More ops (sub, pow, exp, relu), broadcasting and tensors, `zero_grad`; PyTorch does exactly this with tensors.
- *Complexity?* One backward pass is linear in the number of graph nodes.

**Common mistakes:** Using `=` instead of `+=`. Skipping the topological sort (wrong order for shared nodes). Forgetting to seed the output gradient with 1. Reusing a graph without zeroing gradients.

### Q52 ⭐ 🔴 Why does batch norm behave differently at inference (running statistics)? What breaks at small batch sizes and what are GroupNorm/RMSNorm alternatives?
**Asked at:** Senior MLE loops
**Say this first (1 line):** In training, batch norm normalizes with the current mini-batch's mean and variance; at inference there may be a single example, so it uses running averages of those statistics collected during training; with small batches the batch statistics are noisy, so GroupNorm, LayerNorm or RMSNorm (which do not depend on the batch) are used instead.

**Then explain:**
- **Training:** `y = γ (x - μ_B)/sqrt(σ²_B + ε) + β`, with `μ_B, σ²_B` from the batch; also updates `running_mean = (1-m)*running_mean + m*μ_B` (momentum `m=0.1` in PyTorch), same for variance.
- **Inference (`eval()`):** uses the stored running mean/var, so output for an example does not depend on other examples in the batch. This makes predictions deterministic.
- **Mismatch problem:** if running stats are off (tiny batches, different data distribution, forgot `eval()`), train and test behave differently.
- **Small batches:** statistics from 2-8 samples are noisy, hurting accuracy (and batch size 1 in training raises an error). Seen in detection/segmentation with big images, and in per-GPU batch splits.
- **Alternatives:**

| Norm | Normalizes over | Batch-dependent? | Typical use |
|---|---|---|---|
| BatchNorm | batch (and spatial) per channel | Yes | CNNs, large batch |
| LayerNorm | all features of one sample | No | Transformers, RNNs |
| GroupNorm | groups of channels per sample | No | Small-batch vision |
| RMSNorm | features of one sample, no mean subtraction: `x / sqrt(mean(x²) + ε) * γ` | No | LLMs (LLaMA); cheaper than LayerNorm |

**Example:** (run) Train a `BatchNorm1d` on inputs ~ N(5, 2²) for 50 batches: running mean 5.05, running var 4.25 (true 5 and 4). In eval, an input of 5.0 maps to about -0.02, i.e. roughly "average". With one training sample, PyTorch raises `ValueError: Expected more than 1 value per channel when training`.

**Code:** (run)
```python
import torch, torch.nn as nn
torch.manual_seed(0)
bn = nn.BatchNorm1d(1, momentum=0.1)
for _ in range(50): bn(torch.randn(32, 1) * 2 + 5)
print(bn.running_mean.item(), bn.running_var.item())   # 5.046 4.247
bn.eval(); print(bn(torch.tensor([[5.0]])).item())      # -0.0226
r = torch.randn(2, 6); rms = r / r.pow(2).mean(-1, keepdim=True).add(1e-6).sqrt()
print(rms.pow(2).mean(-1))                              # tensor([1.0000, 1.0000]): unit RMS
gn = nn.GroupNorm(2, 4)                                 # 2 groups over 4 channels, batch independent
```

**Follow-ups:**
- *Why does fine-tuning with tiny batches often freeze BN?* Keep running stats from pretraining, put BN in eval mode.
- *SyncBatchNorm?* Computes statistics across all GPUs to get a bigger effective batch.
- *Why RMSNorm?* Drops the mean-centering and bias, so it is a bit faster with similar quality.

**Common mistakes:** Forgetting `model.eval()` at inference (uses batch stats). Using BN with batch size 1-2. Saying BN uses "the whole dataset" statistics in training. Confusing which axes BN vs LayerNorm average over.

### Q53 ⭐ 🔴 How does gradient checkpointing trade compute for memory, and how do you estimate training memory for a model?
**Asked at:** Senior MLE, GenAI teams
**Say this first (1 line):** Gradient checkpointing does not store most intermediate activations during the forward pass; it recomputes them during backward from a few saved checkpoints, trading about one extra forward pass (commonly quoted as roughly 20-30% slower steps; it varies by model) for a large cut in activation memory.

**Then explain:**
- Normal training keeps every layer's activations for backward: memory grows linearly with depth, and with batch size and sequence length.
- With checkpointing, only the inputs of selected segments are stored. In backward, each segment's forward is re-run to regenerate its activations, then differentiated. Activation memory goes from `O(L)` to about `O(√L)` with evenly spaced checkpoints (the classic Chen et al. 2016 result), at roughly one extra forward pass.
- **Training memory estimate** = parameters + gradients + optimizer states + activations:
  - fp32 params: 4 bytes each; grads: 4 bytes; Adam states: 8 bytes (two fp32 moments). That is about **16 bytes per parameter**. Mixed precision with an fp32 master copy is similar (2 + 2 + 4 + 8 = 16), and it saves mainly on activations.
  - Activations depend on batch x sequence x hidden x layers; measure with `torch.cuda.max_memory_allocated()`.
- **Use when** activations dominate (long sequences, big batches, deep transformers); not helpful when the optimizer states dominate (use sharding/8-bit optimizers there).

**Example:** (hand-computed) A 1B-parameter model with fp32 Adam: `1e9 * 16 bytes = 16 GB` before activations. A 7B model would need about 112 GB, which is why people use sharding (FSDP/ZeRO), LoRA or lower precision.

**Code:** (run, small)
```python
import torch, torch.nn as nn
from torch.utils.checkpoint import checkpoint
blk = nn.Sequential(nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, 64))
x = torch.randn(8, 64, requires_grad=True)
out = checkpoint(blk, x, use_reentrant=False)   # activations inside blk not stored; recomputed in backward
out.sum().backward(); print(x.grad.shape)       # torch.Size([8, 64])
```

**Follow-ups:**
- *Any correctness catch?* Recomputed layers must be deterministic (dropout RNG state is preserved by PyTorch; BatchNorm stats can update twice).
- *Other ways to save memory?* Mixed precision, smaller batch plus accumulation, shorter sequences, offloading (Q40).
- *Speed cost?* Often around 20-30% slower per step (varies), but it lets you use a larger batch or model.

**Common mistakes:** Believing it reduces parameter or optimizer memory. Forgetting the recompute cost. Using it on tiny models where activations are not the bottleneck. Forgetting `use_reentrant` choice and getting silent no-grad issues with reentrant mode.

### Q54 ⭐ 🔴 What is double descent and how does overparameterization square with classical bias-variance thinking?
**Asked at:** Research-leaning loops, Europe tech
**Say this first (1 line):** Double descent is the observation that test error first follows the classic U-shape as model size grows, peaks near the interpolation threshold (where the model just barely fits the training data), and then falls again as the model gets even bigger; so heavily overparameterized models can generalize well.

**Then explain:**
- **Classic view:** more capacity means lower bias but higher variance, so there is a sweet spot; models that fit the training data perfectly should generalize badly.
- **What is seen in practice** (Belkin et al. 2019; Nakkiran et al. 2019 "Deep Double Descent"): as parameters (or training epochs, or data size) cross the point where the model can fit all training data, test error spikes, then decreases again in the "modern" regime.
- **Why the peak:** at the threshold there is essentially one way to interpolate the data, so the fit is forced to follow noise. With many more parameters there are many interpolating solutions, and gradient descent's implicit bias picks a simple/smooth one (minimum-norm-like).
- **Reconciling with bias-variance:** the classic argument assumed capacity grows only through variance; in overparameterized models implicit regularisation (SGD, early stopping, weight decay, architecture) keeps the effective complexity low. It extends bias-variance, it does not break it.
- **Practical takeaways:** do not stop growing the model just because training error hits zero; check validation; noisy labels make the peak larger; regularisation and early stopping can flatten it.

**Example:** Fitting a polynomial/random-features model on 100 points: test error is lowest at moderate degree, spikes at degree about 100 (equals the number of points), and drops again at degree much larger than 100 when using minimum-norm fit (typical illustrative picture, not a specific run).

**Follow-ups:**
- *Does it happen with epochs too?* Yes ("epoch-wise" double descent), especially with label noise.
- *Does this mean bigger is always better?* No: cost, data requirements and overfitting to noise still matter; it depends on regime and regularisation.

**Common mistakes:** Claiming bias-variance is "wrong". Ignoring that the effect depends on noise and optimisation. Stating that zero training error means overfitting automatically.

### Q55 ⭐ 🔴 What are knowledge distillation, pruning and quantization, and when would you use each for serving?
**Asked at:** MLE loops, Microsoft IDC-type teams
**Say this first (1 line):** All three make a model cheaper to serve: distillation trains a small student to mimic a big teacher, pruning removes unimportant weights, and quantization stores weights (and sometimes activations) in fewer bits; I pick based on whether I can retrain, what hardware I serve on, and how much accuracy I can lose.

**Then explain:**

| Technique | What it does | Gains | Needs | Watch out |
|---|---|---|---|---|
| **Distillation** | Student learns from teacher's soft probabilities (temperature-softened) plus labels | Smaller, faster architecture (e.g. DistilBERT ~40% smaller, ~60% faster, keeps about 97% of BERT's GLUE score, per its authors) | Retraining, access to teacher and data | Student capacity limits quality |
| **Pruning** | Zero out low-magnitude weights (unstructured) or whole channels/heads (structured) | Smaller model; real speedup mainly with structured pruning or sparse kernels | Usually fine-tune after pruning | Unstructured sparsity gives little speedup on ordinary GPUs |
| **Quantization** | fp32 to fp16/bf16/int8/int4 | 2-4x smaller, faster on supporting hardware, lower memory bandwidth | Post-training (PTQ) is cheap; quantization-aware training (QAT) is more accurate | Outlier activations; calibrate on representative data |

- **Distillation loss:** `L = α · KL(softmax(z_s/T) || softmax(z_t/T)) · T² + (1-α) · CE(z_s, y)`. Soft targets carry "dark knowledge" about class similarity.
- **How I choose:** need the biggest fast win with no retraining: quantize (int8, or 4-bit for LLMs). Need a fundamentally smaller/faster model and have data: distil. Need to shrink further on top: structured pruning. They combine (distil, then quantize).
- Always re-measure accuracy, latency and memory on the target hardware, not just parameter counts.

**Example:** (hand-computed) 1B parameters: fp32 = 4 GB, fp16 = 2 GB, int8 = 1 GB, int4 = 0.5 GB for weights alone.

**Follow-ups:**
- *PTQ vs QAT?* PTQ: calibrate on a small dataset, no training, may lose accuracy at low bits. QAT: simulates quantization during training, better at 4-bit or small models.
- *Why does unstructured pruning not speed up?* Dense hardware still multiplies zeros unless sparse kernels or structured patterns (e.g. 2:4 sparsity on newer NVIDIA GPUs) are used.
- *LLM serving?* Quantized weights (int8/int4) plus KV-cache and batching optimizations.

**Common mistakes:** Judging success by parameter count rather than latency. Pruning without fine-tuning. Quantizing without calibration data. Forgetting that distillation needs training compute.

### Q56 ⭐ 🔴 How do you handle variable-length sequences in PyTorch (padding, masking, pack_padded_sequence)?
**Asked at:** MLE loops, NLP-adjacent teams
**Say this first (1 line):** I pad every sequence in a batch to the same length, keep a mask (or the lengths) saying which positions are real, and make the model ignore padding, either with masks in attention/loss or by packing the batch for an RNN.

**Then explain:**
- **Padding:** `pad_sequence(seqs, batch_first=True)` pads with zeros (or a pad token ID) to the longest sequence in the batch. Do this in the `DataLoader`'s `collate_fn`.
- **Masking:** a boolean mask `arange(T) < lengths[:, None]`. Use it to (a) exclude pad positions from the **loss** (e.g. `ignore_index` in `CrossEntropyLoss`), (b) block pad tokens in **attention**, (c) take correct averages in pooling.
- **`pack_padded_sequence`:** for RNNs/LSTMs, it tells the RNN the real lengths, so it skips padded steps and the final hidden state is the one at the last real token, not after a run of pads. Wrap with `pad_packed_sequence` to get a padded output back.
- **Efficiency:** bucket by length (sort or group similar lengths) to cut wasted padding; cap max length.
- Transformers use the attention mask instead of packing; padding side matters for decoder-only LLMs (left-pad for batched generation).

**Example:** (run) 3 sequences of length 4, 2, 3 with 3 features pad to shape `(3, 4, 3)`; mask rows `[1,1,1,1]`, `[1,1,0,0]`, `[1,1,1,0]`. After packing through an LSTM, the output is `(3, 4, 5)` and the final hidden state `h` matches the output at each sequence's last real step.

**Code:** (run, seeded)
```python
import torch, torch.nn as nn
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence
torch.manual_seed(0)
seqs = [torch.randn(4, 3), torch.randn(2, 3), torch.randn(3, 3)]
lens = torch.tensor([len(s) for s in seqs])
pad = pad_sequence(seqs, batch_first=True)                     # (3, 4, 3)
mask = torch.arange(pad.size(1))[None, :] < lens[:, None]      # True where real
print(mask.int().tolist())          # [[1, 1, 1, 1], [1, 1, 0, 0], [1, 1, 1, 0]]
rnn = nn.LSTM(3, 5, batch_first=True)
pk = pack_padded_sequence(pad, lens, batch_first=True, enforce_sorted=False)
out, (h, c) = rnn(pk); out, _ = pad_packed_sequence(out, batch_first=True)
print(out.shape, h.shape)           # torch.Size([3, 4, 5]) torch.Size([1, 3, 5])
print(torch.allclose(out[1, 1], h[0, 1]))   # True: last real step of seq 2 == final hidden state
```

**Follow-ups:**
- *Why not just pad and ignore it?* A plain RNN would keep updating its state over pad steps and the last state would be polluted.
- *Padding value in loss?* Use `ignore_index=-100` for targets at pad positions.
- *Pad side for LLM generation?* Left-pad so the last token is real.

**Common mistakes:** Averaging over pad positions. Taking `out[:, -1]` as the final state of a padded batch. Passing lengths on GPU to `pack_padded_sequence` (it expects CPU lengths). Not masking pad tokens in attention.

### Q57 ⭐ 🔴 How does LSTM cell-state gradient flow work mathematically, and what is the role of the forget-gate bias initialization?
**Asked at:** Senior DL loops
**Say this first (1 line):** The LSTM cell state updates additively, `c_t = f_t ⊙ c_{t-1} + i_t ⊙ g_t`, so the gradient flowing back along `c` is multiplied only by the forget gate `f_t` at each step, not by a weight matrix and a squashing derivative; if `f ≈ 1`, gradients survive many steps, and that is why initializing the forget-gate bias to a positive value (about 1) helps.

**Then explain:**
- Equations: `f_t = σ(W_f[h_{t-1}, x_t] + b_f)`, `i_t`, `g_t = tanh(...)`, `c_t = f_t ⊙ c_{t-1} + i_t ⊙ g_t`, `h_t = o_t ⊙ tanh(c_t)`.
- **Direct path:** `∂c_t/∂c_{t-1} = f_t` (plus small terms through the gates' dependence on `h_{t-1}`). So along the cell-state highway,
  `∂c_T/∂c_t ≈ Π_{k=t+1..T} f_k`.
- In a vanilla RNN the same product is of `W^T diag(tanh')`, which shrinks or explodes exponentially; in an LSTM the factor is a learned gate in `(0,1)`, which the network can hold near 1 to remember.
- **Bias init:** `σ(0) = 0.5`, so with `b_f = 0` the cell forgets half of its memory every step at the start: `0.5^50 ≈ 9e-16`. With `b_f = 1`, `σ(1) ≈ 0.73` (and `0.73^50 ≈ 1.5e-7`, hand-computed, still small), but the gate starts leaning towards "remember" and can learn to open further. Jozefowicz et al. (2015) found a bias of 1 helps; larger values are used for very long memory. A gate near 0.99 gives `0.99^50 ≈ 0.61`.
- Gradients can still vanish if `f` is small, and can explode (hence clipping); the LSTM makes long memory *possible*, not guaranteed.

**Example:** (run) product of a constant forget gate over 50 steps: `0.5^50 = 8.9e-16`, `0.9^50 = 0.0052`, `0.99^50 = 0.605`. Only a gate near 1 passes a usable gradient across 50 steps.

**Code:** (run)
```python
import torch.nn as nn
T = 50
print(0.5 ** T, 0.9 ** T, 0.99 ** T)       # 8.88e-16  0.00515  0.605
lstm = nn.LSTM(8, 16)
for name, p in lstm.named_parameters():
    if "bias" in name:
        n = p.size(0) // 4                  # PyTorch gate order: input, forget, cell, output
        p.data[n:2 * n].fill_(1.0)          # forget-gate bias = 1 in both bias_ih and bias_hh (effective 2)
```

**Follow-ups:**
- *Note on PyTorch:* there are two biases (`bias_ih`, `bias_hh`); the effective forget bias is their sum, so setting both to 1 gives 2.
- *GRU?* Similar idea with an update gate interpolating between old state and candidate.
- *Does this solve exploding gradients?* No; still clip.

**Common mistakes:** Saying LSTM "eliminates" vanishing gradients. Forgetting the gate order when indexing biases. Ignoring that PyTorch has two bias vectors. Leaving `b_f = 0`.

### Q58 ⭐ 🔴 Explain autoencoders and VAEs at a basic level: what is the loss and what is the reparameterization trick?
**Asked at:** Research-leaning loops, Spotify/Zalando-type teams
**Say this first (1 line):** An autoencoder compresses the input to a small code and reconstructs it, trained with a reconstruction loss; a VAE makes the code a probability distribution, adds a KL term that keeps it close to a standard normal, and uses the reparameterization trick so gradients can flow through the random sampling.

**Then explain:**
- **Autoencoder:** encoder `x → z` (bottleneck), decoder `z → x̂`; loss = reconstruction error (MSE or BCE). Used for compression, denoising, anomaly detection (high reconstruction error). The latent space is not guaranteed to be smooth, so sampling from it gives junk.
- **VAE:** encoder outputs `μ(x)` and `log σ²(x)`, defining `q(z|x) = N(μ, σ²)`. Loss = **negative ELBO** = reconstruction loss + `KL(q(z|x) || N(0, I))`.
- **KL term (closed form for diagonal Gaussians):** `KL = -½ Σ_j (1 + log σ_j² - μ_j² - σ_j²)`. It regularizes the latent space so it is continuous and you can sample `z ~ N(0, I)` to generate data. A weight `β` on KL trades reconstruction against latent regularity (β-VAE).
- **Reparameterization trick:** sampling `z ~ N(μ, σ²)` is not differentiable w.r.t. `μ, σ`. Write `z = μ + σ ⊙ ε`, `ε ~ N(0, I)`, so the randomness is an external input and gradients flow to `μ` and `σ`.

**Example:** (run) With `μ = 0, log σ² = 0` the posterior equals the prior, so KL = 0 (printed `-0.0`, i.e. zero). With `μ = 2` in each of 3 dims, `dz/dμ = 1` flows through the sample: the gradient printed is `[1, 1, 1]`, showing the trick lets gradients reach `μ`.

**Code:** (run, seeded)
```python
import torch
mu = torch.zeros(2, 3); logvar = torch.zeros(2, 3)
z = mu + torch.exp(0.5 * logvar) * torch.randn_like(mu)                    # reparameterization
kl = -0.5 * torch.sum(1 + logvar - mu ** 2 - logvar.exp(), dim=1)
print(z.shape, kl.tolist())                                                # torch.Size([2, 3]) [-0.0, -0.0]
mu = torch.full((1, 3), 2.0, requires_grad=True); lv = torch.zeros(1, 3, requires_grad=True)
z = mu + (0.5 * lv).exp() * torch.randn(1, 3); z.sum().backward()
print(mu.grad.tolist(), lv.grad is not None)                               # [[1.0, 1.0, 1.0]] True
# total loss per batch: recon (e.g. F.mse_loss(x_hat, x, reduction="sum")) + kl.sum(), averaged over batch
```

**Follow-ups:**
- *Why not just an autoencoder for generation?* Its latent space has holes; the KL term fills them.
- *Posterior collapse?* The decoder ignores `z` and KL goes to 0; mitigate with KL annealing or a weaker decoder.
- *VAE vs GAN?* VAEs train stably and give a likelihood bound but tend to blur; GANs are sharper but unstable.

**Common mistakes:** Sampling `z` without the reparameterization (no gradient). Predicting `σ` directly instead of `log σ²` (positivity issues). Mismatched scales between reconstruction and KL terms (sum vs mean). Saying the KL term is the "regularizer for the decoder" (it regularizes the encoder's posterior).
