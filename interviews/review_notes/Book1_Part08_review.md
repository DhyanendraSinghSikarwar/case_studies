# Book 1 Part 08 review (Deep learning, Q1-Q58)

Reviewer pass: all 58 questions read; no ANSWER_PENDING; file kept CRLF.

## Fixes
- Header: added star counts (3-star 16, 2-star 30, 1-star 12); removed stale "star counts may be stale" remark.
- Q11, Q18, Q20, Q21, Q27, Q41: added the missing **Example** field (numbers taken from the executed code).
- Q5: example labelled qualitative (not a run). Q15 already labelled contrived.
- Q23: MACs line made exact (`C_out*C_in*K^2*H_out*W_out`).
- Q26: removed unsupported "beyond ~20 layers" wording.
- Q29: code comment said 1.268; actual run prints 1.9674 (random logits). Fixed.
- Q35: Grinsztajn title corrected to published "...on typical tabular data?" (web-verified: NeurIPS 2022, 45 datasets, ~10k samples).
- Q39: common-mistakes tightened (frozen BatchNorm vs model.train(), param groups after unfreezing; removed the muddled optimizer remark).
- Q41: bug list tightened (4: device + NumPy not tensors; 5: explicit model.train() explained); buggy snippet marked not executed (intentionally buggy); fixed code made standalone with synthetic data and run: val acc 0.825 (text previously claimed 0.96, wrong).
- Q45: label clarified as sketch with placeholders (DDP not executed, needs GPUs).
- Q46: example numbers wrong ([0.097, 0.0544, -0.6801, 0.5287]); actual run gives [0.226, 0.1746, -0.6219, 0.2213]. Fixed in text and code comment.
- Q47: OneCycle default end LR was misstated (max_lr/1e4); correct is start max_lr/25, end = start/1e4.
- Q49: removed unsourced "0.5-2 points behind" for Adam vs SGD; softened to a tendency citing Wilson et al. 2017.
- Q53: "20-35% more compute" softened to "commonly ~20-30%, varies"; memory estimate for mixed precision corrected (2+2+4+8 = 16 bytes/param).

## Citations
- Verified by web search: Grinsztajn et al. 2022 (title, 45 datasets, ~10k samples); DistilBERT (40% smaller, 60% faster, 97%).
- Not re-searched, from memory and standard: Goyal 2017 (linear scaling, batch 8k, 1 hour), Jozefowicz 2015 (forget bias 1), Bergstra-Bengio 2012, Chen 2016 (sqrt memory), Wilson 2017, Telgarsky 2016, Cybenko/Hornik.

## Code
- 41 python blocks extracted; 39 executed standalone and matched quoted numbers after the fixes above (Q1,4,6,9,11,12,14,15,17,18,19,20,21,23,26,27,29,30,31,32,33,34,36,37,38,39,43,44,46,47,50,51,52,53,56,57,58, plus Q41 fixed). Q40 CPU bf16 part ran; Q40 GradScaler loop and Q45 DDP not executed (no GPU/multi-process), labels kept.
- Failures found and fixed: Q29 (printed value), Q46 (numbers), Q41 (not standalone, wrong accuracy).
- Q41 buggy snippet is intentionally not runnable. Q9 prints near-zero means (~1e-8), consistent with "~0".
- Q12 output matches quoted comments. Q30 writes best.pt in cwd (stop at 31, best 0.3816 confirmed).

## Unresolved
- Q42 parity "2^n units shallow" is a textbook statement not verified here.
- Citations listed above as not re-searched remain from memory.
