# Book 1 - Part 05: Clustering, Dimensionality Reduction, Anomaly Detection

**Topic:** k-means, hierarchical, DBSCAN, GMM; PCA/t-SNE/UMAP; anomaly/outlier detection (Isolation Forest, LOF, autoencoders)

**Target:** 40 | **Actual:** 46 (⭐⭐⭐ 12, ⭐⭐ 23, ⭐ 11) | **Date:** 2026-10-20

Web sources for this niche were thin; most questions are expert gap-check additions (see research_notes/Book1_Part05_sources.md).

> Dedupe pass: removed 1 cross-part duplicate(s); renumbered Q1–Q46.

---

### Q1 ⭐⭐⭐ 🟢 Explain the k-means algorithm. What objective does it minimise and why does it converge?
**Asked at:** Product cos, Flipkart/Swiggy-style ML rounds, GCCs, Europe scale-ups
**Say this first (1 line):** K-means splits data into k groups by repeatedly assigning each point to its nearest centre and moving each centre to the mean of its points; it minimises the within-cluster sum of squared distances (inertia), and it always converges because every step can only lower that number.

**Then explain:**
- **Objective:** J = Σ over clusters Σ over points in cluster ‖x − μ_c‖². Small J means tight, compact clusters.
- **Algorithm (Lloyd's):** (1) pick k starting centres; (2) assign every point to its nearest centre; (3) recompute each centre as the mean of its points; (4) repeat until assignments stop changing.
- **Why it converges:** the assign step picks the closest centre per point, so J cannot go up. The update step uses the mean, which is the point that minimises squared distance for a fixed group, so J cannot go up there either. J never rises and there are only finitely many ways to partition the data, so it must stop.
- **Catch:** it stops at a *local* minimum, not necessarily the best one. That is why we use k-means++ and several restarts.
- **Cost:** O(n · k · d) per iteration.

**Example:** Customers described by (orders per month, average basket value). With k=3 you might get "rare small", "regular medium", "frequent big" groups. The centres are the average customer of each group.

**Code:** (NumPy from scratch, matches sklearn's inertia)
```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

def kmeans(X, k, iters=100, seed=0):
    rng = np.random.default_rng(seed)
    C = X[rng.choice(len(X), k, replace=False)]
    for _ in range(iters):
        d = ((X[:, None, :] - C[None]) ** 2).sum(-1)   # n x k squared distances
        lab = d.argmin(1)                              # assignment step
        newC = np.array([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
        if np.allclose(newC, C): break
        C = newC                                       # update step
    return lab, C, d.min(1).sum()

X, _ = make_blobs(600, centers=3, random_state=0)
lab, C, sse = kmeans(X, 3)
km = KMeans(3, n_init=10, random_state=0).fit(X)
print(round(sse, 1), round(km.inertia_, 1))
```
Output: `1041.3 1041.3`

**Follow-ups:**
- *Does it find the global optimum?* No. Finding it is NP-hard; Lloyd's gives a local optimum, so use k-means++ and `n_init` restarts.
- *What if a cluster ends up empty?* Re-seed it with a far-away point (sklearn does this).
- *Why mean and not median?* Squared distance is minimised by the mean. The median goes with absolute distance (k-medians).

**Common mistakes:** Saying it minimises the distance between clusters (it is within-cluster). Forgetting it needs scaled features. Claiming it finds the global optimum. Not saying k must be chosen up front.

### Q2 ⭐⭐⭐ 🟢 How do you choose the number of clusters k? (elbow, silhouette, gap statistic, business constraints)
**Asked at:** Product cos, Amazon India, Zalando/Booking, GCCs
**Say this first (1 line):** There is no single right k; I look at the elbow and silhouette for a statistical hint, check stability, and then let the business decide how many segments they can actually act on.

**Then explain:**
- **Elbow:** plot inertia against k. Inertia always falls as k grows, so look for the bend where gains flatten. It is often vague.
- **Silhouette:** average of how well each point fits its own cluster versus the next nearest (range -1 to 1). Pick the k with the highest score.
- **Gap statistic:** compare your inertia with inertia on random uniform data. Pick the smallest k whose gap is within one standard error of the next k's gap (Tibshirani's rule). More principled, but slower.
- **Stability:** refit on bootstrap samples; a good k gives similar clusters each time.
- **Business constraint:** marketing can run 4-6 campaigns, not 25. Each segment must be big enough to matter and different enough to treat differently.

**Example:** Data with 4 real groups. Output (k, inertia, silhouette): 2 → 7397, 0.705; 3 → 3758, 0.584; 4 → 1973, 0.624; 5 → 1784, 0.541. Inertia bends at k=4. Silhouette is highest at k=2 (merging two pairs of groups looks "cleaner") and has a second peak at 4. This is why I never trust one metric alone.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
X, _ = make_blobs(1000, centers=4, cluster_std=1.0, random_state=1)
for k in range(2, 8):
    km = KMeans(k, n_init=10, random_state=0).fit(X)
    print(k, round(km.inertia_), round(silhouette_score(X, km.labels_), 3))
```
Output: `2 7397 0.705`, `3 3758 0.584`, `4 1973 0.624`, `5 1784 0.541`, `6 1604 0.471`, `7 1436 0.372`.

**Follow-ups:**
- *Elbow and silhouette disagree?* Check stability and look at cluster profiles. Pick the k whose segments are interpretable and actionable.
- *Is the elbow reliable?* Not on real data; the curve is often smooth. Treat it as a hint.
- *Can you avoid choosing k?* Yes: hierarchical clustering with a dendrogram, DBSCAN/HDBSCAN, or a GMM with BIC.

**Common mistakes:** Picking k by minimum inertia (that is always k=n). Using only one metric. Ignoring that the business cannot act on 15 segments. Not fixing `random_state` / `n_init`, so the answer changes run to run.

### Q3 ⭐⭐⭐ 🟢 What is PCA, how does it work, and when would you use it?
**Asked at:** Almost all DS/MLE loops: product, fintech, GCC, Europe
**Say this first (1 line):** PCA rotates the data onto new, uncorrelated axes (principal components) ordered by how much variance they capture, so you can keep the first few and drop the rest with minimal information loss.

**Then explain:**
- **How:** centre the data (and usually scale it), compute the covariance matrix, take its eigenvectors (directions) and eigenvalues (variance along each direction), sort by eigenvalue, project onto the top k. In practice use SVD of the centred data.
- **What you get:** components are orthogonal, linear combinations of the original features; PC1 is the direction of greatest spread.
- **When to use:** compress many correlated features, remove multicollinearity, denoise, speed up models, visualise in 2D, preprocess before k-means.
- **When not to:** when you need interpretable original features, when structure is non-linear (try kernel PCA / UMAP), or when the low-variance directions carry the signal.
- **Unsupervised:** it ignores the target, so high variance does not mean predictive.

**Example:** Six sensor readings that really come from 2 hidden factors. After scaling, explained variance ratios are [0.705, 0.26, 0.018, 0.011, 0.005, 0.002]; two components keep 96.5%. Six columns become two with almost no loss.

**Code:**
```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
rng = np.random.default_rng(0)
z = rng.normal(size=(500, 2))
X = z @ rng.normal(size=(2, 6)) + 0.1 * rng.normal(size=(500, 6))   # 6 features, ~2 true dims
Xs = StandardScaler().fit_transform(X)
p = PCA().fit(Xs)
print(p.explained_variance_ratio_.round(3), p.explained_variance_ratio_.cumsum().round(3))
```
Output: `[0.705 0.26 0.018 0.011 0.005 0.002] [0.705 0.965 0.982 0.993 0.998 1. ]`

**Follow-ups:**
- *Why scale first?* Otherwise the feature with the biggest units dominates the variance (see Q10).
- *PCA vs feature selection?* PCA builds new mixed features; selection keeps original ones (Q26).
- *Does PCA need normality?* No. It only uses second moments; normality just makes variance a richer description.

**Common mistakes:** Not centring or scaling. Fitting PCA on train+test (leakage). Calling components "features" with business meaning. Assuming high-variance directions are the predictive ones.

### Q4 ⭐⭐⭐ 🟢 PCA vs t-SNE vs UMAP: what does each preserve, and when do you use which?
**Asked at:** Product cos, Spotify/Zalando-type, Microsoft IDC
**Say this first (1 line):** PCA preserves global variance linearly and is a general-purpose tool; t-SNE preserves local neighbourhoods for visualisation only; UMAP preserves local structure and more of the global layout, is faster, and can also be used for downstream steps.

**Then explain:**

| | PCA | t-SNE | UMAP |
|---|---|---|---|
| Type | Linear | Non-linear | Non-linear |
| Preserves | Global variance, distances roughly | Local neighbours | Local neighbours, better global shape |
| Speed | Very fast | Slow (Barnes-Hut O(n log n)) | Fast, scales to millions |
| Deterministic | Yes | No (seed dependent) | Mostly no (seed dependent) |
| New data | `transform` works | No built-in transform | `transform` works |
| Axes meaning | Yes (loadings) | No | No |
| Use for | Compression, preprocessing, denoising | 2D/3D plots | Plots, clustering input, embeddings |

- In practice: PCA first (e.g. to 50 dims) to denoise and speed up, then t-SNE/UMAP to 2D.
- t-SNE and UMAP cluster sizes and between-cluster distances are not reliable (see Q22, Q23).

**Example:** Visualising 1M product embeddings: PCA to 50 dims, UMAP to 2D, colour by category. For a model feature pipeline use PCA, because it is a stable, reusable linear transform.

**Follow-ups:**
- *Can I feed t-SNE output to a model?* Avoid it; it cannot embed new points and distorts density.
- *Why does t-SNE use a t-distribution?* Heavy tails in the low-dim space reduce crowding, so clusters separate.
- *Which preserves global structure best?* PCA by design; UMAP usually beats t-SNE.

**Common mistakes:** Reading cluster size or gap distance in t-SNE/UMAP as meaningful. Running one seed and one perplexity. Using t-SNE as a preprocessing step. Saying UMAP is "always better".

### Q5 ⭐⭐⭐ 🟡 What are the assumptions and failure modes of k-means? When does it give bad clusters?
**Asked at:** Product cos, fintech, GCC
**Say this first (1 line):** K-means assumes round, similar-sized, similar-density clusters in a space where Euclidean distance is meaningful, and it breaks when clusters are elongated, nested, unequal, noisy, or when k and scaling are wrong.

**Then explain:**
- **Assumptions:** clusters are roughly spherical (equal variance in all directions), similar size and density, features are on comparable scales, k is known.
- **Failure modes:**
  - Non-convex shapes (moons, rings): it cuts them with a straight line.
  - Different sizes or densities: big clusters steal points from small ones.
  - Outliers: they drag centres, since the mean is not robust.
  - Unscaled features: the large-unit column decides everything.
  - High dimensions: distances become similar (Q14).
  - Bad init: stuck in a local minimum.
  - Categorical data: the mean makes no sense.
- **Fixes:** DBSCAN/HDBSCAN for shapes and noise, GMM for elongated or soft clusters, scaling, outlier trimming, k-medoids, multiple restarts.

**Example:** Two interleaving half-moons with true labels. K-means ARI = 0.25 (it slices them in half); DBSCAN ARI = 1.0.

**Code:**
```python
from sklearn.datasets import make_moons
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import adjusted_rand_score as ari
X, y = make_moons(500, noise=0.06, random_state=0)
print("kmeans ARI", round(ari(y, KMeans(2, n_init=10, random_state=0).fit_predict(X)), 2))
print("dbscan ARI", round(ari(y, DBSCAN(eps=0.15, min_samples=5).fit_predict(X)), 2))
```
Output: `kmeans ARI 0.25`, `dbscan ARI 1.0`.

**Follow-ups:**
- *Can k-means handle elongated clusters?* Poorly; a GMM with full covariance does better, or whiten with PCA first.
- *How do you spot a bad result?* Cluster profiles that overlap, silhouette low, unstable across seeds, one giant cluster.
- *Is k-means always bad for non-spherical data?* Sometimes useful as a quantiser (vector compression), even if clusters are not "real".

**Common mistakes:** Saying k-means "needs Gaussian data" (it needs compact, similar-variance groups, not strictly Gaussian). Forgetting scale and outliers. Treating every output as a meaningful segment.

### Q6 ⭐⭐⭐ 🟡 How does DBSCAN work? What do eps and minPts mean and how do you tune them? When is it better than k-means?
**Asked at:** Product cos, Flipkart/Swiggy, Europe e-commerce
**Say this first (1 line):** DBSCAN grows clusters from dense regions: a point with at least minPts neighbours within radius eps is a core point, clusters are chains of connected core points, and anything not reachable is noise.

**Then explain:**
- **eps:** the neighbourhood radius. **minPts:** how many points (including itself) make a neighbourhood dense.
- **Point types:** core (dense), border (within eps of a core but not dense itself), noise (label -1).
- **Tuning eps:** plot the sorted k-distance (distance to the k-th neighbour, with k = minPts) and pick the knee. Rule of thumb for minPts: at least dims+1, often 2×dims; larger for noisy data.
- **Better than k-means when:** you do not know k, clusters have arbitrary shapes, you want outliers flagged as noise.
- **Weak at:** varying densities (one eps cannot fit all), high dimensions, and scale (neighbour search without an index is O(n²); with a spatial index O(n log n) in low dim).
- Sensitive to feature scaling, since eps is a distance.

**Example:** Delivery GPS pings: dense hotspots (restaurants, apartment blocks) become clusters, stray pings are noise, and you never specify the number of hotspots.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
X, _ = make_moons(500, noise=0.06, random_state=0)
k = 5
d = np.sort(NearestNeighbors(n_neighbors=k).fit(X).kneighbors(X)[0][:, -1])  # k-distance
print("k-dist percentiles 50/90/95/99:", np.percentile(d, [50, 90, 95, 99]).round(3))
lab = DBSCAN(eps=0.12, min_samples=k).fit_predict(X)
print("clusters", len(set(lab)) - (-1 in lab), "noise", (lab == -1).sum())
```
Output: percentiles `[0.058 0.092 0.11 0.136]`; `clusters 2 noise 2`. The k-distance curve rises sharply past the 95th percentile, so eps about 0.11-0.14 is the knee.

**Follow-ups:**
- *eps too small / too large?* Too small: most points become noise. Too large: clusters merge into one.
- *Varying density?* Use HDBSCAN or OPTICS (Q29).
- *Is it deterministic?* Core points yes; border points reachable from two clusters depend on visit order.

**Common mistakes:** Not scaling features. Using DBSCAN in high dimensions without reducing first. Forgetting that label -1 means noise, not a cluster. Picking eps by eye on one plot only.

### Q7 ⭐⭐⭐ 🟡 How does Isolation Forest detect anomalies, and why do anomalies get isolated in fewer splits?
**Asked at:** Fintech (PhonePe, JPMC), Amazon, Booking/Klarna fraud teams
**Say this first (1 line):** Isolation Forest builds many random trees that split on a random feature at a random value; anomalies are few and different, so they get separated from the rest in very few splits, and short average path length means high anomaly score.

**Then explain:**
- **Training:** each tree is built on a small random subsample (default 256 rows) with random feature and random threshold splits until points are isolated or a depth limit is reached. No distances, no labels.
- **Why anomalies isolate fast:** a far-out point sits alone in empty space, so one or two random cuts separate it. A normal point sits in a crowd and needs many cuts.
- **Score:** average path length across trees, normalised by the expected path length of an unsuccessful search in a binary tree: s = 2^(−E[h]/c(n)). Near 1 means anomaly, around 0.5 or below means normal. In sklearn, `score_samples` returns the negative of this, so lower means more anomalous.
- **Strengths:** fast (roughly linear in n), works in many dimensions, no scaling needed, handles large data.
- **Weaknesses:** axis-parallel cuts miss anomalies hidden inside dense regions or off-axis; poor with irrelevant features; local density anomalies are missed (LOF is better there); `contamination` must be guessed for a hard threshold.

**Example:** 980 normal points from N(0,1) plus 20 random far points. Top-20 precision = 0.85; mean anomaly score 0.711 versus 0.431 for normal points.

**Code:**
```python
import numpy as np
from sklearn.ensemble import IsolationForest
rng = np.random.default_rng(0)
X = np.vstack([rng.normal(0, 1, (980, 2)), rng.uniform(-6, 6, (20, 2))])
y = np.r_[np.zeros(980), np.ones(20)]
m = IsolationForest(n_estimators=200, contamination=0.02, random_state=0).fit(X)
s = -m.score_samples(X)          # higher = more anomalous
top = np.argsort(-s)[:20]
print("precision@20:", y[top].mean())
print("mean score normal/anom:", s[y == 0].mean().round(3), s[y == 1].mean().round(3))
```
Output: `precision@20: 0.85`, `mean score normal/anom: 0.431 0.711`. (A few uniform "anomalies" land inside the normal blob by chance, so precision is not 1.0.)

**Follow-ups:**
- *Why subsample so small?* It reduces swamping and masking (normal points hiding anomalies) and makes it fast.
- *How set the threshold?* Use a score quantile tied to the review budget, not blindly `contamination` (Q12).
- *Categorical features?* Encode them first; random splits on one-hot columns work but are crude.

**Common mistakes:** Saying it models density (it does not, it measures isolation depth). Forgetting that sklearn's `score_samples` sign is flipped. Treating `contamination` as known. Expecting it to find collective or contextual anomalies.

### Q8 ⭐⭐⭐ 🟡 How do you evaluate a clustering when there are no labels?
**Asked at:** Product cos, Amazon India, GCCs
**Say this first (1 line):** Without labels I check three things: internal quality metrics (silhouette, Davies-Bouldin), stability across resamples and seeds, and above all whether the clusters are interpretable and useful for the business.

**Then explain:**
- **Internal metrics:** silhouette (higher is better, -1 to 1), Davies-Bouldin (lower is better), Calinski-Harabasz (higher is better). They measure compactness and separation, and they favour convex clusters.
- **Stability:** refit on bootstrap samples or different seeds and compare labels with ARI. Unstable clusters are probably noise.
- **Profile and sanity:** do cluster means differ in a way a human can name? Are sizes sensible (no 95% blob, no 12-user cluster)?
- **Visual:** project with PCA/UMAP and look, remembering the caveats.
- **External validation:** the cluster should predict something it was not built on (churn, spend, response to an offer), or an A/B test of segment-specific treatments.
- **Business use:** if different treatments by segment do not move a metric, the segmentation does not matter.

**Example:** 4-blob data: silhouette 0.624, Davies-Bouldin 0.529, Calinski-Harabasz 4948, and bootstrap-pair ARI 0.995, so strong structure and stable.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score, adjusted_rand_score
X, _ = make_blobs(1000, centers=4, random_state=1)
a = KMeans(4, n_init=10, random_state=0).fit(X)
print("sil", round(silhouette_score(X, a.labels_), 3), "DB", round(davies_bouldin_score(X, a.labels_), 3),
      "CH", round(calinski_harabasz_score(X, a.labels_)))
# stability: refit on two bootstrap samples, compare labels on the full data
rng = np.random.default_rng(0)
labs = []
for _ in range(2):
    idx = rng.choice(len(X), len(X))
    labs.append(KMeans(4, n_init=10, random_state=0).fit(X[idx]).predict(X))
print("bootstrap ARI", round(adjusted_rand_score(*labs), 3))
```
Output: `sil 0.624 DB 0.529 CH 4948`, `bootstrap ARI 0.995`.

**Follow-ups:**
- *Why can't you compare silhouette across algorithms?* It favours convex clusters, so it prefers k-means-style output over DBSCAN shapes (Q16).
- *Good clusters but no business value?* Then go back to features; clustering on the wrong features gives clean but useless groups.
- *Any labels available later?* Use ARI/NMI (Q31).

**Common mistakes:** Picking the metric-optimal k and stopping. Not checking stability. Comparing silhouette between different feature sets. Skipping the business test.

### Q9 ⭐⭐⭐ 🟡 Case: segment customers for an e-commerce / food-delivery app. Walk through features, scaling, algorithm, validation, and how the business uses it.
**Asked at:** Flipkart, Swiggy, Zalando, Booking, Walmart GCC
**Say this first (1 line):** I would start from the business question, build RFM-style behavioural features per customer, transform and scale them, cluster (k-means first), validate stability and usefulness, and hand marketing named segments with a clear action for each.

**Then explain (framework):**
- **Goal:** what will segments drive? (offers, retention, assortment, delivery promises). This sets features and k.
- **Data and features** (per customer, over a fixed window, e.g. 90 days):
  - Recency, frequency, monetary value; average basket; discount sensitivity; category mix; order time-of-day/weekday; cancellation and return rate; delivery-time or rating signals; tenure; app engagement (sessions, searches without purchase).
  - Avoid including the thing you want to predict, and avoid IDs.
- **Preprocessing:** log-transform skewed counts and money (`log1p`), cap outliers, scale (standardise), drop highly correlated features or apply PCA, encode categoricals (share-of-category columns instead of labels).
- **Algorithm:** k-means (fast, explainable centres) or GMM for soft membership; try hierarchical on a sample to see structure. Use k from elbow, silhouette, stability, and what the business can run (Q2).
- **Validation:** stability across bootstrap and time windows; profile each cluster; check size and separation; test that segments differ on an outcome not used in clustering (retention, LTV).
- **Activation:** name each segment ("weekend big-basket families", "discount hunters", "lapsed loyalists"), define a treatment, A/B test it, and monitor the segment mix monthly.
- **Pitfalls:** segments that change every run, one huge "average" cluster, features dominated by money.

**Example:** For a food app, k=5: heavy lunch regulars (high frequency, low basket), weekend families (low frequency, high basket), discount-driven (>70% of orders with a coupon), new and exploring, lapsed. Each gets a different message and offer.

**Follow-ups:**
- *Why not just RFM rules?* Rules are simple and good as a baseline; clustering finds combinations you did not think of.
- *How often to refresh?* Re-run on a schedule, keep a stable mapping of old to new labels, and watch for drift (Q30).
- *Segments vs predictive models?* Segments describe; a churn or uplift model decides who to target. Use both.

**Common mistakes:** Clustering raw skewed numbers. Not scaling. Too many segments. Naming clusters from the plot instead of the profile table. No plan for how the business uses the output.

### Q10 ⭐⭐⭐ 🟡 Why must you scale features before k-means or PCA? How do you handle categorical or mixed-type features?
**Asked at:** Product cos, Microsoft IDC, GCCs
**Say this first (1 line):** Both methods use distances or variance, so a feature measured in big units (income in rupees) would swamp one in small units (orders per month); scaling puts them on equal footing. For categorical data, encode carefully or use a method built for mixed types such as k-prototypes or Gower distance.

**Then explain:**
- **k-means:** it uses Euclidean distance. A column with range 0-100000 dominates one with range 0-10.
- **PCA:** it picks directions of maximum variance. Unscaled, PC1 is just the largest-unit column. (If all features share units, e.g. pixels, you may skip scaling.)
- **How:** standardise (z-score), or robust-scale if there are outliers; log-transform heavy tails first.
- **Categorical features:**
  - One-hot works for k-means only loosely (distances become odd, and many one-hot columns outweigh numeric ones).
  - **k-modes** for all-categorical (uses mismatch counts and modes); **k-prototypes** for mixed.
  - **Gower distance** + hierarchical clustering or DBSCAN for mixed types.
  - Or embed categories (target-free: frequency, share of category) or learn embeddings, then cluster.
  - For PCA: one-hot plus PCA is allowed but crude; MCA (multiple correspondence analysis) or FAMD is the proper tool.
- **Order:** fit the scaler on training data only, then reuse it for new data.

**Example:** Two features: orders per month (informative, true groups at 5 and 8) and income (pure noise, std 20000). Raw k-means ARI vs true groups: 0.0, because income decides the clusters. After standardising: 0.56.

**Code:**
```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score as ari
rng = np.random.default_rng(0)
grp = rng.integers(0, 2, 600)
orders = rng.normal(5 + 3 * grp, 1.5)              # informative, small scale
income = rng.normal(60000, 20000, 600)             # noise, huge scale
X = np.c_[orders, income]
raw = KMeans(2, n_init=10, random_state=0).fit_predict(X)
sc = KMeans(2, n_init=10, random_state=0).fit_predict(StandardScaler().fit_transform(X))
print("ARI vs true group  raw:", round(ari(grp, raw), 2), " scaled:", round(ari(grp, sc), 2))
```
Output: `ARI vs true group  raw: 0.0  scaled: 0.56`.

**Follow-ups:**
- *Does scaling help if features are not equally important?* Scaling makes them equal by default; weight columns if some matter more.
- *Tree models and scaling?* Not needed; trees are scale-invariant.
- *Outliers?* Use robust scaling (median, IQR) or clip.

**Common mistakes:** Fitting the scaler on all data before the split. Label-encoding categories (implies fake order). Using one-hot at full weight so a 12-level categorical swamps numerics. Scaling away a meaningful unit like pixel intensities.

### Q11 ⭐⭐⭐ 🟡 How do you decide how many principal components to keep? (explained variance, scree, cross-validation)
**Asked at:** Product cos, GCCs, Europe
**Say this first (1 line):** I keep enough components to explain a target share of variance (often 90-95%), cross-check with a scree plot, and when there is a downstream task I pick the number by cross-validated performance of that task.

**Then explain:**
- **Cumulative explained variance:** keep the smallest k reaching a threshold (90-95%). In sklearn, `PCA(n_components=0.95)`.
- **Scree plot:** plot eigenvalues; keep components before the elbow. Kaiser rule (eigenvalue > 1 on standardised data) is a rough guide.
- **Cross-validation:** for supervised use, treat k as a hyperparameter inside a pipeline and pick by CV score. For reconstruction, hold out data and measure reconstruction error.
- **Other:** parallel analysis (compare with eigenvalues from shuffled data), Minka's MLE (`n_components="mle"`).
- Depends on purpose: visualisation needs 2-3; denoising keeps the big ones; modelling uses CV.

**Example:** On the digits data (64 pixels), after standardising, 31 components give 90% of variance and 40 give 95%. Logistic-regression CV accuracy: 5 comps 0.771, 15 comps 0.892, 30 comps 0.907, 45 comps 0.922. Accuracy still creeps up after the variance threshold, so the "right" k depends on the task.

**Code:**
```python
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
X, y = load_digits(return_X_y=True)
p = PCA().fit(StandardScaler().fit_transform(X))
cum = p.explained_variance_ratio_.cumsum()
print("components for 90% / 95%:", (cum < .90).sum() + 1, (cum < .95).sum() + 1)
for k in (5, 15, 30, 45):
    pipe = make_pipeline(StandardScaler(), PCA(k), LogisticRegression(max_iter=2000))
    print(k, cross_val_score(pipe, X, y, cv=5).mean().round(3))
```
Output: `components for 90% / 95%: 31 40`, then `5 0.771`, `15 0.892`, `30 0.907`, `45 0.922`.

**Follow-ups:**
- *Is 95% always right?* No. Noisy data may need less (the tail is noise); precise reconstruction needs more.
- *Why PCA inside the CV pipeline?* To avoid leakage: PCA must be fitted on each training fold only.
- *Variance threshold vs target?* Variance does not mean predictive, so the supervised check matters.

**Common mistakes:** Choosing k on the full data before cross-validation. Using the Kaiser rule on unscaled data. Treating the variance threshold as sacred. Keeping 2 components for modelling just because the plot looks nice.

### Q12 ⭐⭐⭐ 🟡 You have no labels and must detect anomalies (fraud, bad orders, sensor faults). How do you choose a method, set a threshold, and evaluate it?
**Asked at:** PhonePe, Klarna, JPMC, Amazon, Swiggy
**Say this first (1 line):** I would start with simple baselines and Isolation Forest, define the anomaly type and review capacity, set the threshold from that capacity (top-k or a score quantile) rather than a guessed contamination, and evaluate with analyst feedback, precision@k and any weak labels, then iterate.

**Then explain (framework):**
- **Requirements:** what is an anomaly (point, contextual, collective)? Cost of a miss vs a false alarm? How many alerts per day can humans review? Latency (batch or real time)?
- **Data and features:** build behaviour features per entity and window (amount z-score against own history, velocity counts, ratios, device/geo changes). Good features matter more than the algorithm.
- **Method choice:**
  - Low dimensional, one feature: z-score / MAD / IQR on the right baseline.
  - Many numeric features, large data: Isolation Forest.
  - Varying density: LOF.
  - Strong linear structure: PCA reconstruction error. Rich non-linear structure with lots of data: autoencoder.
  - Time series: seasonal decomposition or forecast residuals.
- **Threshold:** pick by budget (flag the top 0.5%), by a score quantile on a clean window, or by cost (flag when expected loss > review cost). Use `contamination` only as a convenience.
- **Evaluation:** no labels means weak signals: precision@k from analyst review of a sample, PR-AUC on any confirmed cases, injected synthetic anomalies, and stability across time. Use PR-AUC, not accuracy or ROC-AUC, at extreme imbalance.
- **Deploy and monitor:** score distribution drift, alert volume, analyst-confirmed rate; feed confirmed cases back to move toward supervised learning.

**Example:** 5000 normal + 50 anomalous points in 5-D, Isolation Forest: PR-AUC 0.992 (base rate 0.0099). Flagging the top 1% gives 51 alerts, precision 0.96, recall 0.98.

**Code:**
```python
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score
rng = np.random.default_rng(0)
Xn = rng.normal(0, 1, (5000, 5)); Xa = rng.normal(3, 1.5, (50, 5))
X = np.vstack([Xn, Xa]); y = np.r_[np.zeros(5000), np.ones(50)]
s = -IsolationForest(random_state=0).fit(X).score_samples(X)
print("PR-AUC", round(average_precision_score(y, s), 3), "base rate", round(y.mean(), 4))
thr = np.quantile(s, 0.99)               # alert on top 1% (review budget)
flag = s >= thr
print("flagged", flag.sum(), "precision", round(y[flag].mean(), 2), "recall", round(y[flag].sum() / y.sum(), 2))
```
Output: `PR-AUC 0.992 base rate 0.0099`, `flagged 51 precision 0.96 recall 0.98`. (Synthetic and easy; real data is far messier.)

**Follow-ups:**
- *No labels at all, how do you know it works?* Analyst review of top alerts, injected anomalies, and tracking confirmed-hit rate over time.
- *Threshold drifts?* Recalibrate on a rolling window; alert on rank or quantile, not an absolute score.
- *When to move to supervised?* Once you have enough confirmed labels, train a classifier and keep the unsupervised score as a feature.

**Common mistakes:** Jumping to deep models. Using accuracy. Trusting `contamination`. Ignoring review capacity. Not defining what counts as anomalous before picking a method.

### Q13 ⭐⭐ 🟢 Explain hierarchical (agglomerative) clustering: linkage types, dendrogram, and how you cut it.
**Asked at:** Product cos, GCCs, Europe
**Say this first (1 line):** Agglomerative clustering starts with every point as its own cluster and repeatedly merges the two closest clusters until one remains; the linkage rule defines "closest", and you cut the resulting dendrogram at a height to get the clusters.

**Then explain:**
- **Linkage:**
  - **Single:** distance between the closest pair of points. Finds elongated shapes but "chains" and merges through noise.
  - **Complete:** distance between the farthest pair. Compact clusters, sensitive to outliers.
  - **Average:** mean of all pairwise distances. A compromise.
  - **Ward:** merge the pair that increases within-cluster variance the least. Gives compact, similar-sized clusters; Euclidean only; the usual default.
- **Dendrogram:** a tree of merges; vertical axis is merge distance. A long vertical gap with no merges suggests a natural cut.
- **Cutting:** choose k clusters or a distance threshold. Cutting at the largest jump in merge heights is a common heuristic.
- **Cost:** O(n²) memory and about O(n² log n) to O(n³) time, so it suits up to tens of thousands of points. Deterministic, no k needed up front, no centres.
- Merges are greedy and cannot be undone.

**Example:** On 3 overlapping blobs (300 points), ARI against the true labels: single 0.0 (one giant chain), complete 0.51, average 0.66, Ward 0.53. The last three Ward merge heights were 17.5, 28.7, 41.5; a jump signals where to cut. The point: linkage choice matters, and single is risky on noisy data.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_blobs
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import adjusted_rand_score as ari
X, y = make_blobs(300, centers=3, random_state=0)
for m in ("single", "complete", "average", "ward"):
    Z = linkage(X, method=m)
    lab = fcluster(Z, t=3, criterion="maxclust")
    print(m, "ARI", round(ari(y, lab), 2))
print("last 3 ward merge heights:", Z[-3:, 2].round(1))   # big jump => natural cut
```
Output: `single ARI 0.0`, `complete ARI 0.51`, `average ARI 0.66`, `ward ARI 0.53`, `last 3 ward merge heights: [17.5 28.7 41.5]`.

**Follow-ups:**
- *Why not for 10M rows?* Quadratic memory. Cluster a sample, or use k-means first and cluster the centroids.
- *Divisive vs agglomerative?* Divisive is top-down and rarer; agglomerative is standard.
- *Distance metrics?* Any for single/complete/average (cosine, Gower); Ward needs Euclidean.

**Common mistakes:** Using single linkage on noisy data. Forgetting to scale. Reading the dendrogram's leaf order as meaningful. Using it on huge data.

### Q14 ⭐⭐ 🟢 What is the curse of dimensionality and how does it affect distance-based methods like k-means, DBSCAN and kNN?
**Asked at:** Product cos, Microsoft IDC, Europe
**Say this first (1 line):** As dimensions grow, data becomes sparse and distances between points concentrate: the nearest and farthest neighbours end up almost equally far, so distance-based methods lose their ability to tell near from far.

**Then explain:**
- **Sparsity:** to cover a space at the same density you need exponentially more points as dimensions increase.
- **Distance concentration:** in high dimensions the ratio (max distance) / (min distance) from a point tends to 1.
- **k-means:** centres become barely distinguishable, clusters are unstable.
- **DBSCAN:** a single eps fails because few points have dense neighbourhoods; most become noise.
- **kNN:** neighbours are no more similar than random points, so accuracy drops.
- **Also:** most of a hypercube's volume sits near its corners/surface; irrelevant features add noise to every distance.
- **Remedies:** feature selection, PCA/UMAP before clustering, cosine or learned (embedding) distances, domain-driven features, more data, approximate nearest-neighbour on embeddings.

**Example:** 1000 uniform random points and one query; ratio of the farthest to nearest distance: d=2 → 135.6; d=10 → 4.5; d=100 → 1.39; d=1000 → 1.11. By 1000 dimensions every point is almost the same distance away.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
for d in (2, 10, 100, 1000):
    X = rng.uniform(size=(1000, d))
    q = rng.uniform(size=d)
    dist = np.linalg.norm(X - q, axis=1)
    print(d, "max/min distance ratio:", round(dist.max() / dist.min(), 2))
```
Output: `2 ... 135.62`, `10 ... 4.48`, `100 ... 1.39`, `1000 ... 1.11`.

**Follow-ups:**
- *Does it hit real data as hard?* Less so when the data lies on a low-dimensional manifold (embeddings), which is why reducing first works.
- *Cosine vs Euclidean?* Cosine helps with scale/length effects but does not remove concentration.
- *Do trees suffer?* Less; they select features instead of using all distances equally.

**Common mistakes:** Saying "more features is always better". Running DBSCAN on 500 raw features. Blaming dimensions when the real problem is irrelevant or unscaled features.

### Q15 ⭐⭐ 🟡 Gaussian Mixture Models and the EM algorithm: how do they work and how do they differ from k-means (soft vs hard assignment)?
**Asked at:** Product cos, Amazon, Microsoft IDC, Europe
**Say this first (1 line):** A Gaussian Mixture Model says the data is a blend of k Gaussians and fits their weights, means and covariances with EM; unlike k-means it gives soft probabilities of belonging to each cluster and can model elongated, tilted clusters.

**Then explain:**
- **Model:** p(x) = Σ π_k · N(x | μ_k, Σ_k).
- **EM, repeated until the log-likelihood stops improving:**
  - **E-step:** compute each point's responsibility for each component (posterior probability).
  - **M-step:** update π, μ, Σ using responsibility-weighted averages.
- **Soft vs hard:** k-means gives one label; GMM gives probabilities (0.7 / 0.3), which suits points between clusters.
- **Link:** k-means is GMM with equal, spherical covariance and the variance shrinking to zero, so assignments become hard.
- **Covariance types:** `full`, `tied`, `diag`, `spherical` trade flexibility for parameters.
- **Cautions:** local optima (use `n_init`), a component can collapse onto one point (singular covariance; add `reg_covar`), pick k by BIC/AIC (Q42), also needs scaling.

**Example:** One elongated tilted cluster plus one round cluster. GMM ARI 0.98 versus k-means 0.91. For a point halfway between, GMM would show something like 0.55 / 0.45; k-means just picks one.

**Code:**
```python
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score as ari
rng = np.random.default_rng(0)
A = rng.multivariate_normal([0, 0], [[4, 3.6], [3.6, 4]], 500)   # elongated, tilted
B = rng.multivariate_normal([4, -2], [[1, 0], [0, 1]], 500)
X = np.vstack([A, B]); y = np.r_[np.zeros(500), np.ones(500)]
g = GaussianMixture(2, covariance_type="full", n_init=5, random_state=0).fit(X)
km = KMeans(2, n_init=10, random_state=0).fit_predict(X)
print("GMM ARI", round(ari(y, g.predict(X)), 2), " KMeans ARI", round(ari(y, km), 2))
print("soft probs, 3 points:", g.predict_proba(X[[0, 600, 400]]).round(2).tolist())
```
Output: `GMM ARI 0.98  KMeans ARI 0.91`; the three sampled points had near-certain probabilities (about 0/1), since they were well inside clusters.

**Follow-ups:**
- *Does EM always converge?* The likelihood never decreases, so it converges to a local maximum or saddle point.
- *When pick GMM over k-means?* Overlapping, elongated clusters, or when you need probabilities or a density model (also usable for anomaly detection).
- *Cost?* O(n·k·d²) for full covariance per iteration.

**Common mistakes:** Calling GMM "just k-means with probabilities". Ignoring singular covariances. Choosing k without BIC. Assuming data must be truly Gaussian.

### Q16 ⭐⭐ 🟡 Explain the silhouette score: how it is computed, how to read it, and its limitations.
**Asked at:** Product cos, GCCs
**Say this first (1 line):** For each point, the silhouette compares its average distance to its own cluster (a) with its average distance to the nearest other cluster (b): s = (b − a) / max(a, b). It runs from -1 (probably misassigned) to +1 (well inside its cluster), and the mean over all points scores the clustering.

**Then explain:**
- **Reading it:** near 1 is tight and separated; near 0 means on a boundary; negative means closer to another cluster. Rough guide: above 0.5 reasonable structure, 0.25-0.5 weak, below 0.25 little structure.
- **Uses:** pick k, compare runs of the same algorithm on the same features, find badly fitted points with per-sample silhouettes and silhouette plots.
- **Limits:**
  - Favours convex, round clusters, so it penalises correct DBSCAN shapes.
  - Cost is O(n²) (sample large data).
  - Not comparable across different feature sets or scalings.
  - Tends to prefer small k (merging looks cleaner).
  - Undefined for a single cluster; noise points complicate DBSCAN.
  - A high score does not mean business value.

**Example:** Three blobs: silhouette 0.472. On two interleaved moons, k-means (wrong split) scores 0.489, while the correct DBSCAN labelling scores only 0.329 (its one noise point is dropped before scoring). So a higher silhouette can reflect the worse clustering.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_blobs, make_moons
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, silhouette_samples
X, _ = make_blobs(500, centers=3, random_state=0)
lab = KMeans(3, n_init=10, random_state=0).fit_predict(X)
print("blobs sil", round(silhouette_score(X, lab), 3))
M, _ = make_moons(500, noise=0.06, random_state=0)
db = DBSCAN(eps=0.15).fit_predict(M)
print("moons: kmeans sil", round(silhouette_score(M, KMeans(2, n_init=10, random_state=0).fit_predict(M)), 3),
      " DBSCAN (correct shape) sil", round(silhouette_score(M[db != -1], db[db != -1]), 3))   # noise label dropped
i = 0; d = np.linalg.norm(X - X[i], axis=1)          # one point by hand
a = d[lab == lab[i]].sum() / ((lab == lab[i]).sum() - 1)
b = min(d[lab == c].mean() for c in set(lab) if c != lab[i])
print("manual", round((b - a) / max(a, b), 4), "sklearn", round(silhouette_samples(X, lab)[i], 4))
```
Output: `blobs sil 0.472`, `moons: kmeans sil 0.489  DBSCAN (correct shape) sil 0.329`, `manual 0.6295 sklearn 0.6295`.

**Follow-ups:**
- *Large n?* Use `sample_size` in `silhouette_score` or a sample of rows.
- *Alternatives?* Davies-Bouldin, Calinski-Harabasz, DBCV for density-based clusters, stability.
- *Why divide the in-cluster sum by n−1?* The point itself is excluded.

**Common mistakes:** Using it to compare k-means with DBSCAN. Trusting one number. Not looking at per-cluster silhouettes. Comparing across different scalings.

### Q17 ⭐⭐ 🟡 How does k-means++ initialisation work, and why does initialisation matter (local minima, n_init)?
**Asked at:** Product cos, Amazon
**Say this first (1 line):** K-means++ picks the first centre at random, then picks each next centre with probability proportional to its squared distance from the nearest centre already chosen, so starting centres are spread out; this avoids the bad local minima that random starts often hit and has a proven O(log k) approximation guarantee in expectation.

**Then explain:**
- **Why init matters:** k-means only finds a local minimum. Two centres starting inside one true cluster and none in another gives a poor, stuck solution.
- **k-means++ steps:** (1) choose one centre uniformly at random; (2) for every point compute D(x)², the squared distance to the nearest chosen centre; (3) sample the next centre with probability proportional to D(x)²; (4) repeat until k centres, then run Lloyd's.
- **n_init:** run the whole thing several times with different seeds and keep the lowest inertia. from sklearn 1.4 the default is `"auto"`, which means 1 run with k-means++ (10 with random init); older versions defaulted to 10. Set it explicitly.
- **Cost:** init is O(n·k·d), small compared with the iterations.
- **Extras:** k-means|| for distributed data; sampling-based or mini-batch variants for huge data.

**Example:** 10 true blobs, 20 seeds: random init, single run → median SSE 3132, worst 10573. k-means++ single run → median 2285, worst 2705. k-means++ with 10 restarts → median 2215, worst 2222. Much more reliable.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
X, _ = make_blobs(2000, centers=10, cluster_std=0.8, random_state=3)
for init, n in (("random", 1), ("k-means++", 1), ("k-means++", 10)):
    sse = [KMeans(10, init=init, n_init=n, random_state=s).fit(X).inertia_ for s in range(20)]
    print(init, "n_init", n, "median/worst SSE:", round(np.median(sse)), round(max(sse)))
```
Output: `random n_init 1: 3132 10573`, `k-means++ n_init 1: 2285 2705`, `k-means++ n_init 10: 2215 2222`.

**Follow-ups:**
- *Does k-means++ guarantee the global optimum?* No, only an expected O(log k) approximation of the optimum SSE.
- *Outliers and k-means++?* Far points have high D², so they can get picked as centres; restarts and outlier handling help.
- *Why set random_state?* Reproducibility.

**Common mistakes:** Using random init with a single run. Saying k-means++ removes local minima. Forgetting `random_state` so segments change every run.

### Q18 ⭐⭐ 🟡 What is Local Outlier Factor (LOF)? How does it differ from Isolation Forest, and when would you pick each?
**Asked at:** Fintech, GCCs, Europe fraud/risk
**Say this first (1 line):** LOF scores a point by comparing its local density with the density of its neighbours; a point sitting in a sparser area than its neighbours gets a score well above 1. Isolation Forest scores global isolation by random splits. Pick LOF when normal data has regions of very different density, Isolation Forest for large, high-dimensional data.

**Then explain:**
- **LOF steps:** find k nearest neighbours; compute reachability distances and local density; LOF = average (neighbour density / own density). About 1 means similar to neighbours; clearly above 1 means outlier.
- **Local vs global:** a point near a tight cluster that is "normal-looking" globally can still be a local outlier. LOF catches it; global methods may not.
- **Isolation Forest:** fast, roughly linear, handles many features, little tuning; weaker on local density anomalies.
- **LOF cost:** neighbour search, O(n²) worst case without an index; sensitive to k and to scaling; hurt by high dimensions.
- **Use:** `novelty=True` in sklearn allows scoring new data (fit on clean data); default `novelty=False` only scores the training set.

**Example:** A dense blob (std 0.3) next to a sparse blob (std 3), plus 3 points just outside the dense blob (not globally rare). ROC-AUC for catching them: LOF 1.0, Isolation Forest 0.953. LOF wins because "far for the dense group" is not "far overall".

**Code:**
```python
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
dense = rng.normal(0, 0.3, (500, 2)); sparse = rng.normal(8, 3, (500, 2))
local_out = np.array([[1.5, 1.5], [-1.4, 1.2], [0.2, -1.6]])   # far from the dense blob, but not globally rare
X = np.vstack([dense, sparse, local_out]); y = np.r_[np.zeros(1000), np.ones(3)]
s_lof = -LocalOutlierFactor(n_neighbors=20).fit(X).negative_outlier_factor_
s_if = -IsolationForest(random_state=0).fit(X).score_samples(X)
print("AUC  LOF", round(roc_auc_score(y, s_lof), 3), " IsolationForest", round(roc_auc_score(y, s_if), 3))
```
Output: `AUC  LOF 1.0  IsolationForest 0.953`. (Only 3 positives, so treat as illustration.)

**Follow-ups:**
- *How choose k (n_neighbors)?* Larger than the smallest cluster you care about, commonly 20-50; test sensitivity.
- *Scaling needed?* Yes, both for LOF and any distance method.
- *Streaming/real time?* Isolation Forest scores quickly; LOF with `novelty=True` works but needs the stored training data.

**Common mistakes:** Calling `score_samples` on new data without `novelty=True`. Forgetting the sign (sklearn's `negative_outlier_factor_`). Using LOF on 200 raw dimensions. Not scaling.

### Q19 ⭐⭐ 🟡 How can an autoencoder be used for anomaly detection? How do you set the threshold and what can go wrong?
**Asked at:** Product cos, fintech, Amazon, Microsoft IDC
**Say this first (1 line):** Train an autoencoder (compress then reconstruct) only on normal data; it learns to rebuild normal patterns well, so a high reconstruction error flags a point as anomalous, and I set the threshold from the error distribution on clean validation data or from the review budget.

**Then explain:**
- **Idea:** a narrow bottleneck forces the network to learn the structure of normal data. Anomalies break that structure and reconstruct badly.
- **Score:** per-row mean squared error between input and reconstruction (per-feature errors also help explain the alert).
- **Threshold:** a high percentile (e.g. 99th) of validation error on normal data; or mean + 3 std (weak if errors are skewed); or top-k to fit analyst capacity; or tune on a few labelled cases using PR curves.
- **What can go wrong:**
  - Training data is contaminated with anomalies, so the model learns to reconstruct them.
  - Too much capacity: it reconstructs everything (identity), anomalies included.
  - Unscaled features: large-scale columns dominate the error.
  - Drift: "normal" changes, so errors creep up and false alarms rise.
  - Anomalies that are "simple" (e.g. all zeros) can reconstruct easily.
  - Categorical features need encoding.
- **Compare to baselines first:** PCA and Isolation Forest are often as good on tabular data and far cheaper.

**Example:** 10 features driven by 3 hidden factors. A small autoencoder (16-3-16, sklearn `MLPRegressor` as a stand-in) trained on normal rows: threshold = 99th percentile of training error = 0.067; it caught 100% of 60 random-noise anomalies with 1.5% false alarms on held-out normals; AUC 1.0. (Easy synthetic case.)

**Code:** (sklearn MLP as an autoencoder; in production use PyTorch/Keras)
```python
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
X = rng.normal(size=(3000, 3)) @ rng.normal(size=(3, 10)) + 0.05 * rng.normal(size=(3000, 10))  # normal: ~3-D structure
Xa = rng.normal(size=(60, 10)) * 2                      # anomalies break the structure
tr, val = X[:2000], X[2000:]
sc = StandardScaler().fit(tr)
ae = MLPRegressor(hidden_layer_sizes=(16, 3, 16), max_iter=800, random_state=0).fit(sc.transform(tr), sc.transform(tr))
err = lambda A: ((ae.predict(sc.transform(A)) - sc.transform(A)) ** 2).mean(1)   # per-row reconstruction error
thr = np.quantile(err(tr), 0.99)
y = np.r_[np.zeros(len(val)), np.ones(len(Xa))]
print("AUC", round(roc_auc_score(y, np.r_[err(val), err(Xa)]), 3), "| threshold", round(thr, 3),
      "| anomalies caught", (err(Xa) > thr).mean().round(2), "| false alarms", (err(val) > thr).mean().round(3))
```
Output: `AUC 1.0 | threshold 0.067 | anomalies caught 1.0 | false alarms 0.015`.

**Follow-ups:**
- *Why not just PCA?* Linear autoencoder is essentially PCA; autoencoders add non-linearity, which helps only with enough data and non-linear structure.
- *Contaminated training set?* Filter with a first-pass detector, use robust or denoising variants, or train on a trusted period.
- *VAE?* Adds a probabilistic latent space; use reconstruction probability or ELBO as the score (Q44).

**Common mistakes:** Not scaling inputs. Choosing the threshold on data that includes anomalies. Making the bottleneck too wide. Skipping simple baselines. Never retraining as normal behaviour drifts.

### Q20 ⭐⭐ 🟡 What is the relationship between PCA and k-means?
**Asked at:** Data Scientist/MLE loops (Interview Query tag, March 2025)
**Say this first (1 line):** Both are about variance: PCA finds the directions of greatest variance, k-means minimises within-cluster variance, and the two are mathematically linked (Ding and He, 2004, showed that the continuous relaxation of the k-means cluster indicators is solved by the top k−1 principal components, so PCA gives a relaxed, approximate k-means solution); in practice we run PCA first to denoise and speed up k-means.

**Then explain:**
- **Theory:** relaxing k-means' discrete cluster-indicator to continuous values gives a PCA problem. The continuous solution lies in the space of the top k−1 principal components (the data projected onto them), so PCA "softly" does what k-means does. It is only a relaxation: you still have to turn it into discrete clusters, and the best discrete clusters may differ.
- **Practice (PCA → k-means):** reduces noise, removes correlated features, speeds up distance computations, and counters the curse of dimensionality (Q14). Keep enough variance (e.g. 90-95%).
- **Opposite direction:** k-means can act as a "dictionary" or quantiser: cluster distances as features.
- **Caution:** PCA can drop low-variance directions that separate clusters; check ARI/silhouette both ways. Cluster labels live in the PCA space, so interpret profiles back in original features.

**Example:** Digits (64 pixels). K-means (k=10), ARI against true labels: full 64-d 0.666; after PCA to 20 comps 0.668. Same quality, 3x fewer dimensions.

**Code:**
```python
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score as ari
X, y = load_digits(return_X_y=True)
a = KMeans(10, n_init=10, random_state=0).fit_predict(X)
b = KMeans(10, n_init=10, random_state=0).fit_predict(PCA(20, random_state=0).fit_transform(X))
print("ARI vs digit labels  full 64-d:", round(ari(y, a), 3), " PCA-20:", round(ari(y, b), 3))
```
Output: `ARI vs digit labels  full 64-d: 0.666  PCA-20: 0.668`.

**Follow-ups:**
- *Does PCA always help k-means?* No; it helps with noisy, redundant features, but can hurt if separation lies in small-variance directions.
- *Whiten before k-means?* Usually not; it equalises all component variances and boosts noise.
- *What is k-means equivalent to in a factor view?* Matrix factorisation with a one-hot (hard) membership matrix; PCA is the same with an unconstrained one.

**Common mistakes:** Saying "PCA is clustering". Stating the Ding-He result as exact for the discrete solution (it is for the relaxed problem). Running PCA on all data including new points. Dropping to 2 components and clustering just for convenience.

### Q21 ⭐⭐ 🟡 How can PCA be used for anomaly detection (reconstruction error, Mahalanobis distance in PC space)?
**Asked at:** Fintech, GCC, industrial analytics
**Say this first (1 line):** Fit PCA on normal data, then flag points that either reconstruct badly (large residual, i.e. they break the correlation structure) or sit far out inside the retained subspace (large Mahalanobis distance, i.e. extreme but structurally normal); you usually need both scores because each catches a different anomaly type.

**Then explain:**
- **Reconstruction error (SPE / Q-statistic):** project onto top k components, map back, measure ||x − x̂||². Catches points that violate the correlations (e.g. two sensors that always move together suddenly diverge).
- **Mahalanobis in PC space (Hotelling T²):** Σ z_j² / λ_j over the k retained components; catches points that follow the usual pattern but with extreme magnitude.
- **Thresholds:** percentile on clean data, or chi-square (T²) and Jackson-Mudholkar-type limits (SPE) in classical process monitoring.
- **Choosing k:** too few components: normal variation looks like residual; too many: anomalies get reconstructed. Pick by CV or explained variance.
- **Pros:** fast, linear, explainable (per-feature residual contributions). **Cons:** linear structure only, sensitive to outliers in the training data (use robust PCA), needs scaling.

**Example:** 8 correlated sensors, 2 true factors. Off-subspace anomalies: reconstruction AUC 1.0, Mahalanobis AUC 0.46. Extreme-but-on-subspace anomalies (6 sigma along PC1): reconstruction AUC 0.04, Mahalanobis AUC 1.0. Each metric misses the other's anomaly type.

**Code:**
```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
z = rng.normal(size=(2000, 2)); X = z @ rng.normal(size=(2, 8)) + 0.1 * rng.normal(size=(2000, 8))
A1 = X[:20] + rng.normal(0, 1, (20, 8))                 # off-subspace anomalies (big residual)
tr, test_norm = X[200:], X[:200]
p = PCA(2).fit(tr)
# on-subspace but extreme: scale the top PC direction to 6 sigma
A2 = p.mean_ + 6 * np.sqrt(p.explained_variance_[0]) * p.components_[0] + 0.05 * rng.normal(size=(20, 8))
def scores(A):
    Z = p.transform(A)
    recon = ((A - p.inverse_transform(Z)) ** 2).sum(1)
    mahal = (Z ** 2 / p.explained_variance_).sum(1)     # Mahalanobis distance inside PC space
    return recon, mahal
nr, nm = scores(test_norm)
for name, A in (("off-subspace", A1), ("extreme-in-subspace", A2)):
    r, m = scores(A); y = np.r_[np.zeros(200), np.ones(20)]
    print(name, "AUC recon", round(roc_auc_score(y, np.r_[nr, r]), 2), " AUC mahal", round(roc_auc_score(y, np.r_[nm, m]), 2))
```
Output: `off-subspace AUC recon 1.0  AUC mahal 0.46`; `extreme-in-subspace AUC recon 0.04  AUC mahal 1.0`.

**Follow-ups:**
- *Why not Mahalanobis in the full space?* With near-singular covariance, tiny-variance directions explode the distance; PCA regularises.
- *Outliers in the training data?* They tilt the components; use robust PCA or a trimmed fit.
- *Explain an alert?* Look at which features contribute most to the residual.

**Common mistakes:** Using only reconstruction error. Fitting PCA on data that includes the anomalies. Not scaling. Using the wrong threshold distribution without checking it on clean data.

### Q22 ⭐⭐ 🟡 How does t-SNE work, what does perplexity do, and what are the traps when reading a t-SNE plot?
**Asked at:** Product cos, Spotify/Zalando, Microsoft IDC
**Say this first (1 line):** t-SNE turns pairwise distances into neighbour probabilities in high dimensions, does the same in 2D with a heavy-tailed t-distribution, and moves the 2D points to make the two sets of probabilities match (minimising KL divergence); perplexity roughly sets how many neighbours each point cares about.

**Then explain:**
- **High-dim side:** for each point, a Gaussian over neighbours with a width chosen so the effective neighbour count equals the perplexity (typical 5-50).
- **Low-dim side:** Student-t (1 degree of freedom) similarities. Heavy tails let moderately distant points sit far apart, relieving crowding.
- **Optimisation:** gradient descent on KL(P‖Q); non-convex, so seeds matter. Barnes-Hut makes it O(n log n); init with PCA for stability.
- **Perplexity:** low (2-5) fragments data into tiny clumps; high (50-100+) shows more global shape but blurs details. Try several.
- **Traps when reading the plot:**
  - Cluster size means nothing (it expands dense clusters).
  - Distances between clusters mean little.
  - Random noise can look like clusters at low perplexity.
  - Different seeds give different pictures.
  - Cannot embed new points directly.
  - Too few iterations gives a "pinched" unfinished picture.
- **Use:** visualisation and sanity-checking only, not clustering or features.

**Example:** 4 noisy Gaussian groups in 20-D. Perplexity 2 / 30 / 150: neighbourhood trustworthiness 0.934 / 0.956 / 0.934; silhouette of the true labels in 2D: 0.44 / 0.87 / 0.915. Very small perplexity fragments the picture; mid values preserve neighbours best. (The scores say nothing about between-cluster distances.)

**Code:**
```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.manifold import TSNE, trustworthiness
from sklearn.metrics import silhouette_score
X, y = make_blobs(600, n_features=20, centers=4, cluster_std=3.0, random_state=0)
for perp in (2, 30, 150):
    E = TSNE(2, perplexity=perp, init="pca", random_state=0).fit_transform(X)
    print("perplexity", perp, "trustworthiness(k=10):", round(trustworthiness(X, E, n_neighbors=10), 3),
          " silhouette of true labels in 2D:", round(silhouette_score(E, y), 3))
```
Output: `perplexity 2 trustworthiness(k=10): 0.934  silhouette: 0.44`; `30: 0.956, 0.87`; `150: 0.934, 0.915`.

**Follow-ups:**
- *Why not cluster on t-SNE?* Density and distances are distorted; clusters can be artefacts; no out-of-sample transform.
- *Why PCA first?* Denoises and cuts the cost (e.g. to 50 dims).
- *Better global structure?* PCA initialisation, higher perplexity, or UMAP.

**Common mistakes:** Interpreting cluster size or inter-cluster gaps. Single run, single perplexity. Using the embedding as model features. Not scaling features first.

### Q23 ⭐⭐ 🟡 How does UMAP differ from t-SNE (speed, global structure, reproducibility)? Can you cluster on UMAP output?
**Asked at:** Product cos, Europe scale-ups
**Say this first (1 line):** UMAP builds a weighted nearest-neighbour graph of the data and optimises a low-dimensional layout with the same graph structure; compared with t-SNE it is much faster, usually keeps more global structure, can transform new points, and you can cluster on its output, but only carefully.

**Then explain:**
- **Speed:** UMAP uses approximate nearest neighbours (NN-descent) and stochastic gradient descent with negative sampling; it scales to millions of points where t-SNE becomes painful.
- **Global structure:** better than t-SNE in practice (especially with spectral initialisation), but still not trustworthy for exact distances or cluster sizes.
- **Reproducibility:** both are stochastic. Set `random_state` (this slows UMAP because it disables parallelism); results still vary with data and hyperparameters. t-SNE with PCA init is similar in stability.
- **New data:** `umap.UMAP().transform` works; t-SNE has no standard transform.
- **Key hyperparameters:** `n_neighbors` (local vs global; 15 default), `min_dist` (how tightly points pack; smaller gives tighter clumps), `metric` (e.g. cosine for embeddings).
- **Clustering on UMAP output:**
  - Common practice: UMAP to 5-10 dims (not 2), then HDBSCAN (the BERTopic recipe).
  - Caveat: UMAP distorts density and can create or merge clusters, so verify with stability checks, different seeds and metrics in the original space.
  - Do not read cluster sizes or distances as true; use the 2D map for visualisation only.

**Example:** Embeddings of 5M product titles: PCA to 50 dims, UMAP (`n_neighbors=30`, `min_dist=0.0`, cosine) to 10 dims, HDBSCAN for topics, and a separate 2D UMAP for display.

**Code (runnable, sklearn only):** reduce first, then HDBSCAN (built into scikit-learn). PCA stands in for UMAP here; on this easy data both raw and reduced input work, so the point is the recipe, not the gain.
```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA
from sklearn.cluster import HDBSCAN
from sklearn.metrics import adjusted_rand_score
X, y = make_blobs(900, n_features=100, centers=5, cluster_std=5.0, random_state=0)
Z = PCA(10, random_state=0).fit_transform(X)            # reducer step: UMAP plugs in here
for name, A in (("raw 100-D", X), ("PCA to 10-D", Z)):
    lab = HDBSCAN(min_cluster_size=40).fit_predict(A)
    print(name, "| clusters:", len(set(lab) - {-1}), "| noise %:", round(100 * (lab == -1).mean(), 1),
          "| ARI:", round(adjusted_rand_score(y, lab), 3))
```
Output: `raw 100-D | clusters: 5 | noise %: 0.0 | ARI: 1.0`, `PCA to 10-D | clusters: 5 | noise %: 0.0 | ARI: 1.0`.

**UMAP version (not executed: `umap-learn` is not installed here):**
```python
import umap
from sklearn.cluster import HDBSCAN
Z = umap.UMAP(n_neighbors=30, min_dist=0.0, n_components=10,
              metric="cosine", random_state=42).fit_transform(X)
labels = HDBSCAN(min_cluster_size=50).fit_predict(Z)
```

**Follow-ups:**
- *Why min_dist=0 for clustering?* Packs points tightly, so density-based methods see clear clumps.
- *Is UMAP better than t-SNE always?* Not always; neither is a measuring instrument. t-SNE may show finer local detail.
- *Can UMAP be supervised?* Yes, pass `y` for supervised or semi-supervised embedding.

**Common mistakes:** Treating UMAP distances and cluster sizes as real. Clustering on a 2D plot only. Single seed or default parameters without sensitivity checks. Claiming UMAP "preserves global structure" as a guarantee.

### Q24 ⭐⭐ 🟡 Statistical outlier detection (z-score, IQR, MAD): when does each work and when does it fail?
**Asked at:** Product cos, GCCs, Walmart/Amazon analytics
**Say this first (1 line):** Z-score works for roughly normal data with few outliers, IQR and MAD are robust because they use quartiles and the median, and all three fail on skewed, multimodal or seasonal data, where you need a transform or a model-based baseline first.

**Then explain:**
- **Z-score** (|x − mean| / std > 3): simple, but mean and std are themselves dragged by outliers, so a cluster of outliers can hide itself (masking).
- **IQR rule** (outside Q1 − 1.5·IQR, Q3 + 1.5·IQR): uses quartiles, so up to 25% contamination does not break it. Fine for mild skew; no normality assumption.
- **MAD / modified z-score** (0.6745·(x − median)/MAD > 3.5): median-based, the most robust of the three (breakdown point 50%). Fails if MAD = 0 (many repeated values).
- **All three fail when:** data is heavily skewed (order values, latencies: use log first), data has several groups (compute per segment), there is trend or seasonality (detect on residuals), or the anomaly only shows up in a combination of features (use multivariate methods).
- Univariate rules ignore context: Rs 5,000 is normal for a metro user and odd for a new tier-3 user.

**Example:** 200 normal values around 100 plus 40 values around 300. Z-score flags 0 of the 40 (the outliers inflate the std to about 90, so 300 is under 3 sigma). IQR and MAD flag all 40 with zero false alarms. On 5,000 lognormal values with no true outliers, the flag rate is about 1.5% for z, 7.6% for IQR and 8.0% for MAD (lognormal sigma 1, all false alarms), and after taking logs it drops to about 1% or less for all three. So on skewed data, take logs first.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
x = np.r_[rng.normal(100, 10, 200), rng.normal(300, 10, 40)]   # 40 planted outliers
def z_flags(x, t=3):
    return np.abs((x - x.mean()) / x.std()) > t
def iqr_flags(x, k=1.5):
    q1, q3 = np.percentile(x, [25, 75]); i = q3 - q1
    return (x < q1 - k * i) | (x > q3 + k * i)
def mad_flags(x, t=3.5):
    med = np.median(x); mad = np.median(np.abs(x - med))
    return np.abs(0.6745 * (x - med) / mad) > t          # modified z-score
for n, f in (("z", z_flags), ("iqr", iqr_flags), ("mad", mad_flags)):
    print(n, "flagged planted:", f(x)[-40:].sum(), "of 40; false flags:", f(x)[:-40].sum())
x2 = np.random.default_rng(1).lognormal(0, 1, 5000)        # skewed data, no true outliers
print("lognormal flag rate %:", {n: round(100 * f(x2).mean(), 1) for n, f in (("z", z_flags), ("iqr", iqr_flags), ("mad", mad_flags))})
print("after log:", {n: round(100 * f(np.log(x2)).mean(), 1) for n, f in (("z", z_flags), ("iqr", iqr_flags), ("mad", mad_flags))})
```
Output: `z 0 of 40`, `iqr 40 of 40`, `mad 40 of 40`, all with 0 false flags; lognormal flag rates (%) `z 1.5, iqr 7.6, mad 8.0`, after log `0.3, 0.9, 0.1`.

**Follow-ups:**
- *Why 0.6745?* It makes MAD comparable to the standard deviation for normal data (MAD ≈ 0.6745σ).
- *Should you delete the flagged points?* Not automatically: first check if they are errors, rare-but-real events (big orders) or the exact thing you want to detect.
- *Skewed metric?* Log-transform, or use percentile thresholds per segment.

**Common mistakes:** Z-score on skewed data. Using mean/std when outliers are common. Applying one global threshold to many segments. Removing real extremes and then underestimating risk.

### Q25 ⭐⭐ 🟡 How do outliers affect k-means and PCA, and how do you make them robust (k-medoids, robust scaling, trimming)?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** Both k-means and PCA minimise squared error, so a few extreme points get huge weight: k-means wastes a centroid on them or drags centres, and PCA tilts its first component towards them; the fix is to trim or cap them, scale robustly, or use a robust method (k-medoids, robust PCA).
**Then explain:**
- **k-means:** the squared distance means one far point can cost more than hundreds of normal ones, so the optimiser may give outliers their own cluster and merge two real ones.
- **PCA:** it maximises variance, and variance is dominated by extremes, so PC1 can point at the outlier direction instead of the real structure.
- **Fixes, in order of effort:**
  - Winsorise (cap at 1st/99th percentile), log-transform skewed features, or trim points found by IQR/MAD or Isolation Forest.
  - Robust scaling (median and IQR) instead of mean and std, so the scaler is not distorted either.
  - k-medoids (centre must be a real point, uses absolute distance rather than squared) or a DBSCAN noise label; for PCA, robust PCA or a PCA fit on trimmed data.
  - Cluster with a GMM or HDBSCAN that has an explicit noise or heavy-tail component.
- **Do not drop blindly:** in fraud or high-value-customer work the "outliers" are the signal. Cluster the core, then score outliers separately.
- k-medoids (PAM) is O(k(n−k)²) per iteration, so it is slow on large n. Use CLARA or trimmed k-means instead.

**Example:** Two clean clusters at x = 0 and x = 8 (300 points each) plus 3 points at y around 65. k-means with k=2 puts one centroid on the outliers: centre error 65 for that cluster and 4.07 for the merged one. Without the outliers: 0.09 and 0.06. PCA: PC1 loading on the y-axis goes from 0.01 (clean) to 0.97 (with outliers). Trimming the 1% farthest from the median brings centre error back to 0.09.

**Code:**
```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
rng = np.random.default_rng(0)
A = rng.normal([0, 0], 1, (300, 2)); B = rng.normal([8, 0], 1, (300, 2))
X = np.r_[A, B, [[0, 60], [1, 70], [-1, 65]]]            # 3 extreme outliers
def err(c):   # distance of fitted centres to true centres (0,0) and (8,0)
    c = c[np.argsort(c[:, 0])]; return np.round(np.linalg.norm(c - [[0, 0], [8, 0]], axis=1), 2)
print("with outliers:", err(KMeans(2, n_init=10, random_state=0).fit(X).cluster_centers_))
print("PC1 |loading| with outliers:", np.round(np.abs(PCA(1).fit(X).components_[0]), 2))
d = np.linalg.norm(X - np.median(X, 0), axis=1); keep = d < np.percentile(d, 99)   # trim 1% farthest
print("trimmed:", err(KMeans(2, n_init=10, random_state=0).fit(X[keep]).cluster_centers_))
```
Output: `with outliers: [65. 4.07]`, `PC1 |loading| with outliers: [0.26 0.97]`, `trimmed: [0.09 0.09]`.

**Follow-ups:**
- *Is k-medoids always robust?* Much more than k-means, but costly, and still sensitive to many outliers.
- *Scale first or remove outliers first?* Find and handle outliers first, or use robust scaling, because a plain scaler is itself distorted.
- *Why is the L1 loss robust?* Its penalty grows linearly with distance, not quadratically.

**Common mistakes:** Standard-scaling data that still contains outliers. Deleting outliers without asking if they matter to the business. Using PCA before checking for outliers. Increasing k to "absorb" outliers.

### Q26 ⭐⭐ 🟡 PCA vs feature selection: does PCA help a supervised model, and what do you lose in interpretability?
**Asked at:** Product cos, fintech, GCCs
**Say this first (1 line):** PCA is unsupervised, so it keeps directions of high variance, not directions that predict the target; it helps with multicollinearity, noise and speed for linear models, but it rarely helps trees or boosting and it costs you interpretability, so feature selection is usually the better first choice.
**Then explain:**
- **PCA:** builds new features (linear mixes of all inputs). Ignores y. Good when many features are correlated, p is close to n, or you need fast inference/storage.
- **Feature selection** (L1, tree importance, mutual information, recursive elimination): keeps original features, so you can explain them, and it uses y.
- **Risk with PCA:** the predictive signal may live in a low-variance direction that PCA throws away (see example). Fix by keeping more components, picking k by cross-validated model score, or using supervised alternatives (PLS, LDA).
- **Interpretability loss:** every component mixes all features, so "PC3 = 0.3·income − 0.4·age + ..." has no business meaning. Fraud, credit and regulated models need reason codes, which PCA breaks.
- **Models:** linear/logistic regression and SVM can gain (stability); tree ensembles gain little because they pick splits on their own, and rotating the axes can hurt them.
- **Leakage:** fit scaler and PCA inside the cross-validation pipeline, on train folds only.

**Example:** 10 correlated high-variance columns (noise) and 2 low-variance columns that determine the label. Logistic regression on all 12 scaled features: AUC 0.982. PCA to 2 components first: 0.509 (chance), because the signal sits in tiny-variance directions. PCA with 11 components: 0.982, so more components recover it.

**Code:**
```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
rng = np.random.default_rng(0); n = 2000
big = rng.normal(size=(n, 2)) @ rng.normal(size=(2, 10)) * 5 + rng.normal(size=(n, 10))
small = rng.normal(0, 0.3, (n, 2))                          # low-variance columns hold the signal
y = (small[:, 0] + small[:, 1] + 0.1 * rng.normal(size=n) > 0).astype(int)
X = np.c_[big, small]
cv = lambda m: cross_val_score(m, X, y, cv=5, scoring="roc_auc").mean().round(3)
print("all features:", cv(make_pipeline(StandardScaler(), LogisticRegression())))
print("PCA(2):      ", cv(make_pipeline(StandardScaler(), PCA(2), LogisticRegression())))
print("PCA(11):     ", cv(make_pipeline(StandardScaler(), PCA(11), LogisticRegression())))
```
Output: `all features: 0.982`, `PCA(2): 0.509`, `PCA(11): 0.982`.

**Follow-ups:**
- *Then when is PCA worth it?* Multicollinearity, noisy sensors/images, very wide data, or when you only need a compact representation or visualisation.
- *Supervised alternative?* PLS regression, LDA, or a model with built-in regularisation (L1/L2, trees).
- *Can you recover meaning from components?* Partially, through loadings, but they stay mixed.

**Common mistakes:** Choosing k by explained variance alone. Fitting PCA on the full data before the train/test split. Applying PCA before tree models "to reduce dimensions". Forgetting that regulated models need explainable features.

### Q27 ⭐⭐ 🟡 How do you cluster high-dimensional data such as text or user embeddings? (reduce then cluster, cosine distance, HDBSCAN, BERTopic)
**Asked at:** Product cos, Spotify/Zalando, GenAI-adjacent teams
**Say this first (1 line):** Normalise the vectors so distance means cosine similarity, reduce dimensions (PCA, then optionally UMAP) to fight the curse of dimensionality, cluster with k-means or HDBSCAN, and then check the clusters by reading samples, because high-dimensional clusters are easy to fake.
**Then explain:**
- **Why not cluster raw 384/768-d vectors:** distances concentrate (everything looks equally far), cost grows, and noise dimensions dilute the signal.
- **Cosine, not Euclidean:** embedding direction carries meaning, length often does not. L2-normalise rows; then Euclidean on unit vectors ranks like cosine, so standard k-means works ("spherical k-means").
- **Reduce first:** PCA to 20-100 dims (cheap, denoises), and/or UMAP to 5-10 dims for density-based clustering. Use 2D UMAP only for plotting.
- **Algorithm:** k-means when you want exactly k balanced groups (fast, scales); HDBSCAN when k is unknown and you expect noise and uneven sizes. Agglomerative on a sample is useful for exploring hierarchy.
- **BERTopic recipe:** sentence embeddings, UMAP, HDBSCAN, then c-TF-IDF (TF-IDF per cluster) to extract top words as topic labels. Noise points get topic -1.
- **Validate:** read 10-20 random items per cluster, check cluster coherence, stability across seeds, and downstream usefulness.

**Example:** 1,500 vectors in 384-d from 6 true groups plus 150 random junk vectors. After L2-normalise and PCA(20), k-means (k=6) and HDBSCAN (min_cluster_size=40) both recover the 6 groups (ARI 1.0 on the real points). HDBSCAN returns 7 clusters, though: the junk vectors, once normalised, look alike and form their own cluster (only 0.7% were labelled noise). That is why you read samples, not trust the label count.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, HDBSCAN
from sklearn.metrics import adjusted_rand_score
X, y = make_blobs(1500, n_features=384, centers=6, cluster_std=6.0, random_state=0)
rng = np.random.default_rng(0)
X = np.r_[X, rng.uniform(X.min(), X.max(), (150, 384))]     # 150 random junk points
y = np.r_[y, -np.ones(150, int)]
Z = PCA(20, random_state=0).fit_transform(normalize(X))      # unit length, then PCA
core = y >= 0
km = KMeans(6, n_init=10, random_state=0).fit_predict(Z)
hd = HDBSCAN(min_cluster_size=40, copy=True).fit_predict(Z)
print("kmeans ARI:", round(adjusted_rand_score(y[core], km[core]), 3), " hdbscan ARI:", round(adjusted_rand_score(y[core], hd[core]), 3))
print("hdbscan clusters:", len(set(hd) - {-1}), " junk labelled noise %:", round(100 * (hd[~core] == -1).mean(), 1))
```
Output: `kmeans ARI: 1.0  hdbscan ARI: 1.0`, `hdbscan clusters: 7  junk labelled noise %: 0.7`.
(UMAP version, not executed because `umap-learn` is not installed: `umap.UMAP(n_components=10, metric="cosine", min_dist=0.0)` then HDBSCAN, as in Q23.)

**Follow-ups:**
- *How to choose k for embeddings?* Silhouette is weak here; use stability, topic coherence, and what the business can act on. Or let HDBSCAN decide, then merge small clusters.
- *HDBSCAN leaves 40% as noise?* Lower `min_samples` or `min_cluster_size`, then assign noise to the nearest cluster if you need full coverage.
- *Millions of vectors?* Cluster a sample, assign the rest with nearest-centroid or ANN (see Q45).

**Common mistakes:** Euclidean distance on un-normalised embeddings. Clustering a 2D t-SNE/UMAP plot. Trusting a cluster because its picture looks tidy. No manual inspection of cluster contents. Ignoring the noise group.

### Q28 ⭐⭐ 🟡 How do you evaluate an anomaly detector with very few labels? (precision@k, PR-AUC, contamination parameter, analyst feedback)
**Asked at:** Fintech (PhonePe, Klarna, JPMC), Amazon
**Say this first (1 line):** Use ranking metrics that fit the real workflow, mainly precision@k (how many of the top k alerts are real, where k is the analyst capacity) and PR-AUC, not accuracy or ROC-AUC, and add analyst feedback and injected synthetic anomalies to grow your labels.
**Then explain:**
- **Why not accuracy/ROC-AUC:** at 0.5% anomalies, "flag nothing" is 99.5% accurate, and ROC-AUC looks great even when most alerts are false because the true negatives dominate.
- **Precision@k / recall@k:** the team can review, say, 200 cases a day, so measure precision in the top 200. **PR-AUC (average precision)** summarises precision across recall levels; its baseline equals the anomaly rate.
- **Contamination parameter:** it only sets the cut-off (the expected anomaly share), not the quality of the ranking. Pick the threshold from review capacity or cost (cost of a miss vs cost of a review), not from a guessed contamination.
- **Few labels:** (1) review a random sample plus the top-k of the scores to estimate precision with confidence intervals, (2) inject synthetic anomalies (shift or break correlations) to test recall, (3) use confirmed cases as a hold-out, never to tune on the same ones.
- **Analyst feedback loop:** log accept/reject per alert; this becomes a labelled set for a supervised re-ranker later. Beware that labels exist only for flagged cases (see Q46).
- **Sanity checks:** do alerts cluster in one segment, does the score drift, do the top-ranked cases make business sense?

**Example:** 20,000 points, 100 true anomalies (0.5%). Isolation Forest scores: ROC-AUC 0.999 but PR-AUC 0.944, precision@50 = 1.0, @100 = 0.86, @500 = 0.20. Contamination 0.001 flags 20 (precision 1.0, recall 0.20); 0.005 flags 100 (0.86, 0.86); 0.02 flags 400 (0.25, 0.99). Same model, three very different operating points.

**Code:**
```python
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_auc_score, average_precision_score
rng = np.random.default_rng(0)
Xn = rng.normal(size=(19900, 6)); Xa = rng.normal(0, 1, (100, 6)) + rng.choice([-1, 1], (100, 6)) * 2.2
X = np.r_[Xn, Xa]; y = np.r_[np.zeros(19900), np.ones(100)]       # 0.5% anomalies
s = -IsolationForest(n_estimators=200, random_state=0).fit(X).score_samples(X)   # higher = more anomalous
print("ROC-AUC", round(roc_auc_score(y, s), 3), "PR-AUC", round(average_precision_score(y, s), 3))
top = np.argsort(-s)
for k in (50, 100, 500): print("precision@%d" % k, round(y[top[:k]].mean(), 2))
for c in (0.001, 0.005, 0.02):
    f = IsolationForest(n_estimators=200, contamination=c, random_state=0).fit(X).predict(X) == -1
    print("contamination", c, "flagged", f.sum(), "precision", round(y[f].mean(), 2), "recall", round(f[y == 1].mean(), 2))
```
Output: `ROC-AUC 0.999  PR-AUC 0.944`; `precision@50 1.0, @100 0.86, @500 0.2`; contamination rows as in the example.

**Follow-ups:**
- *Zero labels at launch?* Shadow mode: score, send a sample to analysts, compute precision@k from their verdicts, then go live.
- *How to compare two detectors?* Same review budget, compare precision@k on a fresh labelled sample, plus overlap of the alerts.
- *Is PR-AUC always better?* It depends on the base rate, so only compare it across datasets with the same anomaly share.

**Common mistakes:** Reporting accuracy or only ROC-AUC. Treating contamination as a tuning knob for quality. Tuning on the same few labels used for reporting. Ignoring that analysts' time sets the real k.

### Q29 ⭐⭐ 🟡 HDBSCAN vs DBSCAN: how does it handle varying density, and what are its main hyperparameters?
**Asked at:** Product cos, Europe scale-ups
**Say this first (1 line):** DBSCAN uses one fixed distance eps for the whole dataset, so it cannot handle clusters of different density; HDBSCAN effectively tries all eps values, builds a hierarchy of clusters and keeps the ones that are most stable, so it handles varying density and needs no eps.
**Then explain:**
- **DBSCAN recap:** a point is "core" if at least min_samples points lie within eps; clusters grow from core points; the rest is noise. One eps for everything.
- **The failure:** a tight cluster needs a small eps, a loose one needs a large eps. Small eps turns the loose cluster into noise or fragments; large eps merges the tight neighbours.
- **HDBSCAN idea:** use mutual reachability distance (which stretches distances in sparse areas), build a minimum spanning tree, condense it into a cluster tree over all density levels, and select clusters by stability (how long they persist as density changes).
- **Main hyperparameters:**
  - `min_cluster_size`: smallest group you accept as a cluster. The main knob.
  - `min_samples`: how conservative the density estimate is; larger means more points become noise. Defaults to min_cluster_size.
  - `cluster_selection_method` ("eom" or "leaf": leaf gives more, smaller clusters) and `cluster_selection_epsilon` (merge clusters closer than this).
  - `metric` (use cosine or reduce dimensions for embeddings).
- **Extras:** soft membership probabilities, outlier scores (GLOSH), and no need for k.
- **Cost:** about O(n log n) with tree indexes in low dimensions, degrades in high dimensions. Still has no `predict` for new points in the plain sklearn model (the hdbscan library has `approximate_predict`).

**Example:** Two tight clusters (std 0.2) two units apart, plus a loose one (std 2.0), 300 points each. DBSCAN eps 0.25: only 2 clusters, 33% noise (the loose one is lost). eps 0.5: 7 clusters (loose one fragments). eps 1.0 and 1.5: the two tight clusters merge (sizes 600 and 267 or 294). HDBSCAN (min_cluster_size=30): 3 clusters of 300 / 300 / 294, 0.7% noise.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import DBSCAN, HDBSCAN
X, y = make_blobs([300, 300, 300], centers=[[0, 0], [2, 0], [1, 9]], cluster_std=[0.2, 0.2, 2.0], random_state=0)
def show(name, lab):
    sizes = sorted([int((lab == c).sum()) for c in set(lab) - {-1}], reverse=True)
    print(name, "| clusters:", len(sizes), sizes[:5], "| noise %:", round(100 * (lab == -1).mean(), 1))
for eps in (0.25, 0.5, 1.0, 1.5): show("DBSCAN eps=%.2f" % eps, DBSCAN(eps=eps, min_samples=10).fit_predict(X))
show("HDBSCAN", HDBSCAN(min_cluster_size=30, copy=True).fit_predict(X))
```
Output: as in the example (`DBSCAN eps=0.25 | clusters: 2 [300, 299] | noise 33.4`, ..., `HDBSCAN | clusters: 3 [300, 300, 294] | noise 0.7`).

**Follow-ups:**
- *Is HDBSCAN fully parameter-free?* No: min_cluster_size and min_samples still shape the result, but they are more intuitive than eps.
- *Many points labelled noise?* Lower min_samples, or assign noise to the nearest cluster if full coverage is required.
- *When still use DBSCAN?* Single density, need speed and simplicity, or a known meaningful distance (e.g. 100 m for geo-clustering).

**Common mistakes:** Believing HDBSCAN needs no tuning. Using it on raw high-dimensional embeddings. Treating label -1 as a cluster when computing metrics. Forgetting it cannot label new points without extra work.

### Q30 ⭐⭐ 🟡 How do you check that clusters are stable and reproducible, and how do you deploy a segmentation and monitor it for drift?
**Asked at:** Product cos, Amazon, Booking, GCCs
**Say this first (1 line):** I test stability by re-clustering on bootstrap samples and different seeds and comparing the labels with ARI; for deployment I freeze the scaler and the model, score users in batch, keep segment names stable, and monitor segment shares (PSI), feature drift and business metrics, retraining on a schedule or when drift triggers.
**Then explain:**
- **Stability checks:**
  - Seeds: same data, different `random_state` / `n_init`, compare labels with ARI.
  - Bootstrap/subsample: cluster resamples, predict on the full data, compare with the reference (high mean ARI means the structure is real).
  - Time: cluster two different months, compare. Also check sensitivity to feature set, scaling and outlier handling.
  - Low stability usually means k is too large or there is no real cluster structure.
- **Reproducibility:** fixed seeds, versioned data snapshot, pinned library versions, saved scaler + model (pipeline object), documented feature definitions.
- **Deployment:** batch score daily/weekly into a table (user_id, segment, version, date). Use `predict` of the frozen pipeline; do not re-fit every run, or labels will flip.
- **Keeping labels stable on retrain:** match new centroids to old ones (Hungarian assignment on centroid distance) so "Loyal high-spenders" stays segment 2.
- **Monitor:** share of users per segment (PSI), input feature distributions, average distance to centroid (rising means poor fit), segment-level business KPIs, and the fraction of users near a boundary.
- **Retrain triggers:** PSI above 0.2 (a common rule of thumb), new product/market, or a scheduled quarter; always compare the new run against the old before switching.

**Example:** Three real blobs. Mean bootstrap ARI: k=2: 0.98, k=3: 0.97, k=6: 0.73, k=10: 0.65, so k above 3 splits real clusters arbitrarily. Drift: segment shares were 0.33 / 0.34 / 0.33; next month 0.13 / 0.43 / 0.44, PSI = 0.24 (above 0.2: investigate or retrain).

**Code:**
```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
X, _ = make_blobs(1500, centers=3, cluster_std=1.0, random_state=0)
rng = np.random.default_rng(0)
def stability(k, B=20):
    ref = KMeans(k, n_init=10, random_state=0).fit(X)
    s = []
    for b in range(B):
        idx = rng.choice(len(X), len(X), replace=True)           # bootstrap sample
        m = KMeans(k, n_init=3, random_state=b).fit(X[idx])
        s.append(adjusted_rand_score(ref.predict(X), m.predict(X)))
    return round(np.mean(s), 3)
for k in (2, 3, 6, 10): print("k", k, "mean bootstrap ARI", stability(k))
def psi(base, new): return float(((new - base) * np.log(new / base)).sum())   # share vectors
print("PSI example:", round(psi(np.array([.33, .34, .33]), np.array([.13, .43, .44])), 3))
```
Output: `k 2 0.98`, `k 3 0.972`, `k 6 0.728`, `k 10 0.647`, `PSI example: 0.239`.

**Follow-ups:**
- *k=2 is as stable as k=3, so which one?* Stability is necessary, not sufficient: choose by business usefulness and silhouette too (Q2).
- *Segments must not flip every month?* Freeze the model, or align new centroids to old ones.
- *How do you know the segments are useful?* Different behaviour on KPIs (LTV, churn, response to offers), and an A/B test of segment-specific treatment.

**Common mistakes:** Re-fitting k-means every run so labels change meaning. Judging stability with one seed. Monitoring only accuracy-style metrics (there are none here) instead of segment shares and feature drift. Naming segments once and never checking they still match behaviour.

### Q31 ⭐⭐ 🟡 External clustering metrics when ground truth exists: ARI, NMI, purity, V-measure. When are they appropriate?
**Asked at:** Product cos, GCCs
**Say this first (1 line):** These compare cluster labels with known classes and ignore label names; ARI is the safest default because it is corrected for chance, NMI and V-measure measure shared information, and purity is simple but breaks if you use many clusters, so I report ARI plus one more and never use purity alone.
**Then explain:**
- **ARI (Adjusted Rand Index):** share of point pairs treated the same way in both partitions, adjusted so random labelling gives about 0. Range about -0.5 to 1; 1 is perfect.
- **NMI:** mutual information between clusters and classes, normalised to 0-1. Not chance-corrected, so it favours many clusters.
- **V-measure:** harmonic mean of homogeneity (each cluster has one class) and completeness (each class is in one cluster). Equals NMI with arithmetic averaging.
- **Purity:** share of points in the majority class of their cluster. Trivially 1 when every point is its own cluster.
- **When appropriate:** benchmarking algorithms on labelled data, validating an embedding, or comparing two clusterings (stability). In real segmentation there are usually no true labels, so these are for sanity checks and research, not the final KPI.
- **Caveat:** "ground truth" classes may not match natural structure (clusters may be valid but different from the labels). With HDBSCAN noise, decide how to handle -1 (drop, or treat as its own group, and say which).

**Example:** 1,000 points, 4 true classes. Perfect clustering with relabelled ids: ARI 1.0, NMI 1.0, V 1.0, purity 1.0. Random 4 clusters: ARI -0.001, NMI 0.002, purity 0.28. One big cluster: ARI 0, NMI 0, purity 0.27. Every point alone: ARI 0.0, but NMI 0.33 and purity 1.0, so purity and NMI reward over-splitting.

**Code:**
```python
import numpy as np
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, v_measure_score
from sklearn.metrics.cluster import contingency_matrix
def purity(y, c): m = contingency_matrix(y, c); return m.max(0).sum() / m.sum()
rng = np.random.default_rng(0); y = rng.integers(0, 4, 1000)
cases = {"perfect, relabelled": (y + 1) % 4, "random 4 clusters": rng.integers(0, 4, 1000),
         "1 cluster": np.zeros(1000, int), "every point alone": np.arange(1000)}
for n, c in cases.items():
    print(f"{n:20s} ARI {adjusted_rand_score(y, c):.3f} NMI {normalized_mutual_info_score(y, c):.3f} "
          f"V {v_measure_score(y, c):.3f} purity {purity(y, c):.3f}")
```
Output: rows exactly as listed in the example (`every point alone ARI 0.000 NMI 0.334 V 0.334 purity 1.000`).

**Follow-ups:**
- *Why not accuracy?* Cluster ids are arbitrary; you would need the best label matching (Hungarian), and the cluster count may differ from the class count.
- *Difference between homogeneity and completeness?* Homogeneity penalises mixed clusters; completeness penalises split classes.
- *Fowlkes-Mallows?* Another pair-counting score (geometric mean of pairwise precision and recall), not chance-corrected.

**Common mistakes:** Using purity alone. Comparing NMI across different numbers of clusters. Treating low ARI as "bad clusters" when the labels are not the natural grouping. Forgetting to say how noise points were handled.

### Q32 ⭐⭐ 🟡 Anomaly detection on business metrics (daily orders, payment success rate): how do you handle seasonality and trend, and avoid alert fatigue?
**Asked at:** Swiggy, PhonePe, Booking, Klarna
**Say this first (1 line):** Compare each point with what is normal for that moment (same weekday and hour, current level), alert on the deviation from that expected value with a robust scale, and cut noise with persistence rules, severity tiers and impact thresholds.
**Then explain:**
- **Remove the predictable part first:** trend, weekly/daily seasonality, holidays and promotions (as known events). Options: same-weekday baseline (median of the last 4 weeks), STL decomposition, Prophet/ETS/SARIMA, or a gradient-boosted forecaster with calendar features.
- **Score the residual:** deviation divided by a robust spread (MAD) or use forecast prediction intervals. Rates (payment success) need care: use binomial intervals, because a 100-transaction hour is noisier than a 100,000-transaction hour.
- **Alert fatigue controls:**
  - Persistence: fire only if it breaks for N of the last M intervals.
  - Impact floor: ignore deviations that are statistically odd but small in rupees/users.
  - Severity tiers: page for big, ticket for medium, dashboard only for small.
  - Dedupe and group related alerts (one incident, not 40 city-level alerts); suppress during planned events.
  - Track alert precision (useful alerts / total) weekly and tune thresholds from analyst feedback.
- **Hierarchy:** monitor the total plus key slices (city, payment method, bank); slice alerts catch problems the total hides (one bank down) but multiply false alarms, so control the number of tests.
- **Training baseline:** exclude past incidents from the fit, or the model learns outages as normal.

**Example:** 140 days of orders: trend plus a strong weekend peak, noise sd 25, two real drops of 300 on days 90 and 125. A global z-score (|z|>3) flags nothing (the weekend peaks and trend inflate the std). A same-weekday baseline (median of the previous 4 same weekdays, relative deviation, MAD scale, threshold 4) flags exactly days 90 and 125.

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
n = 140; t = np.arange(n)
y = 1000 + 4 * t + np.tile([0, 0, 0, 0, 100, 350, 300], n // 7) + rng.normal(0, 25, n)   # trend + weekend peak
bad = [90, 125]; y[bad] -= 300                                                          # 2 real drops
s = pd.Series(y)
naive = ((s - s.mean()) / s.std()).abs() > 3
ref = pd.concat([s.shift(7 * k) for k in (1, 2, 3, 4)], axis=1).median(axis=1)   # same-weekday baseline
dev = (s - ref) / ref
sc = 1.4826 * (dev - dev.median()).abs().median()                                 # robust scale (MAD)
flag = ((dev - dev.median()).abs() / sc > 4).fillna(False)
print("naive z flags:", int(naive.sum()), "| weekday baseline flags:", np.where(flag)[0].tolist())
```
Output: `naive z flags: 0 | weekday baseline flags: [90, 125]`.

**Follow-ups:**
- *Holiday or sale causes a spike?* Give the model a calendar/promo feature, or tag the event and suppress; do not train on it as normal.
- *Slow degradation (success rate drifts down 0.1% a day)?* Add a CUSUM or EWMA detector for small persistent shifts.
- *Too many alerts?* Measure alert precision and time-to-detect, then trade the two off with thresholds; add an impact floor.

**Common mistakes:** Global z-score on seasonal data. Training the baseline on data that includes outages. Alerting on every slice with no multiple-testing control. No persistence or impact rule, so people mute the channel. Ignoring volume when alerting on rates.

### Q33 ⭐⭐ 🟡 SVD vs PCA: how are they related, and when do you use Truncated SVD (sparse matrices, LSA)?
**Asked at:** Product cos, recsys/NLP teams
**Say this first (1 line):** PCA is just the SVD of the mean-centred data matrix; Truncated SVD is the same factorisation without centring, which keeps a sparse matrix sparse, so use it for TF-IDF, count or user-item matrices (LSA, recommenders).
**Then explain:**
- **SVD:** any matrix X = U Σ Vᵀ. Columns of V are right singular vectors; singular values in Σ give strength.
- **Link to PCA:** if X is centred, XᵀX/(n−1) is the covariance matrix, so V holds the principal directions and the PC variances are σ²/(n−1). PCA scores are UΣ.
- **Why Truncated SVD:** centring subtracts the column mean from every entry, which turns a sparse matrix dense (memory blow-up, e.g. 1M × 100k). Skipping the centring lets you use sparse algorithms (randomized SVD, ARPACK) and only compute the top k.
- **Cost of not centring:** the first component often just points to the mean direction, and "explained variance" is not the same as in PCA. For TF-IDF that is acceptable (LSA); drop or ignore the first component if it mostly encodes the average.
- **LSA (latent semantic analysis):** TF-IDF matrix, then Truncated SVD to 100-300 dims, giving dense document vectors where similar-topic documents are close (cosine). Also used for collaborative filtering (a simple matrix-factorisation baseline) and as PCA before clustering sparse data.
- **Rule:** dense, small, or you need true variance explained: PCA. Sparse, big: TruncatedSVD.

**Example:** 1,500 toy documents over 300 words in 3 topics (sparse: 47,149 stored values vs 450,000 dense). PCA variance ratios: 0.076, 0.074, 0.006, 0.006 (two components for the 3 topic contrasts, since centred topics sum to a 2-D space). TruncatedSVD: 0.003, 0.075, 0.074, 0.006 (its first component is the uncentred "average document" direction). On centred data, PCA variances equal S²/(n−1) and components equal the rows of Vᵀ up to sign (both True).

**Code:**
```python
import numpy as np, scipy.sparse as sp
from sklearn.decomposition import PCA, TruncatedSVD
rng = np.random.default_rng(0)
rows = []
for d in range(1500):                      # 3 topics, each uses its own block of 100 words
    t = d % 3; v = np.zeros(300); v[t * 100:(t + 1) * 100] = rng.poisson(0.3, 100); v += rng.poisson(0.02, 300); rows.append(v)
X = sp.csr_matrix(np.array(rows))
svd = TruncatedSVD(4, random_state=0).fit(X)
Xd = X.toarray(); pca = PCA(4, svd_solver="full").fit(Xd)
print("TruncatedSVD ratio:", svd.explained_variance_ratio_.round(3))
print("PCA ratio:         ", pca.explained_variance_ratio_.round(3))
U, S, Vt = np.linalg.svd(Xd - Xd.mean(0), full_matrices=False)
print("PCA var == S^2/(n-1):", np.allclose(pca.explained_variance_, S[:4] ** 2 / (len(Xd) - 1)))
print("components == Vt up to sign:", np.allclose(np.abs(pca.components_), np.abs(Vt[:4]), atol=1e-6))
```
Output: `TruncatedSVD ratio: [0.003 0.075 0.074 0.006]`, `PCA ratio: [0.076 0.074 0.006 0.006]`, then `True`, `True`.

**Follow-ups:**
- *Does sklearn PCA accept sparse input?* Not in the standard solver (it must centre); use TruncatedSVD, or implicit centring tricks.
- *LSA vs embeddings?* LSA is linear, cheap and interpretable; neural embeddings capture richer semantics and word order.
- *How is it computed at scale?* Randomized SVD: project onto a random low-rank subspace, then SVD the small matrix.

**Common mistakes:** Calling PCA on a huge sparse matrix after `.toarray()`. Believing the two give identical components without centring. Reading the explained variance of TruncatedSVD as true variance. Not normalising TF-IDF rows before LSA similarity.

### Q34 ⭐⭐ 🔴 Derive PCA: show that principal components are eigenvectors of the covariance matrix, and relate it to SVD.
**Asked at:** Microsoft IDC, Amazon, research-leaning MLE
**Say this first (1 line):** The first principal component is the unit vector w that maximises the variance of the projected data, wᵀΣw; a Lagrange multiplier turns this into Σw = λw, so w is an eigenvector of the covariance matrix Σ, and the best choice is the one with the largest eigenvalue; the SVD of the centred data gives the same directions directly.
**Then explain (derivation):**
1. Centre the data so each column has mean 0. Covariance: Σ = XᵀX/(n−1) (X is n × p, centred).
2. Projecting onto unit vector w gives scores Xw, with variance wᵀΣw (variance of a linear combination).
3. Maximise wᵀΣw subject to wᵀw = 1. Lagrangian: L = wᵀΣw − λ(wᵀw − 1).
4. Set the gradient to zero: ∂L/∂w = 2Σw − 2λw = 0, so **Σw = λw**. Then the variance is wᵀΣw = λwᵀw = λ. To maximise, take the largest eigenvalue.
5. Next components: maximise again with the extra constraint of orthogonality to earlier ones. Because Σ is symmetric, its eigenvectors are orthogonal, so the k-th component is the eigenvector with the k-th largest eigenvalue. Variance explained by component j is λ_j / Σλ.
6. **Equivalent view (min reconstruction error):** by Pythagoras, total variance = variance kept + squared error lost, so maximising kept variance is the same as minimising ‖X − X W Wᵀ‖². The minimum error with k components is the sum of the dropped eigenvalues (times n−1).
7. **SVD link:** write centred X = UΣ_sVᵀ. Then XᵀX = V Σ_s² Vᵀ, so V holds the eigenvectors and λ_j = s_j²/(n−1). Scores are XV = UΣ_s. SVD is numerically better because it avoids forming XᵀX (which squares the condition number).
- **Assumptions to mention:** only second-order (linear, covariance) structure; centring is needed; scaling decides what "variance" means; ties in eigenvalues make directions non-unique; component signs are arbitrary.

**Example:** For Σ = [[2, 0], [0, 1]], eigenvalues are 2 and 1, eigenvectors the axes; PC1 is the x-axis and explains 2/3 of the variance. For a 500 × 6 correlated dataset, the eigenvalues of the covariance, the squared singular values divided by n−1, and sklearn's `explained_variance_` all agree (checked in Q35), and the squared error left after keeping 3 components equals (n−1) times the sum of the 3 dropped eigenvalues (True).

**Follow-ups:**
- *Why eigenvectors of the covariance and not correlation?* Both are valid; correlation equals PCA on standardised features, which you want when units differ.
- *Why do the components stay orthogonal?* Σ is symmetric, so eigenvectors of distinct eigenvalues are orthogonal.
- *What if p > n?* Rank of Σ is at most n−1, so there are at most n−1 non-zero components; use SVD of X (n × p) directly.

**Common mistakes:** Forgetting to centre the data. Saying "eigenvectors of the data matrix". Confusing the loadings (eigenvectors) with the scores (projections). Ignoring the unit-norm constraint, without which the variance could be made arbitrarily large.

### Q35 ⭐⭐ 🔴 Implement PCA from scratch in NumPy and verify it against sklearn.
**Asked at:** Microsoft IDC, Amazon, GCC coding rounds
**Say this first (1 line):** Centre the data, take the SVD, keep the top k right singular vectors as components, project with (X − mean) @ components.T, and check variances and components against sklearn (up to sign, because singular vectors are only defined up to ±1).
**Then explain:**
- **Steps:** (1) mean-centre, (2) `np.linalg.svd(Xc, full_matrices=False)`, (3) components = first k rows of Vt, (4) explained variance = s²/(n−1), (5) transform = Xc @ components.T, (6) inverse = Z @ components + mean.
- **Why SVD, not eigh(cov):** SVD is more stable and works when p > n without building a p × p matrix; eigh on the covariance is fine for small p (shown as a check).
- **Sign ambiguity:** compare absolute values or fix a sign convention; do not assert exact equality of signs with sklearn.
- **Fit on training data only:** store the training mean and reuse it in `transform`.
- Complexity: SVD is O(n p min(n, p)); for large data use randomized SVD or a few top components only.

**Example:** 500 × 6 correlated data, k=3. My variances, variance ratios, components and scores all match sklearn (components and scores up to sign). The eigenvalues of `np.cov` also match, and the reconstruction error equals (n−1) × the sum of the dropped eigenvalues.

**Code:**
```python
import numpy as np
from sklearn.decomposition import PCA
class MyPCA:
    def __init__(self, k): self.k = k
    def fit(self, X):
        self.mean_ = X.mean(0)
        U, S, Vt = np.linalg.svd(X - self.mean_, full_matrices=False)
        self.components_ = Vt[:self.k]                                   # rows = principal directions
        self.explained_variance_ = S[:self.k] ** 2 / (len(X) - 1)
        self.explained_variance_ratio_ = self.explained_variance_ / (S ** 2 / (len(X) - 1)).sum()
        return self
    def transform(self, X): return (X - self.mean_) @ self.components_.T
    def inverse_transform(self, Z): return Z @ self.components_ + self.mean_
rng = np.random.default_rng(0)
X = rng.normal(size=(500, 6)) @ rng.normal(size=(6, 6)) + 3
mine = MyPCA(3).fit(X); ref = PCA(3, svd_solver="full").fit(X)
print("variances:", np.allclose(mine.explained_variance_, ref.explained_variance_))
print("ratios:", np.allclose(mine.explained_variance_ratio_, ref.explained_variance_ratio_))
print("components (up to sign):", np.allclose(np.abs(mine.components_), np.abs(ref.components_)))
print("scores (up to sign):", np.allclose(np.abs(mine.transform(X)), np.abs(ref.transform(X))))
evals = np.linalg.eigh(np.cov(X, rowvar=False))[0][::-1]
print("eigh(cov) route:", np.allclose(evals[:3], ref.explained_variance_))
err = ((X - mine.inverse_transform(mine.transform(X))) ** 2).sum()
print("recon error == (n-1)*dropped eigenvalues:", np.allclose(err, (len(X) - 1) * evals[3:].sum()))
```
Output: all six lines print `True`.

**Follow-ups:**
- *Why does sklearn flip signs sometimes?* Its `svd_flip` makes the largest loading positive in a deterministic way; signs carry no meaning.
- *How to speed up?* `svd_solver="randomized"` for top k of a large matrix, or incremental PCA for data that does not fit in memory.
- *Does it handle new data?* Yes, `transform` uses the stored training mean and components.

**Common mistakes:** Forgetting to centre. Using n instead of n−1 for variance (sklearn uses n−1). Using Vt columns instead of rows as components. Comparing signs with sklearn. Fitting PCA on train + test together.

### Q36 ⭐ 🟡 One-Class SVM vs Isolation Forest vs LOF: how do they compare in assumptions, scale and tuning?
**Asked at:** Fintech, Europe fraud/risk
**Say this first (1 line):** Isolation Forest is my default (fast, scales, little tuning, no scaling needed); LOF is best for local-density anomalies on small or medium data; One-Class SVM learns a boundary around normal data with a kernel, but it is slow, scale-sensitive and fiddly to tune.
**Then explain:**

| | Isolation Forest | One-Class SVM | LOF |
|---|---|---|---|
| Idea | Random splits isolate outliers fast | Kernel boundary separating data from origin (or sphere) | Local density vs neighbours' density |
| Assumption | Anomalies are few and different, so easy to isolate | Normal data fits a smooth region in kernel space | Anomalies sit in lower-density areas than their neighbours |
| Training cost | ~O(n·trees·subsample), near linear | ~O(n²) to O(n³) | O(n²) naive, better with trees in low dim |
| Scaling of features | Not needed | Essential | Essential (distance based) |
| Key knobs | n_estimators, max_samples, contamination | kernel, gamma, nu | n_neighbors, contamination |
| New data | `predict` yes | yes | only with `novelty=True` |
| Weakness | Axis-parallel splits; weak on high-dim noise, local anomalies | Sensitive to gamma and nu, hard to validate | Slow on large n, k matters, curse of dimensionality |

- **Pick Isolation Forest** for large tabular data (fraud features), mixed scales, quick baselines.
- **Pick LOF** when clusters have different densities and "unusual relative to neighbours" is the definition.
- **Pick OCSVM** for small, clean, mostly-normal training data where a smooth boundary is expected (novelty detection), and when you can tune gamma/nu with some labelled checks. nu is roughly an upper bound on the share of training points treated as outliers.
- All need a threshold chosen from review capacity (Q28) and none gives probabilities.

**Example:** Two normal blobs of different density plus 2% uniform anomalies. AUC at n=2,000: IF 0.896, OCSVM 0.810, LOF 0.841; at n=8,000: IF 0.929, OCSVM 0.842, LOF 0.867. In the final run, OCSVM fit+score time grew from 0.15 s to 0.97 s for 4x the data (superlinear); timings are noisy on one laptop (an earlier run gave 0.06 s and 0.46 s), so only the trend matters.

**Code:**
```python
import numpy as np, time
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(0)
def data(n):
    Xn = np.r_[rng.normal([0, 0], 0.5, (n // 2, 2)), rng.normal([6, 6], 1.5, (n // 2, 2))]   # 2 densities
    Xa = rng.uniform(-3, 9, (n // 50, 2))
    return StandardScaler().fit_transform(np.r_[Xn, Xa]), np.r_[np.zeros(len(Xn)), np.ones(len(Xa))]
for n in (2000, 8000):
    X, y = data(n); out = []
    models = {"IF": lambda: -IsolationForest(random_state=0).fit(X).score_samples(X),
              "OCSVM": lambda: -OneClassSVM(nu=0.02, gamma="scale").fit(X).score_samples(X),
              "LOF": lambda: -LocalOutlierFactor(n_neighbors=30).fit(X).negative_outlier_factor_}
    for name, fn in models.items():
        t = time.time(); s = fn(); out.append(f"{name} AUC {roc_auc_score(y, s):.3f} ({time.time() - t:.2f}s)")
    print(n, " | ".join(out))
```
Output: `2000 IF AUC 0.896 | OCSVM AUC 0.810 | LOF AUC 0.841` and `8000 IF AUC 0.929 | OCSVM AUC 0.842 | LOF AUC 0.867` (with times in brackets, machine dependent).

**Follow-ups:**
- *LOF for production scoring?* Fit with `novelty=True` so you can score new points; otherwise it only labels the training set.
- *OCSVM gamma too large?* Overfits: every point looks isolated. Too small: boundary too smooth, misses anomalies.
- *Ensembling?* Rank-average or max of scores from IF and a distance method often beats either alone.

**Common mistakes:** Running OCSVM/LOF without scaling. Treating `contamination`/`nu` as a known truth. Using LOF `fit_predict` results on test data. Using OCSVM on millions of rows.

### Q37 ⭐ 🟡 LLM code review: this LLM-generated clustering/PCA pipeline looks fine but has bugs. Spot them (scaler or PCA fit on all data, leakage, t-SNE used for clustering, wrong k, no random_state).
**Asked at:** AI-era rounds: Microsoft IDC, product cos, Europe scale-ups
**Say this first (1 line):** It runs without errors, so it looks right, but it clusters a t-SNE picture, picks k=8 without evidence, fits the scaler and PCA on all data with no holdout, leaves sources of randomness unfixed in places, and never checks that the clusters are real; I would rebuild it as one pipeline and validate stability on held-out data.
**Buggy snippet (LLM output; excerpt, imports omitted):**
```python
X = StandardScaler().fit_transform(X)                  # fit on ALL data
Z = PCA(0.95).fit_transform(X)                         # fit on ALL data
emb = TSNE(2).fit_transform(Z)                         # no random_state
labels = KMeans(8).fit_predict(emb)                    # k=8 magic number, clustering the 2D t-SNE map
print("Silhouette:", silhouette_score(emb, labels))    # scored in the t-SNE space
```
**Bugs found:**
1. **Clusters on t-SNE output.** t-SNE distorts distances and density and creates apparent clumps; clustering it finds artefacts. Cluster in the PCA/original space; use t-SNE only to plot the result.
2. **Silhouette computed in the same distorted space.** It rewards the very distortion that made the clumps. Score in the space you clustered or, better, the original scaled features.
3. **Scaler and PCA fit on all data.** With a train/test split or a later scoring job, this leaks test statistics. Fit on train only and reuse (`Pipeline`), including for new users.
4. **k=8 with no justification.** No elbow/silhouette/stability sweep, no business reason.
5. **Missing seeds / `n_init`.** `TSNE(2)` and `KMeans(8)` without `random_state` give a different answer every run; `KMeans` also needs `n_init` set explicitly for reproducibility across sklearn versions.
6. **No stability or sanity check.** Nothing tests if the clusters are real.
7. **Unhandled outliers/scale of raw data** (a unit like rupees dominates if the scaler is dropped; skewed columns need log first), and categorical columns are not encoded.
8. **t-SNE has no `transform`**, so the pipeline cannot score new data in production.

**Example (evidence):** Data is pure noise (1,200 rows, 20 features, so no real clusters), plus one column in huge units. The buggy chain gives a silhouette of 0.33 in the t-SNE space (looks like structure!) but 0.00 in the scaled feature space. The fixed pipeline, evaluated on held-out rows, gives a silhouette of 0.023 and a seed-to-seed ARI of 0.08: honest numbers saying "no real clusters". Without scaling, that one column holds 100% of the variance, so any distance-based method would just sort on it.

**Code (fixed; the evidence for the buggy chain is the second block below):**
```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
rng = np.random.default_rng(0)
X = rng.normal(size=(1200, 20)); X[:, 0] *= 1000            # pure noise, one huge-unit column
tr, te = X[:900], X[900:]
pipe = make_pipeline(StandardScaler(), PCA(0.95), KMeans(4, n_init=10, random_state=0)).fit(tr)   # fit on train only
Zt = pipe[:-1].transform(te)                                   # scale + PCA, then score held-out rows
print("held-out silhouette:", round(silhouette_score(Zt, pipe[-1].predict(Zt)), 3))
Ztr = pipe[:-1].transform(tr)
a = KMeans(4, n_init=1, random_state=1).fit_predict(Ztr); b = KMeans(4, n_init=1, random_state=2).fit_predict(Ztr)
print("seed-to-seed ARI:", round(adjusted_rand_score(a, b), 2))
```
Output: `held-out silhouette: 0.023`, `seed-to-seed ARI: 0.08`.

**Code (the buggy chain on the same noise data):**
```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
rng = np.random.default_rng(0)
X = rng.normal(size=(1200, 20)); X[:, 0] *= 1000            # pure noise, one huge-unit column
Xs = StandardScaler().fit_transform(X); Z = PCA(0.95).fit_transform(Xs)
emb = TSNE(2, random_state=0).fit_transform(Z); lab = KMeans(8, n_init=10, random_state=0).fit_predict(emb)
print("silhouette in t-SNE space", round(silhouette_score(emb, lab), 3), "| in scaled feature space", round(silhouette_score(Xs, lab), 3))
print("share of variance in the huge-unit column (unscaled):", round(X.var(0)[0] / X.var(0).sum(), 3))
```
Output: `silhouette in t-SNE space 0.334 | in scaled feature space 0.003`, `share ... 1.0`.

**Follow-ups:**
- *How do you choose k properly?* Sweep k with silhouette and bootstrap stability (Q2, Q30), then check business usefulness.
- *Is fitting PCA on all data a "real" leak in unsupervised work?* Less severe than supervised leakage, but it breaks the train/test discipline, inflates held-out scores, and fails in production where new data arrives later.
- *How would you review LLM code in general?* Run it on noise and on planted structure; if it "finds" clusters in noise, the pipeline is wrong.

**Common mistakes:** Trusting code because it runs and prints a nice silhouette. Believing the t-SNE picture is evidence. Forgetting that production needs `transform` for new data. Reviewing only syntax, not the evaluation logic.

### Q38 ⭐ 🟡 GenAI follow-up: how would you use an LLM to name or interpret clusters, and how do you validate that the labels are correct?
**Asked at:** GenAI-adjacent product teams, Europe scale-ups
**Say this first (1 line):** I give the LLM evidence per cluster (top terms or feature profile plus a few representative and a few random examples, and the neighbouring clusters), ask for a short name and a one-line definition, and then validate the names with held-out examples, a human spot check and a "can the label be used to re-assign items" test, because an LLM will write a confident name for any cluster, even a mixed one.
**Then explain:**
- **Inputs for the prompt:** top c-TF-IDF terms (text) or standardised feature means vs overall (behavioural segments); 5-10 examples closest to the centroid; 3-5 random members (so it sees the spread, not just the typical items); sizes; names of nearby clusters to force it to be distinct.
- **Output format:** JSON with `name` (3-5 words), `definition`, `include_if`, `exclude_if`, `confidence`, and `mixed_themes: true/false`. Temperature 0.
- **Validation:**
  - **Label-to-item test:** give a different LLM call only the names and definitions plus held-out items, ask it to assign each item to a label; compare with the true cluster (accuracy/ARI). Low agreement means vague or overlapping labels.
  - **Human review:** domain experts rate 20-30 items per cluster; check inter-rater agreement.
  - **Coherence:** if the LLM flags multiple themes, or the held-out test confuses two clusters, the problem is the clustering (split, merge, change k), not the label.
  - **Stability:** re-run with different samples/seeds; names should be semantically the same.
  - **Business check:** do the segment names match behaviour on KPIs?
- **Risks:** hallucinated detail not in the data, flattering or biased labels for user segments, leaking PII into the prompt (mask or aggregate first), non-determinism across versions (store the prompt, model version and the output).
- **LLM names, humans own:** keep a human approval step before the labels go into dashboards.

**Example:** 9 support tickets, 3 clusters. Top terms: cluster 0 [late, cold, delivery, arrived] is clean ("Late/cold delivery"); cluster 2 [refund, cancelled, received, pending] is clean ("Refund delays"); cluster 1 [payment, money, refunded, cancellation] mixes payment failures with refund complaints. An LLM would happily name cluster 1 "Payment issues"; the label-to-item test would then show held-out refund tickets scattered between clusters 1 and 2, exposing the mixing.

**Code:** (builds the evidence for the prompt; the LLM call itself is not executed here)
```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
docs = ["refund not received for cancelled order", "money not refunded after cancellation", "refund status pending since a week",
        "delivery boy was rude and late", "order arrived late and cold", "delivery partner late, food cold",
        "app crashes on payment screen", "payment failed but money deducted", "upi payment page keeps crashing"]
vec = TfidfVectorizer(stop_words="english"); X = vec.fit_transform(docs)
km = KMeans(3, n_init=10, random_state=0).fit(X)
terms = np.array(vec.get_feature_names_out())
for c in range(3):
    idx = np.where(km.labels_ == c)[0]
    top = terms[np.argsort(-np.asarray(X[idx].mean(0)).ravel())[:4]]
    near = idx[np.argsort(((X[idx].toarray() - km.cluster_centers_[c]) ** 2).sum(1))[:2]]   # most central docs
    print(f"cluster {c} (n={len(idx)}) top terms: {list(top)} | examples: {[docs[i] for i in near]}")
# not executed: llm.generate(prompt_with(top_terms, examples)) -> {"name":..., "definition":..., "mixed_themes":...}
```
Output: cluster 0 (n=3) terms `late, cold, delivery, arrived`; cluster 1 (n=4) `payment, money, refunded, cancellation`; cluster 2 (n=2) `refund, cancelled, received, pending`.

**Follow-ups:**
- *Why not just ask the LLM to cluster directly?* It does not scale, is non-deterministic and hard to audit; better to cluster with embeddings, then use the LLM for naming and QA.
- *How do you handle a mixed cluster?* Increase k or sub-cluster, or merge if the human reviewers say the themes are really one.
- *Can the LLM judge itself?* Use a separate call/model and a human sample; self-agreement alone is weak evidence.

**Common mistakes:** Showing only the most typical examples. Accepting fluent names without a test. Sending raw PII to the model. Treating the label as ground truth and training a classifier on it without review.

### Q39 ⭐ 🔴 Show that Lloyd's k-means iterations never increase the objective. Why is it only a local optimum, and what is its link to EM?
**Asked at:** Research-leaning MLE, Amazon applied science
**Say this first (1 line):** Each of the two Lloyd steps minimises the objective J = Σ‖x − μ_c(x)‖² over one set of variables while the other is held fixed, so J can only go down or stay equal; J is bounded below and there are finitely many partitions, so it converges, but only to a local optimum because the problem is non-convex.
**Then explain:**
- **Assignment step:** with centroids fixed, each point picks its nearest centroid. That minimises each point's term, so J cannot increase.
- **Update step:** with assignments fixed, for each cluster the mean minimises Σ‖x − μ‖² (set the gradient 2Σ(μ − x) = 0, so μ = mean; the function is convex in μ). So J cannot increase.
- **Convergence:** J is non-negative and non-increasing; there are at most kⁿ partitions and a partition cannot repeat without J being equal (ties broken consistently), so the algorithm stops in finitely many steps.
- **Why only local:** J is non-convex in (assignments, centroids) jointly (it is coordinate descent on a discrete-continuous problem). Which basin you land in depends on the start; the problem is NP-hard in general. Hence k-means++ and `n_init` (Q17).
- **Link to EM:** k-means is the limit of a Gaussian mixture with equal spherical covariances σ²I and equal weights as σ² → 0. The E-step (responsibilities) becomes a hard assignment, and the M-step (weighted means) becomes the cluster mean. Both are coordinate ascent/descent on a bound of the objective; EM monotonically increases the likelihood, k-means monotonically decreases J.
- **Related:** k-means is "classification EM" (hard EM): it assigns each point fully to one component.

**Example:** 600 points, 5 blobs, own NumPy Lloyd with objective recorded after every step: never increases (checked at each of the 60 recorded steps), 4509.6 down to 3142.8. Across 10 random starts the final objectives were 1956.8, 3139.1, 3142.8, 3142.9, 3162.6, 3181.2: the best is about 38% lower than the worst, so local optima matter.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_blobs
X, _ = make_blobs(600, centers=5, cluster_std=1.3, random_state=3)
def lloyd(X, k, seed, iters=30):
    r = np.random.default_rng(seed); C = X[r.choice(len(X), k, replace=False)]; J = []
    for _ in range(iters):
        d = ((X[:, None, :] - C[None]) ** 2).sum(2); a = d.argmin(1)
        J.append(d[np.arange(len(X)), a].sum())                      # objective after assignment step
        C = np.array([X[a == j].mean(0) if (a == j).any() else C[j] for j in range(k)])
        J.append(((X - C[a]) ** 2).sum())                            # objective after update step
    return np.array(J)
J = lloyd(X, 5, seed=0)
print("never increases:", bool(np.all(np.diff(J) <= 1e-9)), "| start", round(J[0], 1), "-> end", round(J[-1], 1))
finals = [round(float(lloyd(X, 5, s)[-1]), 1) for s in range(10)]
print("final objective over 10 seeds:", sorted(set(finals)))
```
Output: `never increases: True | start 4509.6 -> end 3142.8`; `final objective over 10 seeds: [1956.8, 3139.1, 3142.8, 3142.9, 3162.6, 3181.2]`.

**Follow-ups:**
- *Is the global optimum findable?* Not in general (NP-hard); in practice use k-means++ with several restarts.
- *Empty cluster?* Keep the old centroid or re-seed it at the farthest point.
- *Why is k-means sensitive to the metric?* The mean is the minimiser only for squared Euclidean distance; for other distances use k-medoids.

**Common mistakes:** Claiming k-means finds the global minimum. Forgetting that the update step uses the mean because of the squared loss. Saying EM and k-means are unrelated. Ignoring ties and empty clusters in the convergence argument.

### Q40 ⭐ 🔴 Spectral clustering: how does it work and when does it beat k-means?
**Asked at:** Research-leaning roles, Microsoft IDC
**Say this first (1 line):** Spectral clustering builds a similarity graph of the points, takes the bottom eigenvectors of the graph Laplacian as a new representation in which connected groups become well separated blobs, and then runs k-means there; it beats k-means when clusters are connected, non-convex shapes (moons, rings), not round blobs.
**Then explain:**
- **Steps:**
  1. Build a graph: kNN graph or Gaussian (RBF) similarity, W_ij.
  2. Laplacian: L = D − W (or the normalised version I − D^(−1/2) W D^(−1/2)), where D is the diagonal degree matrix.
  3. Take the k eigenvectors with the smallest eigenvalues.
  4. Row-normalise (normalised version), then run k-means on these k-dimensional rows.
- **Why it works:** it approximately solves a graph-cut problem (minimise edges cut between groups relative to group size: normalised cut). The number of zero eigenvalues of L equals the number of connected components; near-zero eigenvalues correspond to weakly connected groups.
- **Beats k-means** when clusters are defined by connectivity, not distance to a centre: moons, concentric rings, intertwined shapes, image segmentation, community detection in graphs.
- **Costs:** eigendecomposition is O(n³) dense (sparse/Lanczos or Nyström approximations help), so it is hard beyond ~tens of thousands of points; you still need k; results depend on the graph (n_neighbors or gamma) and noise bridges can merge clusters.
- **Eigengap:** a big jump in the sorted eigenvalues suggests how many clusters there are.

**Example:** 600 points, noisy two moons: k-means ARI 0.255, spectral 1.0. Two concentric circles: k-means ARI -0.001, spectral 1.0. In my from-scratch version (symmetric kNN graph with 10 neighbours, normalised Laplacian), the four smallest eigenvalues were about 0, 0, 0.0011, 0.0011: the two zeros show the graph splits into two connected components, and k-means on the first two eigenvectors gives ARI 1.0.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_moons
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.neighbors import kneighbors_graph
from scipy.sparse.csgraph import laplacian
from sklearn.metrics import adjusted_rand_score
X, y = make_moons(600, noise=0.06, random_state=0)
km = KMeans(2, n_init=10, random_state=0).fit_predict(X)
sp = SpectralClustering(2, affinity="nearest_neighbors", n_neighbors=10, random_state=0).fit_predict(X)
print("k-means ARI", round(adjusted_rand_score(y, km), 3), "| spectral ARI", round(adjusted_rand_score(y, sp), 3))
W = kneighbors_graph(X, 10).toarray(); W = np.maximum(W, W.T)       # symmetric kNN graph
vals, vecs = np.linalg.eigh(laplacian(W, normed=True))             # ascending eigenvalues
print("smallest eigenvalues:", vals[:4].round(4))
emb = vecs[:, :2] / np.linalg.norm(vecs[:, :2], axis=1, keepdims=True)
print("scratch spectral ARI:", round(adjusted_rand_score(y, KMeans(2, n_init=10, random_state=0).fit_predict(emb)), 3))
```
Output: `k-means ARI 0.255 | spectral ARI 1.0`; eigenvalues about `[0, 0, 0.0011, 0.0011]`; `scratch spectral ARI: 1.0`.

**Follow-ups:**
- *Why use the smallest eigenvectors?* They are smooth over connected regions (nearly constant per component), so they encode cluster membership.
- *Scaling to large data?* Nyström or landmark approximations, or cluster a sample and propagate; otherwise use DBSCAN/HDBSCAN for shape-based clustering at scale.
- *Link to k-means?* Kernel k-means and spectral clustering are closely related (both can be written as trace maximisation).

**Common mistakes:** Using it on blob-like data (no gain, slower). Using a dense RBF with a bad gamma. Applying it to millions of rows. Forgetting that k must be supplied and the graph parameters matter.

### Q41 ⭐ 🔴 Kernel PCA, probabilistic PCA, ICA and NMF: how do they differ from PCA and when would you use them?
**Asked at:** Research-leaning roles, Europe
**Say this first (1 line):** PCA finds orthogonal directions of maximum variance (linear, second-order); Kernel PCA does it in an implicit feature space for non-linear structure, probabilistic PCA adds a noise model, ICA finds statistically independent sources, and NMF finds non-negative parts that add up to the data.

| Method | What it optimises | Use when |
|---|---|---|
| PCA | Orthogonal directions of max variance | Compression, denoising, decorrelation |
| Kernel PCA | PCA on the kernel (Gram) matrix, e.g. RBF | Curved/non-linear manifolds; needs kernel and gamma choice; O(n²) memory, O(n³) time; no direct inverse |
| Probabilistic PCA (PPCA) | Latent-variable model x = Wz + μ + ε, ε ~ N(0, σ²I), fit by ML/EM | Missing data, a likelihood for model comparison, a generative model; its ML solution spans the same subspace as PCA; factor analysis generalises it with per-feature noise |
| ICA | Maximally independent (non-Gaussian) components | Blind source separation (EEG, audio mixtures); sources must be non-Gaussian; components are unordered and unscaled |
| NMF | Non-negative W, H with X ≈ WH | Non-negative data (counts, TF-IDF, pixels): topics, parts-based features, recsys; interpretable because components only add |

- **Key contrast with PCA:** PCA components are uncorrelated and can have negative loadings, so they are hard to read as "parts"; NMF forbids negatives; ICA wants independence (stronger than uncorrelated).
- **Practical:** none of these is a default; start with PCA, switch only with a specific reason (non-linear shape, source separation, interpretability of parts).
- **Caveat:** NMF and ICA are non-convex, so seeds and initialisation (`nndsvda`) matter; NMF needs a chosen rank k.

**Example:** Two noisy concentric circles: a logistic regression on the first PCA component scores 0.487 CV accuracy (chance); on the first RBF Kernel PCA component, 1.0. For two mixed signals (a sine and a square wave), PCA's best correlation with the true sources is 0.83 and 0.87, while FastICA recovers them at 0.998 and 1.0. On digits, NMF components have minimum value 0.0 (all non-negative), while PCA components go down to −0.33.

**Code:**
```python
import numpy as np
from sklearn.datasets import make_circles, load_digits
from sklearn.decomposition import PCA, KernelPCA, FastICA, NMF
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
X, y = make_circles(600, factor=0.3, noise=0.05, random_state=0)
for nm, Z in (("PCA", PCA(2).fit_transform(X)), ("KernelPCA rbf", KernelPCA(2, kernel="rbf", gamma=5).fit_transform(X))):
    print(nm, "CV acc on first component:", round(cross_val_score(LogisticRegression(), Z[:, :1], y, cv=5).mean(), 3))
t = np.linspace(0, 8, 2000); S = np.c_[np.sin(2 * t), np.sign(np.sin(3 * t))]
M = S @ np.array([[1, 0.5], [0.4, 1]]).T                    # mixed signals
for nm, R in (("PCA", PCA(2).fit_transform(M)), ("ICA", FastICA(2, random_state=0).fit_transform(M))):
    print(nm, "best |corr| with true sources:", np.abs(np.corrcoef(S.T, R.T)[:2, 2:]).max(1).round(3))
D = load_digits().data
print("NMF min component value:", NMF(10, init="nndsvda", random_state=0, max_iter=500).fit(D).components_.min().round(3))
```
Output: `PCA ... 0.487`, `KernelPCA rbf ... 1.0`; `PCA [0.826 0.872]`, `ICA [0.998 1. ]`; `NMF min component value: 0.0`.

**Follow-ups:**
- *Is PPCA different from PCA in practice?* Same subspace at the ML solution, but it gives a likelihood, handles missing values via EM and supports Bayesian choice of k.
- *Why does ICA need non-Gaussian sources?* A mix of independent Gaussians is rotation-symmetric, so independence cannot identify the rotation.
- *Kernel PCA at scale?* Nyström approximation or random Fourier features.

**Common mistakes:** Applying ICA to Gaussian-like data. Using NMF on data with negative values. Forgetting the kernel parameters in Kernel PCA. Reaching for the exotic method when plain PCA with scaling would do.

### Q42 ⭐ 🔴 Model selection for GMM: BIC/AIC, covariance types, and degenerate (singular) components.
**Asked at:** Research-leaning roles, Amazon applied science
**Say this first (1 line):** Fit GMMs over a grid of k and covariance types with several restarts, pick the one with the lowest BIC (it penalises parameters more than AIC and picks simpler models), and guard against singular components with covariance regularisation (`reg_covar`), a minimum cluster size, and checks on tiny-weight components.
**Then explain:**
- **BIC = p·ln(n) − 2·ln L̂, AIC = 2p − 2·ln L̂** (p parameters, L̂ max likelihood). Lower is better. BIC is consistent (tends to pick the true k as n grows) and usually preferred for clustering; AIC favours predictive fit and tends to pick more components.
- **Covariance types** (parameters per component, d features): spherical (1), diag (d), tied (one shared full matrix), full (d(d+1)/2). More flexible means better fit but more parameters, so the grid over (type, k) is the model-selection problem.
- **Degenerate components:** the likelihood is unbounded: a component can collapse onto one point (or a few identical/collinear points) with variance → 0 and density → ∞. Symptoms: huge log-likelihood, a component with tiny weight and near-zero covariance determinant, or fitting errors. Also happens when n < d or features are duplicated.
- **Defences:** add `reg_covar` to the diagonal (sklearn default 1e-6; raise it on scaled data), use diag/tied covariance in high dimensions, reduce dimensions first (PCA), drop duplicates, set a minimum component weight/size and re-fit, use several initialisations (k-means init), or a Bayesian GMM with priors (`BayesianGaussianMixture`).
- **Cross-check:** BIC is not truth, so also check stability, held-out log-likelihood and whether the components make sense.

**Example:** Three elliptical clusters (400 points each). BIC picks full covariance with k=3 (BIC 10,195.9), the same as AIC. Within restricted types: spherical needs k=6 (BIC 10,424.0), diag k=5 (10,349.3), tied k=6 (10,420.0): the simpler shapes compensate for wrong covariance by adding components. Adding 30 identical points far away: with `reg_covar=0` the fit fails (ValueError, "ill-defined empirical covariance"); with the default 1e-6 it fits, but one component has a covariance determinant of 1e-12, a clear sign of collapse.

**Code:**
```python
import numpy as np
from sklearn.mixture import GaussianMixture
rng = np.random.default_rng(0)
X = np.r_[rng.multivariate_normal([0, 0], [[2, 1.5], [1.5, 2]], 400),
          rng.multivariate_normal([6, 0], [[3, -2], [-2, 3]], 400),
          rng.multivariate_normal([3, 6], [[0.5, 0], [0, 2]], 400)]
bic = {(ct, k): GaussianMixture(k, covariance_type=ct, n_init=3, random_state=0).fit(X).bic(X)
       for ct in ("spherical", "diag", "tied", "full") for k in range(1, 7)}
best = min(bic, key=bic.get); print("best by BIC:", best, round(bic[best], 1))
Xd = np.r_[X, np.tile([20.0, 20.0], (30, 1))]                 # 30 identical points
try: GaussianMixture(4, reg_covar=0, random_state=0).fit(Xd)
except ValueError as e: print("reg_covar=0 fails:", str(e)[:60])
g = GaussianMixture(4, random_state=0).fit(Xd)
print("smallest covariance det with default reg_covar:", min(np.linalg.det(c) for c in g.covariances_))
```
Output: `best by BIC: ('full', 3) 10195.9`; the failure message for `reg_covar=0`; smallest determinant about `1e-12`.

**Follow-ups:**
- *BIC vs AIC?* BIC penalises p·ln(n) instead of 2p, so it prefers fewer components on large n; AIC may over-split.
- *Alternative to choosing k?* `BayesianGaussianMixture` with a Dirichlet prior prunes unused components automatically.
- *Why does EM get stuck?* Local optima of the likelihood and singularities; use several restarts and regularisation.

**Common mistakes:** Choosing k by training log-likelihood (always improves with k). Ignoring covariance type. Not scaling or reducing dimensions in high-d. Not noticing a collapsed component with a tiny weight.

### Q43 ⭐ 🔴 How would you explain why a particular point was flagged as an anomaly (SHAP on Isolation Forest, feature-wise reconstruction error)?
**Asked at:** Fintech, regulated GCCs (JPMC), Klarna
**Say this first (1 line):** I attribute the anomaly score to features: TreeSHAP for Isolation Forest, per-feature residuals for PCA/autoencoders, or a simple "set this feature to normal and see how much the score drops" check, and then turn the top two or three features into a plain-language reason with the typical range for comparison.
**Then explain:**
- **SHAP on Isolation Forest:** `shap.TreeExplainer(iso)` works on sklearn's IsolationForest; the values explain the score (decision function): negative values push the point towards "anomaly". Sum of values + baseline = the model output, so it is additive and faithful to the model.
- **Reconstruction-based (PCA/autoencoder):** the squared error per feature, (x_j − x̂_j)², shows which features the model could not reproduce. Standardise features first so units do not dominate. Caveat: in a correlated block, error can spread to features that are fine (smearing).
- **Model-agnostic fallback:** replace one feature by its median (or a typical value) and measure the score drop; or compare the feature with the population percentile. Cheap, easy to explain, ignores interactions.
- **Distance/density methods (LOF, kNN):** show the nearest normal neighbours and the feature differences.
- **Presenting it:** "amount is 6x the usual and distance from home is 400 km against a median of about 3 km" beats a SHAP plot for an analyst or a regulator. Provide reason codes, and keep the logs for audit.
- **Limits:** attribution explains the model, not the cause; correlated features share credit; unscaled or leaky features give misleading reasons; explanations can themselves leak detection logic to an adversary, so expose them to analysts, not to end users.

**Example:** Synthetic transactions (6 features). The flagged one has an amount 6x the mean and a 400 km distance, everything else normal. Score 0.668 vs a typical 0.44. Median-replacement score drop: dist_km 0.111, amount 0.108, others about 0. TreeSHAP: amount −3.22, dist_km −3.34 (strongly towards anomaly), the other four features small and slightly positive (0.05 to 0.22). Both methods give the same two reasons.

**Code:**
```python
import numpy as np, shap
from sklearn.ensemble import IsolationForest
rng = np.random.default_rng(0)
cols = ["amount", "n_txn_1h", "dist_km", "acct_age", "hour", "new_device"]
X = np.c_[rng.lognormal(6, .5, 3000), rng.poisson(2, 3000), rng.exponential(5, 3000),
          rng.uniform(10, 900, 3000), rng.normal(14, 3, 3000), rng.binomial(1, .05, 3000)]
x = np.array([[X[:, 0].mean() * 6, 3, 400.0, 400.0, 14.0, 0]])      # huge amount, far from home
iso = IsolationForest(n_estimators=300, random_state=0).fit(X)
base, med = -iso.score_samples(x)[0], np.median(X, 0); drop = {}
for j, c in enumerate(cols):                                         # model-agnostic: set one feature to its median
    z = x.copy(); z[0, j] = med[j]; drop[c] = round(float(base + iso.score_samples(z)[0]), 3)
print("score drop when feature set to median:", dict(sorted(drop.items(), key=lambda t: -t[1])))
sv = shap.TreeExplainer(iso).shap_values(x)[0]                       # more negative = pushes towards anomaly
print("TreeSHAP:", {c: round(float(v), 2) for c, v in zip(cols, sv)})
```
Output: `{'dist_km': 0.111, 'amount': 0.108, 'n_txn_1h': 0.007, 'acct_age': 0.002, 'hour': 0.0, 'new_device': 0.0}` and `TreeSHAP: {'amount': -3.22, 'n_txn_1h': 0.05, 'dist_km': -3.34, 'acct_age': 0.22, 'hour': 0.22, 'new_device': 0.12}`.

**Follow-ups:**
- *Does SHAP tell you why it is fraud?* No: it tells you why the model scored it high; a human still decides.
- *Cost of SHAP at scale?* TreeSHAP is polynomial in tree size; explain only the flagged cases, not everything.
- *Regulatory needs?* Reason codes, stable explanations, audit logs of model version and features at decision time.

**Common mistakes:** Presenting raw SHAP charts to non-technical reviewers. Explaining on unscaled features for reconstruction error. Treating attribution as causation. Forgetting that correlated features split the credit.

### Q44 ⭐ 🔴 Deep anomaly detection: VAE, Deep SVDD, GAN-based methods. When are they worth it over Isolation Forest?
**Asked at:** Senior MLE, Amazon, Microsoft IDC
**Say this first (1 line):** Deep methods are worth it when the data is unstructured or very high-dimensional (images, audio, logs, sequences) and you have plenty of clean normal data and engineering capacity; on ordinary tabular data Isolation Forest is usually as good, cheaper, and easier to explain, so it is my baseline to beat.
**Then explain:**
- **Autoencoder:** compress and rebuild; large reconstruction error means anomaly (Q19). Risk: it may reconstruct anomalies too well.
- **VAE:** encoder gives a distribution over a latent code; trained on reconstruction + KL to a prior. Score by reconstruction error or ELBO (a likelihood bound). Smoother latent space than a plain AE, but likelihood-based scores can still rate some anomalies as likely (e.g. simple images).
- **Deep SVDD:** train a network to map normal data into a small hypersphere around a centre c, minimising mean ‖φ(x) − c‖²; the distance to c is the score. Needs care to avoid collapse (no bias terms, fixed centre, pretrain with an AE).
- **GAN-based (AnoGAN, f-AnoGAN, GANomaly):** learn the normal distribution; score by how poorly a sample can be generated or reconstructed. Hard to train and unstable, so rarely the production pick.
- **Also:** self-supervised/contrastive methods and pretrained-embedding + kNN or Mahalanobis distance, which often beat training a deep model from scratch for images and text.
- **Worth it when:** images, time series with temporal structure, text, logs (use sequence models), plenty of normal data, and Isolation Forest on good features has clearly hit a ceiling.
- **Not worth it when:** tabular data with a few dozen features, small data, tight latency or explainability needs; deep models need tuning, GPUs, monitoring, and give less reliable thresholds.
- **Evaluate the same way for all:** PR-AUC, precision@k on a labelled holdout (Q28), plus cost and latency.

**Example:** Digits (64 pixels), normal = one digit class (120 training images), anomalies = 100 other digits. Isolation Forest AUC vs a small MLP autoencoder (sklearn, 32-8-32 hidden): normal "1": 0.905 vs 0.934 (Deep SVDD 0.924); normal "0": 1.0 vs 1.0 (Deep SVDD 0.996). A modest gain only on the harder class, on a small image problem: the deep model helps a bit on pixels, but the gain is not automatic and is small relative to the extra complexity.

**Code:** (sklearn MLP autoencoder as a stand-in, plus a small PyTorch Deep SVDD; both executed. A VAE is not shown.)
```python
import numpy as np
from sklearn.datasets import load_digits
from sklearn.ensemble import IsolationForest
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import roc_auc_score
d = load_digits(); X = d.data / 16.0; y = d.target
for normal in (1, 0):
    Xn = X[y == normal]; tr, te_n = Xn[:120], Xn[120:]
    te_a = X[y != normal][:100]; Xt = np.r_[te_n, te_a]; lab = np.r_[np.zeros(len(te_n)), np.ones(len(te_a))]
    iso = -IsolationForest(random_state=0).fit(tr).score_samples(Xt)
    ae = MLPRegressor(hidden_layer_sizes=(32, 8, 32), max_iter=2000, random_state=0).fit(tr, tr)
    err = ((Xt - ae.predict(Xt)) ** 2).sum(1)
    print("normal digit", normal, "| IF AUC", round(roc_auc_score(lab, iso), 3), "| AE AUC", round(roc_auc_score(lab, err), 3))
```
Output: `normal digit 1 | IF AUC 0.905 | AE AUC 0.934`; `normal digit 0 | IF AUC 1.0 | AE AUC 1.0`.

Deep SVDD in PyTorch (CPU, same data split; VAE loss would be `recon_mse + beta * KL`, not run):
```python
import numpy as np, torch, torch.nn as nn
from sklearn.datasets import load_digits
from sklearn.metrics import roc_auc_score
torch.manual_seed(0)
d = load_digits(); X = d.data / 16.0; y = d.target
for normal in (1, 0):
    Xn = X[y == normal]; tr, te_n = Xn[:120], Xn[120:]
    te_a = X[y != normal][:100]; Xt = np.r_[te_n, te_a]; lab = np.r_[np.zeros(len(te_n)), np.ones(len(te_a))]
    net = nn.Sequential(nn.Linear(64, 32, bias=False), nn.ReLU(), nn.Linear(32, 8, bias=False))   # no bias: avoids collapse
    xt = torch.tensor(tr, dtype=torch.float32)
    with torch.no_grad(): c = net(xt).mean(0)                    # fixed centre
    opt = torch.optim.Adam(net.parameters(), 1e-3)
    for _ in range(300):
        loss = ((net(xt) - c) ** 2).sum(1).mean(); opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad(): s = ((net(torch.tensor(Xt, dtype=torch.float32)) - c) ** 2).sum(1).numpy()
    print("normal digit", normal, "| Deep SVDD AUC", round(roc_auc_score(lab, s), 3))
```
Output: `normal digit 1 | Deep SVDD AUC 0.924`; `normal digit 0 | Deep SVDD AUC 0.996`.

**Follow-ups:**
- *Training data contains anomalies?* The deep model learns them too; use robust/denoising training, trimmed loss, or filter with a simple detector first.
- *Why can a VAE give high likelihood to anomalies?* Likelihood is dominated by low-level statistics (e.g. smooth images), not semantics; use reconstruction + latent distance, or pretrained features.
- *Threshold?* Set from a validation set of normal data (percentile) and review capacity, as for any detector.

**Common mistakes:** Going deep without trying Isolation Forest or a PCA baseline. Training on data with hidden anomalies. Trusting reconstruction error across very different input scales. Skipping evaluation on realistic anomalies. Ignoring serving cost and explainability.

### Q45 ⭐ 🔴 Scale: how do you cluster 100M users (mini-batch k-means, FAISS, approximate nearest neighbours, sampling then assign)? Why does DBSCAN scale badly?
**Asked at:** Flipkart, Swiggy, Amazon, Walmart GCC
**Say this first (1 line):** I would not cluster all 100M rows in one go: build compact features, fit on a representative sample (or with mini-batch k-means), then assign everyone to the nearest centroid in batch with Spark or an ANN library like FAISS; DBSCAN scales badly because it needs a neighbourhood query for every point, which is O(n²) in the worst case and degrades in high dimensions.
**Then explain:**
- **Reduce the problem first:** 20-100 numeric features (PCA/embeddings), scale them, and cap outliers. Often cluster at a coarser grain (e.g. users aggregated by behaviour) than raw rows.
- **Sample then assign:** fit k-means on 0.1-1% (stratified, so rare segments are present), then `predict` for all users. Centroids stabilise quickly, since k is small. Check stability against a second sample.
- **Mini-batch k-means:** each step updates centroids from a random mini-batch (e.g. 4,096 rows); cost per epoch is O(n·k·d) and it streams from disk; slightly worse objective.
- **Distributed:** Spark MLlib KMeans (k-means|| initialisation); or compute centroids on a sample and run the assignment as a map job, with no shuffles.
- **FAISS / ANN:** for nearest-centroid search with large k (thousands) or for nearest-neighbour search on embeddings; IVF and PQ indexes trade a little recall for big speedups. Used to assign users to many centroids or to build the kNN graph for graph-based clustering.
- **Why DBSCAN is slow:** it needs the eps-neighbourhood of each point. With a spatial index (kd-tree/ball tree) it is about O(n log n) in low dimensions, but indexes stop helping beyond roughly 10-20 dims, so it falls to O(n²) distance computations and O(n²) memory in the worst case (dense neighbourhoods). It also has a single global eps and cannot be fitted on a sample then used to predict.
- **Cheaper alternatives for density:** HDBSCAN on a sample or on UMAP-reduced data, or k-means with many centroids (micro-clusters) and then merge.
- **Operational:** daily or weekly batch, a frozen model, written assignments to a table, and drift monitoring (Q30).

**Example:** 300,000 points, 20 dims, 20 clusters (a scaled-down test). Full k-means: 5.9 s, objective 23,981,616. Mini-batch (batch 4,096): 0.1 s, 23,985,323 (+0.02%). Fit on a 20,000-point sample then assign all: well under a second, 24,004,136 (+0.1%). DBSCAN on the same data is the slow one: in an earlier run, n = 5,000 / 10,000 / 20,000 took 0.04 / 0.13 / 0.36 s (about 3x per doubling, close to quadratic), but repeat runs on a busy machine gave erratic timings, so treat that as indicative only. The argument rests on the O(n²) worst case, not on these numbers. Timings are machine dependent; the objective values are reproducible.

**Code:**
```python
import numpy as np, time
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN
from sklearn.metrics import pairwise_distances_argmin_min
X, _ = make_blobs(300000, n_features=20, centers=20, cluster_std=2.0, random_state=0)
J = lambda C: (pairwise_distances_argmin_min(X, C)[1] ** 2).sum()          # k-means objective on all data
def timed(f):
    t = time.time(); m = f(); return m, time.time() - t
km, t1 = timed(lambda: KMeans(20, n_init=1, random_state=0).fit(X))
mb, t2 = timed(lambda: MiniBatchKMeans(20, n_init=1, batch_size=4096, random_state=0).fit(X))
S = X[np.random.default_rng(0).choice(len(X), 20000, replace=False)]
sm, t3 = timed(lambda: KMeans(20, n_init=1, random_state=0).fit(S))         # fit on 7% sample, then assign all
print(f"full {t1:.1f}s J={J(km.cluster_centers_):.0f} | minibatch {t2:.1f}s J={J(mb.cluster_centers_):.0f} | sample {t3:.1f}s J={J(sm.cluster_centers_):.0f}")
for n in (5000, 10000, 20000):
    print("DBSCAN n", n, f"{timed(lambda: DBSCAN(eps=3, min_samples=10).fit(X[:n]))[1]:.2f}s")
# not executed: faiss not installed. index = faiss.IndexFlatL2(d); index.add(centroids); D, I = index.search(users, 1)
```
Output (J values reproduced; seconds vary by machine and load): `full 5.9s J=23981616 | minibatch 0.1s J=23985323 | sample 0.0s J=24004136`; DBSCAN `0.04s / 0.13s / 0.36s` on the earlier quiet run.

**Follow-ups:**
- *How do you choose k at this scale?* Use a sample for the elbow/silhouette sweep (silhouette on a subsample, since it is O(n²)), plus stability and business needs.
- *How do you assign new users?* Nearest centroid; periodically re-fit and align labels to the old ones.
- *Streaming?* Online/mini-batch updates, or re-cluster on a schedule.

**Common mistakes:** Fitting on a biased sample (e.g. only recent or only active users). Computing silhouette on the full data. Using `n_init=10` on 100M rows. Using DBSCAN for large high-dimensional data. Forgetting to persist the centroids and scaler.

### Q46 ⭐ 🔴 Anomaly detection under drift and feedback loops: how do you handle changing normal behaviour, adversaries adapting (fraud), and labels coming only from flagged cases?
**Asked at:** PhonePe, Klarna, Booking, Amazon
**Say this first (1 line):** Treat it as a living system: refresh the baseline of "normal" on a schedule or on drift triggers (but protect it from slow poisoning), keep several diverse detectors and rules so adversaries cannot learn one, and fix the label bias by also reviewing a small random sample of unflagged cases, because if you only learn from what you flagged, you never find what you miss.
**Then explain:**
- **Changing normal (drift):** seasonality, new products, festivals, app releases. Handle with rolling or recent-window refits, calendar/promo features, drift monitors (PSI/KS on features and on the score distribution), and alert-rate tracking (a jump in alert rate with no business change usually means drift, not fraud).
- **Guard the refit:** an attacker can raise "normal" slowly (boiling the frog). Keep a long-term reference, cap the allowed daily shift, exclude confirmed bad cases from refits, and compare new vs old baseline before deploying (champion/challenger).
- **Adversaries adapt:** the pattern you catch gets abandoned; fraud moves to what you do not see. Use layered signals (rules for known patterns, anomaly models for the unknown, supervised models for the known-known), rotate or ensemble models, keep some features and thresholds private, add randomisation to thresholds, and add features that are costly to fake (device, network and graph signals).
- **Feedback-loop bias:** labels exist only for flagged (and reviewed) cases, so the training set is a biased sample, and a model retrained on it learns to flag what it already flags (self-reinforcing) and under-covers new fraud. Fixes:
  - **Exploration:** review a small random sample of unflagged items (e.g. 0.1-1%) plus items just below the threshold; use these for unbiased precision/recall estimates.
  - **Inverse-propensity weights** for flagged cases, when the flag probability is known.
  - **Holdout/delayed labels:** chargebacks and disputes arrive later and independent of your flags, so use them as ground truth.
  - **Semi-supervised:** keep an unsupervised detector running on everything, and use labels to re-rank, not to replace it.
- **Operational loop:** analyst decisions go back into a labelled store; tracked metrics are precision@k, estimated recall from the random sample, time to detect and alert volume; retraining is a reviewed, versioned process.
- **Trade-off:** more frequent refits adapt faster but absorb attacks and make results less stable; less frequent refits are stable but miss real change.

**Example:** Normal behaviour on 4 features drifts +0.15 sd per week. A model frozen at week 0 (alert rate 1% at week 0) alerts on 4.8% at week 4, 25.6% at week 8 and 66.1% at week 12: pure false alarms and alert fatigue. Refitting each week on the previous week's data keeps the alert rate near the 1% target (1.4%, 1.4%, 0.7%). Drift-adaptation is solved here, but the same refit would happily accept a slow attack as normal, hence the guard rails above.

**Code:**
```python
import numpy as np
from sklearn.ensemble import IsolationForest
rng = np.random.default_rng(0)
week = lambda w, n=2000: rng.normal(0.15 * w, 1, (n, 4))            # normal behaviour drifts +0.15 per week
static = IsolationForest(random_state=0).fit(week(0)); thr0 = np.percentile(static.score_samples(week(0)), 1)
for w in (0, 4, 8, 12):
    X = week(w); fa_static = (static.score_samples(X) < thr0).mean()
    prev = week(max(w - 1, 0)); recent = IsolationForest(random_state=0).fit(prev)
    fa_roll = (recent.score_samples(X) < np.percentile(recent.score_samples(prev), 1)).mean()
    print(f"week {w:2d}: static alert rate {fa_static*100:4.1f}% | refit-on-last-week {fa_roll*100:4.1f}%  (target 1%)")
```
Output: static 1.0 / 4.8 / 25.6 / 66.1 %; refit-on-last-week 1.2 / 1.4 / 1.4 / 0.7 %.

**Follow-ups:**
- *How to know recall if you only label flagged cases?* Random-sample review of unflagged cases, plus delayed ground truth (chargebacks), then estimate recall with confidence intervals.
- *How to detect a slow attack?* Compare against a long-lived reference baseline, monitor per-segment trends, and use CUSUM/EWMA on the score distribution.
- *When retrain?* On scheduled cadence and on triggers: PSI above threshold, alert rate out of band, or a metric drop on fresh labels; always shadow-test first.

**Common mistakes:** Retraining on flagged-only labels and calling it ground truth. Fully automatic refits with no guard against poisoning. One model, one threshold, never rotated. Treating an alert-rate spike as fraud without checking for drift. No exploration budget, so the blind spots stay invisible.
