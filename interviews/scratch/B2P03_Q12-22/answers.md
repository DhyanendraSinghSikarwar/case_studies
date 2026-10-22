### Q12 ⭐⭐⭐ 🟡 Code: validate LLM JSON output against a schema, repair or retry with a bounded budget, and fail closed when retries run out.
**Asked at:** product, GenAI startups, live-coding rounds
**Say this first (1 line):** Parse, validate against a schema, and on failure retry at most twice while feeding the exact error back; if it still fails, raise and do not pass on a guess (fail closed).

**Then explain:**
- **Cheap repair first, retry second.** Strip markdown fences and surrounding chatter in code. That costs nothing. Only call the model again when parsing or validation still fails.
- **Validate shape and rules, not just JSON syntax.** A pydantic v2 model (or `jsonschema`) catches wrong types, missing fields, enums, ranges. `model_validate_json` handles bad JSON and bad schema in one exception type.
- **Bounded budget.** One first call plus at most 2 retries. Each retry adds the previous output and the concrete validation error, so the model knows what to fix. Unbounded retries burn money and latency and can loop forever.
- **Fail closed.** After the budget, raise a typed error. The caller decides: send to a human queue, return a safe default, or show an error. Never "best-effort" parse and continue, because downstream code will trust the data.
- **Log every attempt** (raw output, error, attempt number) so you can measure the retry rate. A rising retry rate is a prompt or model regression signal.
- Schema-valid is still not truth (see Q10). If your provider supports strict structured outputs or constrained decoding (Q7, Q22), use that first and keep this as the safety net.

**Example (run):** the mock model returns a bad value (`"total": "n/a"`) first and a fenced good JSON second. We get a valid object after 1 retry. With three bad outputs in a row, the function raises `FailClosed` after 3 calls total.

**Code:** (executed, python3 with pydantic v2; the model is a mock, no real API)
```python
import json, re
from pydantic import BaseModel, Field, ValidationError

class Invoice(BaseModel):
    vendor: str = Field(min_length=1)
    total: float = Field(ge=0)
    currency: str = Field(pattern="^(INR|USD|EUR)$")

FENCE = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.S)

def parse(raw: str) -> Invoice:
    text = raw.strip()
    m = FENCE.match(text)
    if m:
        text = m.group(1)
    return Invoice.model_validate_json(text)      # raises ValidationError (covers bad JSON too)

class FailClosed(Exception):
    pass

def call_with_retries(model, prompt, max_retries=2):
    messages = [prompt]
    last_err = None
    for attempt in range(1 + max_retries):         # 1 first try + at most 2 retries
        raw = model(messages)
        try:
            return parse(raw), attempt
        except ValidationError as e:
            last_err = e.errors(include_url=False, include_input=False)
            # feed back the concrete error, not just "try again"
            messages = messages + [raw, f"Invalid: {last_err}. Return only corrected JSON."]
    raise FailClosed(f"gave up after {1 + max_retries} calls: {last_err}")

def make_mock(outputs):
    it = iter(outputs)
    return lambda messages: next(it)

bad1 = '{"vendor": "Acme", "total": "n/a", "currency": "INR"}'
bad2 = 'Sure! Here is the JSON: {"vendor": "Acme"'
good = '```json\n{"vendor": "Acme", "total": 1250.5, "currency": "INR"}\n```'

inv, n = call_with_retries(make_mock([bad1, good]), "extract invoice")
print("success-after-retry:", inv, "retries used:", n)

try:
    call_with_retries(make_mock([bad1, bad2, bad2]), "extract invoice")
except FailClosed as e:
    print("fail-closed:", str(e)[:110])
```
Output from my run:
```
success-after-retry: vendor='Acme' total=1250.5 currency='INR' retries used: 1
fail-closed: gave up after 3 calls: [{'type': 'json_invalid', 'loc': (), 'msg': 'Invalid JSON: expected value at line 1 col
```

**Follow-ups:**
- *Why feed the error back?* A bare "try again" often repeats the same mistake; the specific error ("total: input should be a valid number") gives the model something to fix.
- *Retry at temperature 0?* The same prompt gives (nearly) the same output, so changing the prompt (error feedback) matters more than resampling. Some teams raise temperature slightly on retries; test it.
- *Where do you put the retry budget?* In your application layer, per request, together with a timeout; do not rely on a provider SDK's hidden retries for output-validation failures.

