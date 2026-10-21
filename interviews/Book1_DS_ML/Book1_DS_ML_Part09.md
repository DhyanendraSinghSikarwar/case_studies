# Book 1 — Part 09: NLP & Computer Vision (classical → transformers)

**Topic:** TF-IDF/BoW, embeddings, text classification, NER, BERT & fine-tuning basics, attention/transformers, NLP metrics; CNNs, transfer learning, augmentation, detection/segmentation metrics, ViT; light GenAI-in-classical-loop layer.
**Target:** 45  |  **Actual:** 52 (⭐⭐⭐ 14, ⭐⭐ 21, ⭐ 17)  |  **Date:** 2026-10-20  |  **Status:** Answers written and reviewed (Wave C)

Scope note: deep LLM/RAG/agents live in Book 2; classification metrics in Part 3; DL basics (backprop/optimizers) in Part 8.

---

> Dedupe pass: removed 1 cross-part duplicate(s); renumbered Q1–Q52.
---

### Q1 ⭐⭐⭐ 🟢 How does TF-IDF work, and what are its limitations compared with embeddings?
**Asked at:** all types
**Say this first (1 line):** TF-IDF scores a word high if it is frequent in this document but rare across the corpus; it is a fast, strong sparse baseline, but it only matches exact words and has no idea about meaning.

**Then explain:**
- **TF** = how often the term appears in the document. **IDF** = `log(N / df)`, where `df` is the number of documents containing the term. Rare words get a big weight, words like "the" get about zero.
- **TF-IDF = TF x IDF**, then each document vector is L2-normalised so cosine similarity is just a dot product. sklearn uses the smooth form `idf = ln((1+N)/(1+df)) + 1`.
- Output is a sparse, high-dimensional vector (one column per vocabulary word). Great for linear models, search (BM25 is its cousin) and keyword features.
- **Limitations vs embeddings:** (1) no semantics: "cheap" and "inexpensive" are unrelated columns; (2) no word order or context ("bank" the river and "bank" the lender are the same column); (3) vocabulary is fixed, so unseen words are dropped; (4) very high dimension; (5) needs retraining when the corpus changes because IDF depends on it.
- **Where TF-IDF still wins:** small data, exact keywords, IDs and product codes, explainability, microsecond latency, no GPU.

**Example:** 3 short documents about a bank loan. "bank" appears in all 3, so idf = 1.0 (lowest). "loan" appears in 2, idf = 1.29. "river" appears in 1, idf = 1.69. So "river" is the most distinguishing word.

**Code:**
```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
docs = ["the bank approved the loan", "the river bank was flooded",
        "loan approved by the bank manager"]
v = TfidfVectorizer()
X = v.fit_transform(docs)
print({w: round(float(i), 2) for w, i in zip(v.get_feature_names_out(), v.idf_)})
# {'approved': 1.29, 'bank': 1.0, 'by': 1.69, 'flooded': 1.69, 'loan': 1.29, 'manager': 1.69, 'river': 1.69, 'the': 1.0, 'was': 1.69}
print(np.round(cosine_similarity(X), 2))
# [[1.   0.32 0.66]   doc1 is close to doc3 (loan), far from doc2 (river)
#  [0.32 1.   0.18]
#  [0.66 0.18 1.  ]]
```

**Follow-ups:**
- *Why log in IDF?* It dampens the effect: a word in 1 of 1M docs should not be a million times more important than one in 1 of 10.
- *TF-IDF vs BM25?* BM25 adds term-frequency saturation and length normalisation; it is the default for keyword retrieval.
- *Why not just use embeddings?* Often best is hybrid: BM25/TF-IDF for exact matches plus dense embeddings for meaning.

**Common mistakes:** fitting the vectorizer on train+test (leakage of IDF); forgetting that TF-IDF on very short texts is noisy; saying TF-IDF "captures context"; forgetting sublinear_tf for long documents.

### Q2 ⭐⭐⭐ 🟢 Bag-of-Words vs TF-IDF vs word embeddings: when would you use each?
**Asked at:** all types
**Say this first (1 line):** BoW counts words, TF-IDF reweights the counts so rare informative words matter more, and embeddings give each word a dense vector where similar meanings sit close together.

**Then explain:**

| | BoW | TF-IDF | Word embeddings |
|---|---|---|---|
| Vector | sparse counts | sparse weighted | dense (100-1000 dims) |
| Meaning/synonyms | no | no | yes |
| Word order | no (unless n-grams) | no | not in static ones; yes in contextual models |
| Needs pretraining | no | no | yes (or train your own) |
| Interpretable | very | very | hard |
| Best for | tiny data, quick baseline | default for linear text classifiers, keyword search | semantic similarity, low-data transfer, deep models |

- Start with TF-IDF + logistic regression: it is a strong baseline in minutes. Move to embeddings when the vocabulary mismatch is the problem (paraphrases, short texts, multiple languages).
- Averaging static word vectors gives a cheap document vector but loses order and negation ("not good" ~ "good"). Prefer sentence embeddings or a fine-tuned transformer.

**Example:** Classifying support tickets with 2k labelled rows and domain jargon: TF-IDF + LR gets you 85% in an hour. Searching "refund not received" against "money not credited yet": TF-IDF shares no words, embeddings match them.

**Follow-ups:**
- *Why n-grams?* Bigrams recover some local order ("not good") at the cost of a much bigger vocabulary.
- *Hashing trick?* Hash words to a fixed number of columns: no vocabulary to store, but collisions and no reverse lookup.

**Common mistakes:** jumping to BERT without a TF-IDF baseline; averaging word vectors and expecting it to handle negation; using GloVe on text full of domain jargon it never saw.

### Q3 ⭐⭐⭐ 🟢 Word2Vec vs GloVe vs FastText: how do they differ, and how are they trained?
**Asked at:** all types
**Say this first (1 line):** All three learn dense word vectors from co-occurrence; Word2Vec uses a local prediction task, GloVe factorises global co-occurrence counts, and FastText adds character n-grams so it can handle unseen words.

**Then explain:**
- **Word2Vec (Google, 2013):** a shallow network trained to predict words from context. *Skip-gram* predicts context words from the centre word (better for rare words); *CBOW* predicts the centre from the averaged context (faster). Training uses **negative sampling** (push real pairs up, a few random pairs down) or hierarchical softmax, since a full softmax over the vocabulary is too slow.
- **GloVe (Stanford, 2014):** first builds the global word-word co-occurrence matrix, then fits vectors so that `w_i . w_j + b_i + b_j ~ log(X_ij)`, with a weighting function to cap very frequent pairs. Uses corpus-wide statistics directly.
- **FastText (Facebook, 2016):** a word is the sum of its character n-gram vectors (e.g. 3-6 grams of `<where>`). So rare words, typos and morphologically rich languages (Hindi, Turkish, German) get a sensible vector, and unseen words are still embeddable.
- All three are **static**: one vector per word regardless of context.

**Example:** "teh" (typo) or "unbelievably": Word2Vec and GloVe have no vector if unseen; FastText builds one from pieces like `<un`, `bel`, `ably>`.

**Follow-ups:**
- *Famous king - man + woman ~ queen?* It works because vector offsets capture some relations; it is an approximate, cherry-picked demo, not a guarantee.
- *Which would you pick today?* For a new project, a pretrained sentence-transformer or fine-tuned BERT; FastText still shines for fast, tiny, CPU-only classifiers.
- *Window size effect?* Small windows give syntactic similarity; large windows give topical similarity.

**Common mistakes:** saying Word2Vec is "deep"; confusing skip-gram (centre predicts context) with CBOW; claiming GloVe is not trained (it is, by weighted least squares); forgetting negative sampling is why training is fast.

### Q4 ⭐⭐⭐ 🟢 What is IoU, and how is it used in object detection?
**Asked at:** all types
**Say this first (1 line):** IoU (Intersection over Union) is the overlap area of two boxes divided by the area of their union; it runs from 0 (no overlap) to 1 (identical) and is how detectors judge whether a box is "correct".

**Then explain:**
- `IoU = area(A ∩ B) / area(A ∪ B) = inter / (areaA + areaB - inter)`.
- **Evaluation:** a predicted box is a true positive if IoU with a ground-truth box is above a threshold (0.5 in Pascal VOC; COCO averages over 0.50 to 0.95) and the class matches. Each ground-truth box can be matched only once; extra boxes on the same object are false positives.
- **Training:** used to assign anchors/proposals as positive or negative (e.g. IoU > 0.5 positive, < 0.4 negative) and in IoU-based losses (GIoU, DIoU, CIoU) that give gradient even when boxes do not overlap.
- **Inference:** Non-Max Suppression drops a lower-score box if its IoU with a higher-score box of the same class exceeds a threshold (say 0.5).
- Weakness: plain IoU is 0 for all non-overlapping boxes, so it gives no signal on "how far" - that is why GIoU/DIoU exist.

**Example:** Box A = (0,0,10,10), B = (5,5,15,15). Intersection = 5x5 = 25, union = 100 + 100 - 25 = 175, IoU = 0.143.

**Code:**
```python
def iou(a, b):  # boxes as (x1, y1, x2, y2)
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    union = (a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - inter
    return inter / union if union > 0 else 0.0
print(iou((0,0,10,10), (5,5,15,15)), iou((0,0,10,10), (20,20,30,30)), iou((0,0,10,10), (0,0,10,10)))
# 0.14285714285714285 0.0 1.0
```

**Follow-ups:**
- *Why not use plain accuracy for boxes?* There is no discrete answer; you need a continuous overlap measure plus a threshold.
- *What threshold would you use?* 0.5 is lenient; for tasks needing precise localisation (medical, robotics) use stricter, e.g. 0.75 or COCO-style averaging.
- *IoU for segmentation?* Same idea on pixel masks (Jaccard index).

**Common mistakes:** forgetting `max(0, ...)` for the non-overlapping case; mixing (x, y, w, h) and (x1, y1, x2, y2) formats; confusing IoU with Dice.

### Q5 ⭐⭐⭐ 🟢 How do you handle overfitting when training a CNN on a small image dataset (augmentation, regularization, early stopping)?
**Asked at:** all types
**Say this first (1 line):** With little data the best fixes, in order, are: use a pretrained network (transfer learning), augment the data, add regularization (weight decay, dropout, smaller head), and early-stop on a validation set.

**Then explain:**
- **Transfer learning first:** start from ImageNet/CLIP weights, train only the head or the top blocks (see Q10). This usually beats everything else on small data.
- **Augmentation:** random crop, flip, colour jitter, rotation, mixup/cutmix, RandAugment. It creates label-preserving variety. Only use transforms that keep the label valid (see Q17).
- **Regularization:** weight decay (L2, in AdamW), dropout before the classifier, batch norm, label smoothing, smaller or shallower model, global average pooling instead of huge dense layers.
- **Early stopping:** watch validation loss, stop when it has not improved for `patience` epochs, restore the best weights.
- **Data side:** get more labels where the model is wrong (active learning), clean noisy labels, use k-fold CV because one small validation split is noisy.
- **Diagnose with curves:** train loss falling, val loss rising = overfitting. Both high = underfitting, so do not regularize more.

**Example:** 800 chest X-rays, 2 classes. Fine-tune an ImageNet ResNet-18: freeze the backbone for 3 epochs, then unfreeze the top block with a 10x smaller learning rate, add crop/rotation/brightness augmentation, AdamW with 1e-2 weight decay, patience 5. Typically far better than training from scratch.

**Code:**
```python
# ran on a synthetic toy set (torch CPU); this easy toy never plateaus, so it runs all 60 epochs (best val loss ~0.01). Shows the mechanics, not a benchmark.
import torch, torch.nn as nn
torch.manual_seed(0)
def make(n):                        # toy task: class 1 has a bright blob in the top half
    x = 0.3 * torch.randn(n, 1, 16, 16); y = torch.randint(0, 2, (n,))
    x[y == 1, :, 2:7, 4:12] += 1.0
    return x, y
(xtr, ytr), (xva, yva) = make(64), make(200)
def augment(x):                     # random crop via reflect pad + noise; NO flip if left/right defines the label
    x = nn.functional.pad(x, (2, 2, 2, 2), mode="reflect")
    i, j = torch.randint(0, 5, (2,)).tolist()
    return x[:, :, i:i+16, j:j+16] + 0.1 * torch.randn(x.shape[0], 1, 16, 16)
net = nn.Sequential(nn.Conv2d(1, 8, 3, padding=1), nn.BatchNorm2d(8), nn.ReLU(), nn.MaxPool2d(2),
                    nn.Conv2d(8, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU(), nn.AdaptiveAvgPool2d(1),
                    nn.Flatten(), nn.Dropout(0.3), nn.Linear(16, 2))
opt = torch.optim.AdamW(net.parameters(), 1e-2, weight_decay=1e-2)
best, bad, patience, best_state = 1e9, 0, 5, None
for ep in range(60):
    net.train(); opt.zero_grad()
    nn.functional.cross_entropy(net(augment(xtr)), ytr).backward(); opt.step()
    net.eval()
    with torch.no_grad(): vl = nn.functional.cross_entropy(net(xva), yva).item()
    if vl < best - 1e-4: best, bad, best_state = vl, 0, {k: v.clone() for k, v in net.state_dict().items()}
    else:
        bad += 1
        if bad >= patience: break
net.load_state_dict(best_state)       # restore the best epoch
```

**Follow-ups:**
- *Validation set is tiny, how do you trust it?* Use stratified k-fold, report mean and spread, keep a locked test set.
- *Augmentation vs more data?* Augmentation helps but cannot invent new real-world variation; collecting even 20% more real data often helps more.
- *When does early stopping fail?* If the val set leaks or is too small, it stops at a noisy point.

**Common mistakes:** augmenting the validation/test set; flipping digits or text-in-image; adding dropout when the model is actually underfitting; tuning on the test set; training from scratch when a pretrained model exists.

### Q6 ⭐⭐⭐ 🟡 How do you build a text classifier end to end (TF-IDF + logistic regression baseline up to a fine-tuned transformer)? How do you choose between them?
**Asked at:** all types
**Say this first (1 line):** Start with a TF-IDF + logistic regression baseline, then move to embeddings or a fine-tuned transformer only if the extra accuracy justifies the cost, latency and maintenance.

**Then explain (framework):**
1. **Problem and metric:** classes, label quality, class balance, what error costs more. Pick the metric (macro-F1, PR-AUC) before modelling.
2. **Data:** clean, dedupe, split **before** any fitting; split by user/time/thread to avoid leakage; stratify.
3. **Baseline:** TF-IDF (word 1-2-grams, maybe char n-grams) + logistic regression/linear SVM. Minutes to train, interpretable (top coefficients), strong on topic-like tasks.
4. **Middle step:** sentence embeddings (sentence-transformers) + LR. Often a big jump with no fine-tuning and little data.
5. **Fine-tune a transformer** (DistilBERT/BERT/DeBERTa, multilingual if needed): needs a GPU and a few thousand labels; best for nuance, negation, sarcasm, context.
6. **Evaluate:** same held-out set for all; per-class metrics, confusion matrix, error analysis on 50-100 mistakes, calibration.
7. **Deploy and monitor:** latency/cost, drift, periodic relabelling (see Q31).

**How to choose:**

| Factor | TF-IDF + LR | Fine-tuned transformer |
|---|---|---|
| Labels | hundreds+ | thousands+ |
| Latency/CPU | sub-ms, CPU | 10-100 ms, usually GPU or distilled |
| Gain | topic/keyword tasks | context-heavy tasks (sentiment, intent, NLI) |
| Explainability | easy | harder |

Rule: only pay for the transformer if it beats the baseline by a margin that matters to the business on the same test set.

**Example (illustrative numbers):** Routing 5k labelled support tickets into 6 queues. TF-IDF + LR trains in seconds and gives macro-F1 around 0.80. Sentence embeddings + LR lift it to about 0.84. A fine-tuned DistilBERT reaches about 0.86 but needs a GPU and about 20x the inference cost. If the 2 extra points do not change how many tickets get misrouted in a way the business cares about, ship the embeddings + LR model.

**Code:**
```python
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
pos = ["great product works well", "love it fast delivery", "excellent quality highly recommend", "very happy with purchase",
       "amazing value works perfectly", "superb build and quality", "good value will buy again", "fantastic support quick refund"]
neg = ["terrible product broke quickly", "hate it slow delivery", "poor quality do not recommend", "very unhappy with purchase",
       "awful value stopped working", "bad build and quality", "waste of money never again", "horrible support no refund"]
X, y = pos + neg, [1]*8 + [0]*8
pipe = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True),
                     LogisticRegression(C=1.0, max_iter=1000, class_weight="balanced"))
pipe.fit(X, y)                                   # in real work: fit on train only, evaluate on a held-out set
print(pipe.predict(["quality is awful", "works great love it"]))   # [0 1]
```
(This is a 16-row toy to show the pipeline shape, not a benchmark.)

**Follow-ups:**
- *Baseline is 88% F1, BERT is 90%: ship BERT?* Depends: is a 2-point gain worth 50x compute and a GPU? Check the gain on the minority class and the business cost of errors.
- *Few labels?* Zero/few-shot LLM, SetFit, or weak labelling (Q29).
- *Production concerns?* Version the vectorizer with the model; monitor input drift.

**Common mistakes:** no baseline; fitting TF-IDF on all data before the split; reporting accuracy on imbalanced classes; not checking duplicates across train/test; skipping error analysis.

### Q7 ⭐⭐⭐ 🟡 What is the difference between static (Word2Vec) and contextual (BERT) embeddings?
**Asked at:** all types
**Say this first (1 line):** A static embedding gives every word one fixed vector; a contextual embedding computes a different vector for the same word depending on the sentence around it.

**Then explain:**
- **Static (Word2Vec, GloVe, FastText):** a lookup table, `word -> vector`. "bank" has one vector that mixes river-bank and money-bank senses. Cheap, tiny, fast.
- **Contextual (ELMo, BERT, GPT):** the vector is the output of a deep network that reads the whole sentence, so "bank" in "river bank" and "bank loan" get different vectors. Handles polysemy, word order and negation.
- **Cost:** BERT-base is about 110M parameters and needs a forward pass per sentence; Word2Vec is a table lookup.
- **How to use:** static vectors as features (average them) in a quick model; contextual models are fine-tuned end to end, or their `[CLS]`/mean-pooled output is used as a sentence embedding.
- Subword tokenization (WordPiece/BPE) in BERT also removes the out-of-vocabulary problem.

