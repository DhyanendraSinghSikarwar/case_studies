"""Model billed runner-minutes per week. ALL inputs are assumptions to replace with measured values."""
import math

PRS_PER_WEEK = 50
PUSHES_PER_PR = 3          # each push starts a run

# (job name, copies in matrix, minutes per copy). Billing rounds each job up to whole minutes.
BEFORE = [("lint", 1, 3.0), ("unit", 3, 12.0), ("integration-full-data", 1, 20.0), ("docker-build", 1, 8.0)]
AFTER = [("lint", 1, 1.5), ("unit", 3, 7.0), ("integration-smoke-data", 1, 5.0), ("docker-build", 1, 4.0)]
NIGHTLY_HEAVY = [("integration-full-data", 1, 20.0)]
NIGHTS = 7

DOCS_ONLY_SHARE = 0.30     # PRs that touch no code (path filter skips the heavy jobs)
CANCELLED_SHARE = 0.40     # pushes superseded by a newer push (cancel-in-progress)
CANCELLED_COST = 0.30      # fraction of a full run a cancelled run still burns


def run_minutes(jobs):
    return sum(n * math.ceil(m) for _, n, m in jobs)


def before():
    return PRS_PER_WEEK * PUSHES_PER_PR * run_minutes(BEFORE)


def after():
    pushes = PRS_PER_WEEK * PUSHES_PER_PR
    full = pushes * (1 - CANCELLED_SHARE)
    cancelled = pushes * CANCELLED_SHARE * CANCELLED_COST
    code_share = 1 - DOCS_ONLY_SHARE
    pr_cost = (full + cancelled) * (code_share * run_minutes(AFTER) + DOCS_ONLY_SHARE * math.ceil(1.0))
    return pr_cost + NIGHTS * run_minutes(NIGHTLY_HEAVY)


if __name__ == "__main__":
    b, a = before(), after()
    print(f"before: {run_minutes(BEFORE)} billed min per run x {PRS_PER_WEEK * PUSHES_PER_PR} runs = {b:.0f} min/week")
    print(f"after : {a:.0f} min/week (PR runs + {NIGHTS} nightly full-data runs)")
    print(f"saving: {b - a:.0f} min/week = {(b - a) / b:.0%}")
    print("wall clock critical path before:", 3 + 12 + 20 + 8, "min if serial (jobs can also run in parallel)")
