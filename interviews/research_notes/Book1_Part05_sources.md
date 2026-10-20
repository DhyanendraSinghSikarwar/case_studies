# Book 1 Part 05 - Sources (Clustering / PCA / Anomaly detection)

Date: 2026-10-20. WebSearch worked (US-only, returns thin results). Glassdoor, AmbitionBox, Blind, LeetCode Discuss were not fetched directly (only seen as search-result links). WebFetch of interviewquery.com returned HTTP 429, so the page body was not read. No GeeksforGeeks interview-experience page surfaced.

## Evidence seen (URLs appeared in search results; page bodies mostly NOT opened)
| Question theme | Source (seen in search results) | Count | Recency |
|---|---|---|---|
| PCA vs k-means relationship | https://interviewquery.com/questions/pca-and-k-means (tagged DS/MLE, March 2025 per search summary) | 1 | 2025 |
| PCA-based anomaly detection (reconstruction error) | https://visualstudiomagazine.com/articles/2021/10/20/anomaly-detection-pca.aspx?p=1 | 1 | 2021 |
| k-means vs Isolation Forest vs One-Class SVM; PCA before k-means | https://simpson-danielb.medium.com/machine-learning-for-anomaly-detection-39a7dff659ee | 1 | undated |
| Anomaly types, algorithm choice, threshold setting | https://www.javainuse.com/interview/anomaly | 1 | 2025 (per summary) |
| Build anomaly detection on given DB (junior DS) | https://static.glassdoor.com.br/Interview/junior-data-scientist-interview-questions-SRCH_KO0,21_IP30.htm | 1 | unknown |
| Flipkart: clustering-based scenario question (Bengaluru) | https://clear.glassdoor.nl/Interview/Flipkart-Interview-E300494-RVW10756044.htm (search summary said Nov 2025) | 1 | 2025 |
| Swiggy: clustering setup in coding round, NumPy/pandas | https://www.interviewquery.com/interview-guides/swiggy-data-scientist | 1 | 2025 |
| Clustering basics, PCA vs t-SNE, Isolation Forest / OCSVM | https://climbtheladder.com/clustering-interview-questions/ ; https://vskills.in/interview-questions/data-science-interview-questions/unsupervised-machine-learning-interview-questions ; https://talent500.com/blog/unsupervised-machine-learning-clustering-dimensionality-reduction-and-anomaly-detection-techniques | 3 | mixed |

No source specific to Amazon India, PhonePe, Microsoft IDC, Spotify, Zalando, Booking or Klarna was found for this topic. Company names in "Asked at" are plausible-fit labels, not confirmed reports; most questions are therefore expert gap-check additions (marked F in generation; 5 marked S). Star ratings are judgement-based given the thin frequency data: the canonical topics (k-means, choosing k, PCA, DBSCAN, Isolation Forest, t-SNE) are rated 3 stars because they are standard in nearly every ML loop.

## AI-era changes noted
- LLM/embedding clustering (BERTopic, HDBSCAN on embeddings) and LLM-generated cluster labels are now follow-ups.
- LLM-generated pipeline code review (fit-on-all-data leakage, t-SNE misuse) added as questions.
- Candidates are expected to explain results, not just call sklearn; ML-coding rounds (k-means/PCA from scratch) persist.