**Common mistakes:** retrying forever; catching the exception and returning partial data; using `json.loads` only and skipping schema checks; forgetting fences or a prose prefix; not logging failures; treating a truncated output (finish reason `length`, see Q21) as a model error rather than raising `max_tokens`.

### Q13 ⭐⭐ 🟡 How do you select and order few-shot examples (coverage, label balance, recency bias, dynamic selection by retrieval)?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** Pick examples that cover the real input types and edge cases, keep labels balanced, test the order because models lean on the last examples, and when the pool is large pick the k most similar examples per query (kNN retrieval).
**Then explain:**
- **Coverage:** include each label, the common formats, and one or two hard or edge cases (empty field, abbreviation, a near-miss between two classes). Examples teach the format and the decision boundary, so they should look like production traffic (see Q1).
- **Label balance:** if 4 of 5 examples are "positive", the model drifts toward "positive". Keep labels roughly balanced, or match the real prior only if you want that bias.
- **Order and recency bias:** order can change results, and the last examples often have more pull. Do not trust one order: shuffle with several seeds on a golden set (Q6) and check the variance. A common default is hardest or most relevant example last.
- **Dynamic selection:** embed the query and the example pool, take the top-k nearest, put them in the prompt. It adapts to each input, but it can pick near-duplicates, all one label, or a wrong-label neighbour, and it makes outputs harder to cache and debug. Combine similarity with a diversity or per-label cap.
- **Cost:** every example is input tokens on every call. Past a few examples gains flatten; measure k = 0, 2, 4, 8 rather than assuming more is better. Static examples at the start also keep the prefix cacheable (Part 1 Q24).
- Examples must be correct and consistent. One mislabelled example is copied.

**Example (run, toy):** a pool of 10 support tickets, query "my card was charged twice and I need a refund". Bag-of-words cosine similarity (stopwords dropped) picks three billing tickets with scores 0.00, 0.26, 0.55, ordered so the most similar sits last. The balanced variant (max 2 per label, k=4) returns `['bug','bug','billing','billing']`: balance forced in zero-similarity filler. That is the trade-off in miniature, and with a bigger pool the filler would be better. Before I added a stopword filter, the same toy picked a "bug" and a "how_to" ticket just because they shared "I" and "my". Real systems use embeddings, not word counts.

**Code:** (executed; toy, bag-of-words cosine, not a real embedding model)
```python
# Toy: kNN few-shot selection with bag-of-words cosine similarity (a toy, not a real embedding model)
import math, re
from collections import Counter

POOL = [
    ("I want my money back, the card was charged twice", "billing"),
    ("refund has not arrived after 10 days", "billing"),
    ("invoice shows the wrong amount", "billing"),
    ("app crashes when I open the camera", "bug"),
    ("login button does nothing on android", "bug"),
    ("page freezes after I upload a photo", "bug"),
    ("how do I change my email address", "how_to"),
    ("where can I download my statement", "how_to"),
    ("can you add dark mode please", "feature"),
    ("please support export to excel", "feature"),
]

STOP = {"i", "my", "me", "the", "a", "and", "to", "of", "can", "you", "how", "do", "after", "when", "where", "is", "was", "has", "not"}

def bow(text, drop_stop=True):
    toks = re.findall(r"[a-z]+", text.lower())
    return Counter(t for t in toks if not (drop_stop and t in STOP))

def cosine(a, b):
    dot = sum(a[w] * b[w] for w in a)
    na = math.sqrt(sum(v * v for v in a.values())); nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0

def pick_k(query, pool, k=3):
    q = bow(query)
    scored = sorted(pool, key=lambda ex: cosine(q, bow(ex[0])), reverse=True)[:k]
    return scored[::-1]          # most similar LAST (closest to the query, a common ordering choice; test it)

query = "my card was charged twice and I need a refund"
chosen = pick_k(query, POOL, k=3)
for text, label in chosen:
    print(f"{cosine(bow(query), bow(text)):.2f}  {label:8s} {text}")
print("labels in order:", [l for _, l in chosen])

# Balance check: kNN can pick all one label. Guard: cap per-label count.
def pick_k_balanced(query, pool, k=3, per_label=2):
    q = bow(query); out, seen = [], Counter()
    for ex in sorted(pool, key=lambda e: cosine(q, bow(e[0])), reverse=True):
        if seen[ex[1]] < per_label:
            out.append(ex); seen[ex[1]] += 1
        if len(out) == k: break
    return out[::-1]
print("balanced labels:", [l for _, l in pick_k_balanced(query, POOL, k=4, per_label=2)])
```
Output from my run:
```
0.00  billing  invoice shows the wrong amount
0.26  billing  refund has not arrived after 10 days
0.55  billing  I want my money back, the card was charged twice
labels in order: ['billing', 'billing', 'billing']
balanced labels: ['bug', 'bug', 'billing', 'billing']
```