**Example:** "I deposited cash at the bank" vs "we sat on the river bank". Cosine similarity of the two "bank" vectors is 1.0 in Word2Vec by construction, and clearly lower in BERT.

**Follow-ups:**
- *Is BERT's raw token output a good sentence embedding?* Not by default; plain mean-pooled BERT is mediocre for similarity. Sentence-BERT-style contrastive fine-tuning fixes that.
- *When would you still use static?* CPU-only, millisecond latency, tiny data, or as lightweight features.

**Common mistakes:** thinking BERT "has" a vector per word like a dictionary; using `[CLS]` of an un-fine-tuned BERT for semantic search; forgetting that contextual vectors depend on the whole input, so you cannot cache them per word.

### Q8 ⭐⭐⭐ 🟡 Explain self-attention and the transformer architecture. Why did transformers replace RNNs/LSTMs?
**Asked at:** all types
**Say this first (1 line):** Self-attention lets every token look at every other token in one step and take a weighted mix of them, which captures context and trains in parallel; that is why transformers replaced RNNs.

**Then explain:**
- Each token vector is projected into a **query (Q)**, **key (K)** and **value (V)**. Score = `Q K^T / sqrt(d_k)`, softmax turns scores into weights, output = weights x V. Formula: `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V`. The `sqrt(d_k)` keeps dot products from growing with dimension and saturating the softmax.
- **Transformer block:** multi-head self-attention -> add & LayerNorm (residual) -> position-wise feed-forward -> add & LayerNorm. Stack N blocks. Positional encodings are added because attention alone ignores order. Encoder-decoder version adds cross-attention; decoder uses a **causal mask** so a token cannot see the future.
- **Why it beat RNN/LSTM:**
  - Parallel over sequence length (RNNs are step by step), so far faster training on GPUs.
  - Direct path between any two tokens (length 1), so long-range dependencies are easier; RNNs push information through many steps and suffer vanishing gradients.
  - Scales well with data and compute, which enabled pretraining (BERT, GPT).
- **Cost:** attention is O(n^2) in sequence length for time and memory, versus O(n) for an RNN.

**Example:** "The animal didn't cross the street because it was too tired." Attention for "it" puts high weight on "animal", not "street".

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
T, d = 4, 8
X = rng.normal(size=(T, d))
Wq, Wk, Wv = [rng.normal(size=(d, d)) / np.sqrt(d) for _ in range(3)]
Q, K, V = X @ Wq, X @ Wk, X @ Wv
S = Q @ K.T / np.sqrt(d)
S = np.where(np.triu(np.ones((T, T), bool), 1), -1e9, S)   # causal mask
A = np.exp(S - S.max(1, keepdims=True)); A /= A.sum(1, keepdims=True)
print(np.round(A, 2)); print((A @ V).shape, A.sum(1))
# row 0 attends only to itself; row 3 spreads weight over all 4 tokens; (4, 8) [1. 1. 1. 1.]
```

**Follow-ups:**
- *Why multiple heads?* Different heads can learn different relations (syntax, coreference); see Q21.
- *Can RNNs still win?* For streaming, tiny-memory or very long sequences with constant state (and now state-space models like Mamba) they can.
- *Encoder-only vs decoder-only?* Encoder (BERT) for understanding tasks, decoder (GPT) for generation.

**Common mistakes:** forgetting the `sqrt(d_k)` scaling; saying attention is O(n) ; forgetting positional information; confusing self-attention (Q, K, V from the same sequence) with cross-attention (Q from decoder, K/V from encoder).

### Q9 ⭐⭐⭐ 🟡 What is BERT, how is it pretrained (MLM, NSP), and how do you fine-tune it for classification?
**Asked at:** all types
**Say this first (1 line):** BERT is a bidirectional transformer encoder pretrained on huge unlabelled text by predicting masked words; you fine-tune it for classification by adding a small linear layer on the `[CLS]` output and training the whole thing on your labelled data.

**Then explain:**
- **Architecture:** a stack of transformer encoder layers (BERT-base: 12 layers, 768 hidden, 12 heads, ~110M params). Input = WordPiece tokens + position + segment embeddings, with `[CLS]` at the start and `[SEP]` between/after sentences. Max 512 tokens.
- **MLM (masked language model):** randomly pick 15% of tokens; of those, 80% become `[MASK]`, 10% a random token, 10% unchanged. Predict the original. This forces use of both left and right context (bidirectional) and the 80/10/10 split reduces the mismatch with fine-tuning, where `[MASK]` never appears.
- **NSP (next sentence prediction):** predict if sentence B follows A. Later work (RoBERTa) showed NSP adds little and dropped it; ALBERT replaced it with sentence-order prediction.
- **Fine-tuning for classification:** `[CLS]` final hidden state -> dropout -> linear -> softmax; train all weights with a small learning rate (2e-5 to 5e-5), 2-4 epochs, batch 16-32, warmup + linear decay, max length chosen from your data.
- **Variants:** DistilBERT (smaller, faster), RoBERTa (better pretraining), DeBERTa, multilingual BERT / IndicBERT / MuRIL for Indian languages.

**Example:** Ticket intent classifier with 5k labelled tickets: fine-tune `distilbert-base-uncased`, max length 128, lr 3e-5, 3 epochs; macro-F1 beats TF-IDF + LR when messages depend on context or negation.

**Code:**
```python
# not executed: transformers not installed in this environment (API as of recent releases; the Trainer argument for the tokenizer is `processing_class` in newer versions, `tokenizer` in older ones)
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
tok = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=3)
enc = lambda batch: tok(batch["text"], truncation=True, max_length=128)   # dynamic padding via the data collator
args = TrainingArguments("out", learning_rate=3e-5, num_train_epochs=3, per_device_train_batch_size=16,
                         weight_decay=0.01, warmup_ratio=0.1, eval_strategy="epoch", load_best_model_at_end=True)
# trainer = Trainer(model=model, args=args, train_dataset=train_ds.map(enc, batched=True),
#                   eval_dataset=val_ds.map(enc, batched=True), tokenizer=tok); trainer.train()
```

**Follow-ups:**
- *Why not predict the next word like GPT?* That is unidirectional; MLM lets each token see both sides, which suits understanding tasks.
- *Why a small LR?* To avoid destroying pretrained knowledge (catastrophic forgetting, Q39).
- *Text longer than 512 tokens?* Chunking or long-context models (Q28).

**Common mistakes:** saying BERT is a decoder or generative; saying NSP is still essential; using a large learning rate; not setting truncation; using `[CLS]` of the frozen model for similarity.

### Q10 ⭐⭐⭐ 🟡 Explain transfer learning in CNNs. When do you freeze layers versus fine-tune the whole network?
**Asked at:** all types
**Say this first (1 line):** Transfer learning reuses a CNN pretrained on a big dataset; freeze the layers when your data is small and similar to the source, and fine-tune more (or all) layers when you have more data or the domain is different.

**Then explain:**
- **Why it works:** early layers learn generic features (edges, textures), middle layers parts, late layers task-specific patterns. Early features transfer almost anywhere.
- **Recipe:** replace the final classifier head -> train only the head (backbone frozen) -> optionally unfreeze top blocks with a **smaller learning rate** (discriminative LRs: e.g. 1e-5 backbone, 1e-3 head).
- **Decision table:**

| Your data | Domain similar to source | Domain different |
|---|---|---|
| Small (hundreds) | freeze backbone, train head | freeze early layers, fine-tune last blocks carefully |
| Large (tens of thousands+) | fine-tune all with small LR | fine-tune all (or even train from scratch) |

- **Details that matter:** keep the source preprocessing (same image size/normalisation); BatchNorm layers: keep in eval mode when the batch is tiny, otherwise statistics get noisy; use warmup; monitor validation to stop early.

**Example:** Classifying 1,000 photos of 5 crop diseases: ImageNet ResNet-50, freeze backbone, train the head 5 epochs, then unfreeze the last block with lr 1e-5 for 10 epochs. For medical X-rays (very different domain, 50k images), fine-tune everything.

**Code:**
```python
import torch, torch.nn as nn
backbone = nn.Sequential(nn.Conv2d(3,16,3), nn.ReLU(), nn.Conv2d(16,32,3), nn.ReLU(),
                         nn.AdaptiveAvgPool2d(1), nn.Flatten())   # stands in for a pretrained network
head = nn.Linear(32, 5)
model = nn.Sequential(backbone, head)
for p in backbone.parameters(): p.requires_grad = False           # stage 1: feature extraction
for p in backbone[2:].parameters(): p.requires_grad = True        # stage 2: unfreeze top block
opt = torch.optim.AdamW([{"params": backbone.parameters(), "lr": 1e-5},
                         {"params": head.parameters(), "lr": 1e-3}])   # discriminative learning rates
