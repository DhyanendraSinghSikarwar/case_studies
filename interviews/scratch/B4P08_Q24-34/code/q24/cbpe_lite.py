import numpy as np

def expected_metrics(scores, threshold=0.5):
    """Expected accuracy/precision/recall from calibrated P(y=1) scores. No labels used."""
    s = np.asarray(scores, dtype=float)
    pred = s >= threshold
    tp = s[pred].sum()            # expected true positives
    fp = (1 - s[pred]).sum()      # expected false positives
    fn = s[~pred].sum()           # expected false negatives
    tn = (1 - s[~pred]).sum()
    n = len(s)
    return {"acc": (tp + tn) / n,
            "precision": tp / (tp + fp) if tp + fp else float("nan"),
            "recall": tp / (tp + fn) if tp + fn else float("nan")}

def true_metrics(scores, y, threshold=0.5):
    pred = np.asarray(scores) >= threshold
    y = np.asarray(y)
    return {"acc": (pred == y).mean(),
            "precision": y[pred].mean(),
            "recall": pred[y == 1].mean()}

rng = np.random.default_rng(24)
N = 200_000

def world(name, scores, p_true):
    y = (rng.random(len(scores)) < p_true).astype(int)
    e, t = expected_metrics(scores), true_metrics(scores, y)
    print(f"{name:34s} est acc {e['acc']:.3f} true acc {t['acc']:.3f} | est prec {e['precision']:.3f} true prec {t['precision']:.3f}")

# A: reference world. Scores are calibrated: P(y=1 | score) = score.
s_ref = rng.beta(2, 3, N)
world("A calibrated, reference", s_ref, s_ref)
# B: covariate shift. Input mix changes, scores move up, but P(y|x) is unchanged, so calibration still holds.
s_cov = rng.beta(3, 2, N)
world("B covariate shift, calibration holds", s_cov, s_cov)
# C: concept drift. Same inputs and scores, but the real link between score and outcome weakens.
p_c = 0.5 + 0.4 * (s_ref - 0.5)
world("C concept drift (link weakened)", s_ref, p_c)
# D: miscalibrated from day one: model overconfident (true P is pulled toward 0.5).
world("D overconfident model", s_ref, 0.5 + 0.6 * (s_ref - 0.5))
