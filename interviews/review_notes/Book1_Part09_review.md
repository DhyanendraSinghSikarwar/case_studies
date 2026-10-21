# Book 1 Part 09 review (NLP & CV, 52 Qs)

## Fixes
- Header: added star counts (14 / 21 / 17 = 52), status line; removed stale "star counts may be stale" remark.
- Q5: code was not standalone (xtr/ytr undefined). Added a synthetic toy dataset; comment claimed "early stopping at epoch 5" which did not reproduce, so now states it runs all 60 epochs (best val loss ~0.01).
- Q6: added missing Example (labelled illustrative numbers).
- Q9: stale reason fixed to "transformers not installed"; noted Trainer `processing_class` vs `tokenizer` arg naming.
- Q11: missing Example field added.
- Q21: muddled common-mistake wording fixed (output projection after concatenating heads).
- Q27: "recieve" subword split marked as illustrative.
- Q38: removed `\|` escapes from table and text (cosine/Euclidean formulas now use norm(u) notation, renders safely).
- Q39: optimizer-memory claim corrected to roughly 3x weights (gradients + Adam states).
- Q42: muddled "Dice vs IoU for averaging" bullet rewritten.
- Q43: muddled common mistake rewritten (flag noise with out-of-fold predictions).
- Q47: torch.ao.quantization DeprecationWarning noted in code comment and example (torchao not installed, so legacy API kept).

## Code blocks
40 python blocks extracted and run standalone. 37 ran as-is with printed numbers matching the text. Q5 failed (undefined data) -> fixed and rerun. Q24 failed once only when run in parallel (Windows asyncio handle error), passed alone with P .78/R .65/F1 .71, balanced .38/.93/.54, thr .70/.67/.68 as quoted. Q9 is the only not-executed block (transformers missing); Q28/Q50 mention HF/CLIP in comments, marked not executed.

## Unresolved / notes
- Q24 threshold is chosen on the training split (text says so, kept for brevity; could carve a validation split).
- Q47 uses deprecated torch.ao API; not verified against torchao (not installed).
- Numeric claims about typical model sizes/params (LeNet ~60k, VGG16 ~138M, GoogLeNet ~6.8M, CLIP 400M pairs) are from memory of well-known papers, not web-checked.
- Q6/Q40/Q34 example figures are illustrative; Q6 now labelled.
