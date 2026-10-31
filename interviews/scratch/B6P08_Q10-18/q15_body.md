**Say this first (1 line):** A 0.013 AUC gap on a 10,000-row holdout is about 1.2 standard errors if the holdouts differ (1,000 positives), so first measure seed and sampling noise; then recover what you can (lockfile history, image digests, warehouse snapshots), say plainly what is unrecoverable, and record everything from now on.

**Clarifying questions:**
- How many positives are in the holdout, and is it the same 10,000 rows in March and September? Standard error depends on positives (1,000 here, a 10% rate), and the same rows allow a paired comparison.
- Does the auditor need the exact model or evidence the process was controlled? These are different deliverables.
- Is there any snapshot: warehouse time travel, backups, exported training files, or a feature log? It decides what is recoverable.
- Do we still have the container image, CI logs, or a `pip freeze` somewhere? Library versions can often be rebuilt from those.
- Which model version is in production, and which one was approved? A reproduction effort for an unused model is lower priority.

**Approach:**
1. Estimate noise. Hanley-McNeil standard error of one AUC at 0.842 with 1,000 positives and 9,000 negatives is about 0.008; for a gap between two independent holdouts the standard error is about 0.011, so 0.013 is about 1.2 standard errors: not strong evidence of any real change. A bootstrap on simulated scores gave a similar scale (0.006 for one AUC). With the same rows and paired scores the noise would be smaller.
2. Measure seed noise: retrain the current code 20 or more times with different seeds on a frozen snapshot and look at the spread. For a stable linear model it is tiny (0.0003 in my run); for deep or boosted models it can be larger. Report the range.
3. Find what changed: diff the lockfile or `pip freeze` history in git, base image digests, CI logs, and the data (row counts, label rates, null rates by month). Run the old code with the oldest plausible library versions in a clean environment.
4. Classify honestly: recoverable (code commit, many library versions, data if the warehouse retains history); partly recoverable (library versions inferred); unrecoverable (in-place table state, unlogged seeds). Do not claim exact reproduction. Offer the auditor: an approximately equivalent model, a confidence interval for its metrics, and the evidence of the gap analysis.
5. Rollback and escalation: if the September model is already serving and its metrics on a frozen shared holdout are within noise of March, no rollback; if they are below the noise band, escalate to the model owner and compliance before the audit response.
6. First 15 minutes of the request: do not retrain over anything; preserve the current table state (copy or snapshot) and logs. First day: snapshot, freeze versions, run the noise study. Next quarter: immutable data snapshots, lockfiles and image digests per run, seed logging, and a run record.
7. Blameless angle: no process required this; the gap is in the platform, not in whoever ran the retrain. Action items: run record, data versioning, and a reproducibility test that retrains monthly and alarms if the metric moves by more than the noise band.

**Metrics:**
- AUC with a confidence interval (Hanley-McNeil or bootstrap), not a point value.
- Seed spread = standard deviation of AUC across seeds on a frozen snapshot.
- Reproducibility gap = metric of the reproduction minus the reference, compared to the noise band.
- Record completeness = share of runs with data id, code commit, lockfile, seed and environment logged.

**Risks:**
- A significant-looking difference between two retrains can be noise; the opposite risk is dismissing a real shift when the data changed.
- In-place refresh may have changed labels or dropped rows; the AUC gap could be a real population change.
- Claiming reproduction without proof is an audit failure.
- Unpinned libraries can change defaults (editor knowledge: a default solver, a tie-breaking rule).

**What the interviewer scores:**
- Strong: quantifies noise with a standard error and a seed study before explaining the gap.
- Strong: separates recoverable from unrecoverable and tells the auditor the truth.
- Strong: concrete record list and a test that would catch the problem.
- Weak: "set the seed and rerun" or "the model degraded"; claiming exact reproduction.

**Example:** Illustrative: AUC 0.842 in March, 0.829 in September, gap 0.013, 1,000 positives. Weak versus strong:
- Weak: "The September model is worse; I will retrain with a fixed seed to get March back."
- Strong: "With 1,000 positives the standard error of the gap is about 0.011, so this is about 1.2 standard errors. I would rerun with 20 seeds on a frozen snapshot to see the seed spread, rebuild the old library versions from CI logs, and tell the auditor which parts I can reproduce and which, like the in-place table and the unlogged seeds, I cannot. From now on each run stores a data snapshot id, lockfile, image digest and seed."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Is the gap real? Not provable from these two numbers; test on one shared frozen holdout with a paired bootstrap (see Book 4 Part 1, Q5, "How do you make a trained model reproducible six months later?", for the record list).
- What should the record contain? Data snapshot id or hash, code commit, lockfile and image digest, seeds, hardware, metrics with intervals, and the holdout id.
- Can you get exact reproducibility? Only with fixed data, versions, seeds and deterministic settings; some GPU operations are non-deterministic unless configured (editor knowledge, check your framework).

**Common mistakes:**
- Reading a 0.013 difference as real or as noise without computing the error.
- Updating a table in place without a snapshot.
- Logging seeds but not data or library versions.
- Telling an auditor "reproduced" when it was "similar".
