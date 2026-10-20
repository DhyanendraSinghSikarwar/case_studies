# Book 1 Part 09 — Sources & research notes (NLP & CV)

Date: 2026-10-20. WebSearch worked (US-only, standard mode); WebFetch was not used. 6 searches run. Result pages were not individually opened; findings below are from search-result snippets/summaries only.

## Honest caveat on frequency
Searches returned mostly question banks and prep blogs, NOT first-hand 2025-26 interview experiences. Per-question source counts are therefore topic-presence counts across banks, not counts of independent candidate reports. Stars are a blend of (a) presence across multiple banks and (b) expert judgement of loop frequency. Not found: GFG/AmbitionBox/Blind first-hand DS-NLP experiences for Flipkart, Swiggy, PhonePe, Microsoft IDC, Spotify, Zalando, Booking, Klarna (searched; nothing relevant surfaced). No company-specific claims are made beyond the "Asked at" typing in the question file, which is type-level and partly inferential.

## Sources actually seen (URLs from search results)
| Source | URL | Used for |
|---|---|---|
| DataCamp NLP interview questions (45 Qs, updated Feb 2026) | https://www.datacamp.com/blog/nlp-interview-questions | TF-IDF, Word2Vec/GloVe/FastText, metrics |
| WeCreateProblems NLP | https://www.wecreateproblems.com/interview-questions/nlp-interview-questions | BERT vs word2vec, attention, pretrain vs fine-tune |
| Dataford TF-IDF list | https://dataford.io/questions/lists/tf-idf-questions | TF-IDF vs embeddings trade-offs |
| techinterview.org CV guide | https://www.techinterview.org/post/3233460081/computer-vision-interview-questions-cnns-object-detection-and-transfer-learning/ | CNN, ResNet, detection/anchors, transfer learning, domain shift |
| Hyring CV questions (2026) | https://hyring.com/jobseeker-toolkit/interview-questions/technical/computer-vision | metrics, deployment constraints |
| 365DataScience CV questions (2026) | https://365datascience.com/career-advice/job-interview-tips/computer-vision-interview-questions/ | top CV Qs |
| Jotform CV questions | https://www.jotform.com/interview-questions/computer-vision-interview-questions/ | overfitting, pooling |
| techinterview.org RAG vs fine-tuning vs prompting 2026 | https://www.techinterview.org/post/3233475094/rag-fine-tuning-prompting-decision-2026/ | GenAI decision framework |
| techinterview.org ML engineer post-LLM era | https://www.techinterview.org/post/3233474925/ml-engineer-interview-post-llm-era/ | AI-era shift |
| Glassdoor Swiggy review (Aug 2025, via search) | https://www.glassdoor.com.hk/Interview/Swiggy-Interview-E952680-RVW25694400.htm | process: DS/SQL, ML/DL round, HR; L1 vs L2 asked (not NLP-specific) |
| Glassdoor Amazon reviews | https://www.glassdoor.com.hk/Interview/Amazon-Interview-E6036-RVW92165348.htm | ML breadth/depth rounds; one NLP-role candidate reported "NLP specific questions" without detail |
| Blind Microsoft DS thread | https://www.teamblind.com/post/data-scientist-microsoft-ougupgc6 | question-asking thread, no answers seen |

Not found: any source explaining IoU/mAP directly (these were added by gap-check from standard CV interview knowledge); no source on BLEU/ROUGE/perplexity questions.

## AI-era changes noted
- Interviews now probe decision frameworks: prompt first, RAG for changing knowledge, fine-tune for behaviour/format; plus cost, latency, routing to cheaper models.
- "TF-IDF baseline vs transformer" trade-off questions are common; strong answers justify the simpler model.
- Classical NER/text-classification questions increasingly get an "or would you just use an LLM?" follow-up.
- CV: emphasis on domain shift, edge deployment, labelled-data scarcity; ViT/CLIP appear as follow-ups.
- Likely de-emphasised: hand-deriving word2vec/LSTM equations, LDA details (kept at low stars).