**Follow-ups:**
- *Dynamic vs static examples?* Static is simpler, cacheable and reproducible; dynamic wins when inputs vary a lot. Evaluate both on a held-out set.
- *How do you check order sensitivity?* Run the same examples in several shuffled orders and compare accuracy; a large spread means the prompt is fragile.
- *Should examples include the reasoning?* Only for tasks that need it (Q14).

**Common mistakes:** unbalanced labels; examples all from one easy cluster; picking neighbours by similarity only, so the pool leaks near-duplicates of the test item (data leakage in evaluation); never testing order; using more examples than the task needs.

### Q14 ⭐⭐ 🟡 Zero-shot CoT, few-shot CoT, self-consistency and reasoning models: when does explicit "think step by step" prompting help, and when is it counter-productive?
**Asked at:** product, big tech, GenAI startups
**Say this first (1 line):** Explicit step-by-step helps non-reasoning models on multi-step problems (maths, logic, multi-hop), but it is wasted or harmful on simple tasks and on reasoning models that already think before answering.
**Then explain:**
- **Zero-shot CoT:** add "Let's think step by step" or "reason before answering". Cheap, no examples. Basic CoT is in Q3.
- **Few-shot CoT:** your examples include worked reasoning, so the model copies the style and depth. Better control of format, but costs tokens and the examples must be correct.
- **Self-consistency:** sample several reasoning paths at temperature above 0 and majority-vote the final answers. It is N times the cost; details and test-time compute are in Part 2 Q42 and Q43.
- **Reasoning models:** these models produce internal reasoning before the answer. Providers generally advise a clear goal and constraints rather than scripting the steps; "think step by step" adds little and can interfere. Check your provider's current guidance, it changes. Control effort with the provider's reasoning-effort or thinking-budget setting instead (names vary, check the docs).
- **When explicit CoT hurts:** simple lookups, classification, extraction (extra tokens, latency, more room to talk itself into a wrong answer); strict output formats (reasoning leaks into the JSON, so separate a `reasoning` field from the `answer` field or strip it); latency-critical paths; showing users raw reasoning that may be wrong or expose internals. Visible reasoning is also not always a faithful explanation of how the model got the answer, so do not treat it as an audit trail.
- **Decision:** measure on a golden set (Q6): no CoT vs CoT vs reasoning model, comparing accuracy, p95 latency and cost per request.

**Example:** a 4-step word problem on a standard chat model: zero-shot answer is often wrong, CoT fixes many cases. Sentiment of a one-line review: CoT adds 150 tokens and no accuracy. On a reasoning model, the same word problem needs only the problem statement. (Illustrative pattern, not a measured result of mine.)

**Code:** not executed: prompting patterns, no model API available here.
```text
Zero-shot CoT:  "...Think through the steps, then give the final line as 'Answer: <number>'."
Few-shot CoT:   Q: ... / Reasoning: ... / Answer: 42   (x 2-3 examples)
Parse safely:   take only the text after the last "Answer:"; never parse the reasoning.
```

**Follow-ups:**
- *Is self-consistency worth it?* Only when accuracy gain justifies N times cost, and answers can be compared (numbers, labels). See Part 2 Q42.
- *Can you get reasoning without the latency?* Distilled or smaller models, shorter budgets, caching, or reasoning only for hard cases routed by a cheap classifier.
- *Should reasoning be shown to users?* Usually a short rationale you control, not raw chain-of-thought.

**Common mistakes:** adding CoT everywhere by habit; using it on reasoning models and paying twice; parsing the final answer from free text; assuming the shown reasoning explains the answer; skipping the A/B on a golden set.

