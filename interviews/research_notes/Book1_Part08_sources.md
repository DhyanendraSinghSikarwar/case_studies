# Book 1 Part 08 (Deep Learning) - sources

## Method and limits
WebSearch worked (US-only, standard mode), 6 queries. Results were mostly prep-bank/aggregator pages and Glassdoor snippets; I did not open pages with WebFetch, so evidence is from search-result summaries only. No first-hand 2025-26 reports found for Flipkart, Swiggy, PhonePe, Amazon India, Microsoft IDC, Booking, Klarna or Spotify DL rounds. Frequency counts below are therefore low-resolution; stars rely on topic ubiquity in prep banks plus expert judgment. No sources invented.

## URLs seen in search results (with what they supported)
| Source | Supports | Recency |
|---|---|---|
| https://www.techinterview.org/post/3233474404/ai-ml-interview-neural-network-training-backpropagation-gradient-descent-batch-normalization-dropout-regularization/ | backprop, BN, dropout, regularization topics | undated |
| https://www.tryexponent.com/blog/top-deep-learning-interview-questions | general DL question bank | undated |
| https://www.stratascratch.com/blog/a-guide-to-tackling-challenging-deep-learning-interview-questions | general DL question bank | undated |
| https://hackernoon.com/batch-normalization-vs-layer-normalization | BN vs LN | undated |
| https://prachub.com/interview-questions/explain-core-ml-concepts-4 | Snapchat MLE: BN vs LN, vanishing gradients (Feb 2026 per snippet) | Feb 2026 |
| https://www.1point3acres.com/interview/thread/1156166 | OpenAI phone screen: PyTorch autograd/backprop | 2025-26 (title only; login-gated) |
| https://www.1point3acres.com/interview/thread/1174369 | OpenAI onsite: backprop, PyTorch, autograd | 2025-26 (title only) |
| https://www.1point3acres.com/interview/thread/1172952 | OpenAI onsite ML prompt analysis | 2025-26 (title only) |
| https://dataford.io/questions/write-a-clean-pytorch-training-loop-from-scratch-including-zeroing-gradients-loss-calculation-backpropagation-and-optimizer-steps | training loop question | undated |
| https://dataford.io/questions/implement-a-custom-deep-learning-layer-in-pytorch-or-tensorflow-ensuring-correct-dimension-matching-and-backpropagation-capability | custom layer/Module | undated |
| https://www.glassdoor.fr/Entretien/TORC-Robotics-Entretien-E1027022-RVW95538571.htm | TORC Robotics Jan 2025: pen-and-paper NN/PyTorch training loop | Jan 2025 |
| https://www.glassdoor.com.ar/Entrevista/Walmart-Entrevista-E715-RVW30064805.htm (and sibling Walmart Glassdoor review URLs returned) | Walmart Bengaluru: dropout, regularization, vanishing gradients | mostly mid-2025 |
| https://www.interviewquery.com/interview-guides/zalando-machine-learning-engineer | Zalando MLE expects PyTorch/TensorFlow | 2025 guide |
| https://prepfully.com/interview-questions/zalando/machine-learning-engineer?page=3 | Zalando crowdsourced ML bank (general) | undated |
| https://www.interviewquery.com/interview-guides/spotify-machine-learning-engineer | Spotify MLE (recsys focus, little DL) | 2025 guide |
| https://www.interviewquery.com/interview-guides/klarna-data-scientist | Klarna DS (general ML) | 2025 guide |

## Frequency (approximate, from sightings)
- Vanishing gradients: 2 (Walmart, Snapchat) + banks. BN vs LN: 1 + several banks. Dropout/regularization: 1 + banks. PyTorch training loop / autograd: 3-4 (OpenAI x3, dataford, TORC). Others: bank-level only.

## AI-era changes noted
- Autograd/backprop-from-scratch and PyTorch hands-on rounds are rising (OpenAI reports); LLM-code-review of training scripts added (Q45-ish); Adam vs AdamW and norm-layer questions are driven by LLM-training context; model-size sanity check vs AI suggestions added.

