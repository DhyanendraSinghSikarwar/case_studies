### Q35 ⭐ 🔴 Monitoring models on unstructured data (images, text, embeddings) at the Part 8 level. Explain drift on embeddings with distance to a reference centroid, a domain classifier (can a classifier tell reference from production, AUC near 0.5 or not), and simple metadata drift (image size, text length, language mix). Run a domain classifier on simulated embeddings with and without shift and show the AUC. Prompt, retrieval and answer-quality monitoring for LLM systems belong to Book 2, so only name the boundary.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** For embeddings I do not run a test per dimension; I ask "can a classifier tell reference from production?" (AUC near 0.5 means no, near 1 means yes), and I back it with centroid distance and cheap metadata drift like text length or image size.

**Then explain:**
- **Why not per-dimension tests:** a 768-dim embedding has no meaning per axis, and 768 KS tests give false alarms. Use one score for the whole vector.
- **Centroid distance:** distance between the mean embedding of reference and of today, scaled by the reference spread. Cheap, one number, good for a trend line. It misses shape changes where the mean stays put.
- **Domain classifier:** label reference 0 and production 1, cross-validate a simple model, read the AUC. About 0.5 is "cannot tell apart". Higher is "different", and the model's top features or misclassified rows show where.
- **Metadata drift:** text length, language mix, image width and height, file type, null rate. Boring but catches broken upstream pipelines the embedding hides (for example a resized image).
- **Failure modes:** a new embedding model version changes every vector (always compare same-version embeddings); small batches give noisy AUC; a flag tells you "different", not "worse", so pair it with a quality or label check. Prompt, retrieval and answer-quality monitoring for LLM systems is Book 2; this answer stops at the input side.

**Example:** 32-dim embeddings, 1000 rows each. Only 4 of the 32 dims are shifted. The per-dim shift is invisible by eye, but the domain AUC climbs from 0.505 (no shift) to 0.666 (shift 0.3) to 0.915 (shift 1.0). Text length (Poisson mean 40 to 55) is flagged by plain KS.

**Code:** (seeded; `python3 -I`)
```py
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from scipy.stats import ks_2samp

rng = np.random.default_rng(35)
D, N = 32, 1000
def emb(n, shift=0.0):
    x = rng.normal(0, 1, (n, D))
    x[:, :4] += shift            # shift only 4 of 32 dims
    return x
ref = emb(N)
def centroid_dist(ref, cur):     # distance between mean vectors, scaled by ref spread
    return float(np.linalg.norm(cur.mean(0) - ref.mean(0)) / np.sqrt(D))
def domain_auc(ref, cur):
    X = np.vstack([ref, cur]); y = np.r_[np.zeros(len(ref)), np.ones(len(cur))]
    p = cross_val_predict(LogisticRegression(max_iter=500), X, y, cv=5, method="predict_proba")[:, 1]
    return float(roc_auc_score(y, p))
for name, shift in [("no shift", 0.0), ("small shift 0.3", 0.3), ("shift 1.0", 1.0)]:
    cur = emb(N, shift)
    print(f"{name:16s} centroid_dist={centroid_dist(ref,cur):.3f}  domain_AUC={domain_auc(ref,cur):.3f}")
# metadata drift: text length (tokens), same embeddings
len_ref = rng.poisson(40, N); len_cur = rng.poisson(55, N)
print("text length KS D=%.3f p=%.2g" % ks_2samp(len_ref, len_cur))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs).
```text
no shift         centroid_dist=0.044  domain_AUC=0.505
small shift 0.3  centroid_dist=0.118  domain_AUC=0.666
shift 1.0        centroid_dist=0.344  domain_AUC=0.915
text length KS D=0.728 p=6.1e-257
```

**Follow-ups:**
- *What if the domain classifier says AUC 0.9 but metrics are fine?* The shift may not touch what the model uses. Log it, check a labelled sample, do not auto-retrain.
- *Why cross-validate?* Scoring the classifier on its own training rows always looks great; AUC must be on held-out rows.
- *Distances in high dimensions?* Distances concentrate; prefer cosine or a PCA-reduced space, and keep the classifier as the main signal.

**Common mistakes:** per-dimension KS on every axis; mixing embeddings from two model versions; reading AUC on training rows; treating "drift" as "bad"; forgetting metadata checks.

### Q36 ⭐ 🔴 Multivariate drift that univariate tests miss. Show an example where each feature's marginal is unchanged but the correlation flips, explain PCA reconstruction error, a domain classifier, and a pairwise-correlation check, and how to choose among them. Simulate it, run per-feature KS (quiet) against the domain classifier and the correlation diff (loud), and say what the loud detectors cannot tell you (which feature changed).
**Asked at:** Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Per-feature tests look only at one column at a time, so they miss a change in how features relate; I add a domain classifier, a PCA reconstruction error and a pairwise-correlation diff, which are loud when the marginals are quiet.

**Then explain:**
- **The blind spot:** two features can each stay N(0,1) while their correlation flips from +0.8 to -0.8. Every KS test passes, the joint distribution is totally different.
- **Correlation diff:** compare the correlation matrix to the reference. Cheap, readable ("x0 and x1 now move opposite"), but only sees linear pairs.
- **PCA reconstruction error:** fit PCA on reference, reconstruct production with the same components, watch the error. Rising error means production sits off the old structure. Linear again.
- **Domain classifier:** any model that can separate the two windows. A tree model sees non-linear changes too. Most general, and the most expensive to keep running.
- **Choosing:** daily and cheap, correlation diff plus PCA error. When one fires, or on a weekly cadence, run the domain classifier. Per-feature KS stays on, for single-column faults.
- **What the loud ones cannot say:** which feature changed. All of them only say "the joint changed". To localise: look at the pairwise cell with the biggest diff, or the classifier's feature importance; neither is proof of a cause.
- **Failure mode:** with many features, correlation diffs multiply (p features give p(p-1)/2 pairs), so set the threshold from a bootstrap (Q38).

**Example:** 2000 rows each, reference corr +0.81, production -0.79. KS p-values 0.53 and 0.46 (quiet). Random-forest domain AUC 0.893, correlation difference 1.60, PCA(1) error 0.188 to 1.781. In a control with no change the AUC is 0.512, corr diff 0.002 and errors 0.197 vs 0.202.

**Code:** (seeded; `python3 -I`)
```py
import numpy as np
from scipy.stats import ks_2samp
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.decomposition import PCA

rng = np.random.default_rng(36)
n = 2000
def make(rho):
    cov = [[1, rho], [rho, 1]]
    return rng.multivariate_normal([0, 0], cov, n)
ref, cur = make(0.8), make(-0.8)   # marginals identical N(0,1), correlation flips
for j in range(2):
    D, p = ks_2samp(ref[:, j], cur[:, j])
    print(f"per-feature KS x{j}: D={D:.3f} p={p:.2f}")
# domain classifier (non-linear, so it can see the correlation)
X = np.vstack([ref, cur]); y = np.r_[np.zeros(n), np.ones(n)]
pr = cross_val_predict(RandomForestClassifier(100, min_samples_leaf=20, random_state=0), X, y, cv=5, method="predict_proba")[:, 1]
print("domain classifier AUC: %.3f" % roc_auc_score(y, pr))
# correlation diff
c0, c1 = np.corrcoef(ref.T)[0, 1], np.corrcoef(cur.T)[0, 1]
print(f"corr ref={c0:.3f} cur={c1:.3f} abs diff={abs(c1-c0):.3f}")
# PCA reconstruction error: fit on ref, 1 component
pca = PCA(1).fit(ref)
def rec_err(x): return float(np.mean(np.sum((x - pca.inverse_transform(pca.transform(x)))**2, axis=1)))
print(f"PCA(1) recon error ref={rec_err(ref):.3f} cur={rec_err(cur):.3f}")
# control: no change at all
ref2, cur2 = make(0.8), make(0.8)
pr2 = cross_val_predict(RandomForestClassifier(100, min_samples_leaf=20, random_state=0), np.vstack([ref2, cur2]), y, cv=5, method="predict_proba")[:, 1]
print("control (no change) domain AUC: %.3f  corr diff %.3f  recon %.3f vs %.3f" % (
    roc_auc_score(y, pr2), abs(np.corrcoef(cur2.T)[0,1]-np.corrcoef(ref2.T)[0,1]), rec_err(ref2), rec_err(cur2)))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs).