n = lambda m: sum(p.numel() for p in m.parameters() if p.requires_grad)
print(n(model), [g["lr"] for g in opt.param_groups])   # 4805 trainable params after stage 2 (165 in stage 1); [1e-05, 0.001]
```

**Follow-ups:**
- *How many layers to unfreeze?* Treat it as a hyperparameter: grow from head only -> last block -> more while validation improves.
- *Feature extraction vs fine-tuning cost?* Frozen backbone lets you cache features and train a linear model/SVM in seconds.
- *Pretrained on ImageNet but my data is grayscale?* Repeat the channel 3x or sum the first conv's weights.

**Common mistakes:** large LR on a pretrained backbone (wipes out features); different normalisation than pretraining; unfreezing everything on 200 images; forgetting `model.eval()` for frozen BatchNorm.

### Q11 ⭐⭐⭐ 🟡 Explain how a CNN works: convolution, stride, padding, pooling, receptive field, parameter sharing.
**Asked at:** all types
**Say this first (1 line):** A CNN slides small shared filters over an image to detect local patterns, stacks layers so patterns get more complex, and uses pooling/stride to shrink the map; sharing weights is what keeps it small and translation-friendly.

**Then explain:**
- **Convolution:** a small kernel (e.g. 3x3xC) is slid across the image; at each position output = sum(kernel x patch) + bias. Each filter detects one pattern; C_out filters give C_out feature maps.
- **Parameter sharing:** the same kernel weights are reused at every position, so a 3x3 conv from 64 to 128 channels has `3*3*64*128 + 128 = 73,856` parameters, regardless of image size. A dense layer doing the same job on a 32x32 map would need about 8.6 billion.
- **Local connectivity + translation equivariance:** each output looks only at a neighbourhood; shift the input and the feature map shifts.
- **Output size:** `floor((n + 2p - k) / s) + 1`. Example: 224 input, k=3, s=1, p=1 -> 224 ("same"); s=2 -> 112; 7x7 stride 2 pad 3 -> 112.
- **Stride:** step size; larger stride downsamples. **Padding:** zeros around the border to preserve size and let edge pixels contribute.
- **Pooling:** max/average over windows (2x2, stride 2 halves the size) gives small translation invariance and fewer computations. Modern nets often use strided convs plus global average pooling at the end.
- **Receptive field:** the input region a neuron "sees". Three stacked 3x3 stride-1 convs give a 7x7 receptive field with fewer parameters (27C^2) than one 7x7 (49C^2); this is the VGG idea. Strides and pooling grow it faster.
- **Typical flow:** conv-BN-ReLU blocks -> pooling -> deeper filters -> global average pool -> linear classifier.

**Example:** A 224x224 RGB photo goes through a 3x3 conv with 64 filters (stride 1, pad 1): the output is 224x224x64 and the layer has only 3*3*3*64 + 64 = 1,792 parameters, because the same 64 small filters are reused at every position. A 2x2 max-pool then halves it to 112x112x64. The code below checks the output-size formula and a larger parameter count (64 to 128 channels).

**Code:**
```python
def out(n, k, s=1, p=0): return (n + 2*p - k)//s + 1
print(out(224,3,1,1), out(224,3,2,1), out(224,7,2,3), out(32,2,2,0))   # 224 112 112 16
print("conv params", 3*3*64*128 + 128)                                  # 73856
print("dense equiv", (32*32*64) * (32*32*128))                          # 8589934592
rf = 1
for _ in range(3): rf += 2          # each 3x3 stride-1 conv adds 2
print("RF of 3 stacked 3x3:", rf)  # 7
```

**Follow-ups:**
- *Are CNNs rotation/scale invariant?* No; only roughly translation-equivariant. Use augmentation.
- *1x1 convolution?* Mixes channels per pixel; used to reduce/expand channels cheaply (Inception, ResNet bottleneck).
- *Dilated conv?* Larger receptive field without downsampling.

**Common mistakes:** saying pooling gives full invariance; forgetting the bias and channel count when counting parameters; confusing the receptive field with the kernel size; mixing up equivariance (convolution) and invariance (pooling + global pooling).

### Q12 ⭐⭐⭐ 🟡 What is mAP in object detection, and how is it computed (precision-recall curve, AP per class, IoU thresholds)?
**Asked at:** all types
**Say this first (1 line):** mAP is the mean over classes of Average Precision, where AP is the area under that class's precision-recall curve built from detections ranked by confidence, with a detection counted correct only if its IoU with a ground-truth box passes a threshold.

**Then explain:**
1. For one class, collect all predicted boxes across the dataset and **sort by confidence**.
2. Walk down the list. A detection is a **TP** if IoU >= threshold with an unmatched ground-truth box of that class; otherwise **FP** (wrong place, duplicate, or no object). Missed ground truths are FN.
3. At each step compute cumulative **precision = TP/(TP+FP)** and **recall = TP/#GT**; this traces the PR curve.
4. **AP** = area under the curve after making precision monotone (take the max precision to the right, "interpolation"). VOC07 used 11 recall points; VOC10+/COCO use many points (COCO: 101).
5. **mAP** = average AP over classes. **mAP@0.5** uses IoU 0.5; **COCO mAP (AP@[.5:.95])** averages over IoU thresholds 0.50, 0.55, ..., 0.95, rewarding precise boxes. COCO also reports AP_small/medium/large.

**Example (one class, 5 ground truths, 6 detections sorted by score, TP flags 1,1,0,1,0,1):**
precision = 1, 1, 0.67, 0.75, 0.6, 0.67; recall = 0.2, 0.4, 0.4, 0.6, 0.6, 0.8. After interpolation AP@0.5 = 0.2x1 + 0.2x1 + 0.2x0.75 + 0.2x0.67 = 0.683.

**Code:**
```python
import numpy as np
dets = [(0.95,1),(0.9,1),(0.8,0),(0.7,1),(0.6,0),(0.5,1)]   # (score, is_TP at IoU>=0.5), sorted by score
n_gt = 5
tp = np.cumsum([d[1] for d in dets]); fp = np.cumsum([1-d[1] for d in dets])
prec, rec = tp/(tp+fp), tp/n_gt
mrec, mpre = np.r_[0, rec, 1], np.r_[0, prec, 0]
for i in range(len(mpre)-2, -1, -1): mpre[i] = max(mpre[i], mpre[i+1])   # monotone envelope
idx = np.where(mrec[1:] != mrec[:-1])[0]
print("AP@0.5 =", round(float(np.sum((mrec[idx+1]-mrec[idx]) * mpre[idx+1])), 3))   # 0.683
```

**Follow-ups:**
- *Why not accuracy?* There are unlimited "background" boxes, and localisation matters, so you need ranked precision-recall plus IoU.
- *Why average across IoU thresholds?* mAP@0.5 hides sloppy boxes; COCO-style averaging rewards tight localisation.
- *mAP vs F1 at a threshold?* mAP is threshold-free over confidence; for deployment you still pick an operating confidence threshold.

**Common mistakes:** counting duplicates as TP; forgetting to sort by confidence; computing precision/recall per image and averaging; mixing "mAP" definitions across VOC and COCO when comparing papers; not matching one ground truth to at most one detection.

### Q13 ⭐⭐⭐ 🟡 When would you pick an LLM (prompting) over a classic NLP model (TF-IDF/BERT classifier) for a text task? Discuss cost, latency, accuracy, data and maintenance.
**Asked at:** all types
**Say this first (1 line):** Use an LLM when labels are scarce, the task is open-ended or changes often, and volume and latency are modest; use a classic TF-IDF/BERT classifier when you have labels, high volume, tight latency or cost limits, and need stable, auditable behaviour.

**Then explain:**

| Factor | LLM prompting | Classic (TF-IDF / fine-tuned BERT) |
|---|---|---|
| Labelled data | none to a few examples | hundreds to thousands |
| Time to first version | hours | days to weeks |
| Cost per call | tokens billed, grows with volume | tiny (CPU) after training |
| Latency | hundreds of ms to seconds | ~1-50 ms |
| Accuracy | strong on nuance/zero-shot; may be worse than a tuned model on a narrow, labelled task | best on stable narrow tasks with enough labels |
| Consistency | non-deterministic, prompt-sensitive, model versions change | deterministic, versioned |
| Maintenance | prompt tuning, vendor changes, eval harness | retraining, labelling pipeline, drift monitoring |
| Data privacy | data goes to API (unless self-hosted) | stays in your infra |

- **Decision rule:** prototype with an LLM to learn the task and bootstrap labels, then often **distil into a small classifier** for production if volume is high.
- **Hybrid:** classic model handles the 90% easy cases; LLM handles low-confidence or complex ones; LLM labels data for the classic model.
- **Always compare on the same labelled test set**, not by gut feel.

**Example:** Routing 5M support tickets/day into 20 categories with 50k labelled history: fine-tuned DistilBERT or even TF-IDF + LR, cost near zero. Extracting key clauses from 300 unique contracts a month with no labels: LLM with a schema and a human review step.

**Follow-ups:**
- *Latency/cost estimate?* Count tokens per call x calls x price; compare with a small model on CPU. Do it before committing.
- *How do you evaluate the LLM fairly?* Fixed temperature (0), versioned prompt, labelled holdout, check for leakage (Q30).
- *Regulated domain?* Prefer deterministic, explainable models with an audit trail.

**Common mistakes:** using an LLM for a high-volume simple classification problem; comparing LLM few-shot on a few examples against a baseline on a different set; ignoring cost, drift of the vendor model and privacy; assuming an LLM is automatically more accurate than a tuned classifier.

### Q14 ⭐⭐⭐ 🟡 Prompting vs RAG vs fine-tuning: how do you decide? (framing only; depth is in Book 2)
**Asked at:** all types
**Say this first (1 line):** Start with prompting; add RAG when the model lacks knowledge (private or fresh facts); fine-tune when you need a consistent style, format or behaviour, or lower cost and latency at scale; RAG changes what the model knows, fine-tuning changes how it behaves.

**Then explain:**
- **Prompting (incl. few-shot):** cheapest to try; fixes instructions, format, tone. Limited by context length and by what the model already knows.
- **RAG (retrieve then generate):** fetch relevant documents at query time and put them in the prompt. Best for knowledge that is private, large or changing, and when you need citations/traceability. Cheap to update (change the index, not the model). Quality depends on retrieval.
- **Fine-tuning:** train on examples to teach style, structure, domain jargon or a narrow task; can let a small model replace a big one. Poor way to inject facts (stale, hard to update, can hallucinate them).
- **Ladder:** prompt -> add examples -> add RAG for knowledge -> fine-tune for behaviour/cost. They combine: RAG + a fine-tuned small model is common.

| Symptom | Fix |
|---|---|
| Wrong format/tone | better prompt, few-shot, then fine-tune |
| Does not know our docs/policies | RAG |
| Facts change weekly | RAG |
| Prompt too long/expensive at volume | fine-tune or distil |
| Needs exact structured outputs reliably | constrained decoding / fine-tune |

**Example:** HR policy chatbot: RAG over the policy PDFs with citations. Customer-reply drafts in brand voice: few-shot, then fine-tune once you have a few thousand approved replies.

**Follow-ups:**
- *Does RAG remove hallucination?* It reduces it; the model can still ignore or misread context, so check groundedness (Q40).
- *LoRA?* Parameter-efficient fine-tuning (Q39) makes fine-tuning cheap.
- *Depth?* Book 2 covers retrieval quality, chunking, evaluation.

**Common mistakes:** fine-tuning to add facts; skipping evaluation and choosing by vibes; building RAG when a better prompt would do; forgetting that RAG adds retrieval latency and an index to maintain.

### Q15 ⭐⭐ 🟢 Text preprocessing pipeline: tokenization, stop words, stemming vs lemmatization. When should you skip them?
**Asked at:** all types
**Say this first (1 line):** Clean and normalise the text, split it into tokens, and optionally drop stop words and reduce words to a root; but for modern transformer models you mostly skip all of this and keep the raw text.

**Then explain:**
- **Tokenization:** split text into units (words, subwords, characters). Handle punctuation, contractions, emojis, URLs. Transformers use their own subword tokenizer (WordPiece/BPE); feed it raw text.
- **Normalisation:** lowercasing, Unicode normalisation, removing URLs/HTML, collapsing whitespace. Lowercase is often fine for TF-IDF, not for cased NER.
- **Stop words:** very common words ("the", "is"). Removal shrinks vocabulary for TF-IDF/BoW, but can destroy meaning: "not" is in sklearn's English list, so "not happy" becomes "happy".
- **Stemming:** crude suffix chopping ("running" -> "run", "studies" -> "studi"); fast, may produce non-words. **Lemmatization:** dictionary and part-of-speech based ("better" -> "good", "was" -> "be"); slower, cleaner.
- **Skip when:** using BERT/LLMs (they need case, punctuation and word forms); sentiment/negation tasks; NER (capitalisation matters); code-mixed or multilingual text where English tools do not apply; short texts where every word counts.
- **Keep for:** classic sparse models, search indexing, topic models, small data.

**Example:** "Not happy! The delivery was NOT on time". Lowercase + regex tokens gives `not, happy, the, delivery, was, not, on, time`. sklearn's stop-word filter leaves `happy, delivery, time`: both negations are gone and the sentiment flips. Fix: keep negations or skip stop-word removal.

**Code:**
```python
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
text = "Not happy! The delivery was NOT on time, and I'm asking for a refund :( http://x.co/1"
t = re.sub(r"https?://\S+", " ", text.lower())
tokens = re.findall(r"[a-z']+", t)
print(tokens)
# ['not','happy','the','delivery','was','not','on','time','and',"i'm",'asking','for','a','refund']
print([w for w in tokens if w not in ENGLISH_STOP_WORDS])
# ['happy', 'delivery', 'time', "i'm", 'asking', 'refund']   <- negation lost!
```

**Follow-ups:**
- *Stemming vs lemmatization pick?* Stemming for speed in search; lemmatization when clean word forms matter.
- *Do you preprocess for BERT?* Minimal: maybe strip HTML/boilerplate; no stop word removal or stemming.
- *Indian languages?* Use language-aware tokenizers and transliteration handling (Q46).

**Common mistakes:** removing stop words blindly (negations); applying the same pipeline to transformers; fitting preprocessing differently in train and serving; lowercasing for NER; not versioning the pipeline.

### Q16 ⭐⭐ 🟢 Which evaluation metrics do you use for text classification (precision/recall/F1, macro vs micro), and why?
**Asked at:** all types
**Say this first (1 line):** Use precision, recall and F1 per class, then summarise with macro-F1 when every class matters equally and micro-F1 or accuracy when you care about overall volume; accuracy alone hides failures on rare classes.

**Then explain:**
- **Precision** = of what I flagged, how much was right. **Recall** = of what was really there, how much I found. **F1** = harmonic mean of the two.
- **Micro-average:** pool all TP/FP/FN across classes, then compute. Dominated by big classes (for single-label multiclass it equals accuracy).
- **Macro-average:** compute F1 per class, then average with equal weight. Exposes weak rare classes. **Weighted:** macro weighted by class support.
- **Multi-label:** per-label metrics, samples-average, Hamming loss, plus tuned per-label thresholds.
- **Imbalanced binary:** PR-AUC and recall at a fixed precision beat ROC-AUC and accuracy.
- Also look at the confusion matrix, per-class report, and calibration. Choose the metric from the business cost: missing a fraud/abuse message (recall) vs wrongly blocking a customer (precision).

**Example:** 100 emails: 90 normal, 8 spam, 2 phishing. Model gets 95% accuracy, but phishing recall is only 50%.

**Code:**
```python
import numpy as np
from sklearn.metrics import f1_score, classification_report
y = np.array([0]*90 + [1]*8 + [2]*2)
p = np.array([0]*88 + [1]*2 + [1]*6 + [0]*2 + [2]*1 + [0]*1)
for a in ["micro", "macro", "weighted"]: print(a, round(f1_score(y, p, average=a), 3))
# micro 0.95  macro 0.796  weighted 0.948
print(classification_report(y, p, digits=2, zero_division=0))
# class 0: P .97 R .98 | class 1: P .75 R .75 | class 2: P 1.00 R .50   -> macro-F1 (0.80) reveals the weak rare class
```

**Follow-ups:**
- *Micro vs accuracy?* Same for single-label multiclass.
- *When F-beta?* When recall matters more (beta=2) or precision more (beta=0.5).
- *Metric for ranking/search outputs?* Precision@k, recall@k, NDCG, MRR.

**Common mistakes:** reporting only accuracy on imbalanced data; averaging F1 over folds without fixed class sets; using macro when class prevalence truly should weigh in; tuning the threshold on the test set.

### Q17 ⭐⭐ 🟢 What are the common image augmentation techniques, and when can augmentation hurt?
**Asked at:** all types
**Say this first (1 line):** Augmentation creates new training images by applying label-preserving transforms (flip, crop, colour jitter, rotation, mixup/cutmix), and it hurts when a transform changes the true label or produces images that never occur in real use.

**Then explain:**
- **Geometric:** flip, random crop/resized crop, rotation, scale, translation, shear, perspective.
- **Photometric:** brightness, contrast, saturation, hue, blur, noise, JPEG compression.
- **Occlusion/mixing:** cutout/random erasing, mixup (blend two images and labels), cutmix (paste a patch, mix labels), RandAugment/AutoAugment (searched policies), copy-paste for detection/segmentation.
- **Apply to training only.** Validation/test stay unaugmented (except test-time augmentation, TTA, deliberately).
- **When it hurts:**
  - Flipping digits (6/9 rotation), text, left/right-sided medical findings, traffic signs with direction.
  - Heavy colour jitter when colour is the signal (ripe vs unripe fruit, skin lesions).
  - Crops that cut away the object, or rotation that makes unrealistic images (product always upright).
  - For detection/segmentation, you must transform boxes/masks the same way.
  - Too strong augmentation = underfitting; it cannot fix a biased or leaky dataset.
- Always view a batch of augmented images before training.

**Example:** Satellite image classification: random rotations by any angle are fine (no up direction). Handwritten digit recognition: no 180-degree rotations, mild shifts only.

**Follow-ups:**
- *Offline vs online augmentation?* Online (random per epoch) gives more variety and no storage cost.
- *Augmentation for text?* Back-translation, synonym replacement, paraphrasing with LLMs, with label checks.
- *Test-time augmentation?* Average predictions over a few transformed copies for a small accuracy gain at extra latency.

**Common mistakes:** augmenting validation data; label-changing transforms; forgetting to transform the labels/boxes; using the same augmentation randomly seeded across workers, producing duplicates; using augmentation to hide a data-leakage problem.

### Q18 ⭐⭐ 🟢 What is perplexity, and what does it tell you about a language model?
**Asked at:** all types
**Say this first (1 line):** Perplexity is the exponential of the average negative log-likelihood per token; intuitively, it is how many equally likely next tokens the model is "choosing between" on average, so lower is better.

**Then explain:**
- Formula: `PPL = exp( -(1/N) * sum_i log p(w_i | w_<i) )` = `exp(cross-entropy)`. Use natural log with exp (or base 2 with 2^).
- A perfect model gives 1. A uniform guess over a vocabulary of V gives V.
- **Use:** compare language models **on the same test set and the same tokenizer/vocabulary**; track it during pretraining; check domain fit (a medical LM has lower perplexity on medical text).
- **Limits:** not comparable across different tokenizers (token-level PPL changes with segmentation; use bits-per-character/byte for that); low perplexity does not mean a useful, truthful or safe model; it says nothing about downstream task quality; sensitive to test data contamination.

**Example:** The model assigns probabilities 0.2, 0.5, 0.1, 0.4, 0.25 to the true next tokens. Average NLL = 1.382 nats, so PPL = e^1.382 = 3.98, like choosing among about 4 options. A uniform model on a 10,000 word vocabulary has PPL = 10,000.

**Code:**
```python
import numpy as np
p = np.array([0.2, 0.5, 0.1, 0.4, 0.25])      # probability given to each true next token
ce = -np.log(p).mean(); print("CE nats", round(ce, 3), "PPL", round(np.exp(ce), 2))   # 1.382 3.98
print("uniform over 10k vocab PPL:", round(np.exp(-np.log(1/10000))))                   # 10000
```

**Follow-ups:**
- *Why is it not enough for LLMs?* A model can be fluent and wrong; evaluate with task benchmarks, human or LLM-judge evaluation (Q23, Q30).
- *Relation to cross-entropy?* PPL = exp(cross-entropy loss); a drop in loss of 0.1 nat is about 10% lower PPL.
- *Masked LMs like BERT?* Perplexity is not defined the same way (pseudo-perplexity is used).

**Common mistakes:** comparing perplexity across models with different vocabularies; mixing log base and exp base; reporting training-set perplexity; treating lower perplexity as proof of better downstream performance.

### Q19 ⭐⭐ 🟡 How do you get a sentence or document embedding, and how would you use embeddings for semantic search (cosine similarity, ANN index)?
**Asked at:** all types
**Say this first (1 line):** Run text through a sentence-embedding model to get one vector per document, normalise it, store the vectors in an index, and at query time embed the query and return the nearest vectors by cosine similarity, using an ANN index when the corpus is large.

**Then explain:**
- **Getting a vector:** (1) pretrained sentence-transformers (SBERT family, e5, bge), contrastively trained for similarity (Q45) - the default; (2) mean-pool the token outputs of a transformer, better than raw `[CLS]` for an un-tuned BERT; (3) average word vectors or TF-IDF-weighted average - cheap baseline; (4) doc2vec/TF-IDF + SVD (LSA) for classic setups. Chunk long documents (Q28).
- **Cosine similarity:** `cos = (a . b) / (|a||b|)`. If vectors are L2-normalised, cosine = dot product, so one matrix multiply scores everything.
- **Exact search:** brute force is O(N x d) per query; fine up to ~1M vectors on a good machine.
- **ANN (approximate nearest neighbour):** trade a little recall for big speed. HNSW (graph, high recall, memory heavy), IVF (cluster then search nearby clusters), PQ (compress vectors). Libraries: FAISS, hnswlib, ScaNN, or a vector DB (pgvector, Milvus, etc.). Measure **recall@k versus exact search** and latency.
- **Production:** hybrid with BM25, rerank the top 50 with a cross-encoder (Q45), embed with the same model for queries and docs, re-embed everything if you change the model.

**Example:** FAQ search with 20k questions: embed once with a multilingual sentence-transformer, store normalised vectors in FAISS HNSW, return top 5 for each user query under 20 ms.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
E = rng.normal(size=(10000, 64)).astype("float32")
E /= np.linalg.norm(E, axis=1, keepdims=True)           # normalise once -> dot == cosine
q = E[42] + 0.1 * rng.normal(size=64).astype("float32"); q /= np.linalg.norm(q)
scores = E @ q
top = np.argsort(-scores)[:3]; print(top, np.round(scores[top], 2))   # [42 8615 7124] [0.8 0.42 0.42]
```
(Random vectors stand in for real embeddings; the item most similar to the noisy query is itself, index 42.)

**Follow-ups:**
- *Why normalise?* Otherwise vector length (not direction) affects dot-product ranking.
- *ANN downside?* Misses some true neighbours; tune `efSearch`/`nprobe` for the recall you need.
- *Embeddings vs keyword search?* Embeddings handle paraphrase; keyword wins on exact IDs and rare terms; combine both.

**Common mistakes:** mixing embedding models for queries and documents; not normalising; embedding whole long documents past the model limit (silent truncation); ignoring recall measurement of the ANN index; no reranking.

### Q20 ⭐⭐ 🟡 What is NER? How would you build and evaluate a NER system (BiLSTM-CRF vs BERT; entity-level F1)?
**Asked at:** GCCs / MNCs (Walmart, JPMC, Amazon India, Microsoft IDC)
**Say this first (1 line):** NER (named entity recognition) tags spans of text as entities like person, organisation, location or amount; today you build it by fine-tuning a BERT-style token classifier (BiLSTM-CRF is the older, lighter option) and evaluate with entity-level precision/recall/F1.

**Then explain:**
- **Formulation:** token classification with **BIO tags** (`B-PER I-PER O B-ORG ...`). Each token gets a label; contiguous B/I tags form an entity span.
- **BiLSTM-CRF:** word/char embeddings -> bidirectional LSTM for context -> **CRF** layer that scores whole tag sequences so illegal transitions (`O -> I-PER`) are discouraged. Small, fast on CPU, needs less data than people think.
- **BERT token classifier:** transformer encoder + linear layer per token (optionally CRF). Better with context and rare entities; subword issue: label the first subword (or all) and align labels to tokens.
- **Steps:** define the tag set and annotation guide, label (check inter-annotator agreement), split by document, train, evaluate, error analysis; add gazetteers/rules for high-precision entities (PAN, GST numbers via regex); consider an LLM for bootstrapping labels.
- **Evaluation:** **entity-level (strict span + type match)**, as in `seqeval`/CoNLL: an entity is correct only if the full span and the type match. Report per-type P/R/F1 and micro/macro. Token-level accuracy is misleading because most tokens are `O`.

**Example:** Gold `[PER: tokens 0-1] [ORG: 3] [LOC: 5]`; the model predicts PER only for token 0 (partial span). Entity-level: 2 of 3 predicted spans are correct, 2 of 3 gold found, P = R = F1 = 0.67, even though 5 of 6 tokens are tagged right.

**Code:**
```python
def spans(tags):
    out, start, typ = set(), None, None
    for i, t in enumerate(tags + ["O"]):
        if t == "O" or t.startswith("B-") or (t.startswith("I-") and t[2:] != typ):
            if start is not None: out.add((start, i, typ)); start = typ = None
            if t != "O": start, typ = i, t[2:]
    return out
gold = ["B-PER", "I-PER", "O", "B-ORG", "O", "B-LOC"]
pred = ["B-PER", "O",     "O", "B-ORG", "O", "B-LOC"]
g, p = spans(gold), spans(pred); tp = len(g & p)
pr, rc = tp / len(p), tp / len(g); print("P", round(pr, 2), "R", round(rc, 2), "F1", round(2*pr*rc/(pr+rc), 2))   # 0.67 0.67 0.67
```

**Follow-ups:**
- *Nested entities?* Plain BIO cannot; use span-based models.
- *Domain shift?* Fine-tune on in-domain labels; add active learning.
- *LLM for NER?* Good zero-shot and for labelling, but a fine-tuned small model is cheaper and more consistent at scale.

**Common mistakes:** reporting token accuracy; splitting sentences of one document across train/test; ignoring subword-label alignment; lowercasing text for a cased NER model; no per-type breakdown.

### Q21 ⭐⭐ 🟡 Why does the transformer use positional encoding, and how does multi-head attention help?
**Asked at:** all types
**Say this first (1 line):** Self-attention has no sense of order, so we add positional information to the token embeddings; multi-head attention runs several attention operations in parallel so the model can look at different kinds of relationships at once.

**Then explain:**
- **Why positions are needed:** attention is a weighted sum over a set; shuffle the tokens and each token's output is just shuffled (permutation-equivariant). "dog bites man" and "man bites dog" would look identical without position.
- **Options:** fixed **sinusoidal** encodings (original paper): `PE(pos,2i)=sin(pos/10000^(2i/d))`, `PE(pos,2i+1)=cos(...)`, added to embeddings; **learned** position embeddings (BERT, GPT-2); **relative** schemes - **RoPE** (rotary, used in many LLMs) and ALiBi - that encode distance and extrapolate better to long inputs.
- **Multi-head attention:** split `d_model` into h heads (e.g. 12 x 64). Each head has its own Q, K, V projections, attends independently, outputs are concatenated and projected. Same total cost as one big head.
- **Why it helps:** different heads can specialise (local syntax, long-range references, delimiter tokens), giving a richer representation than a single averaged attention pattern. Some heads turn out redundant and can be pruned.

