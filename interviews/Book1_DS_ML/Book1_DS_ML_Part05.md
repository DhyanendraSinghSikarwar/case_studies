# Book 1 - Part 05: Clustering, Dimensionality Reduction, Anomaly Detection

**Topic:** k-means, hierarchical, DBSCAN, GMM; PCA/t-SNE/UMAP; anomaly/outlier detection (Isolation Forest, LOF, autoencoders)

**Target:** 40 | **Actual:** 47 | **Date:** 2026-10-20

Web sources for this niche were thin; most questions are expert gap-check additions (see research_notes/Book1_Part05_sources.md).


### Q1 ⭐⭐⭐ 🟢 Explain the k-means algorithm. What objective does it minimise and why does it converge?
**Asked at:** Product cos, Flipkart/Swiggy-style ML rounds, GCCs, Europe scale-ups
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 How do you choose the number of clusters k? (elbow, silhouette, gap statistic, business constraints)
**Asked at:** Product cos, Amazon India, Zalando/Booking, GCCs
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is PCA, how does it work, and when would you use it?
**Asked at:** Almost all DS/MLE loops: product, fintech, GCC, Europe
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 PCA vs t-SNE vs UMAP: what does each preserve, and when do you use which?
**Asked at:** Product cos, Spotify/Zalando-type, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 What are the assumptions and failure modes of k-means? When does it give bad clusters?
**Asked at:** Product cos, fintech, GCC
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 How does DBSCAN work? What do eps and minPts mean and how do you tune them? When is it better than k-means?
**Asked at:** Product cos, Flipkart/Swiggy, Europe e-commerce
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 How does Isolation Forest detect anomalies, and why do anomalies get isolated in fewer splits?
**Asked at:** Fintech (PhonePe, JPMC), Amazon, Booking/Klarna fraud teams
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 How do you evaluate a clustering when there are no labels?
**Asked at:** Product cos, Amazon India, GCCs
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Case: segment customers for an e-commerce / food-delivery app. Walk through features, scaling, algorithm, validation, and how the business uses it.
**Asked at:** Flipkart, Swiggy, Zalando, Booking, Walmart GCC
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Why must you scale features before k-means or PCA? How do you handle categorical or mixed-type features?
**Asked at:** Product cos, Microsoft IDC, GCCs
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 How do you decide how many principal components to keep? (explained variance, scree, cross-validation)
**Asked at:** Product cos, GCCs, Europe
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 You have no labels and must detect anomalies (fraud, bad orders, sensor faults). How do you choose a method, set a threshold, and evaluate it?
**Asked at:** PhonePe, Klarna, JPMC, Amazon, Swiggy
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🔴 Implement k-means from scratch in NumPy (with k-means++ initialisation if time allows).
**Asked at:** Swiggy ML-coding round, Amazon, Microsoft IDC, GCCs
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟢 Explain hierarchical (agglomerative) clustering: linkage types, dendrogram, and how you cut it.
**Asked at:** Product cos, GCCs, Europe
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 What is the curse of dimensionality and how does it affect distance-based methods like k-means, DBSCAN and kNN?
**Asked at:** Product cos, Microsoft IDC, Europe
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟡 Gaussian Mixture Models and the EM algorithm: how do they work and how do they differ from k-means (soft vs hard assignment)?
**Asked at:** Product cos, Amazon, Microsoft IDC, Europe
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟡 Explain the silhouette score: how it is computed, how to read it, and its limitations.
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 How does k-means++ initialisation work, and why does initialisation matter (local minima, n_init)?
**Asked at:** Product cos, Amazon
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 What is Local Outlier Factor (LOF)? How does it differ from Isolation Forest, and when would you pick each?
**Asked at:** Fintech, GCCs, Europe fraud/risk
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 How can an autoencoder be used for anomaly detection? How do you set the threshold and what can go wrong?
**Asked at:** Product cos, fintech, Amazon, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 What is the relationship between PCA and k-means?
**Asked at:** Data Scientist/MLE loops (Interview Query tag, March 2025)
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 How can PCA be used for anomaly detection (reconstruction error, Mahalanobis distance in PC space)?
**Asked at:** Fintech, GCC, industrial analytics
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 How does t-SNE work, what does perplexity do, and what are the traps when reading a t-SNE plot?
**Asked at:** Product cos, Spotify/Zalando, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How does UMAP differ from t-SNE (speed, global structure, reproducibility)? Can you cluster on UMAP output?
**Asked at:** Product cos, Europe scale-ups
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Statistical outlier detection (z-score, IQR, MAD): when does each work and when does it fail?
**Asked at:** Product cos, GCCs, Walmart/Amazon analytics
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 How do outliers affect k-means and PCA, and how do you make them robust (k-medoids, robust scaling, trimming)?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 PCA vs feature selection: does PCA help a supervised model, and what do you lose in interpretability?
**Asked at:** Product cos, fintech, GCCs
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do you cluster high-dimensional data such as text or user embeddings? (reduce then cluster, cosine distance, HDBSCAN, BERTopic)
**Asked at:** Product cos, Spotify/Zalando, GenAI-adjacent teams
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How do you evaluate an anomaly detector with very few labels? (precision@k, PR-AUC, contamination parameter, analyst feedback)
**Asked at:** Fintech (PhonePe, Klarna, JPMC), Amazon
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 HDBSCAN vs DBSCAN: how does it handle varying density, and what are its main hyperparameters?
**Asked at:** Product cos, Europe scale-ups
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 How do you check that clusters are stable and reproducible, and how do you deploy a segmentation and monitor it for drift?
**Asked at:** Product cos, Amazon, Booking, GCCs
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 External clustering metrics when ground truth exists: ARI, NMI, purity, V-measure. When are they appropriate?
**Asked at:** Product cos, GCCs
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Anomaly detection on business metrics (daily orders, payment success rate): how do you handle seasonality and trend, and avoid alert fatigue?
**Asked at:** Swiggy, PhonePe, Booking, Klarna
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 SVD vs PCA: how are they related, and when do you use Truncated SVD (sparse matrices, LSA)?
**Asked at:** Product cos, recsys/NLP teams
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🔴 Derive PCA: show that principal components are eigenvectors of the covariance matrix, and relate it to SVD.
**Asked at:** Microsoft IDC, Amazon, research-leaning MLE
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🔴 Implement PCA from scratch in NumPy and verify it against sklearn.
**Asked at:** Microsoft IDC, Amazon, GCC coding rounds
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 One-Class SVM vs Isolation Forest vs LOF: how do they compare in assumptions, scale and tuning?
**Asked at:** Fintech, Europe fraud/risk
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 LLM code review: this LLM-generated clustering/PCA pipeline looks fine but has bugs. Spot them (scaler or PCA fit on all data, leakage, t-SNE used for clustering, wrong k, no random_state).
**Asked at:** AI-era rounds: Microsoft IDC, product cos, Europe scale-ups
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 GenAI follow-up: how would you use an LLM to name or interpret clusters, and how do you validate that the labels are correct?
**Asked at:** GenAI-adjacent product teams, Europe scale-ups
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🔴 Show that Lloyd's k-means iterations never increase the objective. Why is it only a local optimum, and what is its link to EM?
**Asked at:** Research-leaning MLE, Amazon applied science
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🔴 Spectral clustering: how does it work and when does it beat k-means?
**Asked at:** Research-leaning roles, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Kernel PCA, probabilistic PCA, ICA and NMF: how do they differ from PCA and when would you use them?
**Asked at:** Research-leaning roles, Europe
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 Model selection for GMM: BIC/AIC, covariance types, and degenerate (singular) components.
**Asked at:** Research-leaning roles, Amazon applied science
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 How would you explain why a particular point was flagged as an anomaly (SHAP on Isolation Forest, feature-wise reconstruction error)?
**Asked at:** Fintech, regulated GCCs (JPMC), Klarna
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 Deep anomaly detection: VAE, Deep SVDD, GAN-based methods. When are they worth it over Isolation Forest?
**Asked at:** Senior MLE, Amazon, Microsoft IDC
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 Scale: how do you cluster 100M users (mini-batch k-means, FAISS, approximate nearest neighbours, sampling then assign)? Why does DBSCAN scale badly?
**Asked at:** Flipkart, Swiggy, Amazon, Walmart GCC
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 Anomaly detection under drift and feedback loops: how do you handle changing normal behaviour, adversaries adapting (fraud), and labels coming only from flagged cases?
**Asked at:** PhonePe, Klarna, Booking, Amazon
<!-- ANSWER_PENDING -->