```text
per-feature KS x0: D=0.026 p=0.53
per-feature KS x1: D=0.027 p=0.46
domain classifier AUC: 0.893
corr ref=0.808 cur=-0.794 abs diff=1.602
PCA(1) recon error ref=0.188 cur=1.781
control (no change) domain AUC: 0.512  corr diff 0.002  recon 0.197 vs 0.202
```

**Follow-ups:**
- *Why a random forest and not logistic regression?* A linear model on (x0, x1) cannot separate a flipped correlation; a tree model can. Pick a classifier that matches the shapes you worry about.
- *Does the model care?* Check feature-pair interactions in the model; a flipped correlation hurts a model that relies on the pair, and may do nothing to one that does not.

**Common mistakes:** trusting green per-feature KS as "no drift"; running a linear domain classifier and calling the joint "fine"; expecting these detectors to name the culprit.

### Q37 ⭐ 🔴 Online change detection on a metric stream: CUSUM, Page-Hinkley and an adaptive window idea (ADWIN at concept level). Explain the delay versus false-alarm trade-off, the parameters (drift allowance and threshold), and why they suit a slow-moving error rate better than repeated KS tests. Implement CUSUM and Page-Hinkley with numpy, run on a stream with a step change and with noise only, report detection delay and false alarms over 200 seeds. Part 9 owns streaming infrastructure.
**Asked at:** Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** CUSUM and Page-Hinkley keep a running sum of "how far above normal, minus an allowance", and alarm when the sum crosses a threshold; that finds a small, lasting rise in an error rate much faster than repeating a KS test on windows.

**Then explain:**
- **CUSUM:** `s = max(0, s + z - k)`; alarm when `s > h`. `k` is the drift allowance (ignore wobble smaller than about k sd), `h` is the threshold.
- **Page-Hinkley:** same idea with a running mean as reference: accumulate `z - mean - delta`, alarm when the sum rises `lam` above its running minimum.
- **ADWIN (concept only, not implemented here):** keeps a window that grows while data is stable and drops the old part when two sub-windows have different means. It adapts the window so you do not pick one.
- **The trade-off:** a low threshold finds changes sooner and fires on noise more; a high threshold is quiet and slow. The "average run length" between false alarms and the detection delay move in opposite directions.
- **Why not repeated KS:** each KS test uses a fixed window, tests again and again (more chances to false-alarm), and is slow for a slow shift; a cumulative sum uses every point since the change.
- **Failure modes:** parameters are in units of the baseline sd, so a wrong baseline mean or sd means wrong alarms; reset the sum after an alarm; for stream infrastructure see Part 9.

**Example:** baseline 0.10, sd 0.02, a +1 sd step (0.12) at t=300, 600 points, 200 seeds. `h=5` is too jumpy (94/200 noise-only runs alarm). `h=8` gives 5/200 false alarms and a median delay of 14 points; Page-Hinkley `lam=15` gives 0/200 false alarms with a median delay of 31.5.

**Code:** (seeded, numpy only; `python3 -I`)
```py
import numpy as np
# Stream: daily error rate-like metric, baseline mean 0.10, sd 0.02; step to 0.12 at t=300 (1 sd).
MU, SD, T, STEP_AT, STEP = 0.10, 0.02, 600, 300, 0.02

def cusum(x, k=0.5, h=5.0):
    """Upper CUSUM on standardised values. k = drift allowance (in sd), h = threshold (in sd). Returns first alarm index or None."""
    s = 0.0
    for i, v in enumerate(x):
        z = (v - MU) / SD
        s = max(0.0, s + z - k)
        if s > h: return i
    return None

def page_hinkley(x, delta=0.5, lam=8.0):
    """Page-Hinkley for an increase. delta = tolerated drift (in sd), lam = threshold (in sd). Running mean as the reference."""
    m, cum, cum_min = 0.0, 0.0, 0.0
    for i, v in enumerate(x):
        z = (v - MU) / SD
        m += (z - m) / (i + 1)
        cum += z - m - delta
        cum_min = min(cum_min, cum)
        if cum - cum_min > lam: return i
    return None

def run(detector, **kw):
    delays, fa_noise, pre = [], 0, 0
    for seed in range(200):
        r = np.random.default_rng(seed)
        noise = r.normal(MU, SD, T)
        fa_noise += detector(noise, **kw) is not None       # noise-only stream: any alarm is false
        shifted = noise.copy(); shifted[STEP_AT:] += STEP    # same noise plus a step at t=300
        a = detector(shifted, **kw)
        if a is not None and a < STEP_AT: pre += 1           # alarmed before the step: false alarm
        elif a is not None: delays.append(a - STEP_AT)
    return np.median(delays), len(delays), fa_noise, pre

print("noise-only: 600 points. step run: +1 sd (0.02) at t=300. 200 seeds.")
for name, det, kws in [("CUSUM k=0.5 h=5", cusum, dict(k=0.5, h=5.0)),
                       ("CUSUM k=0.5 h=8", cusum, dict(k=0.5, h=8.0)),
                       ("PageHinkley d=0.5 lam=8", page_hinkley, dict(delta=0.5, lam=8.0)),
                       ("PageHinkley d=0.5 lam=15", page_hinkley, dict(delta=0.5, lam=15.0))]:
    med, n, fa, pre = run(det, **kws)
    print(f"{name:26s} false alarms (noise-only)={fa:3d}/200  alarmed before step={pre:3d}/200  detected after step={n:3d}/200  median delay={med:.1f} points")
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs). Delay is measured only on runs that had not already alarmed before the step, so it is slightly flattering for the jumpy settings.
```text
noise-only: 600 points. step run: +1 sd (0.02) at t=300. 200 seeds.
CUSUM k=0.5 h=5            false alarms (noise-only)= 94/200  alarmed before step= 56/200  detected after step=144/200  median delay=8.0 points
CUSUM k=0.5 h=8            false alarms (noise-only)=  5/200  alarmed before step=  3/200  detected after step=197/200  median delay=14.0 points
PageHinkley d=0.5 lam=8    false alarms (noise-only)=  6/200  alarmed before step=  3/200  detected after step=197/200  median delay=15.0 points
PageHinkley d=0.5 lam=15   false alarms (noise-only)=  0/200  alarmed before step=  0/200  detected after step=200/200  median delay=31.5 points
```

**Follow-ups:**
- *How do you pick h?* Simulate noise-only streams (as above) to hit a target false-alarm rate, then read the delay you get.
- *Two-sided?* Run one CUSUM for up and one for down.
- *Seasonal metric?* De-trend or compare to the same weekday first, or the weekly cycle looks like drift.

**Common mistakes:** k and h copied from a blog without matching your units; never resetting after an alarm; using it on a metric whose baseline is not stable; claiming a delay number without reporting false alarms next to it.

### Q38 ⭐ 🔴 Calibrating drift thresholds from history instead of rules of thumb. Explain bootstrapping the reference to get a null distribution of PSI or KS D for your batch size, choosing a threshold for a target false-alarm rate, and backtesting on past incidents. Implement it with numpy, run for batch sizes 200, 2000 and 20000, show that the same 0.1 PSI means different things at each, and show the chosen thresholds. Say how seasonality and multiple features change the answer.
**Asked at:** Drift-test pitfall sources (Evidently blog 'data drift detection on large datasets' saying KS is too sensitive on large data, an Arize docs monitors page saying PSI is less sample-sensitive, an ICLR 2026 virtual-page submission 'When drift detectors cry wolf' on false-alarm rates with PSI unstable below about 200 samples and Bonferroni lowering power, a wikidocs PSI and KS guide; search snippets only, not opened; WebFetch of evidentlyai.com failed with getaddrinfo ENOTFOUND; sources partly conflict on PSI versus KS sensitivity); vendor docs and one conference submission, not interview reports; MLOps and data science roles | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I do not use "PSI above 0.1"; I draw many clean batches of my real batch size from history, see what PSI or KS D looks like when nothing changed, and set the threshold at the level that gives me my target false-alarm rate.

**Then explain:**
- **Why a fixed number fails:** PSI on small batches is noisy. At n=200 a clean batch exceeds 0.1 about 3 percent of the time; at n=2000 or 20000 never. 0.1 is a rule of thumb from credit scoring, not a standard.
- **Method:** bootstrap batches of size n from the reference, compute the statistic each time, take the 95th or 99th percentile as threshold. That is the null distribution for this batch size.
- **Backtest:** replay past days and past incidents through the chosen threshold. Count false alarms on known-quiet days and hits on known incidents. Adjust the percentile, not the story.
- **Many features:** with 50 features at a 1 percent per-feature rate you expect at least one alarm on 39.5 percent of days. Use a stricter per-feature level (about 0.0002 for a 1 percent daily rate over 50 independent features), or alert on "how many features moved".
- **Seasonality:** build the reference from the same weekday or season, or the null distribution itself is too narrow and every Monday alarms.
- **Failure modes:** a null built from a reference that already contains drift; bootstrapping with replacement from a tiny reference; a high threshold that no longer catches a real 0.15 sigma shift (check power as well).

**Example:** n=200 gives a PSI null p99 of 0.1217; n=2000 gives 0.0111; n=20000 gives 0.0010. The same 0.1 means "almost the noise ceiling" at 200 and "huge" at 20000. At n=2000 a threshold of 0.0114 had 1.5 percent false alarms on fresh clean batches and caught a 0.15-sigma shift 99 percent of the time.

**Code:** (seeded, numpy and scipy; `python3 -I`)
```py
import numpy as np
from scipy.stats import ks_2samp

