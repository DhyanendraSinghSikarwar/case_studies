# Book 1 — Part 09: NLP & Computer Vision (classical → transformers)

**Topic:** TF-IDF/BoW, embeddings, text classification, NER, BERT & fine-tuning basics, attention/transformers, NLP metrics; CNNs, transfer learning, augmentation, detection/segmentation metrics, ViT; light GenAI-in-classical-loop layer.
**Target:** 45  |  **Actual:** 53  |  **Date:** 2026-10-20  |  **Status:** Phase 1 (questions only)

Scope note: deep LLM/RAG/agents live in Book 2; classification metrics in Part 3; DL basics (backprop/optimizers) in Part 8.

---

### Q1 ⭐⭐⭐ 🟢 How does TF-IDF work, and what are its limitations compared with embeddings?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Bag-of-Words vs TF-IDF vs word embeddings: when would you use each?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Word2Vec vs GloVe vs FastText: how do they differ, and how are they trained?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What is IoU, and how is it used in object detection?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 How do you handle overfitting when training a CNN on a small image dataset (augmentation, regularization, early stopping)?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 How do you build a text classifier end to end (TF-IDF + logistic regression baseline up to a fine-tuned transformer)? How do you choose between them?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 What is the difference between static (Word2Vec) and contextual (BERT) embeddings?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Explain self-attention and the transformer architecture. Why did transformers replace RNNs/LSTMs?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 What is BERT, how is it pretrained (MLM, NSP), and how do you fine-tune it for classification?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Explain transfer learning in CNNs. When do you freeze layers versus fine-tune the whole network?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Explain how a CNN works: convolution, stride, padding, pooling, receptive field, parameter sharing.
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 What is mAP in object detection, and how is it computed (precision-recall curve, AP per class, IoU thresholds)?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 When would you pick an LLM (prompting) over a classic NLP model (TF-IDF/BERT classifier) for a text task? Discuss cost, latency, accuracy, data and maintenance.
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Prompting vs RAG vs fine-tuning: how do you decide? (framing only; depth is in Book 2)
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 Text preprocessing pipeline: tokenization, stop words, stemming vs lemmatization. When should you skip them?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 Which evaluation metrics do you use for text classification (precision/recall/F1, macro vs micro), and why?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 What are the common image augmentation techniques, and when can augmentation hurt?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 What is perplexity, and what does it tell you about a language model?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 How do you get a sentence or document embedding, and how would you use embeddings for semantic search (cosine similarity, ANN index)?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 What is NER? How would you build and evaluate a NER system (BiLSTM-CRF vs BERT; entity-level F1)?
**Asked at:** GCCs / MNCs (Walmart, JPMC, Amazon India, Microsoft IDC)
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Why does the transformer use positional encoding, and how does multi-head attention help?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Compare CNN architectures: LeNet, AlexNet, VGG, ResNet, Inception, EfficientNet. Why do skip connections help?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 BLEU vs ROUGE vs BERTScore: what do they measure and what are their weaknesses?
**Asked at:** GCCs / MNCs (Walmart, JPMC, Amazon India, Microsoft IDC)
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How do you handle class imbalance in text or image classification?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Object detection vs semantic vs instance segmentation: differences, and typical models (YOLO, Faster R-CNN, U-Net, Mask R-CNN).
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Explain batch normalization and dropout in CNNs. Where do you place them and why?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 How do you handle out-of-vocabulary words and misspellings? Explain subword tokenization (BPE/WordPiece).
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do you deal with long documents when BERT has a 512-token limit?
**Asked at:** product cos (Flipkart/Swiggy-type)
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How would you build a text classifier with very few labelled examples (zero-shot, few-shot, SetFit, weak labelling, active learning)?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 How do you evaluate an LLM-based classifier or extractor in a classical DS workflow, and what can go wrong (non-determinism, leakage, prompt sensitivity)?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 How would you detect and handle drift in a production NLP model (e.g. new slang, new product names)?
**Asked at:** product cos (Flipkart/Swiggy-type)
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🔴 What is Non-Max Suppression, and how do anchor boxes work? Anchor-based vs anchor-free detectors.
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🔴 What is the Vision Transformer (ViT)? How does it differ from a CNN, and when does each win?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🔴 Walk through a design for an image classification system with limited labelled data and a latency budget on edge devices.
**Asked at:** product cos (Flipkart/Swiggy-type)
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🔴 Why does a vision model trained in one domain fail in another? How do you diagnose and fix the domain shift?
**Asked at:** GCCs / MNCs (Walmart, JPMC, Amazon India, Microsoft IDC)
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🟢 What is the vanishing gradient problem in RNNs, and how do LSTM/GRU gates address it?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟢 Topic modelling: explain LDA and when you would use it over clustering embeddings (e.g. BERTopic).
**Asked at:** product cos (Flipkart/Swiggy-type)
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 Explain the Naive Bayes text classifier and why it works despite the independence assumption.
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 Cosine similarity vs Euclidean vs dot product for embeddings: when does each apply?
**Asked at:** Europe product cos (Spotify/Zalando/Booking/Klarna-type)
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 Fine-tuning basics: full fine-tuning vs adapters/LoRA vs feature extraction. What goes wrong with catastrophic forgetting or a bad learning rate?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 How do you reduce hallucination and measure factuality when an LLM is part of a DS pipeline?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🟡 What is Grad-CAM, and how do you explain a CNN or transformer prediction?
**Asked at:** GCCs / MNCs (Walmart, JPMC, Amazon India, Microsoft IDC)
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🟡 Dice coefficient vs IoU vs pixel accuracy for segmentation: when is each used?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟡 How do you deal with noisy or ambiguous labels in image or text datasets (inter-annotator agreement, label cleaning)?
**Asked at:** product cos (Flipkart/Swiggy-type)
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟡 Sequence-to-sequence basics: what are the encoder-decoder, teacher forcing and beam search?
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🟡 Explain contrastive learning / sentence-transformers and how a bi-encoder differs from a cross-encoder (reranking).
**Asked at:** Europe product cos (Spotify/Zalando/Booking/Klarna-type)
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🟡 Multilingual and code-mixed text (Hinglish): how would you approach classification or search?
**Asked at:** product cos (Flipkart/Swiggy-type)
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🟡 How do you choose between a distilled small model and a large model for production text inference (quantization, ONNX, latency, cost)?
**Asked at:** product cos (Flipkart/Swiggy-type)
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🟡 How do you check for bias and PII/privacy issues when training on text or image data?
**Asked at:** Europe product cos (Spotify/Zalando/Booking/Klarna-type)
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 Explain the O(n^2) attention cost problem and approaches to mitigate it (sparse, linear, Flash attention) at a high level.
**Asked at:** all types
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 What is self-supervised pretraining for vision (SimCLR, MAE, CLIP)? How would you use CLIP for zero-shot image search?
**Asked at:** Europe product cos (Spotify/Zalando/Booking/Klarna-type)
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 Design an embedding-based product search system (text + image) for an e-commerce catalogue: indexing, retrieval, evaluation, cold start.
**Asked at:** product cos (Flipkart/Swiggy-type)
<!-- ANSWER_PENDING -->

### Q53 ⭐ 🔴 Explain OCR / document-understanding pipelines (e.g. invoices, KYC) and how you would evaluate them.
**Asked at:** GCCs / MNCs (Walmart, JPMC, Amazon India, Microsoft IDC)
<!-- ANSWER_PENDING -->