### Q15 ⭐⭐ 🟡 What is ReAct prompting (thought, action, observation) and how does it differ from plain chain-of-thought?
**Asked at:** all types; agentic-AI loops
**Say this first (1 line):** ReAct interleaves reasoning with actions: the model writes a thought, calls a tool, reads the observation, and repeats until it can answer, so its reasoning is grounded in outside information, unlike CoT, which reasons from memory alone.
**Then explain:**
- **Loop:** Thought (what do I need), Action (tool name and input), Observation (tool result, inserted by your code, not the model), repeat, then Final answer.
- **CoT vs ReAct:** CoT is one pass of reasoning inside the model, so it can hallucinate facts. ReAct can look things up or compute, so facts come from tools, and the trace shows what was done. Cost: more calls, more latency, a growing context.
- **Your code owns the loop:** parse the action, validate the tool name and arguments, run it, append the observation, enforce a step limit. Never let the model write observations. Modern APIs do this with native tool calling (Q8, Q11) rather than text parsing, but the pattern is the same.
- **Failure modes:** infinite or repeated calls (same search again), wrong tool or bad arguments, a bad early observation that the model trusts and compounds, context growth, and prompt injection via tool results (Part 11). Guards: max steps, repeated-action detection, validated tools, timeouts, and a clear "stop and answer or say you cannot" rule.
- Planning, memory, and multi-agent designs build on this: Part 8.

**Example (run, mock):** "What is half of Kerala's population?" The scripted mock model searches (mock data: 35 million), then calculates 35/2, then answers 17.5 million. The second run uses a model that repeats the same search; the loop guard stops it with `STOP: repeated action`. The population figure is mock data, not a real statistic.

**Code:** (executed, plain Python; the model is scripted and the tools are fakes; `eval` is a toy, never use it on untrusted input)
```python
# ReAct loop with a MOCK model (scripted) and fake tools. Plain Python.
import re

TOOLS = {
    "search": lambda q: {"population of kerala": "Kerala population: about 35 million (mock data)"}.get(q.lower(), "no result"),
    "calc": lambda expr: str(eval(expr, {"__builtins__": {}})),   # toy only: never eval untrusted input
}

SCRIPT = iter([
    "Thought: I need Kerala's population.\nAction: search[population of kerala]",
    "Thought: Now divide by 2 for half.\nAction: calc[35/2]",
    "Thought: I have the answer.\nFinal: about 17.5 million",
])
def mock_model(transcript):
    return next(SCRIPT)

def react(question, max_steps=5):
    transcript = f"Question: {question}"
    seen_actions = set()
    for step in range(1, max_steps + 1):
        out = mock_model(transcript)
        transcript += "\n" + out
        print(f"[step {step}]\n{out}")
        if "Final:" in out:
            return out.split("Final:")[1].strip()
        m = re.search(r"Action: (\w+)\[(.*)\]", out)
        if not m or m.group(1) not in TOOLS:
            return "STOP: invalid action"
        key = (m.group(1), m.group(2))
        if key in seen_actions:                      # loop guard: same call twice
            return "STOP: repeated action"
        seen_actions.add(key)
        obs = TOOLS[key[0]](key[1])
        print(f"Observation: {obs}")
        transcript += f"\nObservation: {obs}"
    return "STOP: step budget exhausted"

print("RESULT:", react("What is half of Kerala's population?"))

# Failure mode: a model that repeats itself. The guard stops it.
looper = lambda t: "Thought: try again.\nAction: search[kerala gdp]"
mock_model = looper
print("RESULT:", react("loop demo"))
```
Output from my run:
```
[step 1]
Thought: I need Kerala's population.
Action: search[population of kerala]
Observation: Kerala population: about 35 million (mock data)
[step 2]
Thought: Now divide by 2 for half.
Action: calc[35/2]
Observation: 17.5
[step 3]
Thought: I have the answer.
Final: about 17.5 million
RESULT: about 17.5 million
[step 1]
Thought: try again.
Action: search[kerala gdp]
Observation: no result
[step 2]
Thought: try again.
Action: search[kerala gdp]
RESULT: STOP: repeated action
```

**Follow-ups:**
- *Why not just one big prompt with all the facts?* If the needed facts are unknown ahead of time, or too big, tools or retrieval fetch them on demand.
- *How do you stop loops?* Step cap, repeated-call detection, a total token or time budget, and a fallback answer.
- *Does ReAct need text parsing today?* Not with native tool calling; the structured call replaces the "Action: x[y]" text.