## Question list with origin
Found = supported by sources/prep banks; gap-check = added by expert review.
| Q | Stars | Origin | Question |
|---|---|---|---|
| 1 | 3 | sources/prep-banks | Explain backpropagation in simple terms. How does the chain rule give gradients for each layer? |
| 2 | 3 | sources/prep-banks | Why do neural networks need non-linear activation functions? Compare sigmoid, tanh and ReLU. |
| 3 | 3 | sources/prep-banks | What is overfitting in a neural network and which regularization techniques do you know (L2, dropout, early stopping, augmentation)? |
| 4 | 3 | sources/prep-banks | How does dropout work, and what changes between training and inference (inverted dropout scaling)? |
| 5 | 3 | sources/prep-banks | Batch, mini-batch and stochastic gradient descent: differences, and what does momentum add? |
| 6 | 3 | sources/prep-banks | In PyTorch, why do you call optimizer.zero_grad()? What do model.train(), model.eval() and torch.no_grad() each do? |
| 7 | 3 | sources/prep-banks | What are vanishing and exploding gradients? Why do they happen and how do you fix them? |
| 8 | 3 | sources/prep-banks | Compare MSE, binary cross-entropy and categorical cross-entropy. Why is cross-entropy preferred for classification? |
| 9 | 3 | sources/prep-banks | Compare batch norm and layer norm: how each is computed, when each works, trade-offs. |
| 10 | 3 | sources/prep-banks | Explain how Adam works. Why is it the default and when would you prefer SGD with momentum? |
| 11 | 3 | sources/prep-banks | Write a clean PyTorch training loop from scratch (zero_grad, forward, loss, backward, step) with validation. |
| 12 | 3 | sources/prep-banks | How do you initialize weights? Explain Xavier/Glorot vs He initialization and why zero init fails. |
| 13 | 3 | sources/prep-banks | Your training loss is not decreasing. How do you debug it, step by step? |
| 14 | 3 | sources/prep-banks | How does learning rate affect training? Explain schedulers (step, cosine, warmup) and how you would choose one. |
| 15 | 3 | sources/prep-banks | What is the difference between Adam and AdamW? Why is decoupled weight decay better than L2 inside Adam? |
| 16 | 3 | sources/prep-banks | How do you read training vs validation loss curves to diagnose overfitting, underfitting or a bug? |
| 17 | 2 | sources/prep-banks | Why should you never initialize all weights to the same value (symmetry breaking)? |
| 18 | 2 | sources/prep-banks | How do you save and load PyTorch models (state_dict vs full model) and resume training? |
| 19 | 2 | sources/prep-banks | What is the softmax function and why is it computed with the log-sum-exp trick? Why feed logits to CrossEntropyLoss? |
| 20 | 2 | sources/prep-banks | Write a custom PyTorch Dataset and DataLoader for tabular or text data. What do num_workers, collate_fn and shuffle do? |
| 21 | 2 | sources/prep-banks | Write a custom nn.Module. What do __init__ vs forward do, and how are parameters registered? |
| 22 | 2 | sources/prep-banks | Explain CNNs: convolution, stride, padding, pooling, parameter sharing. Why do they suit images? |
| 23 | 2 | sources/prep-banks | Given an input shape and layer config, compute the output shape and parameter count of a conv layer. |
| 24 | 2 | sources/prep-banks | How do RNNs work and what is backpropagation through time? Why do they struggle with long sequences? |
| 25 | 2 | sources/prep-banks | Explain LSTM gates and how they mitigate vanishing gradients. How does GRU differ? |
| 26 | 2 | sources/prep-banks | What are residual (skip) connections and why do they let you train much deeper networks? |
| 27 | 2 | sources/prep-banks | What is gradient clipping, when do you need it, and norm vs value clipping? |
| 28 | 2 | sources/prep-banks | How does batch size affect convergence and generalization? What is the linear learning-rate scaling rule? |
| 29 | 2 | sources/prep-banks | How would you handle class imbalance in a neural network (weighted loss, focal loss, sampling)? |
| 30 | 2 | sources/prep-banks | What is early stopping and how do you implement it with checkpointing in PyTorch? |
| 31 | 2 | sources/prep-banks | Explain L2 regularization vs weight decay, and when they are equivalent. |
| 32 | 2 | sources/prep-banks | Sigmoid vs softmax output heads: binary, multi-class and multi-label setups and matching losses. |
| 33 | 2 | sources/prep-banks | What is the dead ReLU problem? Compare Leaky ReLU, ELU, GELU and Swish. |
| 34 | 2 | sources/prep-banks | Your loss becomes NaN or spikes mid-training. What are the likely causes and fixes? |
| 35 | 2 | sources/prep-banks | When would you use a neural net versus gradient-boosted trees for tabular data? |
| 36 | 2 | sources/prep-banks | How do embedding layers work for high-cardinality categorical features in tabular deep learning? |
| 37 | 2 | sources/prep-banks | How do you tune hyperparameters for a neural net (random vs grid vs Bayesian), and which matter most? |
| 38 | 2 | sources/prep-banks | How do you make PyTorch experiments reproducible (seeds, determinism, DataLoader workers)? |
| 39 | 2 | sources/prep-banks | Explain transfer learning and fine-tuning: which layers do you freeze and what learning rates do you use? |
| 40 | 2 | expert gap-check | Explain mixed precision training and common reasons for GPU out-of-memory errors; how do you reduce memory? |
| 41 | 2 | expert gap-check | Here is LLM-generated PyTorch training code. Find the bugs (missing zero_grad, eval mode, softmax before CE, data leakage, wrong device). |
| 42 | 2 | expert gap-check | What does universal approximation say, and why do we still use deep rather than wide networks? |
| 43 | 2 | sources/prep-banks | Implement a 2-layer MLP with forward and backward pass in NumPy (no frameworks). |
| 44 | 2 | sources/prep-banks | How does PyTorch autograd work? Explain the computational graph, requires_grad, detach and retain_graph. |
| 45 | 2 | expert gap-check | What is the difference between DataParallel and DistributedDataParallel, and when do you need multi-GPU training? |
| 46 | 2 | sources/prep-banks | Derive the gradient of softmax followed by cross-entropy with respect to the logits. |
| 47 | 1 | sources/prep-banks | What are one-cycle and cosine annealing schedules and how do you find a good learning rate (LR range test)? |
| 48 | 1 | expert gap-check | A GenAI assistant suggests a huge architecture for a 5k-row tabular problem. How do you decide model size and sanity-check the suggestion? |
| 49 | 1 | sources/prep-banks | Why might Adam generalize worse than SGD with momentum? Discuss sharp vs flat minima. |
| 50 | 1 | sources/prep-banks | Explain bias correction in Adam and why the first steps would be off without it. |
| 51 | 1 | sources/prep-banks | Implement a tiny autograd engine (micrograd-style) with add, multiply, tanh and a backward pass. |
| 52 | 1 | sources/prep-banks | Why does batch norm behave differently at inference (running statistics)? What breaks at small batch sizes and what are GroupNorm/RMSNorm alternatives? |
| 53 | 1 | sources/prep-banks | How does gradient checkpointing trade compute for memory, and how do you estimate training memory for a model? |
| 54 | 1 | sources/prep-banks | What is double descent and how does overparameterization square with classical bias-variance thinking? |
| 55 | 1 | expert gap-check | How do you calibrate a neural network's probabilities (temperature scaling) and why are NNs often overconfident? |
| 56 | 1 | expert gap-check | What are knowledge distillation, pruning and quantization, and when would you use each for serving? |
| 57 | 1 | expert gap-check | How do you handle variable-length sequences in PyTorch (padding, masking, pack_padded_sequence)? |
| 58 | 1 | expert gap-check | How does LSTM cell-state gradient flow work mathematically, and what is the role of the forget-gate bias initialization? |
| 59 | 1 | expert gap-check | Explain autoencoders and VAEs at a basic level: what is the loss and what is the reparameterization trick? |