# Book 1 - Part 08: Deep Learning (Question List)

- **Topic:** Neural net basics, backprop, activations, losses, optimizers (SGD/Adam/AdamW), initialization, norm layers, dropout, gradient problems, CNN/RNN/LSTM basics, training diagnostics, PyTorch from scratch
- **Target:** 50 questions | **Actual:** 59
- **Date:** 2026-10-20
- Scope: transformer-agnostic DL only; transformers/CV architectures in Part 9, LLM internals in Book 2.
- Status: questions only; answers pending (Wave B).

### Q1 ⭐⭐⭐ 🟢 Explain backpropagation in simple terms. How does the chain rule give gradients for each layer?
**Asked at:** Product cos, GCCs, MLE loops (OpenAI-style onsite reports)
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Why do neural networks need non-linear activation functions? Compare sigmoid, tanh and ReLU.
**Asked at:** Product cos, GCCs, fintech
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is overfitting in a neural network and which regularization techniques do you know (L2, dropout, early stopping, augmentation)?
**Asked at:** Walmart-type GCCs, product cos
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 How does dropout work, and what changes between training and inference (inverted dropout scaling)?
**Asked at:** Walmart Bengaluru (Glassdoor), product cos
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 Batch, mini-batch and stochastic gradient descent: differences, and what does momentum add?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 In PyTorch, why do you call optimizer.zero_grad()? What do model.train(), model.eval() and torch.no_grad() each do?
**Asked at:** MLE loops, product cos
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 What are vanishing and exploding gradients? Why do they happen and how do you fix them?
**Asked at:** Walmart Bangalore, Snapchat MLE, product cos
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Compare MSE, binary cross-entropy and categorical cross-entropy. Why is cross-entropy preferred for classification?
**Asked at:** Product cos, fintech, GCCs
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Compare batch norm and layer norm: how each is computed, when each works, trade-offs.
**Asked at:** Snapchat MLE (prep site, Feb 2026), product cos
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Explain how Adam works. Why is it the default and when would you prefer SGD with momentum?
**Asked at:** Product cos, MLE loops, Europe tech
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Write a clean PyTorch training loop from scratch (zero_grad, forward, loss, backward, step) with validation.
**Asked at:** MLE loops, OpenAI-style phone screens, Zalando (framework skills)
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 How do you initialize weights? Explain Xavier/Glorot vs He initialization and why zero init fails.
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Your training loss is not decreasing. How do you debug it, step by step?
**Asked at:** Product cos, MLE loops, Europe tech
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 How does learning rate affect training? Explain schedulers (step, cosine, warmup) and how you would choose one.
**Asked at:** Product cos, MLE loops
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 What is the difference between Adam and AdamW? Why is decoupled weight decay better than L2 inside Adam?
**Asked at:** Product cos, LLM-adjacent teams
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 How do you read training vs validation loss curves to diagnose overfitting, underfitting or a bug?
**Asked at:** Product cos, GCCs, Europe tech
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 Why should you never initialize all weights to the same value (symmetry breaking)?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 How do you save and load PyTorch models (state_dict vs full model) and resume training?
**Asked at:** MLE loops
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 What is the softmax function and why is it computed with the log-sum-exp trick? Why feed logits to CrossEntropyLoss?
**Asked at:** Product cos, MLE loops
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Write a custom PyTorch Dataset and DataLoader for tabular or text data. What do num_workers, collate_fn and shuffle do?
**Asked at:** MLE loops, Zalando, product cos
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Write a custom nn.Module. What do __init__ vs forward do, and how are parameters registered?
**Asked at:** MLE loops, TORC-style hands-on rounds
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Explain CNNs: convolution, stride, padding, pooling, parameter sharing. Why do they suit images?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Given an input shape and layer config, compute the output shape and parameter count of a conv layer.
**Asked at:** Pen-and-paper rounds (TORC Robotics), product cos
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How do RNNs work and what is backpropagation through time? Why do they struggle with long sequences?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Explain LSTM gates and how they mitigate vanishing gradients. How does GRU differ?
**Asked at:** Product cos, Amazon-type loops, GCCs
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 What are residual (skip) connections and why do they let you train much deeper networks?
**Asked at:** Product cos, MLE loops
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 What is gradient clipping, when do you need it, and norm vs value clipping?
**Asked at:** Product cos, MLE loops
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How does batch size affect convergence and generalization? What is the linear learning-rate scaling rule?
**Asked at:** Product cos, MLE loops
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How would you handle class imbalance in a neural network (weighted loss, focal loss, sampling)?
**Asked at:** Fintech (PhonePe/Klarna-type), product cos
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 What is early stopping and how do you implement it with checkpointing in PyTorch?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Explain L2 regularization vs weight decay, and when they are equivalent.
**Asked at:** Product cos, MLE loops
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Sigmoid vs softmax output heads: binary, multi-class and multi-label setups and matching losses.
**Asked at:** Product cos, fintech
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 What is the dead ReLU problem? Compare Leaky ReLU, ELU, GELU and Swish.
**Asked at:** Product cos, MLE loops
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 Your loss becomes NaN or spikes mid-training. What are the likely causes and fixes?
**Asked at:** MLE loops, product cos
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 When would you use a neural net versus gradient-boosted trees for tabular data?
**Asked at:** Product cos, fintech, Europe tech
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How do embedding layers work for high-cardinality categorical features in tabular deep learning?
**Asked at:** Flipkart/Swiggy-type recsys-adjacent teams, Zalando
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 How do you tune hyperparameters for a neural net (random vs grid vs Bayesian), and which matter most?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 How do you make PyTorch experiments reproducible (seeds, determinism, DataLoader workers)?
**Asked at:** MLE loops, Europe tech
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 Explain transfer learning and fine-tuning: which layers do you freeze and what learning rates do you use?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 Explain mixed precision training and common reasons for GPU out-of-memory errors; how do you reduce memory?
**Asked at:** MLE loops, product cos
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 Here is LLM-generated PyTorch training code. Find the bugs (missing zero_grad, eval mode, softmax before CE, data leakage, wrong device).
**Asked at:** AI-era code-review rounds, product cos
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 What does universal approximation say, and why do we still use deep rather than wide networks?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🔴 Implement a 2-layer MLP with forward and backward pass in NumPy (no frameworks).
**Asked at:** Product cos, GCCs, from-scratch rounds
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🔴 How does PyTorch autograd work? Explain the computational graph, requires_grad, detach and retain_graph.
**Asked at:** OpenAI-style autograd rounds, MLE loops
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🔴 What is the difference between DataParallel and DistributedDataParallel, and when do you need multi-GPU training?
**Asked at:** MLE loops, product cos
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🔴 Derive the gradient of softmax followed by cross-entropy with respect to the logits.
**Asked at:** Product cos, from-scratch rounds
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟡 What are one-cycle and cosine annealing schedules and how do you find a good learning rate (LR range test)?
**Asked at:** Senior MLE loops
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 A GenAI assistant suggests a huge architecture for a 5k-row tabular problem. How do you decide model size and sanity-check the suggestion?
**Asked at:** AI-era judgment questions, GCCs
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 Why might Adam generalize worse than SGD with momentum? Discuss sharp vs flat minima.
**Asked at:** Senior MLE, research-leaning teams
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 Explain bias correction in Adam and why the first steps would be off without it.
**Asked at:** Senior MLE loops
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 Implement a tiny autograd engine (micrograd-style) with add, multiply, tanh and a backward pass.
**Asked at:** OpenAI-style autograd rounds, senior MLE
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 Why does batch norm behave differently at inference (running statistics)? What breaks at small batch sizes and what are GroupNorm/RMSNorm alternatives?
**Asked at:** Senior MLE loops
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 How does gradient checkpointing trade compute for memory, and how do you estimate training memory for a model?
**Asked at:** Senior MLE, GenAI teams
<!-- ANSWER_PENDING -->

### Q54 ⭐ 🔴 What is double descent and how does overparameterization square with classical bias-variance thinking?
**Asked at:** Research-leaning loops, Europe tech
<!-- ANSWER_PENDING -->

### Q55 ⭐ 🔴 How do you calibrate a neural network's probabilities (temperature scaling) and why are NNs often overconfident?
**Asked at:** Fintech, senior DS loops
<!-- ANSWER_PENDING -->

### Q56 ⭐ 🔴 What are knowledge distillation, pruning and quantization, and when would you use each for serving?
**Asked at:** MLE loops, Microsoft IDC-type teams
<!-- ANSWER_PENDING -->

### Q57 ⭐ 🔴 How do you handle variable-length sequences in PyTorch (padding, masking, pack_padded_sequence)?
**Asked at:** MLE loops, NLP-adjacent teams
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🔴 How does LSTM cell-state gradient flow work mathematically, and what is the role of the forget-gate bias initialization?
**Asked at:** Senior DL loops
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🔴 Explain autoencoders and VAEs at a basic level: what is the loss and what is the reparameterization trick?
**Asked at:** Research-leaning loops, Spotify/Zalando-type teams
<!-- ANSWER_PENDING -->