**Common mistakes:** letting the model fabricate observations; no step limit; not validating tool arguments; unbounded context growth; trusting tool output as instructions; describing ReAct as just "CoT with tools" without the grounding point.

### Q16 ⭐⭐ 🟡 Task decomposition and prompt chaining versus one big prompt: when do you split, and how do you choose the decomposition?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** Split when one prompt is failing on distinct sub-tasks, needs different tools, formats or models per stage, or needs a checkpoint in the middle; keep one prompt when the task is simple, because every extra call adds cost, latency and a place for errors to compound.
**Then explain:**
- **Signals to split:** the prompt has many rules and the model drops some; one stage needs strict JSON while another needs free text; different stages suit different model sizes (cheap classifier first, strong model last); you need to inspect or validate an intermediate result; a stage needs retrieval or a tool.
- **How to choose the cut:** by output type or decision point (classify, extract, decide, write), not by arbitrary length. Each step should have one clear input and one checkable output. Measure each step separately on a golden set (Q6), so you know which stage fails.
- **Error propagation:** if step 1 is 90% right and step 2 is 90% right on good input, the chain is at most about 81% before step 2 ever sees a bad input. So put validation gates between steps (schema check, rule check, confidence threshold) and stop or escalate on failure instead of passing garbage on.
- **Cost and latency:** N sequential calls add latency roughly N times. Mitigate: run independent steps in parallel, use small models for easy stages, cache stable prefixes (Part 1 Q24).
- **Alternatives:** one prompt with sections (Q4), a self-critique second pass, or an agent that picks steps dynamically (Part 8). A fixed chain is more predictable and easier to test than an agent; use an agent only when the path really varies.

**Example (run, mock):** support ticket to reply. Step 1 extracts fields, a code gate validates them, step 2 drafts a reply from the validated fields only. A ticket with data goes through in 2 LLM calls; a vague ticket fails the gate after 1 call and goes to a human, so the reply step never invents an amount.

**Code:** (executed; mock steps, no real LLM)
```python
# Prompt-chain skeleton with MOCK steps: extract -> validate -> summarise. No real LLM.
import json

def mock_extract(text):            # step 1: pretend LLM extracts fields as JSON
    return '{"customer": "Asha", "issue": "double charge", "amount": 499}' if "charged" in text else "I could not find fields"

def validate_extract(raw):         # gate between steps: cheap code check
    d = json.loads(raw)            # raises on bad JSON
    assert isinstance(d.get("amount"), (int, float)) and d["amount"] > 0, "amount must be a positive number"
    assert d.get("issue"), "issue missing"
    return d

def mock_reply(d):                 # step 2: pretend LLM drafts a reply from VALIDATED fields only
    return f"Hi {d['customer']}, we are sorry about the {d['issue']} of Rs {d['amount']}. A refund is on its way."

def chain(ticket):
    calls = 0
    try:
        raw = mock_extract(ticket); calls += 1
        fields = validate_extract(raw)            # stop here instead of propagating garbage
    except (ValueError, AssertionError) as e:     # json.JSONDecodeError is a ValueError
        return {"status": "escalate_to_human", "why": f"step 1 invalid: {e}", "llm_calls": calls}
    reply = mock_reply(fields); calls += 1
    return {"status": "ok", "reply": reply, "llm_calls": calls}

print(chain("Customer Asha was charged twice for Rs 499"))
print(chain("hello, just checking in"))
```
Output from my run:
```
{'status': 'ok', 'reply': 'Hi Asha, we are sorry about the double charge of Rs 499. A refund is on its way.', 'llm_calls': 2}
{'status': 'escalate_to_human', 'why': 'step 1 invalid: Expecting value: line 1 column 1 (char 0)', 'llm_calls': 1}
```

**Follow-ups:**
- *Does chaining always beat one prompt?* No. Test both; strong models handle many multi-part prompts fine, and chains add latency.
- *How do you debug a chain?* Log every intermediate input and output per step with a trace id, and evaluate each stage on its own.
- *Where does structured output fit?* At each handoff: validated JSON between steps (Q12).