**Example:** In "The trophy did not fit in the suitcase because it was too big", one head can link "it" to "trophy" while another tracks the verb-object structure.

**Code:**
```python
import numpy as np
def pe(T, d):
    pos = np.arange(T)[:, None]; i = np.arange(0, d, 2)[None, :]
    ang = pos / 10000**(i / d); P = np.zeros((T, d)); P[:, 0::2] = np.sin(ang); P[:, 1::2] = np.cos(ang); return P
P = pe(50, 16); print(np.round(P[1, :4], 3), P.shape)      # [0.841 0.54 0.311 0.95] (50, 16)
rng = np.random.default_rng(0); X = rng.normal(size=(5, 16)); W = rng.normal(size=(16, 16))
def attn(X):
    S = (X @ W) @ (X @ W).T / 4; A = np.exp(S - S.max(1, keepdims=True)); A /= A.sum(1, keepdims=True); return A @ X
perm = rng.permutation(5); print(np.allclose(attn(X)[perm], attn(X[perm])))   # True: no position info -> order is invisible
```

**Follow-ups:**
- *Sinusoidal vs learned?* Similar quality in practice; sinusoidal can in theory extrapolate to longer lengths, learned cannot beyond trained length.
- *Why RoPE?* Encodes relative distance directly in the dot product and works well for long-context LLMs.
- *Does a decoder need positions given the causal mask?* The mask leaks some order, but explicit position encoding is still used and helps.

**Common mistakes:** saying heads are "different models" with extra compute (head dimension is d/h); forgetting the output projection that mixes the concatenated heads; thinking positional encoding is learned in the original paper (it was sinusoidal).

### Q22 ⭐⭐ 🟡 Compare CNN architectures: LeNet, AlexNet, VGG, ResNet, Inception, EfficientNet. Why do skip connections help?
**Asked at:** all types
**Say this first (1 line):** CNN architectures got deeper and more efficient over time, and ResNet's skip connections are what made very deep networks trainable by giving gradients a direct path back.

**Then explain:**

| Model | Year | Key idea |
|---|---|---|
| LeNet-5 | 1998 | first practical CNN (digits): conv-pool-conv-pool-FC, ~60k params |
| AlexNet | 2012 | deep CNN on GPUs, ReLU, dropout, augmentation; won ImageNet by a huge margin |
| VGG | 2014 | only 3x3 convs stacked deep (16-19 layers); simple but ~138M params (VGG16) |
| Inception (GoogLeNet) | 2014 | parallel 1x1/3x3/5x5 branches, 1x1 bottlenecks; ~6.8M params |
| ResNet | 2015 | residual (skip) connections; 50 to 152 layers trainable |
| EfficientNet | 2019 | compound scaling of depth, width and resolution together, found by NAS; best accuracy per FLOP |

- **Residual block:** `y = F(x) + x`. The block only needs to learn the *residual* F; if the best thing is identity, F just goes to 0.
- **Why skips help:** (1) gradients flow through the identity path without being multiplied by many weights, easing vanishing gradients; (2) they fix the "degradation problem" where plain deeper nets had *higher training error*; (3) smoother loss landscape; (4) ensemble-like behaviour of many shallow paths. Dimensions must match (1x1 conv projection when they do not).
- **Practical picks:** ResNet-50 is the default backbone; EfficientNet/MobileNet for efficiency/edge; ConvNeXt and ViTs for modern accuracy (Q33).

**Example:** A plain 56-layer net trains worse than a 20-layer one; the 56-layer ResNet beats the 20-layer one. That was the ResNet paper's headline observation.

**Follow-ups:**
- *Bottleneck block?* 1x1 reduce -> 3x3 -> 1x1 expand; cuts compute for deep ResNets.
- *DenseNet?* Concatenates all previous feature maps; strong reuse, high memory.
- *MobileNet?* Depthwise-separable convs for cheap inference.

**Common mistakes:** saying skip connections "add parameters" (they add none); claiming the problem is only overfitting (it was optimisation); mixing up VGG's size with efficiency; forgetting that EfficientNet scales all three dimensions.

### Q23 ⭐⭐ 🟡 BLEU vs ROUGE vs BERTScore: what do they measure and what are their weaknesses?
**Asked at:** GCCs / MNCs (Walmart, JPMC, Amazon India, Microsoft IDC)
**Say this first (1 line):** BLEU and ROUGE measure word overlap with a reference (BLEU is precision-oriented, used for translation; ROUGE is recall-oriented, used for summarisation), while BERTScore compares contextual embeddings so it can credit paraphrases; none of them measures factual correctness.

**Then explain:**
- **BLEU:** modified (clipped) n-gram precision for n=1..4, geometric mean, times a **brevity penalty** `BP = exp(1 - r/c)` if the candidate (length c) is shorter than the reference (length r). Clipping stops "the the the the" from scoring high.
- **ROUGE:** ROUGE-N = n-gram **recall** against the reference (often reported as F1); ROUGE-L uses the longest common subsequence.
- **BERTScore:** embeds candidate and reference tokens with BERT, matches each token to its most similar token by cosine, and averages into precision, recall and F1. Captures synonyms and paraphrases.
- **Weaknesses:** BLEU/ROUGE punish valid paraphrases and ignore meaning, are insensitive to factual errors and word order beyond n-grams, depend on the number and quality of references, and BLEU is sensitive to tokenisation (use SacreBLEU). BERTScore depends on the embedding model, scores cluster in a narrow range, and still cannot detect hallucination. For LLM outputs, add human review, task-specific checks, groundedness checks and LLM-as-judge with calibration (Q30, Q40).

**Example:** Reference "the cat is on the mat". Candidate "there is a cat on the mat": clipped unigram precision 5/7 = 0.71, ROUGE-1 P/R/F1 = 0.71/0.83/0.77. Candidate "the the the the the the": naive precision looks like 1.0, clipped precision is 0.33. A 3-word candidate against a 6-word reference gets brevity penalty `exp(1 - 6/3) = 0.37`.

**Code:**
```python
from collections import Counter
import math
ref = "the cat is on the mat".split()
good = "there is a cat on the mat".split(); bad = "the the the the the the".split()
def p1(c, r):
    cc, rc = Counter(c), Counter(r); return sum(min(v, rc[w]) for w, v in cc.items()) / len(c)
print(round(p1(good, ref), 2), round(p1(bad, ref), 2))              # 0.71 0.33  (clipped unigram precision)
def rouge1(c, r):
    cc, rc = Counter(c), Counter(r); o = sum(min(v, rc[w]) for w, v in cc.items())
    p, rec = o / len(c), o / len(r); return round(p, 2), round(rec, 2), round(2*p*rec/(p+rec), 2)
print(rouge1(good, ref))                                             # (0.71, 0.83, 0.77)
print(round(math.exp(1 - 6/3), 2))                                   # 0.37 brevity penalty
```

**Follow-ups:**
- *Which for summarisation?* ROUGE plus human/LLM judgement of faithfulness; ROUGE alone rewards copying.
- *Why SacreBLEU?* Standard tokenisation makes scores comparable across papers.
- *Metric for open-ended generation?* No single one; combine reference-free checks and human evaluation.

**Common mistakes:** treating BLEU as a quality score for chat/LLM answers; comparing BLEU computed with different tokenisers; ignoring the number of references; trusting a high ROUGE for a factually wrong summary.

### Q24 ⭐⭐ 🟡 How do you handle class imbalance in text or image classification?
**Asked at:** all types
**Say this first (1 line):** Fix imbalance at the data level (resample or augment), the loss level (class weights, focal loss) and the decision level (threshold tuning), and always judge with PR-AUC, recall and per-class F1 rather than accuracy.

**Then explain:**
- **Measure right first:** stratified split, report per-class precision/recall/F1 and PR-AUC. Keep the **validation/test sets at the natural distribution**.
- **Data level:** oversample the minority (careful: duplicates cause overfitting), undersample the majority, or generate more minority data: image augmentation, text back-translation/paraphrase/LLM-generated examples. SMOTE works on dense features, not directly on raw text or images (use it on embeddings if at all).
- **Loss level:** class weights (inverse frequency), **focal loss** (down-weights easy examples; popular in detection), label smoothing, balanced sampling per batch.
- **Decision level:** train normally, then choose the threshold that meets the business precision/recall trade-off; calibrate probabilities.
- **Model level:** pretrained models and few-shot/zero-shot help rare classes; ensembles; for extreme cases treat as anomaly detection.
- **Collect:** active learning to find more minority examples.
- Resample **only the training fold**, never before the split.

**Example:** 3% positive class, logistic regression. Plain: precision 0.78, recall 0.65, F1 0.71. With `class_weight="balanced"`: recall jumps to 0.93 but precision falls to 0.38 (F1 0.54) - weights move you along the PR curve, they do not always raise F1. Tuning the threshold instead gave P 0.70, R 0.67, F1 0.68 (the threshold here was picked on train for brevity; use a validation set).

**Code:**
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score, precision_score
from sklearn.model_selection import train_test_split
X, y = make_classification(8000, 20, n_informative=8, weights=[0.97], class_sep=1.0, flip_y=0, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, random_state=0)
def rep(name, pred): print(name, "P", round(precision_score(yte, pred), 2), "R", round(recall_score(yte, pred), 2), "F1", round(f1_score(yte, pred), 2))
m = LogisticRegression(max_iter=2000).fit(Xtr, ytr); rep("plain    ", m.predict(Xte))          # P .78 R .65 F1 .71
mb = LogisticRegression(max_iter=2000, class_weight="balanced").fit(Xtr, ytr); rep("balanced ", mb.predict(Xte))   # P .38 R .93 F1 .54
s = m.predict_proba(Xtr)[:, 1]; t = max(np.linspace(0.02, 0.9, 45), key=lambda t: f1_score(ytr, s >= t))
rep(f"thr={t:.2f}", m.predict_proba(Xte)[:, 1] >= t)                                          # P .70 R .67 F1 .68
```

**Follow-ups:**
- *Does oversampling change probability calibration?* Yes, scores become inflated; recalibrate.
- *Focal loss formula?* `FL = -(1 - p_t)^gamma log(p_t)`, gamma about 2.
- *Image-specific?* Class-balanced sampling, copy-paste augmentation, or collecting more examples of the rare class.

**Common mistakes:** oversampling before the split (leakage); evaluating on a rebalanced test set; reporting accuracy; assuming weights always improve F1; ignoring the cost asymmetry that should set the threshold.

### Q25 ⭐⭐ 🟡 Object detection vs semantic vs instance segmentation: differences, and typical models (YOLO, Faster R-CNN, U-Net, Mask R-CNN).
**Asked at:** all types
**Say this first (1 line):** Classification says what is in the image, detection adds a box per object, semantic segmentation labels every pixel by class, and instance segmentation labels every pixel and separates individual objects.

**Then explain:**

| Task | Output | Separates two cars? | Typical models |
|---|---|---|---|
| Detection | box + class + score per object | yes (two boxes) | YOLO (one-stage, fast), SSD, RetinaNet, Faster R-CNN (two-stage, accurate), DETR |
| Semantic segmentation | class per pixel | no (both "car") | U-Net, DeepLab, FCN, SegFormer |
| Instance segmentation | mask + class per object | yes | Mask R-CNN, YOLO-seg, SOLO |
| Panoptic | semantic + instance | yes for things, labels stuff | Panoptic FPN, Mask2Former |

- **One-stage vs two-stage:** two-stage (Faster R-CNN) first proposes regions (RPN), then classifies and refines them: more accurate, slower. One-stage (YOLO, SSD) predicts boxes and classes directly in one pass: faster, good for real time.
- **Mask R-CNN** = Faster R-CNN + a mask branch and RoIAlign.
- **U-Net:** encoder-decoder with skip connections between matching resolutions; very popular for medical and small-data segmentation.
- **Metrics:** detection - mAP (Q12); segmentation - IoU/Dice (Q42).
- **Pick by need:** count and locate objects -> detection; measure area/shape (tumour size, crop cover) -> semantic segmentation; count touching objects and outline each -> instance segmentation. Labelling cost rises in that order (boxes are cheaper than masks).

**Example:** Self-driving: detection for cars/pedestrians, semantic segmentation for drivable road, instance/panoptic when you must track individual objects precisely.

**Follow-ups:**
- *Why does YOLO suit edge devices?* Single forward pass, small variants (n/s), easy export to ONNX/TensorRT.
- *Data labelling cost?* Weak supervision, SAM-assisted masks, and pretrained backbones reduce it.
- *Which metric for a rare small object?* AP_small, and check recall at your operating threshold.

**Common mistakes:** saying semantic segmentation separates instances; confusing one-stage with "less accurate always" (modern YOLO is competitive); using detection when area is the actual quantity needed; ignoring labelling cost.

### Q26 ⭐⭐ 🟡 Explain batch normalization and dropout in CNNs. Where do you place them and why?
**Asked at:** all types
**Say this first (1 line):** Batch norm normalises each channel's activations using the batch statistics to make training faster and more stable, and dropout randomly zeroes activations during training to reduce overfitting; in CNNs the usual order is conv -> BN -> ReLU, with dropout (if any) near the classifier.

**Then explain:**
- **Batch norm:** for each channel, over the batch and spatial positions: `y = gamma * (x - mu) / sqrt(var + eps) + beta`, with learned `gamma`, `beta`. At inference it uses **running averages** of mu and var from training. Effects: allows higher learning rates, less sensitive to initialisation, mild regularisation (batch noise). Placement: after the conv (conv bias becomes redundant), before the activation (the common convention; after is also used).
- **Small or varying batches:** batch statistics get noisy; use GroupNorm/LayerNorm instead. Transformers use LayerNorm.
- **Dropout:** during training each activation is dropped with probability p and survivors are scaled by `1/(1-p)` ("inverted dropout") so expected values match at test time, when dropout is off. In CNNs it is less effective on conv layers (neighbouring pixels are correlated) so use it before the final dense layer, or use spatial dropout/DropBlock.
- **Interplay:** dropout right before BN can shift variance statistics and hurt; BN often reduces the need for dropout. Deep ResNets typically use BN and no dropout.
- **Train vs eval mode:** both behave differently in `model.train()` and `model.eval()`; forgetting `eval()` at inference is a classic bug.

**Example:** After normalising a batch of feature maps drawn with mean 5 and std 3, each channel has mean about 0 and std 1 (verified below).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
x = rng.normal(5, 3, size=(8, 4, 6, 6))                      # N, C, H, W
g, b, eps = np.ones((1, 4, 1, 1)), np.zeros((1, 4, 1, 1)), 1e-5
mu = x.mean((0, 2, 3), keepdims=True); var = x.var((0, 2, 3), keepdims=True)
y = g * (x - mu) / np.sqrt(var + eps) + b
print(np.round(y.mean((0, 2, 3)), 3), np.round(y.std((0, 2, 3)), 3))    # means ~0, std 1.0 per channel
p = 0.5; a = rng.normal(size=1000)
mask = (rng.random(a.shape) > p) / (1 - p)                              # inverted dropout: scale survivors at train time
a_drop = a * mask
```

**Follow-ups:**
- *Why does BN help?* Originally "reduces internal covariate shift"; later work says it mainly smooths the loss landscape and allows larger LRs.
- *BN with batch size 1-2?* Use GroupNorm or freeze BN statistics.
- *BN at inference?* Uses running mean/variance, so predictions do not depend on the other items in the batch.

**Common mistakes:** forgetting `model.eval()`; using BN with tiny batches; leaving conv bias on before BN (harmless but wasteful); applying dropout to every conv layer; saying dropout scales weights at test time in the inverted version (the scaling is done during training).

### Q27 ⭐⭐ 🟡 How do you handle out-of-vocabulary words and misspellings? Explain subword tokenization (BPE/WordPiece).
**Asked at:** all types
**Say this first (1 line):** Modern models never see an unknown word: they split text into subword pieces (BPE, WordPiece), so a rare or misspelled word becomes a few known fragments, and in the worst case single characters or bytes.

**Then explain:**
- **Old way:** a fixed word vocabulary, everything else mapped to `<UNK>` (information lost). Misspellings like "recieve" were all `<UNK>`.
- **BPE (Byte Pair Encoding):** start with characters, repeatedly merge the most frequent adjacent pair in the corpus, stop at a vocab size (30k-100k). Frequent words become one token, rare words split into pieces. Byte-level BPE (GPT-2/3/4, Llama) starts from bytes, so truly nothing is OOV.
- **WordPiece (BERT):** same idea, but the merge picks the pair that most increases the likelihood of the training data; pieces inside a word carry a `##` prefix. **SentencePiece/Unigram** works on raw text with no pre-splitting on spaces (good for Hindi, Japanese).
- **Misspellings:** subwords give graceful degradation (for example "recieve" might become `re`, `##ci`, `##eve`; the exact split depends on the vocabulary), but the meaning shifts, so also do light normalisation, spell correction for search, or train with noisy/augmented text (typo injection). Character n-gram models (fastText) also handle typos well.
- **Cost:** rare or non-English words become many tokens: longer sequences, more cost, and weaker representations.

**Example:** "lowest" was never seen in training, but BPE trained on "low", "newest", "widest" encodes it as `low` + `est</w>` (verified below).

**Code:**
```python
from collections import Counter
corpus = "low low low low low lower lower newest newest newest newest newest newest widest widest widest".split()
vocab = Counter(tuple(w) + ("</w>",) for w in corpus)
def pairs(v):
    c = Counter()
    for w, f in v.items():
        for a, b in zip(w, w[1:]): c[(a, b)] += f
    return c
def merge(v, pair):
    out = {}
    for w, f in v.items():
        new, i = [], 0
        while i < len(w):
            if i < len(w) - 1 and (w[i], w[i+1]) == pair: new.append(w[i] + w[i+1]); i += 2
            else: new.append(w[i]); i += 1
        out[tuple(new)] = f
    return out
merges = []
for _ in range(8):
    p = pairs(vocab).most_common(1)[0][0]; merges.append(p); vocab = merge(vocab, p)
def encode(word):
    w = tuple(word) + ("</w>",)
    for m in merges: w = next(iter(merge({w: 1}, m)))
    return list(w)
print(encode("lowest"), encode("newer"))
# ['low', 'est</w>'] ['new', 'e', 'r', '</w>']
```