## Question table (53 questions; sorted star desc, then easy->hard)
| Q | Star/Diff | Question | Origin |
|---|---|---|---|
| Q1 | ⭐⭐⭐ 🟢 | How does TF-IDF work, and what are its limitations compared with embeddings? | found in sources (topic present in listed question banks) |
| Q2 | ⭐⭐⭐ 🟢 | Bag-of-Words vs TF-IDF vs word embeddings: when would you use each? | found in sources (topic present in listed question banks) |
| Q3 | ⭐⭐⭐ 🟢 | Word2Vec vs GloVe vs FastText: how do they differ, and how are they trained? | found in sources (topic present in listed question banks) |
| Q4 | ⭐⭐⭐ 🟢 | What is IoU, and how is it used in object detection? | added: expert gap-check |
| Q5 | ⭐⭐⭐ 🟢 | How do you handle overfitting when training a CNN on a small image dataset (augmentation, regularization, early stopping)? | found in sources (topic present in listed question banks) |
| Q6 | ⭐⭐⭐ 🟡 | How do you build a text classifier end to end (TF-IDF + logistic regression baseline up to a fine-tuned transformer)? How do you choose between them? | found in sources (topic present in listed question banks) |
| Q7 | ⭐⭐⭐ 🟡 | What is the difference between static (Word2Vec) and contextual (BERT) embeddings? | found in sources (topic present in listed question banks) |
| Q8 | ⭐⭐⭐ 🟡 | Explain self-attention and the transformer architecture. Why did transformers replace RNNs/LSTMs? | found in sources (topic present in listed question banks) |
| Q9 | ⭐⭐⭐ 🟡 | What is BERT, how is it pretrained (MLM, NSP), and how do you fine-tune it for classification? | found in sources (topic present in listed question banks) |
| Q10 | ⭐⭐⭐ 🟡 | Explain transfer learning in CNNs. When do you freeze layers versus fine-tune the whole network? | found in sources (topic present in listed question banks) |
| Q11 | ⭐⭐⭐ 🟡 | Explain how a CNN works: convolution, stride, padding, pooling, receptive field, parameter sharing. | found in sources (topic present in listed question banks) |
| Q12 | ⭐⭐⭐ 🟡 | What is mAP in object detection, and how is it computed (precision-recall curve, AP per class, IoU thresholds)? | added: expert gap-check |
| Q13 | ⭐⭐⭐ 🟡 | When would you pick an LLM (prompting) over a classic NLP model (TF-IDF/BERT classifier) for a text task? Discuss cost, latency, accuracy, data and maintenance. | found in sources (topic present in listed question banks) |
| Q14 | ⭐⭐⭐ 🟡 | Prompting vs RAG vs fine-tuning: how do you decide? (framing only; depth is in Book 2) | found in sources (topic present in listed question banks) |
| Q15 | ⭐⭐ 🟢 | Text preprocessing pipeline: tokenization, stop words, stemming vs lemmatization. When should you skip them? | found in sources (topic present in listed question banks) |
| Q16 | ⭐⭐ 🟢 | Which evaluation metrics do you use for text classification (precision/recall/F1, macro vs micro), and why? | found in sources (topic present in listed question banks) |
| Q17 | ⭐⭐ 🟢 | What are the common image augmentation techniques, and when can augmentation hurt? | found in sources (topic present in listed question banks) |
| Q18 | ⭐⭐ 🟢 | What is perplexity, and what does it tell you about a language model? | added: expert gap-check |
| Q19 | ⭐⭐ 🟡 | How do you get a sentence or document embedding, and how would you use embeddings for semantic search (cosine similarity, ANN index)? | found in sources (topic present in listed question banks) |
| Q20 | ⭐⭐ 🟡 | What is NER? How would you build and evaluate a NER system (BiLSTM-CRF vs BERT; entity-level F1)? | found in sources (topic present in listed question banks) |
| Q21 | ⭐⭐ 🟡 | Why does the transformer use positional encoding, and how does multi-head attention help? | found in sources (topic present in listed question banks) |
| Q22 | ⭐⭐ 🟡 | Compare CNN architectures: LeNet, AlexNet, VGG, ResNet, Inception, EfficientNet. Why do skip connections help? | found in sources (topic present in listed question banks) |
| Q23 | ⭐⭐ 🟡 | BLEU vs ROUGE vs BERTScore: what do they measure and what are their weaknesses? | added: expert gap-check |
| Q24 | ⭐⭐ 🟡 | How do you handle class imbalance in text or image classification? | added: expert gap-check |
| Q25 | ⭐⭐ 🟡 | Object detection vs semantic vs instance segmentation: differences, and typical models (YOLO, Faster R-CNN, U-Net, Mask R-CNN). | found in sources (topic present in listed question banks) |
| Q26 | ⭐⭐ 🟡 | Explain batch normalization and dropout in CNNs. Where do you place them and why? | added: expert gap-check |
| Q27 | ⭐⭐ 🟡 | How do you handle out-of-vocabulary words and misspellings? Explain subword tokenization (BPE/WordPiece). | added: expert gap-check |
| Q28 | ⭐⭐ 🟡 | How do you deal with long documents when BERT has a 512-token limit? | added: expert gap-check |
| Q29 | ⭐⭐ 🟡 | How would you build a text classifier with very few labelled examples (zero-shot, few-shot, SetFit, weak labelling, active learning)? | added: expert gap-check |
| Q30 | ⭐⭐ 🟡 | How do you evaluate an LLM-based classifier or extractor in a classical DS workflow, and what can go wrong (non-determinism, leakage, prompt sensitivity)? | added: expert gap-check |
| Q31 | ⭐⭐ 🟡 | How would you detect and handle drift in a production NLP model (e.g. new slang, new product names)? | added: expert gap-check |
| Q32 | ⭐⭐ 🔴 | What is Non-Max Suppression, and how do anchor boxes work? Anchor-based vs anchor-free detectors. | found in sources (topic present in listed question banks) |
| Q33 | ⭐⭐ 🔴 | What is the Vision Transformer (ViT)? How does it differ from a CNN, and when does each win? | added: expert gap-check |
| Q34 | ⭐⭐ 🔴 | Walk through a design for an image classification system with limited labelled data and a latency budget on edge devices. | found in sources (topic present in listed question banks) |
| Q35 | ⭐⭐ 🔴 | Why does a vision model trained in one domain fail in another? How do you diagnose and fix the domain shift? | found in sources (topic present in listed question banks) |
| Q36 | ⭐ 🟢 | What is the vanishing gradient problem in RNNs, and how do LSTM/GRU gates address it? | added: expert gap-check |
| Q37 | ⭐ 🟢 | Topic modelling: explain LDA and when you would use it over clustering embeddings (e.g. BERTopic). | added: expert gap-check |
| Q38 | ⭐ 🟡 | Explain the Naive Bayes text classifier and why it works despite the independence assumption. | added: expert gap-check |
| Q39 | ⭐ 🟡 | Cosine similarity vs Euclidean vs dot product for embeddings: when does each apply? | added: expert gap-check |
| Q40 | ⭐ 🟡 | Fine-tuning basics: full fine-tuning vs adapters/LoRA vs feature extraction. What goes wrong with catastrophic forgetting or a bad learning rate? | found in sources (topic present in listed question banks) |
| Q41 | ⭐ 🟡 | How do you reduce hallucination and measure factuality when an LLM is part of a DS pipeline? | added: expert gap-check |
| Q42 | ⭐ 🟡 | What is Grad-CAM, and how do you explain a CNN or transformer prediction? | added: expert gap-check |
| Q43 | ⭐ 🟡 | Dice coefficient vs IoU vs pixel accuracy for segmentation: when is each used? | added: expert gap-check |
| Q44 | ⭐ 🟡 | How do you deal with noisy or ambiguous labels in image or text datasets (inter-annotator agreement, label cleaning)? | added: expert gap-check |
| Q45 | ⭐ 🟡 | Sequence-to-sequence basics: what are the encoder-decoder, teacher forcing and beam search? | added: expert gap-check |
| Q46 | ⭐ 🟡 | Explain contrastive learning / sentence-transformers and how a bi-encoder differs from a cross-encoder (reranking). | added: expert gap-check |
| Q47 | ⭐ 🟡 | Multilingual and code-mixed text (Hinglish): how would you approach classification or search? | added: expert gap-check |
| Q48 | ⭐ 🟡 | How do you choose between a distilled small model and a large model for production text inference (quantization, ONNX, latency, cost)? | added: expert gap-check |
| Q49 | ⭐ 🟡 | How do you check for bias and PII/privacy issues when training on text or image data? | added: expert gap-check |
| Q50 | ⭐ 🔴 | Explain the O(n^2) attention cost problem and approaches to mitigate it (sparse, linear, Flash attention) at a high level. | added: expert gap-check |
| Q51 | ⭐ 🔴 | What is self-supervised pretraining for vision (SimCLR, MAE, CLIP)? How would you use CLIP for zero-shot image search? | added: expert gap-check |
| Q52 | ⭐ 🔴 | Design an embedding-based product search system (text + image) for an e-commerce catalogue: indexing, retrieval, evaluation, cold start. | added: expert gap-check |
| Q53 | ⭐ 🔴 | Explain OCR / document-understanding pipelines (e.g. invoices, KYC) and how you would evaluate them. | added: expert gap-check |