**Common mistakes:** splitting everything by habit; no validation between steps; passing the whole raw history to every step; evaluating only the final answer; ignoring the latency of sequential calls.

### Q17 ⭐⭐ 🟡 How should a prompt handle ambiguity and missing information (fallback behaviour, clarifying questions, defaults, missing tool parameters)?
**Asked at:** product, GCC, customer-facing assistants
**Say this first (1 line):** Decide per field whether to ask, assume a safe default, or refuse, write that policy in the prompt, and for tools validate required parameters in code, because models may guess a missing value instead of asking.
**Then explain:**
- **Three options:** (1) *Ask a clarifying question* when the missing piece changes the outcome or the action is costly or irreversible (booking, payment, delete). (2) *Assume a default and state it* when the choice is low-risk and cheap to correct ("I assumed INR; tell me if not"). (3) *Say you cannot answer* when the information is not in the provided context (Q5).
- **Put the policy in the prompt:** "If the date is missing, ask for it. Never invent dates or amounts. If the question is ambiguous between two readings, ask one short question listing them." Give one example of each behaviour (Q1).
- **Keep it cheap for the user:** one targeted question, not a questionnaire; offer options; do not ask when the answer is obvious from context or earlier turns.
- **Missing tool parameters:** the Anthropic tool-use docs note that when a required parameter is missing, behaviour varies by model and a model may guess a value. So do not rely on the model to ask. Your code checks required fields against the schema (and, for risky fields, that the value is grounded in what the user said), and if anything is missing it returns a question to the user without executing the tool. Strict schema modes (check the current docs, these change) constrain shape, but a value that fits the schema can still be invented.
- **Evaluate it:** add test cases with missing and ambiguous inputs to the golden set and count "asked when it should", "asked when it should not", and "guessed".

**Example (run, mock):** the user says "Book me a flight from BLR to DEL" with no date. The mock model returns a call with an invented date. The validator flags `date` as not grounded in the user message and returns `ASK USER: please confirm date`; no booking is made. With the date in the message, the call executes. The grounding check is a toy substring test, a real system would compare against parsed dates.

**Code:** (executed; model mocked, toy grounding check)
```python
# Validate required tool parameters in code; if missing, ask the user instead of executing. Model is MOCKED.
import json

TOOL_SCHEMA = {"name": "book_flight", "required": ["origin", "destination", "date"]}

def mock_model_call(user_msg):
    # A model may guess a missing value instead of asking (provider docs note this varies by model).
    # Mock the bad case: user gave no date, model invents one.
    return {"name": "book_flight", "arguments": {"origin": "BLR", "destination": "DEL", "date": "2026-11-01"}}

def missing_required(call, schema, user_msg):
    args = call["arguments"]
    missing = [p for p in schema["required"] if p not in args or args[p] in (None, "")]
    # Extra guard for guessed values: the value must be grounded in the user text (toy check)
    ungrounded = [p for p in ("date",) if p in args and args[p] not in user_msg]
    return missing, ungrounded

def handle(user_msg):
    call = mock_model_call(user_msg)
    missing, ungrounded = missing_required(call, TOOL_SCHEMA, user_msg)
    if missing or ungrounded:
        need = missing + ungrounded
        return f"ASK USER: please confirm {', '.join(need)}"      # no side effect executed
    return f"EXECUTE {json.dumps(call['arguments'])}"

print(handle("Book me a flight from BLR to DEL"))
print(handle("Book me a flight from BLR to DEL on 2026-11-01"))
```
Output from my run:
```
ASK USER: please confirm date
EXECUTE {"origin": "BLR", "destination": "DEL", "date": "2026-11-01"}
```

**Follow-ups:**
- *Ask or assume?* Ask when wrong is costly or the options differ a lot; assume when wrong is cheap and easy to fix.
- *Multi-turn?* Keep the answer in state so you never ask twice.
- *Voice or one-shot APIs with no user to ask?* Return a structured `needs_info` result for the caller to handle.

**Common mistakes:** letting the model silently guess; asking too many questions; no policy for "not in context"; assuming schema validation catches invented-but-valid values; not testing ambiguous inputs.

