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