**Follow-ups:**
- *How is the vocab size chosen?* Trade-off: bigger means shorter sequences but a bigger embedding matrix and rarer tokens; 30k-50k is typical.
- *Why can tokenization hurt numbers or code?* Numbers split inconsistently ("1234" may be `12`+`34`), which hurts arithmetic.
- *Can you change the tokenizer when fine-tuning?* Not without retraining embeddings; the model is tied to its tokenizer.

**Common mistakes:** saying BPE and WordPiece are identical (merge criterion differs); lowercasing/stripping accents for a cased or Indic multilingual model; claiming subwords fully fix typos; swapping tokenizers between pretraining and fine-tuning.

### Q28 ⭐⭐ 🟡 How do you deal with long documents when BERT has a 512-token limit?
**Asked at:** product cos (Flipkart/Swiggy-type)
**Say this first (1 line):** First ask whether you need the whole document; if yes, split it into overlapping chunks, run BERT on each, and combine the results, or switch to a long-context model.

**Then explain:**
- **Why 512?** Self-attention cost grows with the square of length (Q49) and BERT's position embeddings stop at 512.
- **Truncate smartly:** head only, tail only, or head + tail (first ~128 + last ~382 tokens). Often the start and end carry most signal (reviews, emails). Cheapest option, so test it first.
- **Sliding window with overlap:** chunks of 512 with a stride/overlap (e.g. 128) so sentences are not cut. Then aggregate: mean or max of chunk logits for classification (max for "does any part mention fraud"), or a small attention/LSTM over chunk embeddings. For QA/extraction, take the best-scoring span across chunks.
- **Hierarchical:** embed sentences/paragraphs, pool, then classify.
- **Retrieve first (RAG-style):** pick the top relevant passages with BM25 or embeddings, feed only those.
- **Long-context models:** Longformer/BigBird (sparse attention, 4k-16k), or modern LLMs with 100k+ context, at higher cost and latency.
- **Summarise first** (extractive or LLM), then classify.

**Example:** A 1,300-token loan agreement with window 512 and overlap 128 gives chunks 0-511, 384-895, 768-1279, 1152-1299. Chunk logits are averaged (mean `[1.83, -0.17]`) or max-pooled (`[3.0, 0.4]`).

**Code:**
```python
import numpy as np
def chunks(ids, size=512, stride=128):          # stride = overlap
    step = size - stride
    return [ids[s:s+size] for s in range(0, max(len(ids) - stride, 1), step)]
ids = list(range(1300))
print([(c[0], c[-1], len(c)) for c in chunks(ids)])
# [(0, 511, 512), (384, 895, 512), (768, 1279, 512), (1152, 1299, 148)]
logits = np.array([[2.0, 0.1], [0.5, 0.4], [3.0, -1.0]])    # one row per chunk
print(logits.mean(0), logits.max(0))
```
(With Hugging Face tokenizers the same is done via `return_overflowing_tokens=True, stride=128`; not executed: transformers not installed.)

**Follow-ups:**
- *Mean or max pooling?* Mean when the label is a document-wide property (sentiment), max when one chunk is enough (compliance flag). Validate on dev data.
- *Does chunk overlap leak across train/test?* Yes if you split chunks randomly; split by document.
- *Cost?* Number of forward passes is about N/(512-overlap), so latency scales linearly.

**Common mistakes:** blindly truncating the head; splitting train/val at chunk level (leakage); ignoring that `[CLS]/[SEP]` take 2 of the 512 slots; assuming a long-context model always beats chunking on cost.

### Q29 ⭐⭐ 🟡 How would you build a text classifier with very few labelled examples (zero-shot, few-shot, SetFit, weak labelling, active learning)?
**Asked at:** all types
**Say this first (1 line):** Start with a zero/few-shot LLM or embeddings plus logistic regression as a baseline, label a small high-value set using active learning, and use weak labels or an LLM as a labeller to grow the data, then train a small supervised model.

**Then explain:**
- **Zero-shot:** an LLM prompt or an NLI model ("this text is about {label}"). No labels needed; good first baseline, but costly per call and prompt-sensitive.
- **Few-shot:** put 3-10 examples per class in the prompt (in-context learning). No training, but context-limited.
- **Embeddings + simple classifier:** encode with a sentence-transformer and fit logistic regression on 20-100 labels. Very strong, cheap, fast to iterate.
- **SetFit:** fine-tune a sentence-transformer contrastively on a few labelled pairs (8-16 per class), then fit a head. Often matches large LLMs with a tiny model.
- **Weak labelling (Snorkel-style):** write keyword rules/regex/heuristics as noisy labelling functions, combine them with a label model, train on the result.
- **Active learning:** train, score the unlabelled pool, send the most uncertain (or diverse) items to humans, repeat. Usually reaches target accuracy with far fewer labels than random sampling.
- **LLM as annotator:** let a strong LLM label thousands, have humans check a sample, distil into a small model.
- **Always keep a clean, human-labelled test set**, even if only 200-300 items, otherwise you cannot tell which approach works.

**Example:** Tagging support tickets into 12 intents with 5 labels each: embeddings + LR gives a baseline in an hour; 3 rounds of active learning (50 labels per round) lift macro-F1; an LLM labels the rest and a DistilBERT is trained for cheap serving.

**Follow-ups:**
- *How do you pick uncertain samples?* Least confidence, smallest margin between the top two classes, or entropy; add diversity (clustering) to avoid near-duplicates.
- *Risk of weak labels?* Correlated rules inflate confidence and bake in bias; check against the gold set.
- *Class imbalance?* Stratify the labelled seed, use targeted search (keywords) to find rare classes.

**Common mistakes:** no gold test set; tuning prompts on the test set; fine-tuning a big model on 30 examples (overfits); active learning with a biased seed; random sampling when classes are rare.

### Q30 ⭐⭐ 🟡 How do you evaluate an LLM-based classifier or extractor in a classical DS workflow, and what can go wrong (non-determinism, leakage, prompt sensitivity)?
**Asked at:** all types
**Say this first (1 line):** Treat the LLM like any classifier: a held-out, human-labelled test set, standard metrics with confidence intervals, plus extra checks for things classical models do not have: non-determinism, prompt sensitivity, output-format failures, and test-data leakage into the model's training data.