### Q18 ⭐⭐ 🟡 What is context engineering? How do you decide what goes into the context window, and how do you manage long-running conversations (rolling summary vs retrieval)?
**Asked at:** product, GenAI startups, big tech
**Say this first (1 line):** Context engineering is deciding what information goes into the model's input on each call (instructions, tools, retrieved facts, history, examples) and in what order, within a token budget, so the model has what it needs and nothing that distracts it.
**Then explain:**
- **What to include:** stable instructions and policies, the current task, only the facts needed (retrieved, not dumped), a few examples, tool definitions the task may need, and recent conversation. Ask for each item: would the answer change without it?
- **Ordering:** stable content first (system prompt, tools, examples) so prefix caching works (Part 1 Q24); long documents before the question; key instructions at the start and repeated or restated at the end for long contexts, since the middle is used less reliably (Part 1 Q19).
- **Trimming:** set a token budget per section (for example, cap retrieval at a share of the window), drop lowest-scored chunks first, keep the newest turns contiguous, and always keep system prompt and the current question. Count tokens with the provider's tokenizer.
- **Rolling summary vs retrieval:** a summary is compact and keeps the narrative, but it is lossy and errors persist (a wrong summary poisons later turns). Retrieval over past turns or stored facts keeps exact details and scales, but needs good queries and can miss context. Common design: recent turns verbatim, a rolling summary of older ones, and a store of key facts or decisions retrieved on demand. Long-term memory belongs to Part 8; retrieval to Parts 6-7.
- **More is not better:** extra context costs money and latency and can distract; irrelevant or conflicting text hurts accuracy. Treat retrieved text and tool outputs as untrusted data (Part 11).

**Example (run):** a trimmer with word count as a proxy for tokens. With a budget of 200 it keeps the system prompt, summary and question, 2 of 3 retrieved chunks (the low-score "noise" chunk is dropped), and the 4 newest of 10 turns (182 used, 6 dropped). With a budget of 400 it keeps all 3 chunks and all 10 turns (354 used).

**Code:** (executed, plain Python; word count is a proxy, use the provider's real tokenizer in production)
```python
# Token-budget trimmer. Word count is only a PROXY for tokens (real tokenizers differ: use the provider's counter).
def n_tokens(text):
    return len(text.split())

def build_context(system, summary, retrieved, history, question, budget):
    """Always keep system + question. Then add retrieved chunks by score, then newest history turns,
    stopping when the budget would be exceeded. Older history is represented by the rolling summary."""
    used = n_tokens(system) + n_tokens(question) + n_tokens(summary)
    assert used <= budget, "fixed parts alone exceed budget"
    kept_chunks, kept_turns = [], []
    for score, chunk in sorted(retrieved, reverse=True):          # best chunks first
        if used + n_tokens(chunk) <= budget * 0.6:                 # cap retrieval share at 60% of budget
            kept_chunks.append(chunk); used += n_tokens(chunk)
    for turn in reversed(history):                                 # newest turns first
        if used + n_tokens(turn) <= budget:
            kept_turns.insert(0, turn); used += n_tokens(turn)
        else:
            break                                                  # keep a contiguous recent window
    return {"used": used, "chunks": len(kept_chunks), "turns": len(kept_turns),
            "dropped_turns": len(history) - len(kept_turns)}

history = [f"turn {i}: " + "word " * 20 for i in range(10)]        # 10 turns x 22 words
retrieved = [(0.9, "policy " * 40), (0.7, "faq " * 40), (0.2, "noise " * 40)]
print(build_context("You are a support bot.", "Earlier: user asked about refunds.", retrieved, history,
                    "Where is my refund?", budget=200))
print(build_context("You are a support bot.", "Earlier: user asked about refunds.", retrieved, history,
                    "Where is my refund?", budget=400))
```
Output from my run:
```
{'used': 182, 'chunks': 2, 'turns': 4, 'dropped_turns': 6}
{'used': 354, 'chunks': 3, 'turns': 10, 'dropped_turns': 0}
```

**Follow-ups:**
- *When summarise vs retrieve?* Summarise for continuity and tone; retrieve for exact facts, IDs, numbers.
- *How do you evaluate context choices?* Ablate: remove a section and check the golden set; track answer quality versus context size.
- *Does a bigger window remove the problem?* No: cost, latency and degraded use of long contexts remain.

**Common mistakes:** stuffing everything in; trimming from the front and losing the system prompt; summaries that drop numbers or constraints; no token budget; counting words and treating them as tokens; putting volatile content before stable content and breaking the cache.