rng = np.random.default_rng(38)
ref = rng.normal(0, 1, 50000)                       # history: a large, clean reference
edges = np.quantile(ref, np.linspace(0, 1, 11)); edges[0], edges[-1] = -np.inf, np.inf  # 10 reference-quantile bins
ref_p = np.full(10, 0.1)

def psi(x):
    c = np.histogram(x, edges)[0] / len(x)
    c = np.clip(c, 1e-4, None)
    return float(np.sum((c - ref_p) * np.log(c / ref_p)))

B = 1000
print("null distribution = PSI/KS between the reference and clean batches drawn from the SAME history, %d bootstrap batches" % B)
print(f"{'n':>6} {'mean PSI':>9} {'p95 PSI':>8} {'p99 PSI':>8} {'P(PSI>0.1) on clean':>20} {'p99 KS D':>9}")
for n in (200, 2000, 20000):
    ps, ds = [], []
    for _ in range(B):
        b = rng.choice(ref, n, replace=True)
        ps.append(psi(b)); ds.append(ks_2samp(ref, b).statistic)
    ps, ds = np.array(ps), np.array(ds)
    print(f"{n:6d} {ps.mean():9.4f} {np.quantile(ps,.95):8.4f} {np.quantile(ps,.99):8.4f} {np.mean(ps>0.1):20.3f} {np.quantile(ds,.99):9.4f}")

# backtest: a threshold at the 99th pct, n=2000, against a real 0.15-sigma shift and 200 clean days
n = 2000
ps = [psi(rng.choice(ref, n)) for _ in range(B)]
thr = float(np.quantile(ps, .99))
clean_fa = np.mean([psi(rng.normal(0, 1, n)) > thr for _ in range(200)])
hit = np.mean([psi(rng.normal(0.15, 1, n)) > thr for _ in range(200)])
print(f"\nn=2000 chosen PSI threshold (p99 of null) = {thr:.4f}; false alarms on 200 fresh clean batches = {clean_fa:.3f}; detection of a 0.15-sigma shift = {hit:.3f}")
# many features: per-feature alpha 0.01 across 50 independent features
print("50 features, per-feature false-alarm rate 0.01: P(at least one alarm per day) = %.3f" % (1 - 0.99**50))
print("per-feature rate for a 0.01 daily family-wise rate over 50 features = %.5f" % (1 - 0.99**(1/50)))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs). (The batches are drawn from the same 50000-row history that is the reference, so the null is slightly narrower than with fully independent data.)
```text
null distribution = PSI/KS between the reference and clean batches drawn from the SAME history, 1000 bootstrap batches
     n  mean PSI  p95 PSI  p99 PSI  P(PSI>0.1) on clean  p99 KS D
   200    0.0470   0.0896   0.1217                0.031    0.1157
  2000    0.0046   0.0085   0.0111                0.000    0.0346
 20000    0.0005   0.0008   0.0010                0.000    0.0113

n=2000 chosen PSI threshold (p99 of null) = 0.0114; false alarms on 200 fresh clean batches = 0.015; detection of a 0.15-sigma shift = 0.990
50 features, per-feature false-alarm rate 0.01: P(at least one alarm per day) = 0.395
per-feature rate for a 0.01 daily family-wise rate over 50 features = 0.00020
```

