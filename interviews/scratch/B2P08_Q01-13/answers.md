### Q1 ⭐⭐⭐ 🟢 What is an AI agent? Distinguish an agent from a chatbot and from a fixed workflow, describe the agent loop, and say when you should not use an agent.
**Asked at:** all types; agentic-AI and GenAI-engineer loops
**Say this first (1 line):** An agent is an LLM that decides its own next step in a loop, calls tools, sees the results and keeps going until it reaches an objective; a workflow is the same pieces wired by fixed code, and a chatbot just replies.

**Then explain:**
- **Anthropic's split:** workflows are systems where LLMs and tools are orchestrated through predefined code paths; agents are systems where LLMs dynamically direct their own process and tool usage. Both are "agentic systems".
- **Agent vs chatbot:** an agent has tools, state and an objective (the Educative framing). The real differences are autonomy (it chooses the steps) and side effects (it can change the world: send mail, write files, issue refunds). A chatbot only produces text.
- **The loop:** perceive (read the goal, state and last observation), decide (pick an action or finish), act (the host code runs the tool, not the model), observe (append the result), repeat until a stop condition (see Q4).
- **When NOT to use an agent:** simple lookups, tight latency budgets, high-stakes actions with no ground truth to check each step, or when a fixed path already solves the task. Agents cost more LLM calls, and errors compound across steps.
- **Start simple:** Anthropic's advice is to begin with the simplest solution, often one LLM call with retrieval and a few examples, and add complexity only when it measurably helps.

**Example:** "Total of the cheapest laptop and a mouse." A workflow always does extract items, look up prices, compose: 2 LLM calls, predictable. An agent decides one lookup at a time, so it spends one more call to decide it is done. For this fixed task the workflow wins; the agent only pays off when the number or order of steps cannot be known in advance (for example "debug why this test fails").

**Code:** (mock LLM, scripted; counts calls only, no real model output)
```python
# MOCK demo: fixed workflow vs agent loop on a toy task. No real LLM is used.
# Task: "What is the total price of the cheapest laptop and a mouse?"
CATALOG = {"laptop": [("A", 900), ("B", 750)], "mouse": [("M", 20)]}
calls = {"n": 0}

def mock_llm(role, payload):
    """Scripted stand-in for a model. Each call counts as one LLM call."""
    calls["n"] += 1
    if role == "extract":                      # workflow step 1: pull item names
        return ["laptop", "mouse"]
    if role == "compose":                      # workflow step 3: write the answer
        return f"Total = {sum(payload)}"
    if role == "agent_decide":                 # agent: choose next action from history
        history = payload
        looked = [h for h in history if h[0] == "lookup"]
        if len(looked) < 2:
            return ("lookup", ["laptop", "mouse"][len(looked)])
        return ("final", f"Total = {sum(h[2] for h in looked)}")

def tool_cheapest(item):
    return min(p for _, p in CATALOG[item])

def workflow(question):                        # predefined code path: always 2 LLM calls
    items = mock_llm("extract", question)
    prices = [tool_cheapest(i) for i in items]
    return mock_llm("compose", prices)

def agent(question, max_steps=6):              # LLM picks the next step each loop
    history = []
    for _ in range(max_steps):
        action = mock_llm("agent_decide", history)
        if action[0] == "final":
            return action[1]
        history.append(("lookup", action[1], tool_cheapest(action[1])))
    return "STOPPED: max steps"

for name, fn in [("workflow", workflow), ("agent", agent)]:
    calls["n"] = 0
    print(name, "->", fn("cheapest laptop + mouse?"), "| LLM calls:", calls["n"])
```
Output (real run):
```
workflow -> Total = 770 | LLM calls: 2
agent -> Total = 770 | LLM calls: 3
```

**Follow-ups:**
- *Is a RAG pipeline an agent?* Classic RAG is a workflow (retrieve then generate). It becomes agentic when the model decides whether, what and how often to retrieve (Part 7 Q13).
- *How do you get from workflow to agent safely?* Add one degree of freedom at a time, keep step budgets, and test in a sandbox (Q4, Q14).
- *Do I need a framework?* Anthropic notes frameworks can obscure prompts and responses; start with direct API calls.

**Common mistakes:** calling any LLM app with a tool "an agent"; reaching for an agent when a workflow suffices; forgetting side effects and budgets; describing the loop without saying who executes the tool (the host does).

### Q2 ⭐⭐⭐ 🟢 What is ReAct, and why does interleaving reasoning with actions beat reasoning-only or acting-only? Go beyond the prompt format.
**Asked at:** all types; agentic-AI and GenAI-engineer loops
**Say this first (1 line):** ReAct (Yao et al., arXiv 2210.03629) has the model interleave reasoning traces with actions, so thoughts plan and revise while actions fetch real information that feeds the next thought.

