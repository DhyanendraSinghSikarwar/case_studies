### Q14 ⭐⭐⭐ 🟡 How do you evaluate an agent: outcome vs trajectory, success rate, steps and cost, LLM judges, and where do you start?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
**Say this first (1 line):** I judge an agent on two layers: did it reach the right end state (outcome), and how it got there (trajectory: steps, tool choices, cost, latency). I start with a small hand-built set, add an LLM judge with a rubric, and keep humans in the loop for what automation misses.

**Then explain:**
- **Outcome (end-state) evaluation:** check the final result or the changed state. For an agent that edits a database or files, compare the end state with the expected one instead of demanding one exact path. Anthropic's multi-agent write-up reports using end-state evaluation for agents that change persistent state (reported by the vendor).
- **Trajectory evaluation:** steps taken, tool calls per task, redundant or wrong calls, loops, cost (tokens or dollars) and latency. Two agents with the same success rate can differ 2x in cost. Report **cost per successful task**, not per attempt.
- **Success rate needs an interval.** With 20 to 60 tasks the noise is large (see the run: overlapping intervals mean you cannot call a winner). Use a bootstrap or a paired comparison on the same tasks.
- **LLM judge:** Anthropic reports a rubric of factual accuracy, citation accuracy, completeness, source quality and tool efficiency, scored 0.0 to 1.0 with a pass/fail (vendor-reported). Calibrate the judge against human labels before you trust it. Depth in Part 9.
- **Where to start:** Anthropic reports starting with about 20 queries; that is enough to see big effects early (reported). Add failures from production as new test cases. Human testers catch what automation misses, for example odd source choices or subtle bias toward low-quality pages (reported by Anthropic).
- Tool-call level checks (right tool, right arguments) are in Part 3 Q44; here the unit is the whole run.

**Example:** support agent, 60 test tickets. Agent A resolves 80%, agent B 85%. B takes 7.4 steps on average vs 4.5 and costs about 55% more per success. The confidence intervals overlap, so "B is better" is not proven, but "B is costlier" is. Ship A, keep investigating B's wasted calls.

**Code:** (run with `python3 -I`; the trajectories are SYNTHETIC, generated with assumed success rates and waste; it shows the metrics and the bootstrap, not a real agent)
```python
# Agent evaluation harness on SYNTHETIC trajectories (no real agent). Outcome vs trajectory metrics + bootstrap CI.
import random, statistics
random.seed(7)
def make_traj(agent):
    """Synthetic trajectory generator. Agent B is built to succeed more but waste more calls (assumption)."""
    p_ok, extra = (0.70, 0.5) if agent == "A" else (0.85, 3.0)
    ok = random.random() < p_ok
    needed = random.randint(3, 6)
    wasted = int(random.expovariate(1 / extra)) if extra else 0
    return {"success": ok, "steps": needed + wasted, "needed": needed,
            "tokens": (needed + wasted) * 900, "latency_s": (needed + wasted) * 2.1}
def tool_efficiency(t): return t["needed"] / t["steps"]          # 1.0 = no wasted calls
def boot_ci(xs, stat=statistics.mean, n=2000, alpha=0.05):
    rng = random.Random(1); vals = sorted(stat([rng.choice(xs) for _ in xs]) for _ in range(n))
    return vals[int(n * alpha / 2)], vals[int(n * (1 - alpha / 2)) - 1]
for agent in "AB":
    ts = [make_traj(agent) for _ in range(60)]
    succ = [1.0 if t["success"] else 0.0 for t in ts]
    steps = [t["steps"] for t in ts]; eff = [tool_efficiency(t) for t in ts]
    lo, hi = boot_ci(succ)
    # cost per SUCCESS, not per attempt
    cps = sum(t["tokens"] for t in ts) / max(1, sum(succ))
    print(f"agent {agent}: success={statistics.mean(succ):.2f} CI95=({lo:.2f},{hi:.2f}) "
          f"mean_steps={statistics.mean(steps):.1f} tool_eff={statistics.mean(eff):.2f} tokens_per_success={cps:.0f}")
# paired comparison on the same 60 tasks would be better; here we just check CI overlap
```
Output (my run):
```
agent A: success=0.80 CI95=(0.68,0.90) mean_steps=4.5 tool_eff=0.97 tokens_per_success=5044
agent B: success=0.85 CI95=(0.75,0.93) mean_steps=7.4 tool_eff=0.69 tokens_per_success=7835
```

**Follow-ups:**
- *Why not only check the final answer?* It hides unsafe or wasteful paths and cannot catch a right answer reached by luck. But demanding an exact trajectory punishes valid alternative paths, so score the trajectory on properties (no loops, budget, allowed tools).
- *Can the LLM judge be trusted?* Only after you measure agreement with human labels on a sample; use it for scale, humans for calibration (Part 9).
- *Non-determinism?* Run each task several times and report the pass rate per task, not one run.

**Common mistakes:** judging only on a few demo prompts; reporting success without a confidence interval; ignoring cost and latency; one exact-path trajectory match; trusting an uncalibrated LLM judge; no human review.