**Follow-ups:**
- *Why PSI and KS both?* PSI shrinks with n (noise), KS D shrinks too; a p-value alone grows sensitive at large n, so I also set a minimum effect size (Evidently's blog says the same for KS at large n; check current docs).
- *What target rate?* Whatever the on-call can bear: alert fatigue is the real cost, so tie it to one false page per feature-month, not 5 percent.

**Common mistakes:** one threshold for every batch size; quoting 0.1 and 0.25 as industry standards; calibrating on a reference that includes the incident; checking false alarms but never power.

### Q39 ⭐ 🔴 Monitoring at scale and cost. Explain why you do not log or test every row: sampling, sketches and mergeable profiles (whylogs-style), pre-aggregated histograms, windowed jobs, and the cost of many models times many features. Use whylogs to profile three daily batches, merge the profiles, compare against the reference with its drift scores, and compare the profile size with the raw data size. Record the whylogs version and what ran; SaaS storage (WhyLabs) was not executed.
**Asked at:** Prometheus and Grafana monitoring mentions (K21Academy and Towards AI question lists naming Prometheus, Grafana and Evidently for drift and accuracy dashboards; Devinterview-io page opened, Q12 mentions inference monitoring with Grafana and Prometheus; search snippets otherwise); question lists, not verified reports; MLOps and platform roles; Prometheus, Grafana and Alertmanager servers were not available in this sandbox | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** At scale I do not store or test every row; I keep small mergeable profiles (histograms and counts, whylogs-style) per day, merge them for longer windows, and compare profiles to the reference, which costs almost nothing compared with raw data.

**Then explain:**
- **Sampling:** a random sample is fine for aggregate drift; keep every flagged or rare event (fraud, errors) at 100 percent.
- **Sketches and profiles:** a profile stores counts, min/max, distribution sketches per column. Profiles are mergeable: day1 + day2 + day3 = a 3-day profile without the rows.
- **Pre-aggregated histograms:** if you already have bucket counts in your warehouse, compute PSI from those; no raw pull.
- **Windowed jobs:** schedule per model per window; cost scales as models x features x windows, so tier models (critical ones get more features and hourly windows).
- **Failure modes:** sketches are approximate; a profile cannot be re-sliced by a column you did not profile; high-cardinality columns blow up size; string columns failed here (see below).

**Example:** three daily batches of 50000 rows (day 3 has `amount` shifted up), compared to a 50000-row reference. Day 1 shows no drift on any column; day 3 shows drift on `amount` only (statistic 0.237); the merged 3-day profile shows `amount` drift (0.079) diluted by two clean days. Merged profile file about 61.8 KB against 3.6 MB of in-memory dataframes (58 times smaller, and it does not grow with rows).

**Code:** (seeded; whylogs env with `[viz]`; `python3 -I`)
```py
import os, tempfile, warnings, logging
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
import numpy as np, pandas as pd, whylogs as why
from whylogs.viz.drift.column_drift_algorithms import calculate_drift_scores

rng = np.random.default_rng(39)
def batch(n, mean, scale=1.0):
    return pd.DataFrame({"amount": rng.lognormal(mean, 0.5 * scale, n),
                         "age": rng.normal(40, 10, n),
                         "channel_code": rng.choice([0, 1, 2], n, p=[.5, .3, .2])})  # ints on purpose: string columns hit an np.unicode_ error on numpy 2 here
ref = batch(50000, 3.0)
days = [batch(50000, 3.0), batch(50000, 3.0), batch(50000, 3.3)]   # day 3 amount shifted
print("whylogs", why.__version__, "| pandas", pd.__version__)
ref_view = why.log(ref).view()
views = [why.log(d).view() for d in days]
merged = views[0]
for v in views[1:]: merged = merged.merge(v)
print("merged rows (count of amount):", merged.get_column("amount").get_metric("counts").n.value)
for name, tgt in [("day1", views[0]), ("day3", views[2]), ("merged 3 days", merged)]:
    s = calculate_drift_scores(target_view=tgt, reference_view=ref_view, with_thresholds=True)
    print(f"{name:14s}", {k: (round(v["statistic"], 3), v["algorithm"], v["drift_category"]) for k, v in s.items() if v})
raw = sum(d.memory_usage(deep=True).sum() for d in days)
d = tempfile.mkdtemp(); p = os.path.join(d, "merged.bin"); merged.write(p)
print("raw bytes in memory (3 days):", int(raw), "| merged profile file bytes:", os.path.getsize(p), "| ratio raw/profile: %.0f" % (raw / os.path.getsize(p)))
```

**Output (my run):** whylogs 1.6.4, pandas 3.1.0, numpy 2.5.4 in /tmp/claude-0/b8p08/e_whylogs. Drift scores come from `calculate_drift_scores` (needs `whylogs[viz]`); the number printed is the score for the KS algorithm, and the DRIFT or NO_DRIFT label uses whylogs' default threshold (check current docs). I did not rerun the string column case; a string column raised `AttributeError: np.unicode_ was removed in the NumPy 2.0 release` here, so I used numeric columns only. WhyLabs or any SaaS storage: not executed (no account or network service); the profile file above is the local equivalent.
```text
whylogs 1.6.4 | pandas 3.1.0
merged rows (count of amount): 150000
day1           {'amount': (0.003, 'ks', 'NO_DRIFT'), 'age': (0.006, 'ks', 'NO_DRIFT'), 'channel_code': (0.003, 'ks', 'NO_DRIFT')}
day3           {'amount': (0.236, 'ks', 'DRIFT'), 'age': (0.005, 'ks', 'NO_DRIFT'), 'channel_code': (0.004, 'ks', 'NO_DRIFT')}
merged 3 days  {'age': (0.005, 'ks', 'NO_DRIFT'), 'amount': (0.078, 'ks', 'DRIFT'), 'channel_code': (0.003, 'ks', 'NO_DRIFT')}
raw bytes in memory (3 days): 3600396 | merged profile file bytes: 61818 | ratio raw/profile: 58
```

**Follow-ups:**
- *Are merged profiles exact?* Counts, min, max, mean are exact. Quantile or distribution sketches carry a small error.
- *What do you lose?* Row-level debugging; keep a small sampled raw store next to the profiles.
- *Cost lever?* Fewer features, a longer window, a lower tier for low-risk models.

**Common mistakes:** logging every row to the warehouse "just in case"; profiling only the averages (distribution shape lost); forgetting that a merged window hides a one-day spike; assuming a library works on a new numpy without running it.

### Q40 ⭐ 🔴 Attribution drift and 'metric dropped but no drift detected'. Explain monitoring feature importance or contribution shift (permutation importance on a recent labelled window, mean absolute contribution for linear or tree models), the cases drift tests miss (concept change, a changed label definition, a join bug), and the debugging order when performance drops and every drift test is green. Simulate a concept change where only importance shifts, show the importance comparison catching it, and give the checklist.
**Asked at:** Label-delay and estimation sources (NannyML blog 'machine learning monitoring workflow' on delayed or absent targets, CBPE and DLE, and warning that drift alerts alone can flood a team; arXiv 'Monitoring Machine Learning Systems: A Multivocal Literature Review' 2509.14294; arXiv 2403.16795 interview study 'We have no idea how models will behave in production until production' reporting alert fatigue from false positives; search snippets only, not opened); vendor blog and academic papers, not interview reports; ML engineer and MLOps roles | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** When the metric drops and every drift test is green, I suspect the relationship between inputs and the label changed (concept change), a label or join bug, so I compare feature importance on a recent labelled window against the reference; the model's key feature stops mattering.

**Then explain:**
- **Drift tests only see inputs (and scores).** If the inputs look the same but the label's meaning moved, they stay quiet. That is the classic case.
- **Permutation importance:** on a labelled recent window, shuffle one feature and measure the metric drop. A big feature that used to matter and now matters 0 is a strong sign. Needs labels, so it lags.
- **Mean absolute contribution** (linear coefficients times values, or tree SHAP values; check your library's docs): label-free, can run daily; a shift in contribution means the inputs push the score differently.
- **Cases drift tests miss:** concept change; a changed label definition (a new chargeback rule); a join bug (labels attached to the wrong rows, so everything looks fine on inputs); feedback loops.
- **Debugging order when metric is down and drift is green:** (1) is the metric itself right (label definition, cohort, time window)? (2) label and join integrity on a sample; (3) data quality and schema; (4) score distribution and thresholds; (5) importance and slice analysis; (6) then conclude concept change and retrain on new labels.
- **Failure mode:** importance on a tiny window is noisy; correlated features share importance; importance shift is a clue, not proof.

**Example:** f0 drives the label before, f1 after (marginals never change). AUC drops 0.933 to 0.511; KS p-values 0.52, 0.58, 0.75 (quiet); mean score 0.498 vs 0.500 (quiet). Permutation importance of f0 falls 0.413 to -0.001 while f1 stays near 0 (the model never learned it).

**Code:** (seeded; `python3 -I`)
```py
import numpy as np
from scipy.stats import ks_2samp
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(40)
n = 6000
def X(n): return rng.normal(0, 1, (n, 3))          # f0, f1, f2: marginals never change
def y_old(x): return (x[:, 0] + 0.2 * x[:, 2] + rng.normal(0, 0.5, len(x)) > 0).astype(int)  # f0 drives the label
def y_new(x): return (x[:, 1] + 0.2 * x[:, 2] + rng.normal(0, 0.5, len(x)) > 0).astype(int)  # concept change: f1 drives it now
Xtr, Xref, Xcur = X(n), X(n), X(n)
ytr, yref, ycur = y_old(Xtr), y_old(Xref), y_new(Xcur)
m = GradientBoostingClassifier(random_state=0).fit(Xtr, ytr)
print("AUC reference window: %.3f   AUC current window: %.3f" % (roc_auc_score(yref, m.predict_proba(Xref)[:, 1]), roc_auc_score(ycur, m.predict_proba(Xcur)[:, 1])))
print("per-feature KS p-values ref vs cur:", [round(float(ks_2samp(Xref[:, j], Xcur[:, j]).pvalue), 2) for j in range(3)], "(all quiet)")
def perm(Xw, yw):
    return permutation_importance(m, Xw, yw, scoring="roc_auc", n_repeats=5, random_state=0).importances_mean
pr, pc = perm(Xref, yref), perm(Xcur, ycur)
print("perm importance (AUC drop) ref:", np.round(pr, 3), " cur:", np.round(pc, 3))
print("importance change cur-ref     :", np.round(pc - pr, 3))
# Mean |contribution| of the model's own scores per feature is label-free; show prediction distribution stays put
print("mean predicted prob ref %.3f cur %.3f (score drift quiet too)" % (m.predict_proba(Xref)[:, 1].mean(), m.predict_proba(Xcur)[:, 1].mean()))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs).
```text
AUC reference window: 0.933   AUC current window: 0.511
per-feature KS p-values ref vs cur: [0.52, 0.58, 0.75] (all quiet)
perm importance (AUC drop) ref: [ 0.413 -0.     0.018]  cur: [-0.001  0.002  0.013]
importance change cur-ref     : [-0.414  0.002 -0.005]
mean predicted prob ref 0.498 cur 0.500 (score drift quiet too)
```

**Follow-ups:**
- *So what is the fix?* New labels under the new rule, retrain, validate (Q41 gates). A threshold tweak does not repair a concept change.
- *No labels yet?* Use contribution shift plus proxy labels, or an estimate like NannyML's CBPE (concept only here).

**Common mistakes:** "no drift so no problem"; blaming the model before checking the label definition; trusting a feature-importance diff on a few hundred rows.

### Q41 ⭐ 🔴 Model risk governance and monitoring for a regulated lender, for example an Indian bank or NBFC credit-scoring model. Cover model inventory, periodic validation, monitoring thresholds that trigger review, challenger models, audit trail of decisions, explainability on request, and change control for retraining. Give a whiteboard answer and a monitoring-policy YAML, validate it with pyyaml, and state that the specific regulator expectations (check current RBI and other guidance, which was not looked up here) are not quoted. Part 12 owns system design in depth.
**Asked at:** Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** For a regulated lender I treat the model as a controlled asset: it is in an inventory, validated independently, monitored against thresholds that trigger a human review, changed only through change control, and every decision is traceable and explainable.

**Then explain:**
- **Model inventory:** every model has an owner, risk tier, intended use and version. If it is not in the inventory, it should not score.
- **Validation:** independent validation before go-live and periodic revalidation; monitoring feeds that, it does not replace it.
- **Thresholds that trigger review:** warn then breach levels (input PSI, score PSI, matured-cohort Gini or KS drop, approval-rate change, data quality). A breach opens a review, not an automatic retrain.
- **Challenger:** run a shadow challenger; promotion needs validation, approval and a rollback plan.
- **Audit trail:** log request id, model version, features (hashed or referenced), score, decision, reason codes, timestamp; retention set by compliance.
- **Explainability on request:** reason codes from contributions, reproducible for an old decision with the logged version.
- **Change control:** retrain request with ticket, validation report, approver who is not the author; rollback to the previous registered version.
- **Failure modes:** labels (defaults) mature slowly; a policy YAML nobody enforces; thresholds copied, not calibrated (Q38).
- **Regulator:** I did not look up RBI or other regulator guidance, so none is quoted. In the interview I would say "my policy follows whatever the bank's model-risk framework and current regulator guidance require; I would check with compliance".

**Example (whiteboard):** inventory -> validate -> deploy v3 -> monthly monitor -> warn: notify owner; breach: review meeting -> challenger in shadow -> committee approves -> versioned rollout with rollback. Next to it, a decision log row per application.

**Code:** (placeholders, not real policy numbers; validated with pyyaml)
```yaml
# Illustrative monitoring policy for a regulated credit-scoring model.
# Numbers are placeholders for the model-risk team to set; regulator expectations are NOT quoted here.
model:
  id: credit_score_v3
  owner: retail-risk-analytics
  risk_tier: high
  inventory_ref: MRM-0042
  intended_use: unsecured personal loan underwriting
validation:
  independent_validation_before_go_live: true
  periodic_revalidation_months: 12
monitoring:
  cadence: monthly
  checks:
    - {name: input_psi_max, level: warn, threshold: 0.10, action: notify_owner}
    - {name: input_psi_max, level: breach, threshold: 0.25, action: open_review}
    - {name: score_psi, level: breach, threshold: 0.20, action: open_review}
    - {name: gini_matured_cohort_drop, level: breach, threshold: 0.05, action: open_review}
    - {name: approval_rate_change_abs, level: warn, threshold: 0.05, action: notify_owner}
    - {name: missing_rate_any_feature, level: breach, threshold: 0.02, action: block_scoring_and_page}
  thresholds_status: calibrated_on_history   # see Q38; backtest on past incidents
challenger:
  enabled: true
  mode: shadow
  promote_requires: [independent_validation, committee_approval, rollback_plan]
audit:
  log_fields: [request_id, model_version, feature_hash, score, decision, reason_codes, timestamp]
  retain_years: TBD_by_compliance
  pii_policy: hash_or_omit
explainability:
  on_request: true
  method: reason_codes_from_contributions
change_control:
  retrain_requires: [ticket, validation_report, approver_not_author]
  rollback_to: previous_registered_version
```
```py
import yaml, sys
p = yaml.safe_load(open(sys.argv[1]))
need = ["model", "validation", "monitoring", "challenger", "audit", "explainability", "change_control"]
missing = [k for k in need if k not in p]
assert not missing, missing
levels = {"warn", "breach"}
for c in p["monitoring"]["checks"]:
    assert c["level"] in levels and isinstance(c["threshold"], float) and c["action"], c
# every check name with a breach level must have an action that is not just a notification
breach_actions = {c["action"] for c in p["monitoring"]["checks"] if c["level"] == "breach"}
assert breach_actions <= {"open_review", "block_scoring_and_page"}, breach_actions
# a warn threshold must be below its breach threshold when both exist
by = {}
for c in p["monitoring"]["checks"]: by.setdefault(c["name"], {})[c["level"]] = c["threshold"]
for n, d in by.items():
    if len(d) == 2: assert d["warn"] < d["breach"], n
assert p["challenger"]["mode"] == "shadow" and "retain_years" in p["audit"]
print("policy OK: sections", sorted(p), "| checks", len(p["monitoring"]["checks"]), "| names with both levels:", [n for n, d in by.items() if len(d) == 2])
```

**Output (my run):** PyYAML 6.0.3. Structural validation only (sections present, thresholds numeric, warn < breach where both exist, breach actions are reviews or blocks). Actual regulator rules, audit-retention length and any bank tooling: not executed / not looked up.
```text
policy OK: sections ['audit', 'challenger', 'change_control', 'explainability', 'model', 'monitoring', 'validation'] | checks 6 | names with both levels: ['input_psi_max']
```

**Follow-ups:**
- *Who approves a retrain?* Someone other than the author, per the policy (validation plus committee).
- *Why shadow challenger?* It scores live traffic without affecting decisions, so you compare before promotion.
- *Fairness?* Add segment-level checks to the policy (concept in the YAML for Q43; regulator expectations not looked up).

**Common mistakes:** automatic retraining with no validation; no model inventory; logging features without a version; quoting regulator rules from memory.

### Q42 ⭐ 🟡 LLM and GenAI monitoring, only at the boundary with Book 2. State what carries over from classic ML monitoring (input data quality, schema, latency, cost, error rates, feedback logging, drift on input categories, privacy of logs, incident process) and what does not (hallucination, groundedness, prompt-injection and retrieval quality, which Book 2 and a later LLMOps part own). Implement a small logger for request, response length, latency and thumbs feedback with a rolling summary, run it on a stub model (no real API call, so say the real provider is not executed).
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Most classic monitoring carries over (input quality, schema, latency, cost, errors, feedback, privacy, incidents); what does not is quality judgement like hallucination, groundedness, prompt-injection and retrieval quality, which Book 2 and a later LLMOps part own.

**Then explain:**
- **Carries over:** request validity and schema, latency percentiles, error and timeout rate, token or cost per call, response length, drift on input categories, thumbs or other feedback with a delay, privacy of logs, an incident process.
- **Does not carry over cleanly:** there is no single label; "correct" is fuzzy. Hallucination, groundedness, injection and retrieval quality need their own evaluators (Book 2).
- **Log metadata first:** store length, latency, a hash of the prompt and feedback; store raw text only if policy allows, masked.
- **Rolling summary:** a fixed window of recent calls gives p50, p95, error rate, mean length and thumbs-up rate; compare to a baseline.
- **Failure modes:** feedback is sparse and biased (only unhappy users click); a rolling window over a quiet hour is noisy; changing the provider's model silently moves everything.

**Example:** 80 calls to a stub, window of 50. At call 50: error 0.06, p50 266 ms, p95 390 ms. At call 80 (a simulated slowdown): p50 362, p95 853, error 0.08, thumbs-up 0.812 on 16 votes (too few to read much into).

**Code:** (stub model, seeded; `python3 -I`). The real provider call is not executed; latencies are simulated numbers.
```py
import time, json, random, zlib, statistics as st
from collections import deque

class CallLogger:
    """Log metadata first: no raw text stored, only length, latency, a hash of the request, feedback."""
    def __init__(self, window=50):
        self.rows = deque(maxlen=window)
    def log(self, request_id, prompt, response, latency_ms, error=None):
        self.rows.append({"id": request_id, "prompt_len": len(prompt), "resp_len": len(response or ""),
                          "latency_ms": latency_ms, "error": error, "thumb": None, "prompt_hash": zlib.crc32(prompt.encode())})
    def feedback(self, request_id, thumb):
        for r in self.rows:
            if r["id"] == request_id: r["thumb"] = thumb
    def summary(self):
        rows = list(self.rows); lat = sorted(r["latency_ms"] for r in rows)
        fb = [r["thumb"] for r in rows if r["thumb"] is not None]
        return {"n": len(rows), "error_rate": round(sum(r["error"] is not None for r in rows) / len(rows), 3),
                "p50_ms": lat[len(lat) // 2], "p95_ms": lat[int(0.95 * (len(lat) - 1))],
                "mean_resp_len": round(st.mean(r["resp_len"] for r in rows), 1),
                "feedback_n": len(fb), "thumbs_up_rate": round(sum(fb) / len(fb), 3) if fb else None}

def stub_model(prompt, rng):                       # stands in for a real provider call (NOT executed here)
    if rng.random() < 0.10: raise TimeoutError("stub timeout")
    return "ok " * rng.randint(3, 30)

rng = random.Random(42); lg = CallLogger(window=50)
for i in range(80):
    p = "question %d " % i + "x" * rng.randint(0, 100)
    t0 = time.perf_counter()
    try: out, err = stub_model(p, rng), None
    except TimeoutError as e: out, err = None, str(e)
    lat = rng.randint(80, 400) if i < 60 else rng.randint(300, 900)   # simulated latency; late slowdown
    lg.log(i, p, out, lat, err)
    if i % 3 == 0 and err is None: lg.feedback(i, rng.random() < 0.7)
    if i in (49, 79): print(f"after {i+1} calls:", json.dumps(lg.summary()))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs).
```text
after 50 calls: {"n": 50, "error_rate": 0.06, "p50_ms": 266, "p95_ms": 390, "mean_resp_len": 46.1, "feedback_n": 16, "thumbs_up_rate": 0.562}
after 80 calls: {"n": 50, "error_rate": 0.08, "p50_ms": 362, "p95_ms": 853, "mean_resp_len": 46.0, "feedback_n": 16, "thumbs_up_rate": 0.812}
```

**Follow-ups:**
- *Is the thumbs-up rate a quality metric?* A weak one; use it as a trend, and sample for human review.
- *What do you log about the prompt?* Length, hash, category; raw text only under a masking and retention policy.

**Common mistakes:** logging full prompts with personal data; treating latency as quality; reusing a classification-accuracy dashboard for generation; claiming a stub run proves anything about a real provider.

### Q43 ⭐ 🔴 Design question: the monitoring system for a card-fraud model with chargeback labels that arrive 30 to 90 days late, millions of events per day, and a regulated Indian bank or a global payments company. Cover logging, data-quality gates, feature and score drift, delayed-label performance with matured cohorts, analyst feedback labels, alert tiers, retraining policy, shadow challenger, fairness checks, privacy and on-call. Give a one-page whiteboard answer, a monitoring-spec YAML validated with pyyaml, and state which parts are concept only. Part 12 owns system design in depth.
**Asked at:** MLOps interview question banks and guides (K21Academy '47 MLOps interview questions' PDF, Towards AI '101 ML LLM agentic AIOps interview questions', DataCamp MLOps interview questions, The Interview Guys MLOps post, wecreateproblems.com, hyring.com, dev.to vivekk101, a Medium skphd post; search snippets only, not opened; the Devinterview-io/mlops-interview-questions GitHub page WAS opened and has no dedicated monitoring or drift question, only monitoring bullets inside Q1, Q2, Q4, Q6, Q7 and Q12); editorial question lists, not verified candidate reports; MLOps, ML platform and ML engineer roles at IT-services firms, product companies and GCCs | Scenario question write-ups (a Glassdoor EPAM Systems interview page whose snippet lists 'why does production differ from training' with feature, preprocessing and version mismatch as causes, and an end-to-end design prompt; one candidate's review, search snippet only, not opened, unverified; The Interview Guys post saying drift is asked in almost every MLOps interview, snippet only); anecdotal, not company-verified reports; MLOps and ML engineer roles | Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Log every scored event with a feature snapshot, gate the data first, watch feature and score drift in real time as early warnings, measure true performance only on matured cohorts once chargebacks arrive, and use tiered alerts so only data-quality or score-collapse issues page someone.

**Then explain (whiteboard in order):**
- **Logging:** event id, timestamp, model version, feature snapshot reference, score, decision; tokenised card data; sampled raw rows plus all flagged.
- **Data-quality gates:** null rate, schema, freshness, volume vs same weekday. A failed gate pages the data owner and blocks drift alerts (no point testing garbage).
- **Drift:** daily feature drift with calibrated thresholds (Q38), hourly score drift plus a score-band pile-up check (Q44). These are early warnings, not proof of damage.
- **Delayed labels:** chargebacks arrive 30 to 90 days late. Compute recall and precision on matured cohorts (events old enough that most labels exist), and mark the share of labels received. Early proxies: analyst feedback labels, alert rate, score-based estimates.
- **Alert tiers:** page (gate failed, score collapse), ticket (persistent drift, matured-cohort drop), info (one-day feature drift).
- **Retraining:** hybrid (monthly schedule plus a trigger confirmed by labels); offline backtest, shadow challenger, approval; rollback to the previous version.
- **Fairness and privacy:** false-positive-rate gaps across segments monthly; minimise stored PII; access-controlled logs.
- **On-call:** a runbook per page; the model owner is on a rota; false-alert reviews monthly.
- **Concept only (not run):** fairness checks, shadow challenger, analyst labels, on-call routing. Run here: the YAML validation and the matured-cohort simulation.

**Example:** in the simulation real recall drops from 0.80 to 0.60 at day 120. By day 199, the day-110 cohort is 98 percent labelled and shows 0.80; day 130 is 68 percent labelled and shows 0.57; day 150 is only 32 percent labelled. The drop is visible only as old cohorts mature, which is why the proxies and drift stay as early warnings.

**Code:** (YAML spec with placeholders; validation and cohort simulation, seeded)
```yaml
# Illustrative monitoring spec for a card-fraud model (concept; thresholds are placeholders to calibrate, see Q38)
model: {id: card_fraud_v7, serving: real_time, volume: millions_per_day}
logging:
  fields: [event_id, ts, model_version, feature_snapshot_ref, score, decision]
  pii: {card_number: tokenised, raw_text: not_logged}
  sampling: {features: full_for_aggregates, raw_rows: one_percent_plus_all_flagged}
data_quality_gates:       # run before drift; a failed gate pages the data owner, not the model owner
  - {check: null_rate, max: 0.02}
  - {check: schema_match, required: true}
  - {check: freshness_minutes, max: 15}
  - {check: volume_vs_same_weekday, min_ratio: 0.7, max_ratio: 1.4}
drift:
  features: {test: psi_calibrated, window: daily, per_feature_alpha: bonferroni}
  score: {test: ks_and_band_pileup, window: hourly}
performance:
  label_source: chargeback
  label_delay_days: {min: 30, max: 90}
  matured_cohort_days: 90
  early_proxy: [analyst_feedback_labels, alert_rate, estimated_precision_from_scores]
  metric: [recall_at_fixed_review_capacity, precision_at_threshold]
fairness:
  segments: [region, card_type, customer_age_band]
  check: false_positive_rate_gap
  cadence: monthly
alert_tiers:
  - {tier: page, when: [data_quality_gate_failed, score_distribution_collapse], route: oncall}
  - {tier: ticket, when: [feature_drift_persistent_3_days, matured_cohort_metric_drop], route: ml_team}
  - {tier: info, when: [single_day_feature_drift], route: dashboard}
retraining:
  policy: hybrid
  schedule: monthly
  triggers: [matured_cohort_metric_drop, persistent_drift_with_label_confirmation]
  gate: [offline_backtest, shadow_challenger_14_days, approver_sign_off]
  rollback: previous_registered_version
shadow_challenger: {enabled: true, compare: [score_correlation, flagged_overlap, matured_metrics]}
concept_only: [fairness, shadow_challenger, analyst_feedback_labels, oncall_routing]
```
```py
# --- q43_validate.py ---
import yaml, sys
s = yaml.safe_load(open(sys.argv[1]))
for k in ["logging", "data_quality_gates", "drift", "performance", "fairness", "alert_tiers", "retraining", "shadow_challenger"]:
    assert k in s, k
assert s["performance"]["matured_cohort_days"] >= s["performance"]["label_delay_days"]["max"]
assert {t["tier"] for t in s["alert_tiers"]} == {"page", "ticket", "info"}
assert s["retraining"]["rollback"] and "shadow_challenger_14_days" in s["retraining"]["gate"]
print("spec OK:", len(s["data_quality_gates"]), "gates,", len(s["alert_tiers"]), "alert tiers, matured cohort", s["performance"]["matured_cohort_days"], "days")

# --- q43_cohort.py ---
import numpy as np
# Matured-cohort recall: labels arrive 30-90 days after the event, so today's cohort is unlabelled.
rng = np.random.default_rng(43)
days, per = 200, 20000
rec = []
for d in range(days):
    fraud = rng.random(per) < 0.01
    caught = fraud & (rng.random(per) < (0.80 if d < 120 else 0.60))   # real recall drops from day 120
    delay = rng.integers(30, 91, per)
    rec += [(d, f, c, dl) for f, c, dl in zip(fraud, caught, delay)]
d_, f_, c_, dl_ = map(np.array, zip(*rec))
today = 199
def recall_cohort(day):  # what we know today about the cohort of that day
    m = (d_ == day) & f_ & (day + dl_ <= today)
    return (c_[m].sum() / max(m.sum(), 1)), int(m.sum())
for day in (60, 110, 130, 150):
    r, n = recall_cohort(day)
    known = ((d_ == day) & f_ & (day + dl_ <= today)).sum() / max(((d_ == day) & f_).sum(), 1)
    print(f"cohort day {day}: share of its fraud labelled by day {today}: {known:.2f}  recall on labelled part: {("%.2f" % r) if n else "n/a"} (n={n})")
```

**Output (my run):** PyYAML 6.0.3 for validation, numpy 2.5.4 for the simulation. Kafka, a feature store, the bank's alerting stack and on-call tooling: not executed. The simulation assumes label delay is independent of whether the fraud was caught.
`validation`
```text
spec OK: 4 gates, 3 alert tiers, matured cohort 90 days
```
`matured cohorts`
```text
cohort day 60: share of its fraud labelled by day 199: 1.00  recall on labelled part: 0.78 (n=226)
cohort day 110: share of its fraud labelled by day 199: 0.98  recall on labelled part: 0.80 (n=200)
cohort day 130: share of its fraud labelled by day 199: 0.68  recall on labelled part: 0.57 (n=126)
cohort day 150: share of its fraud labelled by day 199: 0.32  recall on labelled part: 0.65 (n=66)
```

**Follow-ups:**
- *Why not wait for chargebacks?* You would learn about a bad model 3 months late; hence drift and proxies as early warning.
- *Bias in analyst labels?* Analysts only review flagged cases, so labels are biased toward what the model already flags; keep a random review sample.
- *Millions of events?* Profiles and sketches (Q39), tiered features.

**Common mistakes:** computing recall on the latest week (labels missing); paging on any drift; one retraining trigger with no validation gate; forgetting that blocked transactions get no chargeback label.

### Q44 ⭐ 🔴 Adversarial and non-stationary inputs: gaming and fraud adaptation, a model whose decisions change user behaviour (performative drift), and bot or test traffic polluting the monitor. Explain how monitoring must separate organic drift from adaptation, filter synthetic or internal traffic, and why a rising score for a blocked segment may be the model working. Simulate an adaptive attacker moving features just below a threshold, show feature drift and the score-band pile-up, and write the detector for the pile-up.
**Asked at:** Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** Adversaries and the model itself change the data, so I separate organic drift from adaptation: watch the score bands just below the decision threshold for a pile-up, filter internal and test traffic before drift tests, and read a rising score in a blocked segment as possibly the model working.

**Then explain:**
- **Adaptive attackers:** they probe, then tune inputs to land just under a threshold. Marginal feature drift is mild; the signature is a pile-up in the band below the line.
- **Performative drift:** decisions change behaviour (a declined user retries with different details), so the data you see after launch depends on the model. The old reference stops being "normal".
- **Bot, test and internal traffic:** synthetic or QA traffic can make drift tests fire or mask real shifts; tag it (header, IP list, test account) and filter it before computing drift.
- **Blocked segment:** if the blocked group's average score rises, that may be the model correctly catching more; do not "fix" it.
- **Detector:** compare mass just below the threshold with the reference band and with the band just above it; alert when the ratio is high and the count is large enough.
- **Failure modes:** label feedback is biased (you only see outcomes for approved cases); a retrain on attacker-shaped data teaches the model the attacker's pattern; threshold is public knowledge in some systems.

**Example:** threshold 0.80; 15 percent of week-8 traffic is an attacker with feature value 1.25 to 1.50 (score about 0.65 to 0.76). Feature KS D 0.134. The block rate falls from 6.05 to 5.24 percent. The band 0.70 to 0.80 holds 3.26 percent of traffic at week 0 and 12.2 percent at week 8 (ratio 3.74, 4.79 times the band above); the control run shows ratio 0.93 and no alert.

**Code:** (seeded, numpy and scipy; `python3 -I`)
```py
import numpy as np
from scipy.stats import ks_2samp
rng = np.random.default_rng(44)
n = 20000
THRESH = 0.80                                    # model blocks at score >= 0.80
def score(x): return 1 / (1 + np.exp(-(x - 1.0) * 2.5))   # monotone score from a risk feature
organic = rng.normal(0, 1, n)                     # week 0 traffic
score0 = score(organic)
# week 8: 15% of traffic is an adaptive attacker who tunes the feature to land just under the block line
atk = int(0.15 * n)
x_cur = rng.normal(0, 1, n)
x_cur[:atk] = rng.uniform(1.25, 1.50, atk)       # score about 0.65 to 0.76 (just below 0.80) , i.e. x < ~1.55
score1 = score(x_cur)
print("block threshold on score: %.2f (feature x=%.2f)" % (THRESH, 1 + np.log(THRESH/(1-THRESH))/2.5))
print("feature KS D=%.3f  score KS D=%.3f  block rate %.4f -> %.4f" % (
    ks_2samp(organic, x_cur).statistic, ks_2samp(score0, score1).statistic, (score0 >= THRESH).mean(), (score1 >= THRESH).mean()))

def pileup_detector(ref_scores, cur_scores, thr, width=0.10, min_ratio=2.0, min_count=30):
    """Compare the mass in the band just BELOW the threshold with the mass in the same band at reference, and with the band just ABOVE."""
    lo, hi = thr - width, thr
    ref_b = np.mean((ref_scores >= lo) & (ref_scores < hi)); cur_b = np.mean((cur_scores >= lo) & (cur_scores < hi))
    above = np.mean((cur_scores >= thr) & (cur_scores < thr + width))
    cnt = int(np.sum((cur_scores >= lo) & (cur_scores < hi)))
    return {"below_band_ref": round(float(ref_b), 4), "below_band_cur": round(float(cur_b), 4),
            "band_ratio": round(float(cur_b / ref_b), 2), "below_over_above": round(float(cur_b / max(above, 1e-9)), 2),
            "alert": bool(cnt >= min_count and cur_b / ref_b >= min_ratio)}
print("week 8 vs week 0:", pileup_detector(score0, score1, THRESH))
print("control (no attacker):", pileup_detector(score0, score(rng.normal(0, 1, n)), THRESH))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs). The traffic filter was not simulated; it is a rule applied before the test.
```text
block threshold on score: 0.80 (feature x=1.55)
feature KS D=0.134  score KS D=0.134  block rate 0.0605 -> 0.0524
week 8 vs week 0: {'below_band_ref': 0.0326, 'below_band_cur': 0.122, 'band_ratio': 3.74, 'below_over_above': 4.79, 'alert': True}
control (no attacker): {'below_band_ref': 0.0326, 'below_band_cur': 0.0304, 'band_ratio': 0.93, 'below_over_above': 1.03, 'alert': False}
```

**Follow-ups:**
- *Do you tell the model team or the fraud ops?* Both: the model team for threshold or feature changes, ops for the attacker segment.
- *Randomise the threshold?* A defensive idea (check your risk team); it makes probing harder.

**Common mistakes:** retraining on traffic that includes the attacker's tuned samples without review; including QA traffic in the baseline; treating every score rise as a model failure.

### Q45 ⭐ 🔴 Testing the monitors themselves. How do you know your drift and data-quality checks work before an incident: inject known faults (null spike, unit change, shifted mean, dropped partition) into a clean batch, assert the right monitor fires and the others stay quiet, measure detection rate and false-alarm rate over many seeds, and replay logged history through new monitor versions (backfill) before enabling alerts. Write pytest cases for a small monitor suite with a fault-injection helper, run them, and report the detection matrix. Part 1 owns pytest basics.
**Asked at:** Expert extension: no source found for the exact question; the topic follows from the library behaviour tested in this sandbox and from general monitoring practice, and Wave B must verify against current docs; MLOps, ML platform and ML engineer roles, including IT-services firms, product companies and GCCs
**Say this first (1 line):** I test monitors like code: inject known faults into a clean batch, assert that the right monitor fires and the others stay quiet, measure detection and false-alarm rate over many seeds, and replay logged history through a new monitor version before enabling its alerts.

**Then explain:**
- **Fault injection helper:** one function per fault (null spike, unit change, mean shift, dropped partition) applied to a clean batch.
- **Detection matrix:** rows are faults, columns are monitors, cells are the fraction of seeds where it fired. You want a clean diagonal-like pattern and an all-zero "no fault" row.
- **Many seeds:** one lucky seed proves nothing; 30 to 200 seeds give a rate. Assert rates (at least 95 percent detect, at most 5 percent false alarm).
- **Backfill replay:** run the new monitor over past logged days, count alerts, compare with known incidents, then enable paging (concept here; the logic is the same function in a loop).
- **What the first run taught me:** the volume monitor (min ratio 0.7) missed a dropped region because 1 of 4 regions is only 25 percent of rows (75 percent remain). My first test failed (0 of 30 detections). I added a category-presence monitor and left a test that documents the volume monitor's limit.
- **Failure modes:** tests with fixed seeds that hide flakiness; thresholds tuned until the tests pass; asserting only "something fired".

**Example:** the matrix below. `none` row all 0.00 (no false alarms in 200 seeds). Unit change fires `drift` and `range`; mean shift only `drift`; null spike only `null`; dropped partition only `category`.

**Code:** (three files in `code/q45/`: monitors, tests, matrix script; pytest basics are Part 1)
```py
# --- q45/monitors.py ---
import numpy as np, pandas as pd
from scipy.stats import ks_2samp

# each monitor returns True when it fires
def null_monitor(ref, cur, col="amount", max_rate=0.02):
    return cur[col].isna().mean() > max_rate
def drift_monitor(ref, cur, col="amount", alpha=0.001, min_d=0.1):
    d = ks_2samp(ref[col].dropna(), cur[col].dropna())
    return d.pvalue < alpha and d.statistic > min_d          # significant AND big enough
def range_monitor(ref, cur, col="amount", factor=3.0):
    return cur[col].max() > factor * ref[col].max()          # catches unit changes
def volume_monitor(ref, cur, min_ratio=0.7):
    return len(cur) < min_ratio * len(ref)                   # catches dropped partitions
def category_monitor(ref, cur, col="region"):
    return bool(set(ref[col].unique()) - set(cur[col].unique()))   # a known value vanished
MONITORS = {"null": null_monitor, "drift": drift_monitor, "range": range_monitor, "volume": volume_monitor, "category": category_monitor}

# fault injection
def clean_batch(rng, n=5000):
    return pd.DataFrame({"amount": rng.lognormal(3.0, 0.5, n), "region": rng.choice(list("NSEW"), n)})
def inject(df, fault, rng):
    df = df.copy()
    if fault == "null_spike": df.loc[rng.random(len(df)) < 0.10, "amount"] = np.nan
    elif fault == "unit_change": df["amount"] = df["amount"] * 100       # rupees to paise
    elif fault == "mean_shift": df["amount"] = df["amount"] * 1.25
    elif fault == "dropped_partition": df = df[df["region"] != "W"].reset_index(drop=True)
    elif fault != "none": raise ValueError(fault)
    return df

# --- q45/test_monitors.py ---
import numpy as np, pytest
from monitors import MONITORS, clean_batch, inject

# expected: which monitors MUST fire for each fault (the rest are not asserted here; the matrix script reports them)
MUST = {"null_spike": {"null"}, "unit_change": {"drift", "range"}, "mean_shift": {"drift"}, "dropped_partition": {"category"}}
SEEDS = range(30)

@pytest.mark.parametrize("fault", list(MUST))
def test_fault_detected(fault):
    hits = {m: 0 for m in MONITORS}
    for s in SEEDS:
        rng = np.random.default_rng(1000 + s)
        ref, cur = clean_batch(rng), inject(clean_batch(rng), fault, rng)
        for m, f in MONITORS.items(): hits[m] += bool(f(ref, cur))
    for m in MUST[fault]:
        assert hits[m] / len(SEEDS) >= 0.95, (fault, m, hits)

def test_clean_batches_are_quiet():
    fa = {m: 0 for m in MONITORS}
    for s in SEEDS:
        rng = np.random.default_rng(2000 + s)
        ref, cur = clean_batch(rng), clean_batch(rng)
        for m, f in MONITORS.items(): fa[m] += bool(f(ref, cur))
    assert all(v / len(SEEDS) <= 0.05 for v in fa.values()), fa

def test_null_spike_does_not_trigger_volume():
    rng = np.random.default_rng(7)
    ref, cur = clean_batch(rng), inject(clean_batch(rng), "null_spike", rng)
    assert not MONITORS["volume"](ref, cur)

def test_volume_monitor_misses_a_one_in_four_drop():
    """Documented limit found by the first run: dropping 1 of 4 regions leaves 75 percent of rows, above the 0.7 floor."""
    rng = np.random.default_rng(9)
    ref, cur = clean_batch(rng), inject(clean_batch(rng), "dropped_partition", rng)
    assert not MONITORS["volume"](ref, cur)
    assert MONITORS["category"](ref, cur)

# --- q45/matrix.py ---
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from monitors import MONITORS, clean_batch, inject
faults = ["none", "null_spike", "unit_change", "mean_shift", "dropped_partition"]
print(f"{'fault':18s}" + "".join(f"{m:>9s}" for m in MONITORS) + "   (fraction of 200 seeds where the monitor fired)")
for fault in faults:
    row = {m: 0 for m in MONITORS}
    for s in range(200):
        rng = np.random.default_rng(s)
        ref, cur = clean_batch(rng), inject(clean_batch(rng), fault, rng)
        for m, f in MONITORS.items(): row[m] += bool(f(ref, cur))
    print(f"{fault:18s}" + "".join(f"{row[m]/200:9.2f}" for m in MONITORS))
```

**Output (my run):** Python 3.13, numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, scikit-learn 1.9.1, pytest 9.1.1, PyYAML 6.0.3 (sandbox; numbers are from these seeded runs). First pytest run (before adding the category monitor):
```text
E            +  where 30 = len(range(0, 30))

/home/user/case_studies/interviews/scratch/B4P08_Q35-45/code/q45/test_monitors.py:16: AssertionError
=========================== short test summary info ============================
FAILED test_monitors.py::test_fault_detected[dropped_partition] - AssertionEr...
1 failed, 5 passed in 1.86s
```After the fix:
`pytest`
```text
.......                                                                  [100%]
7 passed in 1.91s
```
`matrix.py`
```text
fault                  null    drift    range   volume category   (fraction of 200 seeds where the monitor fired)
none                   0.00     0.00     0.00     0.00     0.00
null_spike             1.00     0.00     0.00     0.00     0.00
unit_change            0.00     1.00     1.00     0.00     0.00
mean_shift             0.00     1.00     0.00     0.00     0.00
dropped_partition      0.00     0.00     0.00     0.00     1.00
```

**Follow-ups:**
- *How do you avoid tuning to the tests?* Keep a held-out set of historic incidents and faults the thresholds never saw.
- *Which fault is the hardest?* Slow, small shifts; test with graded fault sizes and read power, not one size.

**Common mistakes:** testing only the happy path; asserting on one seed; no "no fault" row; enabling a new monitor's pager without a backfill replay.