**Then explain:**
- **From the abstract:** reasoning helps the model create, track and update plans and handle exceptions; actions let it gather information from external sources. Tested on HotpotQA and FEVER (with a simple Wikipedia API) and on ALFWorld and WebShop.
- **Reported results (authors' claims, one or two in-context examples):** ReAct overcomes hallucination and error propagation seen in chain-of-thought, and beats imitation and RL methods by absolute success rates of 34% on ALFWorld and 10% on WebShop. These are the authors' numbers in their setting, not a guarantee for your task.
- **Why not reason-only:** facts come from the model's memory, so they can be stale or invented, and a wrong early step propagates. Nothing grounds it.
- **Why not act-only:** actions with no thought have no plan and no exception handling; the agent repeats a failing call or loses track of sub-goals.
- **Beyond the prompt format:** (1) the scratchpad grows every step, so cost and context rise (Q8); (2) set a stop sequence at `Observation:` so the model cannot write its own observation; the host runs the tool and appends the real result; (3) the host must parse `Action: tool[input]` robustly and handle malformed output; (4) you still need step budgets (Q4). Basic prompting and parsing are in Part 3 Q15; the from-scratch build is Q15 of this part.

**Example:** "Which country is Company Zeta's HQ city in?" Reason-only answers from memory (a stale "Lyon, France"). Act-only searches the bare name, gets no result, and repeats it. ReAct notes the bare name failed, reformulates, finds Pune, then searches Pune and answers India.

**Code:** (mock policies, scripted; shows the shape of the three behaviours, not real model results)
```python
# MOCK demo: reason-only vs act-only vs ReAct on a 2-hop lookup. Scripted policies, no real LLM.
# Question: "In which country is the headquarters city of company Zeta?"  Truth: Zeta -> Pune -> India
KB = {"Zeta company": "Zeta's headquarters are in Pune.", "Pune": "Pune is a city in India."}

def search(q):
    return KB.get(q, "NO RESULT")

def reason_only():                       # chain-of-thought with no tools: answers from memory
    return "Lyon -> France", 0           # (answer, tool_calls) ; ungrounded and wrong

def act_only(max_steps=4):               # actions with no reasoning: searches the raw name, cannot adapt
    calls = 0
    for _ in range(max_steps):
        obs = search("Zeta"); calls += 1         # same action every time; no thought to revise it
        if obs != "NO RESULT": return obs, calls
    return "gave up", calls

def react(max_steps=6):                  # Thought -> Action -> Observation, each step uses the last observation
    scratch, calls = [], 0
    plan = "Thought: need Zeta's HQ city, then its country. Action: search[Zeta]"
    scratch.append(plan)
    obs = search("Zeta"); calls += 1; scratch.append("Observation: " + obs)
    if obs == "NO RESULT":               # exception handling: reformulate instead of repeating
        scratch.append("Thought: bare name failed, try 'Zeta company'. Action: search[Zeta company]")
        obs = search("Zeta company"); calls += 1; scratch.append("Observation: " + obs)
    city = obs.split(" in ")[-1].rstrip(".")
    scratch.append(f"Thought: HQ city is {city}; now find its country. Action: search[{city}]")
    obs = search(city); calls += 1; scratch.append("Observation: " + obs)
    country = obs.split(" in ")[-1].rstrip(".")
    scratch.append(f"Thought: done. Final Answer: {country}")
    return country, calls, scratch

print("reason-only :", reason_only(), "(truth: India)")
print("act-only    :", act_only(), "(truth: India)")
ans, calls, scratch = react()
print("ReAct       :", (ans, calls))
print("\n".join("  " + s for s in scratch))
```
Output (real run):
```
reason-only : ('Lyon -> France', 0) (truth: India)
act-only    : ('gave up', 4) (truth: India)
ReAct       : ('India', 3)
  Thought: need Zeta's HQ city, then its country. Action: search[Zeta]
  Observation: NO RESULT
  Thought: bare name failed, try 'Zeta company'. Action: search[Zeta company]
  Observation: Zeta's headquarters are in Pune.
  Thought: HQ city is Pune; now find its country. Action: search[Pune]
  Observation: Pune is a city in India.
  Thought: done. Final Answer: India
```

**Follow-ups:**
- *Does ReAct always win?* No. For tasks answerable from the prompt it just adds calls; its gains are on tasks needing external information or interaction.
- *Why stop at "Observation:"?* Otherwise the model hallucinates the tool result and continues as if it were real.
- *What replaced the text format?* Native function calling carries the same loop in structured fields (Part 3 Q8).

**Common mistakes:** treating ReAct as only a prompt template; quoting the 34% and 10% as universal gains; letting the model emit observations; ignoring scratchpad growth.

### Q3 ⭐⭐⭐ 🟡 Workflows vs agents: explain prompt chaining, routing, parallelisation, orchestrator-workers and evaluator-optimizer, and when each is the right choice.
**Asked at:** all types; product, GenAI startups, agent-building teams
**Say this first (1 line):** These are Anthropic's five workflow patterns, which keep control flow in your code; reach for them before a free-running agent, and pick the one that matches the shape of the task.

**Then explain:**
| Pattern | Shape | Example | Trade-off |
|---|---|---|---|
| Prompt chaining | step 1 output feeds step 2, optional gates between | outline, check, write the document | more latency (serial), cheaper and more accurate per step than one giant prompt |
| Routing | classify the input, send to one specialised path | refund vs FAQ; small model for easy queries, large for hard | one extra cheap call; saves cost; accuracy depends on the router |
| Parallelisation: sectioning | independent subtasks at once | safety check and answer generation in parallel | lower latency, cost roughly the sum of calls |
| Parallelisation: voting | same task several times, aggregate | 3 reviewers flag unsafe code | cost times N, higher confidence |
| Orchestrator-workers | a planner LLM splits a task dynamically, workers run subtasks, results are merged | edit an unknown set of files | flexible when subtasks are not known ahead; many calls, more latency |
| Evaluator-optimizer | generate, critique, revise in a loop | translation polish against a rubric | cost grows per round; works only when you have clear criteria |
- **Choosing:** fixed steps known in advance means chaining; distinct input types means routing; independent checks mean parallelisation; unknown subtasks mean orchestrator-workers; a clear quality bar and measurable gain from iteration means evaluator-optimizer.
- **Versus a true agent:** all five are workflows, because the code path is predefined (the orchestrator's subtask list is the one dynamic part). A full agent loop is for open-ended problems (Q1). Add complexity only when it measurably helps.

**Example:** Customer support. A router sends "refund" to a refund flow (2 calls) and "how do I reset?" to an FAQ answerer. For a long reply, an evaluator checks tone and facts and asks for a rewrite, usually 1 to 3 rounds. Each round adds 2 calls and seconds of latency, so cap rounds.

**Code:** (mock LLM calls; the counts come from the run, they are not real-model costs)
```python
# MOCK implementations of workflow patterns with LLM-call counts. No real LLM; all "models" are scripted.
from concurrent.futures import ThreadPoolExecutor
import threading
lock = threading.Lock(); calls = {"n": 0}
def llm(fn, *a):
    with lock: calls["n"] += 1
    return fn(*a)

# --- 1. Routing: one cheap classifier call, then ONE specialised handler ---
def classify(q): return "refund" if "refund" in q else "faq"
HANDLERS = {"refund": lambda q: "refund-flow answer", "faq": lambda q: "faq answer"}
def routing(q):
    route = llm(classify, q)
    return llm(HANDLERS[route], q)

# --- 2a. Parallel sectioning: independent subtasks run at the same time ---
def check(section, text): return f"{section}:ok"
def sectioning(text):
    with ThreadPoolExecutor(3) as ex:
        return list(ex.map(lambda s: llm(check, s, text), ["safety", "pii", "tone"]))

# --- 2b. Parallel voting: same task N times, majority wins (scripted votes) ---
VOTES = ["unsafe", "safe", "unsafe"]
def vote_once(i): return VOTES[i]
def voting(text, n=3):
    with ThreadPoolExecutor(n) as ex:
        votes = list(ex.map(lambda i: llm(vote_once, i), range(n)))
    return max(set(votes), key=votes.count), votes

# --- 3. Evaluator-optimizer: generate, critique, revise until the evaluator accepts ---
DRAFTS = ["draft v1 (too long)", "draft v2 (shorter)", "draft v3 (concise)"]
def generate(i): return DRAFTS[i]
def evaluate(d): return ("concise" in d, "make it concise")
def evaluator_optimizer(max_rounds=4):
    for i in range(max_rounds):
        d = llm(generate, i)
        ok, fb = llm(evaluate, d)
        if ok: return d, i + 1
    return d, max_rounds

def run(label, fn, *a):
    calls["n"] = 0; out = fn(*a); print(f"{label:22s} calls={calls['n']}  out={out}")
run("routing", routing, "I want a refund")
run("sectioning", sectioning, "some text")
run("voting (n=3)", voting, "some text")
run("evaluator-optimizer", evaluator_optimizer)
```
Output (real run):
```
routing                calls=2  out=refund-flow answer
sectioning             calls=3  out=['safety:ok', 'pii:ok', 'tone:ok']
voting (n=3)           calls=3  out=('unsafe', ['unsafe', 'safe', 'unsafe'])
evaluator-optimizer    calls=6  out=('draft v3 (concise)', 3)
```

**Follow-ups:**
- *Sectioning vs voting?* Sectioning splits different subtasks to cut latency; voting repeats the same one to raise confidence.
- *How does orchestrator-workers differ from parallel sectioning?* The subtasks are decided at run time by the orchestrator, not hard-coded.
- *Where do multi-agent systems fit?* See Q12 for token cost and failure modes.

**Common mistakes:** jumping to agents when chaining works; evaluator loops with no round cap or no objective rubric; routing with a weak classifier and no fallback route; ignoring that voting multiplies cost.

### Q4 ⭐⭐⭐ 🟡 How does an agent loop terminate? Cover stop conditions, step and token budgets, loop detection and what to do when the budget runs out.
**Asked at:** all types; agentic-AI loops; a Codemia guide for an Amazon agentic-AI loop lists an agent-stuck-in-a-loop prompt (a guide, not a candidate report)
**Say this first (1 line):** A loop should end by a success signal (a final-answer action) or by a guard the host enforces, such as step, token, cost, time and error budgets plus repeated-action and no-progress detection, and on a guard stop it returns a partial result with the reason or escalates.

**Then explain:**
- **Success stop:** the model emits a final-answer action (or stops calling tools). Never rely on this alone; the model may never emit it.
- **Hard budgets (host-enforced):** max steps, max tokens, max cost, wall-clock time, and an error budget (stop after N failed tool calls). Budgets bound the worst case; the model cannot argue with them.
- **Repeated-action detection:** same tool with the same canonicalised arguments K times in a row. Canonicalise (sorted keys) or `{"a":1,"b":2}` and `{"b":2,"a":1}` look different.
- **No-progress detection:** different actions but the same observations (for example "NO RESULTS" four times), or nothing new added to state. This catches loops that repeat-detection misses.
- **When a budget runs out:** do not return nothing. Return the partial result, the stop reason, and what was tried; then retry with a different plan, hand to a human or a stronger model, or fail clearly. Log the trace so the loop can be debugged.
- **Why it matters:** agentic loops use many LLM calls (one explainer I saw reports 5 to 10 times more than classic RAG, snippet-level), so unbounded loops are a cost and reliability risk.

**Example:** An agent keeps calling `search("refund policy")` and gets "NO RESULTS". After three identical calls the repeated-action guard fires; with varied queries but the same empty result, the no-progress guard fires on the fourth. The caller gets `{"reason": "no_progress", "partial": ..., "escalate": true}` and routes to a human.

**Code:** (standalone, with assertion tests; the clock is injectable so the time budget is tested without sleeping)
```python
# Loop guard: repeated-action detection, no-progress detection, step/token/time/error budgets. Standalone with tests.
import json, time

class LoopGuard:
    def __init__(self, max_steps=10, max_tokens=5000, max_seconds=60, max_errors=3,
                 repeat_limit=3, patience=3, clock=time.monotonic):
        self.max_steps, self.max_tokens, self.max_seconds = max_steps, max_tokens, max_seconds
        self.max_errors, self.repeat_limit, self.patience = max_errors, repeat_limit, patience
        self.clock, self.t0 = clock, clock()
        self.steps = self.tokens = self.errors = 0
        self.history = []            # (action_signature, observation_signature)
        self.seen_obs = set()
        self.stale = 0               # consecutive steps with no new observation

    @staticmethod
    def sig(name, args):             # canonical form so {"a":1,"b":2} == {"b":2,"a":1}
        return name + json.dumps(args, sort_keys=True)

    def record(self, name, args, observation, tokens=0, error=False):
        """Call after each step. Returns None to continue, or a stop reason string."""
        self.steps += 1; self.tokens += tokens; self.errors += int(error)
        a, o = self.sig(name, args), str(observation)
        self.history.append((a, o))
        if o in self.seen_obs: self.stale += 1
        else: self.seen_obs.add(o); self.stale = 0
        return self.check()

    def check(self):
        if self.steps >= self.max_steps: return "max_steps"
        if self.tokens >= self.max_tokens: return "token_budget"
        if self.clock() - self.t0 >= self.max_seconds: return "time_budget"
        if self.errors >= self.max_errors: return "error_budget"
        last = [a for a, _ in self.history[-self.repeat_limit:]]
        if len(last) == self.repeat_limit and len(set(last)) == 1: return "repeated_action"
        if self.stale >= self.patience: return "no_progress"
        return None

def finish(reason, partial):         # never fail silently: partial result + reason + escalate flag
    return {"status": "stopped", "reason": reason, "partial": partial, "escalate": True}

# ---- tests ----
g = LoopGuard(); assert g.record("search", {"q": "x"}, "r1") is None
g = LoopGuard(repeat_limit=3, patience=99)
assert [g.record("search", {"q": "x", "n": 1}, f"r{i}") for i in range(3)] == [None, None, "repeated_action"]
g = LoopGuard(repeat_limit=3, patience=99)                      # key order must not hide repeats
assert g.record("s", {"a": 1, "b": 2}, "o1") is None and g.record("s", {"b": 2, "a": 1}, "o2") is None
assert g.record("s", {"a": 1, "b": 2}, "o3") == "repeated_action"
g = LoopGuard(repeat_limit=99, patience=3)                      # different actions, same observation
r = [g.record("s", {"q": i}, "NO RESULTS") for i in range(4)]
assert r == [None, None, None, "no_progress"], r
assert LoopGuard(max_steps=2).record("a", {}, "o1") is None
g = LoopGuard(max_steps=2); g.record("a", {}, "o1"); assert g.record("b", {}, "o2") == "max_steps"
assert LoopGuard(max_tokens=100).record("a", {}, "o", tokens=100) == "token_budget"
g = LoopGuard(max_errors=2, repeat_limit=99, patience=99)
g.record("a", {"i": 1}, "e1", error=True); assert g.record("a", {"i": 2}, "e2", error=True) == "error_budget"
t = [0.0]; g = LoopGuard(max_seconds=5, clock=lambda: t[0]); t[0] = 6.0
assert g.record("a", {}, "o") == "time_budget"
print(finish("no_progress", {"found": ["doc1"]}))
print("all tests passed")
```
Output (real run):
```
{'status': 'stopped', 'reason': 'no_progress', 'partial': {'found': ['doc1']}, 'escalate': True}
all tests passed
```

**Follow-ups:**
- *Which default budgets?* Derive them from the task: look at the step-count distribution of successful runs and set the cap a bit above the high percentile; tune with evals (Q14).
- *Can the model decide to stop?* Yes for success, but not for safety limits; those stay in host code.
- *What about retries inside one tool?* That is a separate cap (Q13).

**Common mistakes:** relying on the model to stop itself; only a max-step cap and no cost cap; comparing raw argument strings; returning an exception with no partial result; never escalating.

### Q5 ⭐⭐⭐ 🟡 Planning in agents: ReAct vs plan-then-execute vs a hybrid with re-planning checkpoints. What are the trade-offs?
**Asked at:** all types; agentic-AI loops
**Say this first (1 line):** ReAct decides one step at a time, so it adapts but spends an LLM call per step; plan-then-execute plans once, so it is cheap but rigid; a hybrid plans once, executes cheaply, and re-plans only at checkpoints where reality diverges from the plan.
**Then explain:**
| Strategy | LLM calls | Strength | Weakness |
|---|---|---|---|
| ReAct | about one per step | adapts to every observation | cost and latency grow with steps; can wander without a plan |
| Plan-then-execute | one plan (plus a cheap executor) | cheap, predictable, plan can be reviewed or approved first | brittle if a step fails or the world changes |
| Hybrid with checkpoints | plan plus a re-plan only when needed | most of the cost saving and most of the adaptivity | needs a good checkpoint test (did the step succeed? is the plan still valid?) |
- **Re-plan triggers:** a step fails after local retries, an observation contradicts a plan assumption, a budget threshold is hit. Keep a re-plan cap, or the hybrid becomes a loop (Q4).
- **What the market says:** several prep guides (seen as search snippets, not opened) describe the plan-then-execute and re-planning hybrid as a common 2026 enterprise pattern. Treat that as an expectation, not a measured fact.
- **Choose by volatility:** stable environment and long known procedure means plan-then-execute; unpredictable environment or exploration means ReAct; mixed means hybrid. Plan representation and approval are covered in Q19.

**Example:** A 5-step task. If nothing changes, ReAct needs 6 calls while the others need 2. If the world changes after step 2 in 40% of runs, the rigid plan fails in many of those; the hybrid re-plans once and recovers.

**Code:** (SYNTHETIC simulation with scripted policies and assumed probabilities; it illustrates the shape of the trade-off and is not a benchmark of real agents)
```python
# SYNTHETIC simulation (not a benchmark): ReAct vs plan-then-execute vs hybrid when the world changes.
# Assumptions: 5-step task; mock "LLM" policies are scripted; one LLM call = one decision or one plan.
import random
N_STEPS = 5

class Env:
    def __init__(self, rng, p_change, p_flaky):
        self.need = [f"s{i}" for i in range(N_STEPS)]
        self.pos, self.rng, self.p_flaky = 0, rng, p_flaky
        # with prob p_change the world changes after step 2 (remaining required steps differ)
        self.change_at = 2 if rng.random() < p_change else None
    def act(self, a):
        if self.change_at is not None and self.pos == self.change_at:
            self.need[self.pos:] = [f"alt{i}" for i in range(self.pos, N_STEPS)]; self.change_at = None
        if a != self.need[self.pos]: return "mismatch"
        if self.rng.random() < self.p_flaky: return "transient_error"
        self.pos += 1; return "ok"
    def done(self): return self.pos == N_STEPS
    def state(self):  # what an observation reveals: the next needed step
        if self.change_at is not None and self.pos == self.change_at:
            return f"alt{self.pos}"
        return self.need[self.pos] if self.pos < N_STEPS else None

def react(env, budget=20):
    calls = 0
    while not env.done() and calls < budget:
        calls += 1                                   # 1 LLM call per step: decide from latest observation
        env.act(env.state())
    return calls + 1, env.done()                     # +1 final-answer call

def plan_then_execute(env):
    calls, plan = 1, [f"s{i}" for i in range(N_STEPS)]   # 1 planning call, executor needs no LLM
    for a in plan:
        r = env.act(a)
        if r == "transient_error": r = env.act(a)        # executor may retry once, no LLM
        if r != "ok": return calls + 1, False            # rigid: stale plan, no re-plan
    return calls + 1, env.done()

def hybrid(env, max_replans=2):
    calls, plan, replans = 1, [f"s{i}" for i in range(N_STEPS)], 0
    while not env.done():
        a = plan[env.pos]
        r = env.act(a)
        if r == "transient_error": r = env.act(a)
        if r == "mismatch":                               # checkpoint: plan no longer valid -> re-plan
            if replans == max_replans: return calls + 1, False
            replans += 1; calls += 1
            plan = plan[:env.pos] + [f"alt{i}" for i in range(env.pos, N_STEPS)]
        elif r != "ok": return calls + 1, False
    return calls + 1, True

def run(p_change, p_flaky, trials=2000):
    out = {}
    for name, fn in [("react", react), ("plan_then_execute", plan_then_execute), ("hybrid", hybrid)]:
        rng = random.Random(0); tot, ok = 0, 0
        for _ in range(trials):
            c, s = fn(Env(rng, p_change, p_flaky)); tot += c; ok += s
        out[name] = (round(tot / trials, 2), round(ok / trials, 3))
    return out

for p_change, p_flaky in [(0.0, 0.0), (0.0, 0.2), (0.4, 0.0), (0.4, 0.2)]:
    print(f"p_change={p_change} p_flaky={p_flaky}  (avg LLM calls, success rate)")
    for k, v in run(p_change, p_flaky).items(): print(f"   {k:18s} {v}")
```
Output (real run):
```
p_change=0.0 p_flaky=0.0  (avg LLM calls, success rate)
   react              (6.0, 1.0)
   plan_then_execute  (2.0, 1.0)
   hybrid             (2.0, 1.0)
p_change=0.0 p_flaky=0.2  (avg LLM calls, success rate)
   react              (7.24, 1.0)
   plan_then_execute  (2.0, 0.809)
   hybrid             (2.0, 0.809)
p_change=0.4 p_flaky=0.0  (avg LLM calls, success rate)
   react              (6.0, 1.0)
   plan_then_execute  (2.0, 0.593)
   hybrid             (2.39, 1.0)
p_change=0.4 p_flaky=0.2  (avg LLM calls, success rate)
   react              (7.24, 1.0)
   plan_then_execute  (2.0, 0.475)
   hybrid             (2.37, 0.809)
```
Reading it: with no changes the cheap strategies use 2 calls versus 6. With a 40% chance of the world changing, plan-then-execute success falls to 0.593 while the hybrid recovers to 1.0 for about 2.4 calls. With flaky steps, ReAct retries by deciding again (more calls), while my executors retry only once without an LLM, which is why they fail when two attempts in a row fail. That retry cap is a design choice you would tune.

**Follow-ups:**
- *Does the plan need an LLM executor?* Not always; deterministic code can execute simple steps and call the LLM only for judgement.
- *What is a checkpoint here?* A verification point after a step, which compares the observation with the expected result. It is separate from a persistence checkpoint (Q7).
- *How do you keep the plan safe?* Validate it against allowed tools and, for risky actions, get approval before executing.

**Common mistakes:** claiming one strategy is always better; no check that the plan is still valid; unlimited re-planning; presenting simulated numbers as real-world results.

### Q6 ⭐⭐⭐ 🟡 How do you design tools for agents (the agent-computer interface): granularity, names, descriptions, error messages, and mistake-proofing?
**Asked at:** product, GenAI startups, agent-building teams
**Say this first (1 line):** Treat the tool interface as a product for the model: give tool definitions as much prompt engineering as prompts, make wrong use hard (poka-yoke), return concise and actionable results, and test with many real inputs.
**Then explain:**
- **Anthropic's guidance (agent-computer interface):** put yourself in the model's shoes (is it obvious how to use this tool from the description alone?), use clear parameter names, include examples and edge cases in the description, and run many example inputs to see what mistakes the model makes.
- **Poka-yoke:** change the design so a mistake is hard to make. Anthropic reports that in their SWE-bench agent work the model made errors with relative paths after changing directory, and requiring absolute file paths removed that class of error (vendor-reported).
- **Granularity:** prefer workflow-level tools (`create_refund(order_id, reason)`) over raw endpoint wrappers that force several calls and leak API detail (a DataCamp guide's point). Too many tools hurt selection (Part 3 Q30).
- **Errors:** return what went wrong, why, and what to try next ("'absolute_path' must start with '/'. Example: ..."), not a stack trace or "Error".
- **Responses:** concise, with pagination and truncation flags (`next_offset`) so one call cannot flood the context.
- **Side effects:** mark which tools mutate, validate arguments with a schema, and make writes idempotent (Part 3 Q28, Q29 for schemas and safety; Part 3 Q9 for definitions).

**Example:** A file-read tool took `path`. After another step changed the working directory, `README.md` silently resolved to the wrong place. Renaming the parameter to `absolute_path` and rejecting anything not starting with `/` turns a confusing "not found" into an immediate fix hint.

**Code:** (mock filesystem; before/after wrapper; asserts pass)
```python
# Before/after tool wrapper on a MOCK filesystem: relative-path bug vs absolute-path poka-yoke.
import posixpath
FS = {"/repo/README.md": "readme text", "/repo/src/config.py": "DEBUG = True\n" * 400}
state = {"cwd": "/repo"}

# ---- BEFORE: ambiguous 'path'; resolved against a cwd that other tools may have changed ----
def change_dir(path): state["cwd"] = path; return "ok"
def read_file_v1(path):
    full = posixpath.normpath(posixpath.join(state["cwd"], path))
    return FS.get(full, "Error: not found")          # unhelpful error, no hint

# ---- AFTER: absolute paths required, actionable errors, truncation + pagination ----
def read_file_v2(absolute_path, offset=0, max_chars=100):
    if not absolute_path.startswith("/"):
        return {"error": f"'absolute_path' must start with '/'. Got '{absolute_path}'. "
                         f"Example: '/repo/README.md'."}
    if absolute_path not in FS:
        near = [p for p in FS if posixpath.basename(p) == posixpath.basename(absolute_path)]
        return {"error": f"No such file: {absolute_path}.", "did_you_mean": near}
    text = FS[absolute_path]; chunk = text[offset:offset + max_chars]
    nxt = offset + max_chars if offset + max_chars < len(text) else None
    return {"content": chunk, "total_chars": len(text), "truncated": nxt is not None, "next_offset": nxt}

# The agent reads a relative path, then another step changes directory (a realistic side effect).
print("v1 before cd :", read_file_v1("README.md"))
change_dir("/repo/src")
print("v1 after cd  :", read_file_v1("README.md"))                 # silent wrong-cwd bug
print("v2 relative  :", read_file_v2("README.md"))                 # fails fast with a fix hint
print("v2 absolute  :", read_file_v2("/repo/README.md"))
page = read_file_v2("/repo/src/config.py")
print("v2 large file:", {k: (v if k != "content" else v[:20] + "...") for k, v in page.items()})
print("v2 typo      :", read_file_v2("/repo/config.py"))
assert read_file_v1("README.md") == "Error: not found"
assert "must start with '/'" in read_file_v2("README.md")["error"]
assert read_file_v2("/repo/README.md")["content"] == "readme text"
assert read_file_v2("/repo/src/config.py")["truncated"] is True
assert read_file_v2("/repo/config.py")["did_you_mean"] == ["/repo/src/config.py"]
```
Output (real run):
```
v1 before cd : readme text
v1 after cd  : Error: not found
v2 relative  : {'error': "'absolute_path' must start with '/'. Got 'README.md'. Example: '/repo/README.md'."}
v2 absolute  : {'content': 'readme text', 'total_chars': 11, 'truncated': False, 'next_offset': None}
v2 large file: {'content': 'DEBUG = True\nDEBUG =...', 'total_chars': 5200, 'truncated': True, 'next_offset': 100}
v2 typo      : {'error': 'No such file: /repo/config.py.', 'did_you_mean': ['/repo/src/config.py']}
```

**Follow-ups:**
- *How do you know the tool design is good?* Log the model's tool-call errors on a test set and fix descriptions or schemas until they drop.
- *Should a tool return raw JSON?* Return only the fields the model needs; extra fields cost tokens and distract.
- *Bash tool or many small tools?* Many small typed tools are safer and easier to validate; a shell is flexible but needs a sandbox.

**Common mistakes:** one-line descriptions; wrapping every REST endpoint 1:1; error strings that say only "failed"; unbounded outputs; ambiguous parameters like `path` or `id` with no format stated.

### Q7 ⭐⭐⭐ 🟡 Memory in agents: short-term vs long-term, and episodic, semantic and procedural memory. What is the difference between state, memory and checkpointing?
**Asked at:** all types; agentic-AI loops
**Say this first (1 line):** Short-term memory is the working state of one conversation or thread; long-term memory is information stored so it can be recalled in later threads; a checkpoint is a saved snapshot of state so a run can resume.
**Then explain:**
- **Short-term vs long-term (LangGraph docs, seen as search snippets, not opened, so check the docs):** short-term memory is thread-scoped state, persisted by a checkpointer so the thread can be resumed; long-term memory is shared across threads and kept in a store organised by namespaces.
- **Types, snippet-level (borrowed from cognitive science):** *semantic* is facts ("user prefers Hindi"), *episodic* is past events or experiences ("last time this refund failed because..."), *procedural* is how to do things (instructions or prompts the agent refines). The three-way split is a useful vocabulary, not a standard.
- **State vs memory vs checkpoint:** state is the working data of a run (messages, to-do list, tool results). A checkpoint is a persisted snapshot of that state at a step, giving crash recovery, resume after human approval, and replay. Long-term memory is knowledge recalled across runs. A checkpoint is not memory: it is one thread's snapshot.
- **Writing and recalling:** decide what is worth saving (not every message), store with metadata, retrieve by namespace or similarity, and let users delete entries (privacy). Stale memories need expiry or update rules.
- **Context link:** whatever is recalled still has to fit in the prompt (Q8).

**Example:** A support agent crashes after step 2 of a thread. Restoring the latest checkpoint resumes at step 3 with the same to-do list. A brand-new thread has empty state, but it still greets the user in Hindi because the language preference sits in the long-term store under the user's namespace.

**Code:** (stdlib: sqlite3 checkpoints, a namespaced dict store, mock agent; asserts pass)
```python
# Stdlib demo: thread state vs long-term store vs checkpoints. Mock agent, no LLM.
import json, os, sqlite3, tempfile

class CheckpointStore:                       # persisted snapshots of a thread's state
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS cp(thread TEXT, step INT, state TEXT)")
    def save(self, thread, step, state):
        self.db.execute("INSERT INTO cp VALUES (?,?,?)", (thread, step, json.dumps(state))); self.db.commit()
    def latest(self, thread):
        row = self.db.execute("SELECT step,state FROM cp WHERE thread=? ORDER BY step DESC LIMIT 1", (thread,)).fetchone()
        return (row[0], json.loads(row[1])) if row else (0, None)

class LongTermStore:                         # cross-thread memory, namespaced, e.g. ("user","u1","prefs")
    def __init__(self): self.d = {}
    def put(self, ns, key, value): self.d[(tuple(ns), key)] = value
    def get(self, ns, key): return self.d.get((tuple(ns), key))
    def search(self, ns): return {k: v for (n, k), v in self.d.items() if n == tuple(ns)}

def run_thread(thread, user, cps, ltm, crash_after=None):
    step, state = cps.latest(thread)
    if state is None: state = {"messages": [], "todo": ["greet", "fetch_order", "answer"]}   # short-term state
    while state["todo"]:
        task = state["todo"].pop(0); step += 1
        if task == "greet":
            lang = ltm.get(("user", user, "prefs"), "language") or "en"      # long-term recall across threads
            state["messages"].append(f"greeting in {lang}")
        elif task == "fetch_order": state["messages"].append("order #42 shipped")
        else:
            state["messages"].append("answer sent"); ltm.put(("user", user, "prefs"), "last_topic", "shipping")
        cps.save(thread, step, state)                                       # checkpoint after each step
        if crash_after == step: raise RuntimeError("process crashed")
    return state

path = os.path.join(tempfile.mkdtemp(), "cp.db")
ltm = LongTermStore(); ltm.put(("user", "u1", "prefs"), "language", "hi")
cps = CheckpointStore(path)
try: run_thread("t1", "u1", cps, ltm, crash_after=2)
except RuntimeError as e: print("crash:", e)
cps2 = CheckpointStore(path)                                                # new process, same file
print("resume from:", cps2.latest("t1")[0], "->", cps2.latest("t1")[1]["todo"])
final = run_thread("t1", "u1", cps2, ltm)
print("final state :", final["messages"])
t2 = run_thread("t2", "u1", cps2, ltm)                                      # a NEW thread: fresh state...
print("thread t2   :", t2["messages"][0], "| long-term:", ltm.search(("user", "u1", "prefs")))
assert final["messages"] == ["greeting in hi", "order #42 shipped", "answer sent"]
assert ltm.get(("user", "u1", "prefs"), "last_topic") == "shipping"
assert t2["messages"][0] == "greeting in hi"
```
Output (real run):
```
crash: process crashed
resume from: 2 -> ['answer']
final state : ['greeting in hi', 'order #42 shipped', 'answer sent']
thread t2   : greeting in hi | long-term: {'language': 'hi', 'last_topic': 'shipping'}
```

**Follow-ups:**
- *Where do you keep long-term memory?* A key-value store for facts, or a vector store when recall is by meaning; start with the simplest that works.
- *Why checkpoint?* Crash recovery, human-in-the-loop pauses, and time-travel debugging.
- *What are the risks?* Storing wrong or sensitive facts, stale facts, and memory injection by an attacker (Part 11).

**Common mistakes:** using "memory" and "state" as synonyms; storing the whole transcript as long-term memory; no deletion or expiry; thinking a checkpoint lets the agent learn across users.

### Q8 ⭐⭐⭐ 🟡 How do you manage context in a long-running agent (summarisation, trimming, offloading to notes or files, tiered memory)?
**Asked at:** product, GenAI startups, agent-building teams
**Say this first (1 line):** Keep the prompt inside a budget by keeping recent turns verbatim, compressing or dropping old ones, moving bulky or important material out to notes or files that can be re-read, and pinning the facts that must never be lost.
**Then explain:**
- **Sliding-window trimming:** keep the last N turns or tokens. Simple and predictable, but silently forgets early facts.
- **Rolling summarisation:** when over budget, summarise the oldest turns into a running summary. Cheaper than the full history, but each pass is lossy: details drift or vanish (summary drift), and the summariser can add errors.
- **Offloading:** write plans, findings and tool outputs to a notes file or external store and keep only a pointer or short digest in the prompt; re-read on demand. Anthropic's research-system post reports that the lead agent saves its plan to memory because context beyond 200,000 tokens is truncated (vendor-reported).
- **Tiered memory:** the MemGPT abstract (arXiv 2310.08560) proposes virtual context management inspired by operating-system memory hierarchies: memory tiers, with interrupts for control flow. It was evaluated on document analysis beyond the context window and on multi-session chat. Think main context as RAM, external storage as disk.
- **Pinned facts:** identifiers, user constraints and the task goal go in a protected block outside the summariser's reach.
- **Risks:** losing a critical fact, summary drift, cost of the summarising call, and stale offloaded notes. Test with questions whose answers sit in early turns.

**Example:** A refund agent talks for 40 turns. Order id and "refund to the original card" are pinned; turns 1 to 36 become a short summary; the last 2 turns stay verbatim. In the run below, an unpinned manager loses the order id after compression while the pinned one keeps it within the same budget.

**Code:** (mock summariser that is lossy on purpose; word count as a token proxy; asserts pass)
```python
# Rolling-summary context manager with a token budget (word count as a proxy) and pinned facts. Mock summariser.
def tokens(text): return len(text.split())          # proxy only; real systems use the model's tokenizer

def mock_summarise(old_summary, messages, max_words=12):
    """Scripted stand-in for an LLM summariser: lossy on purpose (keeps the first 4 words of each message)."""
    words = (old_summary + " " + " ".join(" ".join(m.split()[:4]) for m in messages)).split()
    return " ".join(words[-max_words:])              # older material falls off: this is summary drift

class ContextManager:
    def __init__(self, budget=40, keep_recent=2, pinned=None):
        self.budget, self.keep_recent = budget, keep_recent
        self.pinned = list(pinned or [])             # facts that must never be summarised away
        self.summary, self.recent = "", []
    def add(self, msg):
        self.recent.append(msg)
        while self.size() > self.budget and len(self.recent) > self.keep_recent:
            overflow = self.recent[:-self.keep_recent]
            fixed = tokens("\n".join(["PINNED: " + "; ".join(self.pinned)] * bool(self.pinned) + self.recent[-self.keep_recent:]))
            room = max(0, self.budget - fixed - 1)            # summary must fit what is left of the budget
            self.summary = mock_summarise(self.summary, overflow, max_words=room)
            self.recent = self.recent[-self.keep_recent:]
    def size(self): return tokens(self.render())
    def render(self):
        parts = []
        if self.pinned: parts.append("PINNED: " + "; ".join(self.pinned))
        if self.summary: parts.append("SUMMARY: " + self.summary)
        parts += self.recent
        return "\n".join(parts)

turns = ["user: my order id is 8841 and the refund must go to the original card",
         "agent: noted, checking the order status now please wait",
         "user: also my name is Asha and I live in Pune",
         "agent: your order shipped three days ago via courier",
         "user: can you tell me the courier phone number please",
         "agent: the courier number is on the tracking page",
         "user: ok and what is the return window for this item",
         "agent: the return window is thirty days from delivery"]

plain = ContextManager(budget=40)
pinned = ContextManager(budget=40, pinned=["order id 8841", "refund to original card"])
for t in turns: plain.add(t); pinned.add(t)
print("--- pinned manager context ---\n" + pinned.render())
print("sizes (words):", plain.size(), pinned.size(), "budget 40")
print("plain keeps '8841'  :", "8841" in plain.render())
print("pinned keeps '8841' :", "8841" in pinned.render())
assert pinned.size() <= 40 and plain.size() <= 40
assert "8841" in pinned.render() and "original card" in pinned.render()
assert "8841" not in plain.render()                 # drift: unpinned fact was lost
assert turns[-1] in pinned.render()                 # most recent turn always kept verbatim
```
Output (real run):
```
--- pinned manager context ---
PINNED: order id 8841; refund to original card
SUMMARY: your order shipped user: can you tell agent: the courier number
user: ok and what is the return window for this item
agent: the return window is thirty days from delivery
sizes (words): 40 40 budget 40
plain keeps '8841'  : False
pinned keeps '8841' : True
```

**Follow-ups:**
- *Summarise or drop?* Drop low-value tool output first (large and rarely re-read), summarise conversation, keep decisions and constraints.
- *How do you test a summary?* Ask fixed probe questions against the compressed context and compare with the full one.
- *Does a bigger window remove the problem?* No: cost, latency and attention quality still matter; retrieval from notes stays useful (Part 6 and 7 for retrieval).

**Common mistakes:** recursive summarising with no pinned facts; trimming by turn count while tool outputs are huge; counting words instead of real tokens in production; never testing recall of early facts.

### Q9 ⭐⭐⭐ 🟡 What is the Model Context Protocol (MCP)? Explain the problem it solves, the host-client-server architecture, JSON-RPC messaging and the connection lifecycle.
**Asked at:** all types; agentic-AI and GenAI-engineer loops
**Say this first (1 line):** MCP is an open protocol that lets AI applications connect to tools and data sources in one standard way, so N applications and M tools need N plus M integrations instead of N times M.
**Then explain:**
- **Origin (reported by a prep guide, not verified by me):** introduced by Anthropic in November 2024. Check the current specification, because versions move quickly; I opened the 2025-06-18 base-protocol page.
- **The N x M problem:** without a standard, every app writes a custom connector for every tool. With MCP, a tool provider writes one server and every MCP-capable host can use it.
- **Architecture:** the *host* is the AI application (an IDE, a chat app); it creates one *client* per connection; each client talks to one *server* that exposes capabilities. The host owns user consent and security decisions.
- **Messages:** JSON-RPC 2.0. A *request* has a non-null string or integer `id` that must not be reused in the session; a *response* carries either `result` or `error`, never both (error codes are integers); a *notification* has no `id` and gets no reply.
- **Components in the spec page:** base protocol, lifecycle management, authorisation, server features (resources, prompts, tools), client features (sampling, roots) and utilities. Base protocol and lifecycle MUST be supported; the other components MAY be.
- **Lifecycle (general understanding; the lifecycle page itself was not opened):** the client sends `initialize` with its protocol version and capabilities; the server replies with its own; the client sends a `notifications/initialized` notification; then normal operation (`tools/list`, `tools/call`, ...); then shutdown. Capabilities negotiated at the start decide which features are used.
- **Transports and auth (guide-reported):** stdio for local servers, Streamable HTTP for remote ones; the spec says HTTP transports SHOULD follow its authorisation spec and stdio should take credentials from the environment.

**Example:** A host starts a filesystem server over stdio, sends `initialize` (id 1), gets the server's capabilities (it offers tools), sends the `initialized` notification, then asks `tools/list` (id 2) and shows the tools to the model.

**Code:** (standalone validator for the base-protocol rules above, with tests; message examples printed)
```python
# JSON-RPC 2.0 message examples in MCP style + a validator for the base-protocol rules. Standalone, with tests.
import json

class Session:
    """Tracks request ids so an id is never reused within a session."""
    def __init__(self): self.used_ids = set(); self.pending = set()

    def validate(self, msg, direction="client->server"):
        """Returns a list of problems (empty list = valid)."""
        errs = []
        if msg.get("jsonrpc") != "2.0": errs.append("jsonrpc must be '2.0'")
        has = {k for k in ("method", "id", "result", "error") if k in msg}
        if "method" in has and "id" in has:                                   # request
            rid = msg["id"]
            if rid is None or isinstance(rid, bool) or not isinstance(rid, (str, int)):
                errs.append("request id must be a non-null string or integer")
            elif (direction, rid) in self.used_ids:
                errs.append(f"request id {rid!r} already used in this session")
            else:
                self.used_ids.add((direction, rid)); self.pending.add((direction, rid))
        elif "method" in has:                                                  # notification
            if not isinstance(msg["method"], str): errs.append("method must be a string")
        elif "id" in has and ({"result", "error"} & has):                      # response
            if "result" in has and "error" in has: errs.append("response must set result or error, not both")
            if "error" in has:
                e = msg["error"]
                if not isinstance(e, dict) or not isinstance(e.get("code"), int) or isinstance(e.get("code"), bool):
                    errs.append("error.code must be an integer")
                if isinstance(e, dict) and not isinstance(e.get("message"), str):
                    errs.append("error.message must be a string")
            other = "server->client" if direction == "client->server" else "client->server"
            # a response answers a request that travelled the other way
            key = (other, msg["id"])
            if key not in self.pending: errs.append(f"response id {msg['id']!r} matches no pending request")
            else: self.pending.discard(key)
        else:
            errs.append("not a valid request, response or notification")
        if "method" in has and "id" not in has and "result" in has: errs.append("notification must not have result")
        return errs

init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "demo", "version": "0"}}}
init_ok = {"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}},
                                                 "serverInfo": {"name": "toy", "version": "0"}}}
initialized = {"jsonrpc": "2.0", "method": "notifications/initialized"}
tools_list = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
err_resp = {"jsonrpc": "2.0", "id": 2, "error": {"code": -32601, "message": "Method not found"}}

s = Session()
assert s.validate(init_req) == []
assert s.validate(init_ok, "server->client") == []
assert s.validate(initialized) == []
assert s.validate(tools_list) == []
assert s.validate(err_resp, "server->client") == []
assert "already used" in " ".join(s.validate({**tools_list}))                  # id reuse
assert "non-null" in " ".join(Session().validate({"jsonrpc": "2.0", "id": None, "method": "x"}))
assert "non-null" in " ".join(Session().validate({"jsonrpc": "2.0", "id": 1.5, "method": "x"}))
s2 = Session(); s2.validate({"jsonrpc": "2.0", "id": "a", "method": "x"})
assert "not both" in " ".join(s2.validate({"jsonrpc": "2.0", "id": "a", "result": {}, "error": {"code": 1, "message": "m"}}, "server->client"))
s3 = Session(); s3.validate({"jsonrpc": "2.0", "id": 7, "method": "x"})
assert "integer" in " ".join(s3.validate({"jsonrpc": "2.0", "id": 7, "error": {"code": "bad", "message": "m"}}, "server->client"))
assert Session().validate({"jsonrpc": "2.0", "method": "notifications/x"}) == []
assert "matches no pending" in " ".join(Session().validate({"jsonrpc": "2.0", "id": 99, "result": {}}, "server->client"))
print(json.dumps(init_req)); print(json.dumps(init_ok)); print(json.dumps(initialized))
print("all tests passed")
```
Output (real run):
```
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "demo", "version": "0"}}}
{"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}, "serverInfo": {"name": "toy", "version": "0"}}}
{"jsonrpc": "2.0", "method": "notifications/initialized"}
all tests passed
```

**Follow-ups:**
- *Why a stateful session?* The lifecycle negotiates capabilities and version up front. Later spec versions may change this; reported changes come from one guide, so verify.
- *Security?* Treat tool descriptions and results as untrusted input (Q25 onwards, Part 11).
- *Is MCP only for tools?* No: resources and prompts too (Q10).

**Common mistakes:** saying MCP is a model feature; mixing up host and client; forgetting notifications have no id; claiming spec details from later versions as fact.

### Q10 ⭐⭐⭐ 🟡 What are MCP's tools, resources and prompts, who controls each, and how do you decide which to use?
**Asked at:** all types; agentic-AI and GenAI-engineer loops
**Say this first (1 line):** Tools are model-controlled actions, resources are application-controlled read-only context, and prompts are user-controlled templates; the spec lists all three as server features.
**Then explain:**
- **Tools (model-controlled):** functions the model can choose to call, for actions or live computation (query a database, create a ticket). They may have side effects, so they need schemas, validation and often user confirmation. The DataCamp guide notes tool annotations are hints, not guarantees, so do not trust them for security.
- **Resources (application-controlled):** data the host application decides to attach as context, identified by URI (a file, a schema, a policy document). Read-only reference data.
- **Prompts (user-controlled):** reusable templates a user picks explicitly, such as a slash command like "summarise this ticket".
- **Who decides** is the key idea: the model, the app, or the user.
- **Decision rule:** does it change something or compute something live? A tool. Is it stable reference content the app can fetch and attach? A resource. Is it a canned workflow the user triggers? A prompt. When in doubt about control, ask "who should be able to trigger this?".
- **Caveat:** the control labels come from the guide plus the spec's feature list; in practice hosts differ (some expose resources to the model through tools). Check your host's behaviour. The tools, resources and prompts spec pages were not opened by me.

**Example:** An order-support server. `cancel_order(order_id)` is a tool (side effect, model decides). `file:///policies/refunds.md` is a resource (read-only, the app attaches it). `summarise_ticket` is a prompt (the user invokes it). Putting `cancel_order` behind a resource would hide a side effect in a "read".

**Code:** (toy registry, not the real SDK; method names mirror MCP's shape from general understanding)
```python
# Toy MCP-style server registry: tools, resources, prompts with list and dispatch. Not the real SDK.
class ToyServer:
    def __init__(self): self.tools, self.resources, self.prompts = {}, {}, {}
    # registration
    def tool(self, name, description, schema, fn): self.tools[name] = (description, schema, fn)
    def resource(self, uri, description, text): self.resources[uri] = (description, text)
    def prompt(self, name, description, template): self.prompts[name] = (description, template)
    # dispatch by method name, mirroring the *shape* of MCP methods
    def handle(self, method, params=None):
        params = params or {}
        if method == "tools/list":
            return [{"name": n, "description": d, "inputSchema": s} for n, (d, s, _) in self.tools.items()]
        if method == "tools/call":
            d, s, fn = self.tools[params["name"]]
            missing = [k for k in s.get("required", []) if k not in params.get("arguments", {})]
            if missing: return {"isError": True, "content": f"missing arguments: {missing}"}
            return {"isError": False, "content": fn(**params["arguments"])}
        if method == "resources/list":
            return [{"uri": u, "description": d} for u, (d, _) in self.resources.items()]
        if method == "resources/read": return self.resources[params["uri"]][1]
        if method == "prompts/list":
            return [{"name": n, "description": d} for n, (d, _) in self.prompts.items()]
        if method == "prompts/get": return self.prompts[params["name"]][1].format(**params.get("arguments", {}))
        raise KeyError(f"Method not found: {method}")

srv = ToyServer()
ORDERS = {"A1": "shipped"}
srv.tool("cancel_order", "Cancel an order (side effect!)", {"type": "object", "required": ["order_id"]},
         lambda order_id: ORDERS.__setitem__(order_id, "cancelled") or f"{order_id} cancelled")
srv.resource("file:///policies/refunds.md", "Refund policy (read-only reference)", "Refunds within 30 days.")
srv.prompt("summarise_ticket", "User-invoked template", "Summarise this ticket in {n} bullets.")

for m in ["tools/list", "resources/list", "prompts/list"]: print(m, "->", srv.handle(m))
print(srv.handle("tools/call", {"name": "cancel_order", "arguments": {"order_id": "A1"}}), ORDERS)
print(srv.handle("tools/call", {"name": "cancel_order", "arguments": {}}))
print(srv.handle("resources/read", {"uri": "file:///policies/refunds.md"}))
print(srv.handle("prompts/get", {"name": "summarise_ticket", "arguments": {"n": 3}}))
assert ORDERS["A1"] == "cancelled" and srv.handle("tools/call", {"name": "cancel_order", "arguments": {}})["isError"]
try: srv.handle("nope"); raise SystemExit("should fail")
except KeyError as e: print("unknown method ->", e)
```
Output (real run):
```
tools/list -> [{'name': 'cancel_order', 'description': 'Cancel an order (side effect!)', 'inputSchema': {'type': 'object', 'required': ['order_id']}}]
resources/list -> [{'uri': 'file:///policies/refunds.md', 'description': 'Refund policy (read-only reference)'}]
prompts/list -> [{'name': 'summarise_ticket', 'description': 'User-invoked template'}]
{'isError': False, 'content': 'A1 cancelled'} {'A1': 'cancelled'}
{'isError': True, 'content': "missing arguments: ['order_id']"}
Refunds within 30 days.
Summarise this ticket in 3 bullets.
unknown method -> 'Method not found: nope'
```

**Follow-ups:**
- *Why not make everything a tool?* Tool lists consume prompt tokens and confuse selection (Part 3 Q30); static context fits better as resources.
- *Can a resource be dynamic?* Yes, a URI can be backed by live data, but it stays a read.
- *What else can servers do?* The spec also has client features (sampling, roots) and utilities.

**Common mistakes:** treating all three as interchangeable; exposing writes as resources; trusting a tool's "read-only" annotation; giving the model unlimited tools.

### Q11 ⭐⭐⭐ 🟡 MCP vs function calling vs a plain REST API: how do they differ and when would you use each?
**Asked at:** all types; product, GenAI startups
**Say this first (1 line):** Function calling is a model API feature where the model emits a structured call that your code executes; MCP is a protocol that lets a host discover and connect to tools at runtime across applications and models; REST is an interface written for developers to call from code.
**Then explain:**
| | Function calling | MCP | REST API |
|---|---|---|---|
| What it is | model feature (structured call output) | client-server protocol (JSON-RPC) | HTTP interface for code |
| Who uses it | your app, with one model provider's format | any MCP host and server | developers |
| Discovery | you hand-write tool schemas into the request | `tools/list` at runtime | docs or OpenAPI, read by humans |
| Best for | one app, a few tools, you control everything | reusing tools across apps and models, many integrations | one integration, or a service with no MCP server |
- **They compose (general understanding, not from one source):** a host typically discovers tools from an MCP server and feeds the descriptors into the model's function-calling interface; when the model emits a call, the host forwards it with `tools/call`. So MCP does not replace function calling; it standardises where the tools come from.
- **MCP vs RAG (guide):** RAG for indexed knowledge retrieved by similarity; MCP for live lookups and actions.
- **Trade-off:** a direct API can be simpler and safer for one integration. MCP adds a moving part (a server, a protocol that is still evolving, new security surface such as tool poisoning, see Part 11).
- **Do not hand-wave provider details:** schema shapes differ by provider and change; check docs.

**Example:** An internal bot needs one internal endpoint, "get order status". Wrap it as a function in your function-calling loop (Part 3 Q8) and be done. A company wanting its CRM tools usable from three different AI apps writes one MCP server instead of three connectors.

**Code:** (adapter from an MCP-style descriptor to two illustrative function-calling shapes; the shapes are examples, verify each provider's current format)
```python
# Adapter: MCP-style tool descriptor -> generic function-calling schemas, then route a model's call back to MCP.
# Provider shapes differ and change: the two shapes below are illustrative; check each provider's docs.
mcp_tool = {"name": "get_order_status", "description": "Look up an order's status by id.",
            "inputSchema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}}

def to_nested_style(t):      # a "type: function" wrapper style
    return {"type": "function", "function": {"name": t["name"], "description": t["description"],
                                             "parameters": t["inputSchema"]}}
def to_flat_style(t):        # a flat style with a differently named schema key
    return {"name": t["name"], "description": t["description"], "input_schema": t["inputSchema"]}

def mcp_call(name, arguments):                       # stands in for an MCP tools/call round trip
    return {"isError": False, "content": f"{arguments['order_id']}: shipped"}

def route(model_call):                               # model emitted a structured call; the HOST executes it
    return mcp_call(model_call["name"], model_call["arguments"])

print(to_nested_style(mcp_tool)); print(to_flat_style(mcp_tool))
result = route({"name": "get_order_status", "arguments": {"order_id": "A1"}})   # scripted 'model' output
print(result)
assert to_nested_style(mcp_tool)["function"]["parameters"] == mcp_tool["inputSchema"]
assert to_flat_style(mcp_tool)["input_schema"] == mcp_tool["inputSchema"]
assert result["content"] == "A1: shipped"
```
Output (real run):
```
{'type': 'function', 'function': {'name': 'get_order_status', 'description': "Look up an order's status by id.", 'parameters': {'type': 'object', 'properties': {'order_id': {'type': 'string'}}, 'required': ['order_id']}}}
{'name': 'get_order_status', 'description': "Look up an order's status by id.", 'input_schema': {'type': 'object', 'properties': {'order_id': {'type': 'string'}}, 'required': ['order_id']}}
{'isError': False, 'content': 'A1: shipped'}
```

**Follow-ups:**
- *Does MCP make the model call tools?* No. The model proposes a call; the host executes it, as with function calling.
- *When is REST enough?* One stable integration, no need for runtime discovery or reuse.
- *Is MCP safer?* Not by itself; it adds trust and auth decisions (Q25 onwards).

**Common mistakes:** presenting them as competitors; saying MCP is a model feature; adopting MCP for a single endpoint; assuming schema formats are identical across providers.

### Q12 ⭐⭐⭐ 🟡 When do you use multiple agents instead of one? Cover orchestrator-worker designs, the token cost, and the main multi-agent failure modes.
**Asked at:** all types; agentic-AI loops; a Codemia guide lists this as an Amazon agentic-AI depth question (a guide, not a candidate report)
**Say this first (1 line):** Use multiple agents only when the task is valuable enough, parallelisable, bigger than one context window or needs many tools, because multi-agent systems cost far more tokens and add their own failure modes; otherwise a single agent or a workflow is better.
**Then explain:**
- **Anthropic's research system (vendor-reported):** a lead agent plans and spawns parallel sub-agents, then a citation agent. They report it beat a single-agent baseline by 90.2% on an internal research eval whose size and scoring were not described. Read it as one vendor's result in its own setting.
- **Token cost (reported):** about 4x the tokens for agents versus chat, and about 15x for multi-agent versus chat. On BrowseComp they report token usage alone explained 80% of the performance variance, and 95% together with tool calls and model choice. So part of the gain is simply spending more tokens.
- **Good fit:** heavy parallelisation, information beyond one context window, many tools, high-value tasks. **Poor fit:** tasks needing shared context or many dependencies between steps, such as most coding tasks, per the same post.
- **Failure modes (MAST, arXiv 2503.13657):** from 1,600+ annotated traces across 7 frameworks, the authors report that multi-agent gains on benchmarks are often minimal and define 14 failure modes in three categories: system design issues, inter-agent misalignment and task verification. I will not list the 14 from memory. Early failures Anthropic describes: spawning too many sub-agents for simple queries, endless searching, vague delegation causing duplicated work.
- **Mitigations:** explicit delegation with objective, output format and boundaries; effort-scaling rules; verification of sub-results; budgets (Q4).

**Example:** "Compare 12 competitors' pricing" splits cleanly across workers. "Fix a bug across 5 tightly linked files" does not, since workers need each other's edits. Under the assumed numbers below, multi-agent only pays off when a success is worth more than about $0.73; for cheap tasks it loses money.

**Code:** (ILLUSTRATIVE cost model: 4x and 15x are the reported multipliers used as example inputs; the baseline tokens, price, success rates and task value are ASSUMED)
```python
# Illustrative cost model. EVERY input marked ASSUMED is invented for the demo; the 4x and 15x multipliers are
# the token multipliers Anthropic REPORTED (agents vs chat, multi-agent vs chat) used here only as example inputs.
BASE_TOKENS = 2_000            # ASSUMED tokens for one chat answer
PRICE_PER_MTOK = 5.0           # ASSUMED blended USD per million tokens
MULT = {"chat": 1, "single_agent": 4, "multi_agent": 15}              # reported multipliers, illustrative
SUCCESS = {"chat": 0.40, "single_agent": 0.60, "multi_agent": 0.75}   # ASSUMED success rates
VALUE_PER_SUCCESS = 3.0        # ASSUMED USD value of one successful task

def economics(value=VALUE_PER_SUCCESS):
    rows = {}
    for k in MULT:
        cost = BASE_TOKENS * MULT[k] * PRICE_PER_MTOK / 1e6
        rows[k] = (cost, SUCCESS[k] * value, SUCCESS[k] * value - cost)
    return rows

def break_even_value(a, b):
    """Smallest value per success at which design b has higher net value than design a."""
    ca = BASE_TOKENS * MULT[a] * PRICE_PER_MTOK / 1e6; cb = BASE_TOKENS * MULT[b] * PRICE_PER_MTOK / 1e6
    return (cb - ca) / (SUCCESS[b] - SUCCESS[a])

for v in (VALUE_PER_SUCCESS, 0.05):
    print(f"value per success = ${v}")
    for k, (c, ev, net) in economics(v).items(): print(f"  {k:13s} cost=${c:.4f}  expected value=${ev:.4f}  net=${net:.4f}")
be = break_even_value("single_agent", "multi_agent")
print(f"multi-agent beats single agent only if value per success > ${be:.4f} (under these ASSUMED inputs)")
assert economics(3.0)["multi_agent"][2] > economics(3.0)["single_agent"][2]
assert economics(0.05)["multi_agent"][2] < economics(0.05)["single_agent"][2]
```
Output (real run):
```
value per success = $3.0
  chat          cost=$0.0100  expected value=$1.2000  net=$1.1900
  single_agent  cost=$0.0400  expected value=$1.8000  net=$1.7600
  multi_agent   cost=$0.1500  expected value=$2.2500  net=$2.1000
value per success = $0.05
  chat          cost=$0.0100  expected value=$0.0200  net=$0.0100
  single_agent  cost=$0.0400  expected value=$0.0300  net=$-0.0100
  multi_agent   cost=$0.1500  expected value=$0.0375  net=$-0.1125
multi-agent beats single agent only if value per success > $0.7333 (under these ASSUMED inputs)
```

**Follow-ups:**
- *Is a multi-agent system more accurate?* Not automatically; MAST reports minimal benchmark gains in many cases.
- *How do sub-agents share state?* Through the lead's instructions, shared files or a store; shared mutable state is a source of conflicts.
- *Alternative?* A workflow with orchestrator-workers (Q3) keeps control in code.

**Common mistakes:** multi-agent by default; quoting 90.2% without its setting; ignoring the token multiplier; vague delegation; no verifier.

### Q13 ⭐⭐⭐ 🟡 How do agents handle tool errors, hallucinated tool calls and retries (validation, feeding errors back, retry caps, circuit breakers)?
**Asked at:** product, GenAI startups, agent-building teams
**Say this first (1 line):** Validate every call against the schema before running it, catch exceptions in the host, return a short actionable error to the model, cap retries, trip a circuit breaker when a tool keeps failing, then fall back or escalate.
**Then explain:**
- **Hallucinated calls:** the model may invent a tool name or argument. Check the name and arguments against the schema (the `jsonschema` library does this) and reply with what is valid: "unknown tool 'get_ordr'. Available: [...]". Never execute unvalidated arguments.
- **Execution errors:** wrap the call in try/except in the host so a tool crash never kills the loop. Feed back a compact observation (what failed, whether retrying makes sense), not a stack trace.
- **Retry cap:** bound retries; one prep guide suggests three. Retry only transient errors (timeouts, 503) and, for side-effecting tools, only with idempotency keys (Part 3 Q28).
- **Circuit breaker:** after N consecutive failures stop calling that tool for a cooldown period, then allow a trial call. This stops the "agent loops forever on a failing tool" scenario (Q4) and protects the downstream service.
- **Fallbacks and escalation:** an alternative tool, cached data, a clear "I could not do X" with the partial result, or a human handoff.
- **Separate error kinds:** the model's mistake (fix and retry), a transient fault (retry with backoff), a permanent fault (stop). Details on failure modes and schemas: Part 3 Q27, Q28, Q29.

**Example:** The model calls `get_ordr`. The host replies "unknown tool; available: get_order", and the model corrects itself. Later the order service returns 503: the host retries up to 3 times, then the breaker opens, so further calls return "circuit open, use fallback or escalate" without touching the service until the cooldown ends.

**Code:** (stdlib, mock flaky tool, injectable clock, asserts pass; a minimal validator keeps it standalone, use `jsonschema` in production)
```python
# Validation + retry wrapper + circuit breaker against a flaky MOCK tool. Stdlib only, injectable clock, with tests.
# (In production use the jsonschema library; here a minimal validator keeps the demo standalone.)
class ToolError(Exception): pass
class CircuitOpen(Exception): pass

SCHEMAS = {"get_order": {"required": ["order_id"], "types": {"order_id": str}}}

def validate(name, args):
    if name not in SCHEMAS: return f"unknown tool '{name}'. Available: {sorted(SCHEMAS)}"   # hallucinated tool
    s = SCHEMAS[name]
    for k in s["required"]:
        if k not in args: return f"missing required argument '{k}'"
    for k, v in args.items():
        if k not in s["types"]: return f"unexpected argument '{k}'. Allowed: {sorted(s['types'])}"
        if not isinstance(v, s["types"][k]): return f"argument '{k}' must be {s['types'][k].__name__}"
    return None

class CircuitBreaker:
    def __init__(self, threshold=3, cooldown=30, clock=None):
        self.threshold, self.cooldown, self.clock = threshold, cooldown, clock
        self.failures, self.opened_at = 0, None
    def allow(self):
        if self.opened_at is None: return True
        if self.clock() - self.opened_at >= self.cooldown: self.opened_at = None; self.failures = 0; return True  # half-open: try again
        return False
    def ok(self): self.failures = 0
    def fail(self):
        self.failures += 1
        if self.failures >= self.threshold: self.opened_at = self.clock()

def call_tool(name, args, impl, breaker, max_retries=3):
    """Returns a compact observation dict for the model; never raises into the agent loop."""
    problem = validate(name, args)
    if problem: return {"ok": False, "error": problem, "retryable": False}       # fed back; model can fix its call
    if not breaker.allow(): return {"ok": False, "error": "tool temporarily disabled (circuit open); use fallback or escalate", "retryable": False}
    for attempt in range(1, max_retries + 1):
        try:
            res = impl(**args); breaker.ok(); return {"ok": True, "result": res, "attempts": attempt}
        except ToolError as e:
            last = str(e); breaker.fail()
            if not breaker.allow(): break                                        # breaker tripped mid-retry
    return {"ok": False, "error": f"tool failed after {attempt} attempts: {last}", "retryable": False}

# ---- mock flaky tool + tests ----
t = [0.0]; clock = lambda: t[0]
def make_flaky(fail_times):
    state = {"n": 0}
    def impl(order_id):
        state["n"] += 1
        if state["n"] <= fail_times: raise ToolError("503 upstream unavailable")
        return f"{order_id}: shipped"
    return impl, state

b = CircuitBreaker(clock=clock); impl, st = make_flaky(2)
r = call_tool("get_order", {"order_id": "A1"}, impl, b); assert r == {"ok": True, "result": "A1: shipped", "attempts": 3}
assert "unknown tool" in call_tool("get_ordr", {}, impl, b)["error"]                      # hallucinated name
assert "missing required" in call_tool("get_order", {}, impl, b)["error"]
assert "unexpected argument" in call_tool("get_order", {"order_id": "A1", "x": 1}, impl, b)["error"]
assert "must be str" in call_tool("get_order", {"order_id": 5}, impl, b)["error"]
b = CircuitBreaker(threshold=3, cooldown=30, clock=clock); impl, st = make_flaky(99)
r = call_tool("get_order", {"order_id": "A1"}, impl, b); print(r); assert not r["ok"] and st["n"] == 3
n_before = st["n"]; r = call_tool("get_order", {"order_id": "A1"}, impl, b)
print(r); assert "circuit open" in r["error"] and st["n"] == n_before                     # no call made while open
t[0] = 31.0; impl2, st2 = make_flaky(0); b.allow()                                          # cooldown over
assert call_tool("get_order", {"order_id": "A1"}, impl2, b)["ok"]
print("all tests passed")
```
Output (real run):
```
{'ok': False, 'error': 'tool failed after 3 attempts: 503 upstream unavailable', 'retryable': False}
{'ok': False, 'error': 'tool temporarily disabled (circuit open); use fallback or escalate', 'retryable': False}
all tests passed
```

**Follow-ups:**
- *Should the model see raw errors?* A compact, sanitised one; raw errors can leak internals or carry injected text (Part 11).
- *Backoff?* Exponential with jitter for transient faults; the demo omits sleeping to stay fast.
- *Breaker per tool or global?* Per tool (or per downstream service), so one failing dependency does not disable everything.

**Common mistakes:** unlimited retries; retrying non-idempotent writes blindly; passing stack traces to the model; no breaker so a down service is hammered; swallowing errors so the agent claims success.