**Then explain:**
- **Gold set:** 300-1000 human-labelled examples (more for rare classes), labelled by two annotators with agreement measured (Cohen's kappa; Q43). Split a dev set (for prompt tuning) from a frozen test set (used once).
- **Metrics:** classification: precision/recall/F1 per class, confusion matrix. Extraction: exact match and field-level F1, plus a "valid JSON/schema" rate. Report bootstrap confidence intervals; with 200 items the accuracy interval is about +/-5 points.
- **Non-determinism:** set temperature 0 and a seed where available, but outputs can still vary across runs and model-version updates. Run 3-5 times and report run-to-run agreement; pin the model version.
- **Prompt sensitivity:** re-word the prompt, reorder few-shot examples and labels; a robust system changes little. Large swings mean your score is partly prompt luck.
- **Leakage:** public benchmarks may be in the model's training data; also do not tune the prompt on the test set, and do not include test examples as few-shot demos.
- **LLM-as-judge:** biased toward longer answers and its own style; calibrate against human labels.
- **Operational:** cost, latency, refusal rate, parse failures, and subgroup performance.

**Example:** On 200 labelled tickets the LLM scores 0.815 accuracy, bootstrap 95% CI about 0.76-0.87. Re-running the same prompt gives 92% label agreement (kappa 0.84): the gap between two prompt variants has to exceed this noise to be real.

**Code:**
```python
import numpy as np
from sklearn.metrics import cohen_kappa_score
rng = np.random.default_rng(0)
y = rng.integers(0, 2, 200); pred = np.where(rng.random(200) < 0.85, y, 1 - y)
accs = [(pred[i] == y[i]).mean() for i in (rng.integers(0, 200, 200) for _ in range(1000))]
print(round((pred == y).mean(), 3), np.round(np.percentile(accs, [2.5, 97.5]), 3))   # 0.815 [0.76 0.865]
run2 = np.where(rng.random(200) < 0.9, pred, 1 - pred)          # simulated second run
print((pred == run2).mean(), round(cohen_kappa_score(pred, run2), 3))                 # 0.92 0.84
```

**Follow-ups:**
- *LLM or fine-tuned small model?* Compare on the same gold set including cost/latency; often the LLM labels and a small model serves.
- *How do you compare two prompts?* Paired test (McNemar) on the same items, not just two accuracy numbers.
- *Version changes?* Keep a regression suite and re-run on every model/prompt change.

**Common mistakes:** reporting a single number from one run; tuning on test; ignoring format failures (counted as wrong or silently dropped); trusting public benchmark scores; no confidence intervals.

### Q31 ⭐⭐ 🟡 How would you detect and handle drift in a production NLP model (e.g. new slang, new product names)?
**Asked at:** product cos (Flipkart/Swiggy-type)
**Say this first (1 line):** Monitor the inputs (OOV rate, embedding and length distributions), the outputs (predicted class mix, confidence), and, as soon as labels arrive, the real quality; alert on thresholds, and retrain on a schedule or trigger with fresh labelled data.

**Then explain:**
- **Input drift (no labels needed):** share of unseen tokens/OOV or rare subwords, new product names/brands, text length, language mix; PSI or KS on those features; and distance between the embedding distribution of last week vs the training period (e.g. a domain classifier's AUC, or MMD).
- **Prediction drift:** shift in class proportions, mean confidence, share of low-confidence predictions. Cheap and fast.
- **Concept drift:** the meaning of labels changes (a new slang term flips sentiment). Needs labels: sample a few hundred production items weekly for human review (prioritise low-confidence ones), track F1 by class.
- **Fixes:** retrain on recent data plus a replay of old data; add new terms via subword models (no vocab change); for new product names use retrieval/embeddings or rules as a stop-gap; keep a champion/challenger and shadow-test before swapping.
- **Triggers:** PSI > 0.2 is a common "significant" rule of thumb (0.1-0.2 moderate); also calendar retrains (monthly) for fast-moving domains.

**Example:** Last week's OOV rate vs the training vocab was 0%; this week 33% of sampled queries contain new words ("rizz", "skibidi"): input drift alert. PSI on class mix: 0.0016 for a stable week vs 0.55 when mix shifts from 50/30/20 to 20/30/50 (verified below).

**Code:**
```python
import numpy as np
def psi(a, b):
    a = np.clip(a / a.sum(), 1e-6, None); b = np.clip(b / b.sum(), 1e-6, None)
    return float(np.sum((b - a) * np.log(b / a)))
print(round(psi(np.array([50, 30, 20]), np.array([48, 31, 21])), 4))   # 0.0016  stable
print(round(psi(np.array([50, 30, 20]), np.array([20, 30, 50])), 3))   # 0.55    big shift
```

**Follow-ups:**
- *Drift but accuracy fine?* Not every drift hurts; prioritise alerts tied to quality or business metrics.
- *Retrain frequency?* Based on how fast the domain moves and on measured decay, not a fixed habit.
- *No labels?* Use proxies: user corrections, click-through, escalation to humans.

**Common mistakes:** monitoring only accuracy (labels arrive late); retraining blindly on model-labelled data (feedback loop); alerting on every PSI wiggle; forgetting seasonality (festival sales) is not drift.

### Q32 ⭐⭐ 🔴 What is Non-Max Suppression, and how do anchor boxes work? Anchor-based vs anchor-free detectors.
**Asked at:** all types
**Say this first (1 line):** NMS removes duplicate detections of the same object by keeping the highest-scoring box and dropping overlapping boxes above an IoU threshold; anchor boxes are preset box shapes the detector refines instead of predicting boxes from scratch, and anchor-free detectors skip the presets and predict object centres or edges directly.

**Then explain:**
- **NMS:** detectors output many overlapping boxes per object. Algorithm: sort by score; take the best; delete all remaining boxes with IoU with it above a threshold (0.5 typical); repeat. Per class in practice. Cost O(n^2) worst case.
- **Soft-NMS:** instead of deleting, lower the score of overlapping boxes. Helps crowded scenes where real objects overlap.
- **Anchors:** at every feature-map location, place k boxes of different scales and aspect ratios (e.g. 9 in Faster R-CNN/RetinaNet). The network predicts, per anchor, an objectness/class score and offsets (dx, dy, dw, dh) from the anchor. An anchor is positive if IoU with a ground-truth box is above a threshold (e.g. 0.7), negative below (0.3).
- **Anchor-based:** Faster R-CNN, SSD, RetinaNet, YOLOv3-v5. Pros: stable training, strong priors. Cons: extra hyperparameters (sizes, ratios), many easy negatives (RetinaNet uses focal loss), anchors need tuning per dataset (k-means on boxes).
- **Anchor-free:** FCOS, CenterNet, YOLOX/YOLOv8 predict a centre point plus box distances. Fewer hyperparameters, simpler. DETR (transformer) is anchor-free and NMS-free: it uses set prediction with Hungarian matching.

**Example:** Three boxes around one dog at IoU 0.82, plus a separate cat box: NMS at 0.5 keeps the dog box with score 0.9 and the cat, and drops the other two overlapping dog boxes.

**Code:**
```python
import numpy as np
def iou(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1]); x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area = lambda r: (r[2] - r[0]) * (r[3] - r[1])
    return inter / (area(a) + area(b) - inter)
def nms(boxes, scores, thr=0.5):
    order = np.argsort(scores)[::-1]; keep = []
    while len(order):
        i = order[0]; keep.append(int(i))
        order = np.array([j for j in order[1:] if iou(boxes[i], boxes[j]) < thr], dtype=int)
    return keep
boxes = np.array([[10,10,50,50],[12,12,52,52],[100,100,140,140],[11,9,49,51]], float)
print(nms(boxes, np.array([0.9, 0.8, 0.7, 0.6])))   # [0, 2]
```

**Follow-ups:**
- *Threshold choice?* Low (0.3-0.4) removes more duplicates but can kill real neighbours in crowds; high keeps duplicates.
- *Why can NMS hurt?* Heavily overlapping true objects (crowds) get suppressed; it is also non-differentiable and a latency cost on edge hardware.
- *How are anchors chosen?* K-means over training box sizes with 1-IoU as distance (YOLOv2+).

**Common mistakes:** applying NMS across all classes jointly; confusing the NMS IoU threshold with the mAP IoU threshold; saying anchors are learned (the shapes are preset, only offsets are learned); forgetting NMS is inference-time only.

### Q33 ⭐⭐ 🔴 What is the Vision Transformer (ViT)? How does it differ from a CNN, and when does each win?
**Asked at:** all types
**Say this first (1 line):** ViT cuts an image into fixed patches (e.g. 16x16), treats each patch as a token, and feeds them to a standard Transformer encoder; a CNN instead builds features with local, shared convolutions, so CNNs win with little data and tight compute, and ViTs win with lots of data or pretraining.

**Then explain:**
- **How ViT works:** split the 224x224 image into 196 patches of 16x16x3 = 768 values, linearly project each into an embedding, add position embeddings and a `[CLS]` token, run Transformer layers (self-attention), classify from `[CLS]`.
- **Inductive bias:** CNNs hard-code locality and translation equivariance, which helps with small data. ViT has little such bias, so it must learn it and needs large data (JFT-300M, ImageNet-21k) or strong augmentation/distillation (DeiT) to beat CNNs.
- **Global view:** attention connects every patch to every other from layer 1; CNNs grow the receptive field gradually.
- **Cost:** attention is O(n^2) in the number of patches; high-resolution images get expensive (Swin uses windowed attention to fix this).
- **When each wins:** small/medium data, edge devices, low latency -> CNN (ResNet, EfficientNet, MobileNet) or a pretrained ViT fine-tuned. Large pretraining, transfer learning, multimodal (CLIP), dense tasks -> ViT/Swin. In practice: fine-tune a pretrained model of either kind.

**Example:** 224x224 image, 16x16 patches gives 14x14 = 196 tokens + 1 CLS = 197; the attention matrix has 197^2 = 38,809 entries per head. Halving the patch size to 8 gives 784 tokens, roughly 16x the attention cost.

**Code:**
```python
import numpy as np
img = np.random.default_rng(0).random((224, 224, 3)); P = 16
patches = img.reshape(224 // P, P, 224 // P, P, 3).swapaxes(1, 2).reshape(-1, P * P * 3)
print(patches.shape)    # (196, 768): 196 patch tokens, each 768 numbers
```

**Follow-ups:**
- *Why position embeddings?* Attention has no notion of order; without them the patches are a bag.
- *Hybrid options?* Convolutional stem before the transformer, or ConvNeXt (a CNN modernised with transformer-era design) that matches ViTs.
- *Why did ViT need so much data?* Fewer built-in assumptions; with ImageNet-1k only it underperformed ResNets.

**Common mistakes:** saying ViTs always beat CNNs; ignoring the data requirement; not mentioning the quadratic cost; forgetting position embeddings; training a ViT from scratch on a small dataset.

### Q34 ⭐⭐ 🔴 Walk through a design for an image classification system with limited labelled data and a latency budget on edge devices.
**Asked at:** product cos (Flipkart/Swiggy-type)
**Say this first (1 line):** Fine-tune a small pretrained backbone (MobileNet/EfficientNet-Lite) on the few labels with heavy augmentation, grow the data with active learning and pseudo-labels, then quantise and export it to fit the device's latency budget.

**Then explain (framework):**
- **Requirements:** classes, accuracy target, latency (e.g. under 50 ms per image on a mid-range phone), model size (e.g. under 10 MB), offline or online, cost of a false positive vs miss.
- **Data:** start with 100-500 labelled images per class; label the most informative via active learning; add pseudo-labels from a big teacher model on unlabelled images; capture the real device camera conditions (lighting, blur) early. Split by user/session/product, not by image, to avoid leakage.
- **Model:** pretrained small backbone with a new head; freeze most layers first, then unfreeze the top blocks with a low LR. Alternatives: embeddings from a strong frozen model (CLIP/DINO) + logistic regression for very few labels. Distil a large teacher into the small student.
- **Augmentation:** flips, crops, colour jitter, MixUp/CutMix, RandAugment; matched to what the camera will see.
- **Compression:** post-training or quantisation-aware training to INT8 (about 4x smaller, 2-4x faster), pruning, export to TFLite/ONNX/Core ML/TensorRT; benchmark on the real device, not a laptop.
- **Evaluation:** per-class precision/recall, confusion matrix, calibration, accuracy by lighting/device slice; check the accuracy drop after quantisation (aim under 1-2 points).
- **Serving/monitoring:** on-device inference, send low-confidence images (with consent) to the cloud or for labelling; track confidence drift and update the model over the air.
- **Trade-offs:** accuracy vs size/latency; on-device (privacy, no network) vs cloud (bigger model, easier updates); a cascade (small model first, big model for uncertain cases) often wins.

**Example (illustrative numbers, not measured):** MobileNetV3 fine-tuned on 300 images per class reaches the target F1 on a phone in about 20 ms after INT8 quantisation, with the model about a quarter of its FP32 size.

**Follow-ups:**
- *Few-shot extreme (5 images per class)?* Frozen CLIP/DINO embeddings + nearest neighbour or linear head.
- *Accuracy dropped after INT8?* Use quantisation-aware training or keep sensitive layers in higher precision; use a representative calibration set.
- *How do you know the latency budget is met?* Measure p95 latency on target hardware including preprocessing.

**Common mistakes:** training from scratch; benchmarking latency on a GPU; random image-level splits with near-duplicate frames; skipping the post-quantisation evaluation; ignoring the camera domain gap.

### Q35 ⭐⭐ 🔴 Why does a vision model trained in one domain fail in another? How do you diagnose and fix the domain shift?
**Asked at:** GCCs / MNCs (Walmart, JPMC, Amazon India, Microsoft IDC)
**Say this first (1 line):** The model learned patterns specific to the training domain (lighting, camera, backgrounds, textures), so when the input distribution changes those patterns no longer hold; diagnose by comparing source and target data and errors, and fix with target-domain data, augmentation, or domain adaptation.

**Then explain:**
- **Types of shift:** covariate shift (input look changes, labels same: new camera), label/prior shift (class mix changes), concept shift (what a label means changes). Vision is mostly covariate shift.
- **Spurious features:** the model may rely on shortcuts (hospital watermark, grass behind cows, white background in catalogue photos), which break elsewhere.
- **Diagnose:**
  - **Domain classifier:** train a classifier to tell source from target images; AUC near 0.5 means similar, near 1.0 means a big shift (shown below).
  - Compare embedding distributions (t-SNE/UMAP, MMD) and basic stats (brightness, resolution, blur).
  - Slice the errors by device, lighting, location; use Grad-CAM (Q41) to see what the model looks at.
  - Evaluate on a small labelled target set: the only real measure of damage.
- **Fix, in order of cost:** (1) collect and label some target data and fine-tune (best return); (2) augmentation matching the target (colour jitter, blur, noise, style transfer); (3) normalisation tweaks (re-estimate BatchNorm statistics on target, test-time adaptation); (4) unsupervised domain adaptation (DANN: adversarial features that cannot reveal the domain; self-training with pseudo-labels); (5) pretrain on diverse data / foundation models, which are usually more robust; (6) fall back with confidence thresholds and human review.
- **Prevent:** train on diverse sources, hold out whole domains (leave-one-site-out) for validation, monitor drift after launch.

**Example:** Synthetic check: a domain classifier on 10 features gives AUC 0.53 between two same-distribution samples, but 0.90 when the target has shifted mean and larger variance.

**Code:**
```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
rng = np.random.default_rng(0)
src = rng.normal(0, 1, (500, 10)); same = rng.normal(0, 1, (500, 10)); shift = rng.normal(0.6, 1.2, (500, 10))
def dom_auc(a, b):
    X = np.vstack([a, b]); y = np.r_[np.zeros(len(a)), np.ones(len(b))]
    return cross_val_score(LogisticRegression(max_iter=500), X, y, cv=5, scoring="roc_auc").mean()
print(round(dom_auc(src, same), 2), round(dom_auc(src, shift), 2))    # 0.53 0.9
```

**Follow-ups:**
- *Few target labels?* Fine-tune only the last layers, or use few-shot with frozen foundation embeddings.
- *No target labels?* Pseudo-labelling, DANN, test-time adaptation, with careful monitoring.
- *Importance weighting?* Reweight source samples by p_target/p_source from a domain classifier; works for mild covariate shift.

**Common mistakes:** validating on a random split of the source domain (always optimistic); blaming the architecture; ignoring spurious shortcuts; assuming more source data fixes it; no labelled target sample at all.

### Q36 ⭐ 🟢 What is the vanishing gradient problem in RNNs, and how do LSTM/GRU gates address it?
**Asked at:** all types
**Say this first (1 line):** In an RNN the gradient is multiplied by the same recurrent factor at every time step, so over long sequences it shrinks toward zero (or blows up); LSTM and GRU add gated, mostly additive paths so the gradient can flow across many steps.

**Then explain:**
- **Why it happens:** backprop through time multiplies about T Jacobians `W^T * diag(tanh')`. If their typical size is below 1 the product vanishes; above 1 it explodes. tanh/sigmoid derivatives (at most 1 and 0.25) make shrinking likely.
- **Effect:** the model cannot learn dependencies more than about 10-20 steps back; early inputs get almost no update.
- **LSTM:** has a cell state `c_t = f_t * c_{t-1} + i_t * g_t`. The forget gate `f_t` (0-1) decides what to keep, input gate what to write, output gate what to expose. Because the cell path is additive with gate `f_t` near 1, the gradient along it is a product of `f` values, not of squashing matrices, so it survives long distances.
- **GRU:** two gates (update, reset), no separate cell state; fewer parameters, often similar accuracy.
- **Exploding gradients:** handled by gradient clipping, not by gates.
- **Today:** Transformers largely replaced them as attention gives direct paths between positions; LSTMs remain useful for small, streaming, low-memory cases.

**Example:** Factor 0.9 per step over 50 steps: 0.9^50 = 0.005 (vanishes). Factor 1.1: 1.1^50 = 117 (explodes). A forget gate of 0.99 over 50 steps keeps 0.99^50 = 0.61 (verified below).

**Code:**
```python
T = 50
print(0.9 ** T, 1.1 ** T, 0.99 ** T)   # 0.0052  117.4  0.605
```

**Follow-ups:**
- *Initialise forget-gate bias to 1?* Yes, a common trick so the LSTM starts by remembering.
- *LSTM vs GRU?* GRU is smaller and faster; LSTM sometimes better on long dependencies; try both.
- *Do LSTMs fully solve it?* No, just much better; very long ranges still hard, hence attention.

**Common mistakes:** saying LSTM fixes exploding gradients (clipping does); describing gates without the additive cell-state path; confusing vanishing gradients with overfitting; forgetting ReLU RNNs with identity init as an alternative.

### Q37 ⭐ 🟢 Topic modelling: explain LDA and when you would use it over clustering embeddings (e.g. BERTopic).
**Asked at:** product cos (Flipkart/Swiggy-type)
**Say this first (1 line):** LDA is a probabilistic model where each document is a mixture of topics and each topic is a distribution over words; I use it when I want soft, interpretable topic proportions on bag-of-words data, and embedding clustering (BERTopic) when meaning, short texts, or synonyms matter.

**Then explain:**
- **LDA generative story:** for each document draw topic proportions (Dirichlet prior); for each word draw a topic, then a word from that topic's word distribution. Fitting (variational Bayes or Gibbs sampling) inverts this. You choose the number of topics K.
- **Output:** document-topic matrix (each row sums to 1) and topic-word weights (top words describe the topic).
- **Pros:** soft membership (a doc can be 60% sports, 40% politics), fast, no GPU, transparent, works on long documents.
- **Cons:** ignores word order and context (synonyms split topics), poor on short text (tweets, reviews), needs K, needs preprocessing (stopwords, lemmas), unstable across runs.
- **BERTopic:** embed with sentence-transformers, reduce with UMAP, cluster with HDBSCAN, describe clusters with class-based TF-IDF. Captures semantics, finds K automatically, labels outliers; hard assignment by default and slower.
- **Choice:** LDA for long documents, interpretability, tight compute, topic mixtures; BERTopic for short/semantic text, multilingual, exploratory work. Evaluate with topic coherence (e.g. c_v) and human inspection, not perplexity alone.

**Example:** On six tiny documents with two themes, LDA with K=2 recovers topic 0 = team/win/match/score (sports) and topic 1 = trade/share/market/stock (finance), with the first document about 92% topic 0 (verified below).

**Code:**
```python
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
docs = ["cricket match score team win", "team coach match goal win", "stock market price share trade",
        "market investor share profit trade", "cricket team score goal", "profit stock investor price"]
cv = CountVectorizer(); X = cv.fit_transform(docs)
lda = LatentDirichletAllocation(n_components=2, random_state=0, max_iter=50).fit(X)
vocab = np.array(cv.get_feature_names_out())
for k, t in enumerate(lda.components_): print(k, vocab[t.argsort()[::-1][:4]])
print(np.round(lda.transform(X)[:2], 2))
# 0 ['team' 'win' 'match' 'score'] / 1 ['trade' 'share' 'market' 'stock'] / [[0.92 0.08] [0.91 0.09]]
```

**Follow-ups:**
- *How do you pick K?* Coherence across a range of K plus manual review.
- *Why not use perplexity?* It often disagrees with human judgement of topic quality.
- *LLM-based alternative?* Use an LLM to name clusters or label documents with a fixed taxonomy.

**Common mistakes:** using LDA on tweets and expecting clean topics; no stopword removal; treating topics as ground truth labels; ignoring instability (fix the seed, check across runs).

### Q38 ⭐ 🟡 Cosine similarity vs Euclidean vs dot product for embeddings: when does each apply?
**Asked at:** Europe product cos (Spotify/Zalando/Booking/Klarna-type)
**Say this first (1 line):** Cosine compares direction only, Euclidean compares absolute position, dot product mixes direction and magnitude; use whichever the embedding model was trained with, and note that for unit-normalised vectors all three give the same ranking.

**Then explain:**

| Measure | Formula | Sensitive to length? | Use when |
|---|---|---|---|
| Cosine | `u.v / (norm(u) * norm(v))` | no | text/sentence embeddings, semantic similarity (default) |
| Dot product | `u.v` | yes | models trained with it (many recommenders, MIPS); magnitude encodes popularity/confidence |
| Euclidean | `norm(u - v)` | yes | clustering (k-means), when distances in the space are meaningful |

- **Relationship:** for unit vectors, `norm(u - v)^2 = 2 - 2cos(u,v)`, so cosine similarity, dot product and Euclidean all give the same nearest neighbours.
- **Magnitude:** in word/sentence embeddings the norm often tracks frequency or text length, which is noise for semantics, hence cosine. In recommendation, a large item norm can legitimately mean "popular", so dot product is used (a different top-k than cosine).
- **High dimensions:** Euclidean distances concentrate (all points look similarly far); cosine is more robust but not immune.
- **Practical:** normalise embeddings and use an inner-product index (FAISS `IndexFlatIP`); then it is cosine.

**Example:** `a=[1,2,2]`, `b=10a`: cosine 1.0 (same direction), Euclidean 27, dot 90. `c=[2,1,2]`: cosine 0.889, Euclidean 1.41, dot 8. Euclidean says `c` is much closer, cosine says `b` is identical in direction (verified below). After normalising, squared Euclidean 0.2222 equals `2-2cos` = 0.2222.

**Code:**
```python
import numpy as np
a = np.array([1., 2., 2.]); b = 10 * a; c = np.array([2., 1., 2.])
cos = lambda u, v: u @ v / np.linalg.norm(u) / np.linalg.norm(v)
print(cos(a, b), np.linalg.norm(a - b), a @ b)                 # 1.0  27.0  90.0
print(round(cos(a, c), 3), round(np.linalg.norm(a - c), 2), a @ c)   # 0.889 1.41 8.0
an, cn = a / np.linalg.norm(a), c / np.linalg.norm(c)
print(round(np.linalg.norm(an - cn) ** 2, 4), round(2 - 2 * cos(a, c), 4))   # 0.2222 0.2222
```

**Follow-ups:**
- *Is cosine a metric?* Cosine similarity is not; `1 - cos` does not satisfy the triangle inequality, but the angular distance does.
- *Which for a vector DB?* Match the model's training (read the model card); normalise and use inner product.
- *Why is MIPS harder than cosine search?* Dot product is not a metric, so tree/graph indexes need transforms.

**Common mistakes:** using Euclidean on unnormalised text embeddings; mixing metrics between index build and query; believing cosine and dot product differ even after normalisation; ignoring that norm can carry signal in recommenders.

### Q39 ⭐ 🟡 Fine-tuning basics: full fine-tuning vs adapters/LoRA vs feature extraction. What goes wrong with catastrophic forgetting or a bad learning rate?
**Asked at:** all types
**Say this first (1 line):** Feature extraction trains only a new head on a frozen model (cheapest), adapters/LoRA train a small number of extra weights (cheap, near full quality), and full fine-tuning updates everything (best fit, most compute and most risk of forgetting).

**Then explain:**

| Approach | What trains | Cost / memory | Forgetting risk | Use when |
|---|---|---|---|---|
| Feature extraction | new head only | lowest | none | very little data, quick baseline |
| Adapters / LoRA | small inserted modules (LoRA: low-rank update `W + BA`) | low (about 1-2% params) | low | LLMs, many task variants, limited GPU |
| Full fine-tuning | all weights | highest (gradients + Adam states add roughly 3x the weights in memory) | highest | lots of data, domain far from pretraining |

- **LoRA:** freeze `W`, learn `B (d x r)` and `A (r x d)` with small rank r (4-64); output `Wx + (alpha/r) B A x`. B starts at zero so training starts from the original model. After training you can merge `BA` into `W` (no extra latency). QLoRA does this on a 4-bit quantised base.
- **Catastrophic forgetting:** training on a narrow task overwrites general knowledge. Mitigate with a small learning rate, fewer epochs, LoRA/frozen layers, mixing in some general data (replay), and evaluating on general benchmarks as well as the task.
- **Bad learning rate:** too high destroys pretrained features (loss spikes, accuracy collapses); too low underfits. Typical full fine-tune for BERT: 2e-5 to 5e-5 with warmup and linear decay; LoRA tolerates higher (1e-4 to 3e-4). Use layer-wise LR decay (lower LR for lower layers).
- **Other pitfalls:** tiny data overfits (early stopping, validation), label leakage, mismatch between tokenizer/prompt formats.

**Example:** For a 768x768 linear layer (590,592 params with bias), rank-8 LoRA trains 2 x 8 x 768 = 12,288 parameters, about 2.1% (verified below).

**Code:**
```python
import torch, torch.nn as nn
torch.manual_seed(0)
class LoRALinear(nn.Module):
    def __init__(self, base, r=8, alpha=16):
        super().__init__(); self.base = base
        for p in base.parameters(): p.requires_grad = False          # freeze W
        self.A = nn.Parameter(torch.randn(r, base.in_features) * 0.01)
        self.B = nn.Parameter(torch.zeros(base.out_features, r)); self.s = alpha / r
    def forward(self, x): return self.base(x) + self.s * (x @ self.A.T @ self.B.T)
base = nn.Linear(768, 768); lora = LoRALinear(base)
tot = sum(p.numel() for p in base.parameters()); tr = sum(p.numel() for p in lora.parameters() if p.requires_grad)
print(tot, tr, round(100 * tr / tot, 2))                 # 590592 12288 2.08
x = torch.randn(2, 768); print(torch.allclose(lora(x), base(x)))   # True: B=0 so starts identical
```

**Follow-ups:**
- *How to choose rank r?* Start at 8-16; raise if underfitting; gains saturate quickly.
- *LoRA vs prompt tuning?* Prompt tuning learns input vectors only (even fewer params), usually weaker on small models.
- *Detect forgetting?* Track a held-out general benchmark during fine-tuning.

**Common mistakes:** using a pretraining-sized LR for full fine-tuning; no warmup; fine-tuning too many epochs on tiny data; saying LoRA changes the architecture at inference (it can be merged); forgetting to freeze the base.

### Q40 ⭐ 🟡 How do you reduce hallucination and measure factuality when an LLM is part of a DS pipeline?
**Asked at:** all types
**Say this first (1 line):** Ground the model in retrieved, trusted sources, constrain and validate its outputs, and measure factuality with a labelled evaluation set (claims checked against sources) instead of trusting fluent answers.

**Then explain:**
- **Why it happens:** an LLM predicts plausible next tokens; it has no built-in notion of truth, and fills gaps confidently.
- **Reduce it:**
  - **RAG:** retrieve relevant documents and instruct "answer only from the context; say 'I don't know' otherwise"; include citations.
  - **Constrain the task:** classification/extraction with a fixed schema or label set beats open-ended generation; use structured output/JSON schema, enums.
  - **Prompting:** low temperature, explicit abstain option, ask for quotes from the source.
  - **Verification:** a second pass or tool checks (look up the number in a database, run the code, regex/schema validation); self-consistency (sample several, keep the majority).
  - **Fine-tuning** on in-domain data with refusals; human review for high-stakes outputs.
- **Measure:**
  - **Faithfulness/groundedness:** break the answer into claims, check each is supported by the retrieved context (human or LLM-judge; frameworks like RAGAS/TruLens).
  - **Accuracy on a gold QA set** with exact match or F1 for extraction.
  - **Hallucination rate** = % answers with at least one unsupported claim; **abstention rate** and accuracy when abstaining.
  - **Retrieval quality** separately: recall@k of the relevant passage (if retrieval is wrong, generation fails).
  - Calibrate any LLM judge against human labels.
- **Monitor in production:** sample outputs for review, track user corrections/thumbs-down, log inputs/outputs.

**Example (illustrative numbers):** A support bot answers 500 test questions; reviewers find 40 contain unsupported claims: 8% hallucination rate. After RAG with "answer only from context" it drops to 3%, while abstentions rise to 6%: you report both.

**Follow-ups:**
- *Does low temperature remove hallucination?* No; it only reduces randomness, a wrong answer can be confidently repeated.
- *Trade-off?* Stricter grounding raises refusals; tune against the business cost of a wrong answer vs a refusal.
- *LLM-as-judge risk?* Bias to longer answers and self-preference; spot-check with humans.

**Common mistakes:** judging only by how fluent answers look; measuring answer quality without checking retrieval; counting refusals as correct; using the same LLM to generate and judge without calibration.

### Q41 ⭐ 🟡 What is Grad-CAM, and how do you explain a CNN or transformer prediction?
**Asked at:** GCCs / MNCs (Walmart, JPMC, Amazon India, Microsoft IDC)
**Say this first (1 line):** Grad-CAM makes a heatmap of which image regions pushed the model toward a class, by weighting the last convolutional feature maps with the gradient of the class score and summing them.

**Then explain:**
- **Steps:** (1) forward pass, take the score for the target class; (2) backprop to the last conv layer's feature maps A_k; (3) weights `alpha_k` = average of gradient over spatial positions; (4) `CAM = ReLU(sum_k alpha_k A_k)`; (5) upsample to image size and overlay. ReLU keeps only positive evidence.
- **Use it to:** check the model looks at the object, not background shortcuts (watermark, ruler in skin-lesion photos), debug errors, and build trust. It is a sanity check, not proof of causation; resolution is coarse (feature-map size).
- **Other methods:** saliency maps/Integrated Gradients (pixel-level), SHAP/LIME (perturbation, work on any model), occlusion tests, Grad-CAM++/Score-CAM. For transformers: attention maps are not reliable explanations; use attention rollout, Grad-CAM-style on a late block, or Integrated Gradients/SHAP on tokens. For text, token attribution (IG, SHAP) highlights influential words.
- **Sanity checks:** randomise the model weights and the explanation should change (Adebayo et al.); some methods fail this.

**Example:** A pneumonia classifier shows hot spots on a hospital tag, not the lungs: a shortcut found via Grad-CAM, fixed by cropping and removing tags.

**Code:**
```python
import torch, torch.nn as nn
torch.manual_seed(0)
net = nn.Sequential(nn.Conv2d(1, 4, 3, padding=1), nn.ReLU(), nn.Conv2d(4, 4, 3, padding=1), nn.ReLU())
head = nn.Linear(4, 2)
img = torch.zeros(1, 1, 8, 8); img[0, 0, 2:5, 2:5] = 1
fmap = net(img); fmap.retain_grad()                          # last conv feature maps
head(fmap.mean((2, 3)))[0, 1].backward()                     # score of class 1
w = fmap.grad.mean((2, 3), keepdim=True)                     # alpha_k: pooled gradients
cam = torch.relu((w * fmap).sum(1)).detach()[0]
cam = cam / (cam.max() + 1e-8)                               # 8x8 heatmap in [0, 1]
print(cam.shape)   # torch.Size([8, 8])
```
(Same recipe on a real ResNet: hook the last conv block; libraries such as `pytorch-grad-cam` do this.)

**Follow-ups:**
- *Why the last conv layer?* Best balance of high-level meaning and spatial information.
- *Is attention an explanation?* Not reliably; high attention does not mean high influence.
- *Regulated settings?* Combine local explanations with global audits, document limitations.

**Common mistakes:** treating heatmaps as causal proof; skipping the ReLU; using it on a layer with no spatial structure; explaining only correct predictions; presenting attention weights as explanations.

### Q42 ⭐ 🟡 Dice coefficient vs IoU vs pixel accuracy for segmentation: when is each used?
**Asked at:** all types
**Say this first (1 line):** IoU and Dice both measure overlap between predicted and true masks and are the standard for segmentation, while pixel accuracy is misleading whenever the object is small compared to the background.

**Then explain:**
- **IoU (Jaccard):** `|P ∩ T| / |P ∪ T|`. **Dice (F1 on pixels):** `2|P ∩ T| / (|P| + |T|)`. They are related: `Dice = 2 IoU / (1 + IoU)`, so they rank models the same way but Dice is always higher (for IoU between 0 and 1).
- **Pixel accuracy:** fraction of pixels correct; a model predicting all background on a tiny tumour still scores 99%.
- **Where used:** IoU/mIoU (mean over classes) for benchmarks (Cityscapes, Pascal VOC); Dice in medical imaging and as a loss function (Dice loss handles class imbalance, often combined with cross-entropy).
- **Dice vs IoU in practice:** IoU punishes the same error harder than Dice does (the example below: Dice 0.64 vs IoU 0.47 for the same pair of masks), so never compare a Dice number with an IoU number.
- **Edge cases:** empty ground truth and empty prediction give 0/0: define it as 1 (or skip) explicitly. Boundary-sensitive tasks also use Hausdorff distance.

**Example:** A 10x10 true region and a prediction shifted by 2 pixels each way on a 100x100 image: IoU 0.471, Dice 0.640, pixel accuracy 99.3% (verified below). Accuracy looks great, overlap tells the real story.

**Code:**
```python
import numpy as np
def iou_dice(p, t):
    inter = (p & t).sum(); return inter / (p | t).sum(), 2 * inter / (p.sum() + t.sum())
t = np.zeros((100, 100), bool); t[40:50, 40:50] = True
p = np.zeros_like(t); p[42:52, 42:52] = True
i, d = iou_dice(p, t)
print(round(i, 3), round(d, 3), (p == t).mean())    # 0.471 0.64 0.9928
```

**Follow-ups:**
- *Which loss?* Cross-entropy + Dice (or focal/Tversky for tiny objects).
- *Why not accuracy for imbalance?* Same reason as classification: majority class dominates.
- *Per-image or per-dataset?* Per-class, then average; per-image averages weigh empty images oddly.

**Common mistakes:** reporting pixel accuracy on imbalanced masks; mixing up Dice and IoU values across papers; not handling empty masks; thresholding probabilities differently for train and eval.

### Q43 ⭐ 🟡 How do you deal with noisy or ambiguous labels in image or text datasets (inter-annotator agreement, label cleaning)?
**Asked at:** product cos (Flipkart/Swiggy-type)
**Say this first (1 line):** Measure how much annotators disagree (Cohen's/Fleiss' kappa), fix the guidelines where they disagree, and then find and fix likely wrong labels with model-based methods (confident learning), while using noise-robust training for what remains.

**Then explain:**
- **Inter-annotator agreement:** raw agreement is inflated by chance; **Cohen's kappa** `(p_o - p_e) / (1 - p_e)` corrects for it (two raters; Fleiss/Krippendorff for more). Rough guide: above 0.8 strong, 0.6-0.8 good, below 0.4 weak. Low kappa means ambiguous guidelines or genuinely subjective labels: fix the definition before blaming the model.
- **Reduce noise at source:** clear guidelines with examples, multiple annotators + majority vote or adjudication, gold-standard check items, annotator quality tracking, keep soft labels where genuine ambiguity exists.
- **Find noisy labels:** train with cross-validation, flag examples where the out-of-fold model confidently disagrees with the given label (confident learning / cleanlab), or those with persistent high loss; review them manually and fix.
- **Train with noise:** label smoothing, robust losses (symmetric cross-entropy, bootstrapping), early stopping (networks memorise noise late), co-teaching, using soft labels from annotator votes.
- **Evaluate:** the test set must be cleaned most carefully, else metrics are capped by label noise.
- **Know the ceiling:** with 85% inter-annotator agreement, expecting 99% model accuracy is unrealistic.

**Example:** Two annotators agree on 85% of 100 items, but with a 40/60 class split kappa is 0.68, not 0.85. Separately, on synthetic data with 10% flipped labels, picking the 60 examples whose given label gets the lowest out-of-fold probability finds 55 of the 60 flipped ones (verified below).

**Code:**
```python
import numpy as np
from sklearn.metrics import cohen_kappa_score
from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LogisticRegression
a = np.array([1]*40 + [0]*60); b = a.copy(); b[:10] = 0; b[40:45] = 1
print(round((a == b).mean(), 2), round(cohen_kappa_score(a, b), 3))   # 0.85 0.681
rng = np.random.default_rng(0); X = rng.normal(size=(600, 5)); y = (X[:, 0] + X[:, 1] > 0).astype(int)
flip = rng.choice(600, 60, replace=False); yn = y.copy(); yn[flip] = 1 - yn[flip]   # 10% label noise
pr = cross_val_predict(LogisticRegression(), X, yn, cv=5, method="predict_proba")
sus = np.argsort(pr[np.arange(600), yn])[:60]                         # lowest prob of the GIVEN label
print(len(set(sus) & set(flip)), "of 60 flipped found")                # 55 of 60
```

**Follow-ups:**
- *Is noise always bad?* Random noise is tolerable with lots of data; systematic (class-dependent) noise biases the model.
- *LLM annotators?* Useful for cheap first labels; measure their kappa against humans.
- *Soft labels?* Keep the annotator vote distribution and train on it for ambiguous tasks.

**Common mistakes:** quoting raw agreement instead of kappa; cleaning the train set but leaving the test set noisy; deleting hard examples that are actually rare true classes; flagging noisy labels with a model that was trained on those same examples instead of out-of-fold predictions (the model has already memorised the noise).

### Q44 ⭐ 🟡 Sequence-to-sequence basics: what are the encoder-decoder, teacher forcing and beam search?
**Asked at:** all types
**Say this first (1 line):** A seq2seq model uses an encoder to read the input into a representation and a decoder to generate the output one token at a time; teacher forcing feeds the true previous token during training, and beam search keeps the k best partial outputs at inference.

**Then explain:**
- **Encoder-decoder:** encoder compresses the source (translation: French sentence); decoder produces the target token by token, each step conditioned on previous outputs and the encoder. Early versions used one fixed-size vector (bottleneck); **attention** lets the decoder look at all encoder states each step. Transformers (T5, BART, original Attention paper) use the same layout; decoder-only LLMs drop the encoder.
- **Teacher forcing:** in training the decoder input at step t is the ground-truth token t-1, not its own prediction: faster, stable convergence. Downside, **exposure bias**: at inference it sees its own (sometimes wrong) tokens, which it never saw in training. Mitigations: scheduled sampling, sequence-level training/RL, more robust decoding.
- **Greedy decoding:** pick the most probable token each step; fast but can miss better sequences.
- **Beam search:** keep the top k partial sequences by total log-probability, expand each, prune back to k. Better sequences than greedy at k times the cost. Add length normalisation (long sequences have lower probability) and stop on end token.
- **Sampling** (top-k, top-p/nucleus, temperature) is used for creative generation; beam search for translation/summarisation where accuracy matters.

**Example:** Greedy picks the first-step token with probability 0.5 and ends with sequence `a x` (prob 0.25), but beam search with k=2 finds `b x` with probability 0.4 x 0.9 = 0.36, which is better (verified below).

**Code:**
```python
import math
probs = {(): {"a": .5, "b": .4, "c": .1}, ("a",): {"x": .5, "y": .5}, ("b",): {"x": .9, "y": .1}}
step = lambda seq: probs.get(tuple(seq), {"<e>": 1.0})
def greedy():
    s = []
    for _ in range(2): d = step(s); s.append(max(d, key=d.get))
    return s
def beam(k=2):
    beams = [([], 0.0)]
    for _ in range(2):
        cand = [(s + [w], lp + math.log(p)) for s, lp in beams for w, p in step(s).items()]
        beams = sorted(cand, key=lambda z: -z[1])[:k]
    return [(s, round(math.exp(lp), 2)) for s, lp in beams]
print(greedy(), beam(2))    # ['a', 'x'] [(['b', 'x'], 0.36), (['a', 'x'], 0.25)]
```

**Follow-ups:**
- *Why does bigger beam sometimes hurt?* Favours short or generic outputs; use length penalty.
- *Why do encoder-decoder models suit translation/summarisation?* Input is fully known and read bidirectionally.
- *Cost of decoding?* Sequential (one token per step), so latency grows with output length; KV caching avoids recomputing past states.

**Common mistakes:** saying teacher forcing is used at inference; no mention of attention fixing the bottleneck; calling beam search optimal (it is still approximate); forgetting length normalisation.

### Q45 ⭐ 🟡 Explain contrastive learning / sentence-transformers and how a bi-encoder differs from a cross-encoder (reranking).
**Asked at:** Europe product cos (Spotify/Zalando/Booking/Klarna-type)
**Say this first (1 line):** Contrastive learning trains embeddings so matching pairs are close and non-matching pairs are far; sentence-transformers do this for text, and a bi-encoder embeds query and document separately (fast, indexable) while a cross-encoder reads them together (more accurate, slow), so you retrieve with the bi-encoder and rerank with the cross-encoder.

**Then explain:**
- **Contrastive loss (InfoNCE):** in a batch of N (anchor, positive) pairs, treat the other N-1 positives as negatives; for each anchor maximise softmax probability of its own positive over all positives, using cosine similarity divided by a temperature (e.g. 0.05). Pairs come from labelled data (question-answer, NLI, click logs) or augmentation (SimCSE: same sentence with different dropout).
- **Sentence-transformers:** BERT-like model + mean pooling, trained contrastively (Siamese setup), output one vector per sentence; similar meaning gives high cosine.
- **Bi-encoder:** `embed(query)` and `embed(doc)` independently; document vectors are precomputed and stored in a vector index (ANN), so search over millions takes milliseconds. Weaker because query and document never interact inside the model.
- **Cross-encoder:** feeds `[query; doc]` jointly through the transformer with full cross-attention and outputs a relevance score. Much more accurate but needs one forward pass per (query, doc) pair, so only usable on a shortlist (top 50-200).
- **Pipeline:** BM25/dense retrieval -> top 100 -> cross-encoder rerank -> top 10. Hard negatives (similar but wrong docs) improve training a lot.
- **Late interaction (ColBERT):** keeps token-level vectors, a middle ground.

**Example:** 1M products: the bi-encoder indexes them offline; at query time one query embedding plus ANN search takes ~10 ms. Reranking the top 100 with a cross-encoder costs 100 forward passes; scoring all 1M would be impossible.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
a = rng.normal(size=(4, 16)); p = a + 0.1 * rng.normal(size=(4, 16))      # anchors and their positives
a /= np.linalg.norm(a, axis=1, keepdims=True); p /= np.linalg.norm(p, axis=1, keepdims=True)
def info_nce(a, p, tau=0.05):
    S = a @ p.T / tau; S -= S.max(1, keepdims=True)
    logp = S - np.log(np.exp(S).sum(1, keepdims=True)); return -np.mean(np.diag(logp))
print(round(info_nce(a, p), 4), round(info_nce(a, p[::-1]), 2))   # ~0.0 (matched)  vs ~25 (mismatched)
```
(sentence-transformers usage: `SentenceTransformer(...).encode(texts)`, `CrossEncoder(...).predict(pairs)`; not executed: library not installed.)

**Follow-ups:**
- *Why large batches help?* More in-batch negatives make the task harder and the embeddings better.
- *Why temperature?* Low tau sharpens the softmax, focusing on hard negatives.
- *Can the cross-encoder be used for retrieval?* Only on candidates; it cannot be pre-indexed.

**Common mistakes:** using a cross-encoder to score the whole corpus; false negatives in in-batch negatives (duplicate items); embedding with one model and querying with another; not normalising before cosine.

### Q46 ⭐ 🟡 Multilingual and code-mixed text (Hinglish): how would you approach classification or search?
**Asked at:** product cos (Flipkart/Swiggy-type)
**Say this first (1 line):** Use a multilingual pretrained model (XLM-R, mBERT, MuRIL, IndicBERT, or multilingual embeddings), normalise transliteration/spelling noise, and fine-tune on in-domain Hinglish examples; for search combine lexical (BM25 with character n-grams) and multilingual dense retrieval.

**Then explain:**
- **Why it is hard:** code-mixing (Hindi in Roman script mixed with English), no standard spelling ("kya", "kyaa", "kia"), slang, emojis, and few labelled datasets. Word-level vocabularies explode.
- **Preprocessing:** lowercase, collapse repeated letters, normalise emojis; optionally transliterate Roman Hindi to Devanagari (or the reverse) and apply language identification at token level. Do not over-clean: negations and slang carry signal.
- **Models:** XLM-R or MuRIL (trained on Indian languages and transliterated text) fine-tuned for classification; fastText with character n-grams as a cheap, strong baseline (robust to spelling variants); multilingual sentence embeddings (LaBSE, multilingual-e5) for similarity; LLMs with few-shot for low data. Subword tokenization (Q27) absorbs spelling variation partly.
- **Data:** augment with synthetic transliteration/back-translation; collect real user queries; use an LLM to generate and label Hinglish examples, then verify with humans.
- **Search:** index both original and normalised/transliterated text; use character n-gram BM25 for spelling variants plus dense multilingual retrieval; add query rewriting/spell-correction; evaluate on real Hinglish query logs.
- **Evaluation:** report metrics by language/script slice (Hindi, English, Hinglish) so the mixed slice does not hide behind the English average.

**Example:** Query "sasta mobile under 10k": BM25 on English-only titles fails on "sasta" (cheap); a multilingual embedding places it near "cheap phone budget", and the hybrid retrieval returns relevant listings.

**Follow-ups:**
- *Transliterate or not?* Try both; transliteration helps Hindi-specific models, while multilingual models see enough Romanized text.
- *Language ID on mixed text?* Token-level or sentence-level with confidence; do not drop low-confidence rows.
- *Cheap baseline?* TF-IDF char n-grams (2-5) + logistic regression often beats a poorly fine-tuned transformer on small data.

**Common mistakes:** using an English-only tokenizer or stopword list; evaluating on clean Devanagari only; heavy normalisation that deletes signal; one aggregate metric hiding weak mixed-script performance.

### Q47 ⭐ 🟡 How do you choose between a distilled small model and a large model for production text inference (quantization, ONNX, latency, cost)?
**Asked at:** product cos (Flipkart/Swiggy-type)
**Say this first (1 line):** Start from the requirement (accuracy target, p95 latency, throughput, cost per 1k requests), try the smallest model that meets the accuracy bar, then compress it (distillation, quantisation, ONNX/TensorRT) before paying for a bigger one.

**Then explain:**
- **Decide with numbers:** build a table on the same test set: accuracy/F1, p50/p95 latency on production hardware, throughput, cost per 1k requests, memory. Pick the cheapest option within the accuracy tolerance (e.g. within 1 point of the large model).
- **Distillation:** train a small student (DistilBERT, TinyBERT) to mimic the teacher's soft probabilities, optionally on lots of unlabelled data; typically keeps 95-99% of accuracy at half size or smaller. Also: LLM labels the data, a small classifier is trained on it.
- **Quantisation:** FP32 -> FP16/INT8 (or 4-bit for LLMs): about 2-4x smaller and faster, small accuracy loss; post-training (needs a calibration set) or quantisation-aware training.
- **Pruning / smaller sequence length / early exit** and **caching** repeated inputs.
- **Runtime:** export to ONNX Runtime/TensorRT, batching, dynamic batching on GPU, CPU inference for small models; a **cascade** (small model for easy cases, large model only for low-confidence ones) is usually the best cost/quality trade.
- **When large wins:** complex reasoning, many tasks, little labelled data, long-tail inputs where a prompt beats a trained model; use an API/hosted LLM if volume is low.

**Example:** Dynamic INT8 quantisation of a small two-layer MLP head: weights file drops from 2.37 MB to 0.60 MB (about 4x), with identical predictions on a test batch (verified below; PyTorch is migrating this API to torchao, so check the current docs for the import).

**Code:**
```python
import io, torch, torch.nn as nn
torch.manual_seed(0)
m = nn.Sequential(nn.Linear(768, 768), nn.ReLU(), nn.Linear(768, 2)).eval()
# note: torch.ao.quantization prints a DeprecationWarning in recent torch (the API is moving to torchao); output below was run with it
q = torch.ao.quantization.quantize_dynamic(m, {nn.Linear}, dtype=torch.qint8)
x = torch.randn(4, 768)
print(m(x).argmax(1).tolist() == q(x).argmax(1).tolist())        # True
def mb(mod): b = io.BytesIO(); torch.save(mod.state_dict(), b); return round(b.getbuffer().nbytes / 1e6, 2)
print(mb(m), mb(q))                                              # 2.37 0.6  (MB)
```

**Follow-ups:**
- *Does quantisation always keep accuracy?* Usually within 1%; check per-slice and outlier-heavy layers.
- *Latency vs throughput?* Batching raises throughput but also latency; tune per SLA.
- *Cost of a GPU?* Only worth it above a traffic level where CPU instances cannot meet p95.

**Common mistakes:** choosing the largest model by default; benchmarking latency without preprocessing/tokenisation; quantising without re-evaluating; comparing models on different test sets; ignoring cost per request.

### Q48 ⭐ 🟡 How do you check for bias and PII/privacy issues when training on text or image data?
**Asked at:** Europe product cos (Spotify/Zalando/Booking/Klarna-type)
**Say this first (1 line):** Audit the data and the model by subgroup for unequal performance and stereotyped outputs, detect and remove or mask personal data before training, and document a legal basis and retention policy (GDPR in Europe, DPDP Act in India).

**Then explain:**
- **Bias checks:**
  - **Data:** representation by group (gender, region, skin tone, language), label balance, annotator bias, proxies for sensitive attributes (pincode, name).
  - **Model:** metrics per subgroup (error rate, false positive/negative rate, recall gap); fairness measures such as demographic parity difference or equalised odds; for text, counterfactual tests (swap names/pronouns and check outputs) and benchmarks like WEAT/StereoSet; for images, face/skin-tone performance gaps.
  - **Fix:** rebalance/reweight, collect more data for weak groups, remove proxy features, threshold per group where lawful, human review for high-stakes use.
- **PII detection:** regex for structured items (email, phone, PAN, Aadhaar, card numbers), NER models (e.g. Presidio/spaCy) for names and addresses; faces and licence plates in images (detect and blur). Redact/pseudonymise before training; never train on raw PII without need.
- **Privacy risks in models:** memorisation and extraction of training text; membership inference. Mitigate with deduplication, minimal data, differential privacy (DP-SGD) where needed, access control, and testing for memorisation (canary strings).
- **Governance:** consent/legal basis, purpose limitation, retention/deletion (right to erasure), data minimisation, data cards/model cards, DPIA for high-risk uses, and the EU AI Act risk categories where relevant.

**Example:** Before training a support-ticket classifier, a regex scrub replaces phone numbers, emails and PAN numbers with tags (verified below), and an NER pass catches names; recall is checked on a hand-labelled sample because regex misses free-form PII.

**Code:**
```python
import re
txt = "Call Rahul on 9876543210 or mail rahul.k@example.com, PAN ABCDE1234F"
pats = {"EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+", "PHONE": r"\b[6-9]\d{9}\b", "PAN": r"\b[A-Z]{5}\d{4}[A-Z]\b"}
for k, p in pats.items(): txt = re.sub(p, f"<{k}>", txt)
print(txt)   # Call Rahul on <PHONE> or mail <EMAIL>, PAN <PAN>   (note: the name "Rahul" needs NER)
```

**Follow-ups:**
- *Fairness metrics conflict?* Yes; demographic parity, equalised odds and calibration cannot all hold at once when base rates differ; pick based on the harm.
- *Can you just drop the sensitive attribute?* No; proxies remain; keep it for auditing, not as a feature.
- *Is anonymised data safe?* Re-identification is possible from combinations; prefer aggregation/differential privacy for sensitive data.

**Common mistakes:** only reporting overall accuracy; relying on regex alone; removing the sensitive column and calling it fair; ignoring memorisation in LLM fine-tuning; no retention/deletion plan.

### Q49 ⭐ 🔴 Explain the O(n^2) attention cost problem and approaches to mitigate it (sparse, linear, Flash attention) at a high level.
**Asked at:** all types
**Say this first (1 line):** Self-attention compares every token with every other, so compute and memory grow with the square of sequence length; fixes are sparse patterns, low-rank/linear approximations, and Flash attention, which computes exact attention without ever storing the full n x n matrix.

**Then explain:**
- **The cost:** scores `QK^T` are n x n, so time is O(n^2 d) and the naive score matrix needs O(n^2) memory per head. At n = 8,192 in fp16 one head's matrix is 8192^2 x 2 bytes = 134 MB per layer (verified below); at 128k it is impossible without tricks. (The MLP layers are only linear in n; attention dominates at long n.)
- **Sparse attention:** each token attends to a subset: local window + a few global tokens (Longformer), plus random links (BigBird); cost about O(n w). Cheaper, but approximate.
- **Linear / low-rank attention:** Linformer (project K, V to a low rank), Performer (kernel feature maps) give O(n); usually some quality loss, so less used in frontier LLMs.
- **Flash attention:** exact attention, but tiled so blocks of Q, K, V live in fast on-chip SRAM and the softmax is computed online (running max and sum), so the n x n matrix is never written to slow GPU memory. Same O(n^2) FLOPs, but memory O(n) and 2-4x faster because it is memory-bandwidth bound.
- **Other tricks:** KV cache and grouped-query attention for decoding, sliding-window attention (Mistral), state-space models (Mamba) as alternatives, retrieval to avoid long contexts.

**Example:** The online-softmax idea in NumPy: process K/V in blocks, keeping a running max `m`, normaliser `l`, and output `o`; the result matches full attention exactly (verified below).

**Code:**
```python
import numpy as np
def attn(Q, K, V):
    S = Q @ K.T / np.sqrt(Q.shape[1]); S -= S.max(1, keepdims=True)
    P = np.exp(S); P /= P.sum(1, keepdims=True); return P @ V
def online(Q, K, V, blk=16):                 # flash-style: never builds the n x n matrix
    n = len(Q); m = np.full(n, -np.inf); l = np.zeros(n); o = np.zeros_like(Q)
    for s in range(0, len(K), blk):
        S = Q @ K[s:s+blk].T / np.sqrt(Q.shape[1]); mn = np.maximum(m, S.max(1))
        sc = np.exp(m - mn); Pb = np.exp(S - mn[:, None])
        l = l * sc + Pb.sum(1); o = o * sc[:, None] + Pb @ V[s:s+blk]; m = mn
    return o / l[:, None]
rng = np.random.default_rng(0); Q, K, V = (rng.normal(size=(64, 8)) for _ in range(3))
print(np.allclose(attn(Q, K, V), online(Q, K, V)))     # True
```

**Follow-ups:**
- *Does Flash attention change results?* No, it is exact (up to floating-point order), unlike sparse/linear methods.
- *Why not always linear attention?* Quality gaps on tasks needing precise recall; hardware-efficient exact attention won out so far.
- *Decoding cost?* Each new token attends to all past ones: O(n) per token with a KV cache, memory grows with context.

**Common mistakes:** saying Flash attention reduces FLOPs (it reduces memory traffic); saying it is approximate; forgetting memory (not only time) is the bottleneck; ignoring the KV cache at inference.

### Q50 ⭐ 🔴 What is self-supervised pretraining for vision (SimCLR, MAE, CLIP)? How would you use CLIP for zero-shot image search?
**Asked at:** Europe product cos (Spotify/Zalando/Booking/Klarna-type)
**Say this first (1 line):** Self-supervised vision learns useful features from unlabelled images by inventing a task (match two views of the same image, or reconstruct hidden patches); CLIP learns from image-text pairs so images and text share one embedding space, which gives zero-shot classification and image search with a text query.

**Then explain:**
- **SimCLR (contrastive):** make two random augmentations (crop, colour jitter, blur) of each image; pull their embeddings together and push other images in the batch apart (InfoNCE loss, Q45). Needs large batches/many negatives.
- **MAE (masked autoencoder):** mask about 75% of the patches, encode only the visible ones with a ViT, reconstruct the missing pixels with a light decoder; efficient and scales well. (Related: DINO/DINOv2 self-distillation, BYOL without negatives.)
- **CLIP:** an image encoder and a text encoder trained on about 400M image-caption pairs with a contrastive loss: in a batch, each image should match its own caption and vice versa. Result: images and text live in the same vector space.
- **Why useful:** pretrained features transfer with few labels (linear probe or fine-tune); CLIP also transfers without labels.
- **Zero-shot classification with CLIP:** embed text prompts ("a photo of a {class}"), embed the image, pick the class with highest cosine similarity (softmax with a temperature of about 100 over the similarities).
- **Zero-shot image search:** embed all images once and store them in a vector index; embed the text query, retrieve nearest image vectors. Improve with prompt wording, a domain fine-tune, and reranking.
- **Limits:** weak at counting, fine-grained attributes, text-in-image (OCR), spatial relations; inherits web biases; domain-specific images (medical) need adaptation.

**Example:** Toy version with stand-in embeddings: an image vector close to the "dog" text vector gets softmax probability about 1.0 for dog and 0.0 for cat and car (verified below).

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
labels = ["cat", "dog", "car"]
txt = rng.normal(size=(3, 32)); txt /= np.linalg.norm(txt, axis=1, keepdims=True)   # stand-in for text-encoder outputs
img = txt[1] + 0.1 * rng.normal(size=32); img /= np.linalg.norm(img)                # stand-in for an image embedding
z = 100 * img @ txt.T; p = np.exp(z - z.max()); p /= p.sum()
print(dict(zip(labels, p.round(3).tolist())))   # {'cat': 0.0, 'dog': 1.0, 'car': 0.0}
# Real CLIP: model.encode_image / encode_text then the same cosine + softmax (not executed: transformers not installed)
```

**Follow-ups:**
- *Contrastive vs masked pretraining?* Contrastive gives strong linear-probe features but needs augmentations/negatives; MAE is cheaper and better when fine-tuned, weaker on linear probe.
- *Why does CLIP generalise?* Huge, diverse web data and language as flexible supervision.
- *Prompt engineering?* Averaging several templates ("a photo of a...") improves zero-shot accuracy.

**Common mistakes:** thinking CLIP needs labels for each new class; forgetting to normalise embeddings; ignoring CLIP's weakness on fine-grained/specialised domains; mixing up what is masked in MAE (patches, not text tokens).

### Q51 ⭐ 🔴 Design an embedding-based product search system (text + image) for an e-commerce catalogue: indexing, retrieval, evaluation, cold start.
**Asked at:** product cos (Flipkart/Swiggy-type)
**Say this first (1 line):** Embed products (title/description text plus image) and queries into a shared vector space, index them in an approximate nearest-neighbour (ANN) store, retrieve candidates together with keyword search, rerank with a learned model, and evaluate with recall@k/NDCG offline plus A/B tests online.

**Then explain (framework):**
- **Requirements:** catalogue size (e.g. 50M items), query latency (under 100 ms p95), freshness (new products within minutes), languages (Hinglish, Q46), business goal (conversion, not only relevance).
- **Data:** product text, images, attributes, category; query logs with clicks/add-to-cart/purchases as relevance signals (watch position bias); synthetic queries from an LLM for cold-start tails.
- **Model:** text encoder (multilingual sentence-transformer) and image encoder (CLIP-style); fine-tune contrastively on (query, clicked product) pairs with hard negatives; fuse text + image vectors (concatenate or average, or a CLIP-like joint space so text queries retrieve images directly). Query and product towers are separate (bi-encoder, Q45).
- **Indexing/retrieval:** precompute item vectors, store in an ANN index (HNSW or IVF-PQ via FAISS/ScaNN/Milvus/OpenSearch); product quantisation shrinks memory (e.g. 768 floats = 3 KB -> 64 bytes); shard by category; filters for in-stock/price applied as pre- or post-filter. **Hybrid:** merge BM25 results (exact model numbers, brands) and dense results (semantics).
- **Ranking:** cross-encoder or gradient-boosted/learning-to-rank model on top 100-500 with features (price, rating, popularity, personalisation).
- **Evaluation:** offline on judged queries: recall@k, MRR, NDCG@10; ANN recall vs exact (e.g. 95%+); slice by head/torso/tail queries and language; online A/B on CTR, add-to-cart, conversion, null-result rate, latency.
- **Cold start:** new items have no clicks, so rely on content embeddings (text + image) and attributes; boost exploration (small slot for new items); for new users/queries use popularity and semantic matching; seed training with LLM-generated queries.
- **Monitoring/trade-offs:** embedding drift and re-indexing when the model changes (version both sides together), index refresh cadence, memory vs recall (PQ), latency vs accuracy (HNSW `ef`), bias toward popular items.

**Example:** Query "red floral kurti": BM25 finds exact "kurti" titles; dense text retrieval finds "ethnic top flower print"; the image tower finds visually floral red items missing keywords; the merged top 200 are reranked and the top 20 shown.

**Code:**
```python
def recall_at_k(ranked, rel, k): return len(set(ranked[:k]) & rel) / len(rel)
def mrr(ranked, rel): return next((1 / (i + 1) for i, r in enumerate(ranked) if r in rel), 0)
ranked, rel = [5, 2, 9, 1], {2, 1}                  # model ranking vs relevant items
print(recall_at_k(ranked, rel, 3), mrr(ranked, rel))   # 0.5 0.5
```

**Follow-ups:**
- *How do you update the index?* Incremental inserts for new items, periodic full rebuild after a model change.
- *Exact vs ANN?* ANN trades about 1-5% recall for 100x speed; measure it against brute force.
- *Position bias in click data?* Use inverse propensity weighting or randomised experiments.

**Common mistakes:** judging only by offline similarity, not business metrics; changing the encoder without re-embedding the catalogue; no keyword/exact-match path; ignoring cold-start items; no ANN-vs-exact recall check.

### Q52 ⭐ 🔴 Explain OCR / document-understanding pipelines (e.g. invoices, KYC) and how you would evaluate them.
**Asked at:** GCCs / MNCs (Walmart, JPMC, Amazon India, Microsoft IDC)
**Say this first (1 line):** A document pipeline cleans the image, detects text regions, recognises the characters (OCR), understands layout and key fields (key-value extraction with a layout-aware model or LLM), validates the values, and routes low-confidence cases to humans; I evaluate each stage separately and the end-to-end field accuracy.

**Then explain (pipeline):**
- **1. Ingest/preprocess:** classify document type, deskew, denoise, binarise, fix resolution (about 300 DPI); detect and handle rotations, stamps, handwriting.
- **2. Text detection + recognition (OCR):** engines such as Tesseract, PaddleOCR, cloud OCR, or a detector (DBNet/CRAFT) plus a recogniser (CRNN with CTC loss, or transformer OCR like TrOCR). Output: words/lines with boxes and confidences.
- **3. Layout analysis:** find tables, headers, key-value regions, reading order.
- **4. Information extraction:** map text to fields (invoice number, date, total, PAN): rules/regex for fixed formats; layout-aware transformers (LayoutLM, Donut) fine-tuned on labelled forms; or a multimodal LLM with a JSON schema. Table structure recognition for line items.
- **5. Validation and business rules:** checksum/format checks (PAN pattern, GST number), arithmetic (line items sum to total), dates plausible, cross-check with master data; confidence thresholds.
- **6. Human in the loop:** low-confidence or failed validation goes to a reviewer; corrections feed back as training data.
- **Evaluation:**
  - **OCR:** CER (character error rate) and WER = edit distance / reference length.
  - **Detection:** precision/recall/F1 of text boxes at IoU 0.5 (Q32).
  - **Extraction:** per-field exact-match precision/recall/F1 (normalise formatting first: "1,250.00" vs "1250"), and **document-level straight-through-processing rate** (share of documents with all critical fields correct without review).
  - **Business:** cost per document, review rate, error cost (a wrong amount costs more than a blank).
  - Slice by document template, scan quality, language, handwriting; hold out whole vendors/templates for a true generalisation test.
- **KYC specifics:** face match, liveness, tamper/forgery detection, PII handling and masking (Q48), audit trail, regulatory retention.

**Example:** Reference `Invoice No 10234 Total 1,250.00` vs OCR `Invoice No 1O234 Total 1.250.00` (letter O for zero, dot for comma): CER 0.065 (2 edits in 31 characters) but WER 0.4 (2 of 5 words wrong), and the extracted total fails the exact-match check; validation (amount format, sum of lines) would catch it (verified below).

**Code:**
```python
def edit(a, b):                                   # Levenshtein distance
    dp = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, len(b) + 1):
            prev, dp[j] = dp[j], min(dp[j] + 1, dp[j-1] + 1, prev + (a[i-1] != b[j-1]))
    return dp[-1]
ref, hyp = "Invoice No 10234 Total 1,250.00", "Invoice No 1O234 Total 1.250.00"
print(round(edit(ref, hyp) / len(ref), 3), round(edit(ref.split(), hyp.split()) / len(ref.split()), 3))   # 0.065 0.4
```

**Follow-ups:**
- *OCR vs layout-aware model errors?* Evaluate each stage on its own so you know where errors start; OCR mistakes propagate to extraction.
- *Handwriting/low quality?* Better scanning guidance, specialised recognisers, human review thresholds.
- *LLM for extraction?* Good with few labels; add schema validation and compare against field-level gold labels, watch for hallucinated values.

**Common mistakes:** only reporting CER while the business needs correct fields; no formatting normalisation before matching; random splits that leak templates into the test set; no validation rules or human fallback; ignoring confidence calibration.
