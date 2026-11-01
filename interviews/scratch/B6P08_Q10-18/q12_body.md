**Say this first (1 line):** Stop making it worse (no immediate retries, add backoff with jitter and a retry budget), then shift traffic to the fallback in small steps while checking its limits and its answers, because a fallback never used in production is untested.

**Clarifying questions:**
- Are the errors 429 (rate limit) or 5xx (provider trouble)? A 429 means our own volume matters; a 5xx means the provider is hurt and retries only add load.
- Does the provider status page or our own account dashboard show a quota issue on our side? It decides whether to ask for more quota or leave.
- What is the fallback's quota, prompt compatibility, price and data-handling agreement? Switching can break a contract or a privacy promise.
- How tolerant is the product of a slightly different answer (a support chatbot versus a structured JSON extractor)? It sets how much traffic can move.
- Is there a cached or rule-based degraded mode? It is the safest third option.

**Approach:**
1. First 15 minutes: confirm the error type from logs, post a status line, and cut the retry amplification. Immediate retries add load: with 25% failing and up to 3 retries, 40 calls per second becomes about 53 offered calls per second (+33%). If the cause is a hard rate cap, retries are worse (see the run: a crude model collapses).
2. Replace immediate retries with exponential backoff and jitter, honour `Retry-After` if present, and cap retries at about 10% extra calls (a retry budget). Add a circuit breaker: after a run of failures, stop calling for a short time.
3. First 30 minutes: ramp the fallback: 5% of traffic, then 10%, then 25%, watching its error rate, latency, token cost and a quality check (JSON validity, a small canned evaluation set, thumbs-down rate). Do not flip 100% at once.
4. Escalate to the incident lead and the vendor contact at about minute 15 if error rate is still above 10%. Roll the fallback back if its error rate is above the primary's, its output fails the validity check more than a small margin (for example 2% absolute), or cost per call exceeds the pre-agreed ceiling.
5. Shed or degrade low-value traffic (batch jobs, background summaries) first and keep interactive users.
6. First day: restore the primary slowly (ramp 10, 25, 50, 100%) so we do not trigger the limit again. Confirm customers who got fallback answers were not harmed (a different model, different language, different safety behaviour).
7. Next quarter: run a fallback game day twice a year, keep the fallback warm with 1 to 5% real traffic, write prompts and tests that pass on both providers, negotiate quota in both accounts, and add a per-provider SLO.
8. Blameless postmortem: "the fallback had never been used" is the finding, not a person. Action items: warm traffic, quota check, retry budget in the client library.

**Metrics:**
- Failure rate = failed calls / all calls (here 10 / 40 = 25%).
- Retry amplification = total calls sent / original requests (1.33 under independent failures at 25%).
- Goodput = successful calls per second; compare before and after.
- Final failure rate after retries (user-visible): 0.25^4 = 0.39% if failures were independent, but rate limits are not independent.
- Fallback guardrails: error rate, p95 latency, cost per 1,000 calls, output validity rate.

**Risks:**
- The fallback has its own quota; moving 100% of traffic may just move the outage.
- Different model means different tone, formatting, refusals and cost; silent quality loss does not show in HTTP success.
- A different region or vendor may break a data-residency or privacy commitment.
- Prompt and tool-calling formats may not match (editor knowledge: providers differ in function-call formats).
- Retry storms: many clients retry at the same moment unless jittered.

**What the interviewer scores:**
- Strong: names retry amplification and gives the number; adds backoff, jitter, retry budget and a circuit breaker.
- Strong: ramps the fallback with checks for quota, cost and quality, and has rollback criteria.
- Strong: first 15 minutes, first day and next quarter are separate; blameless action items.
- Weak: "switch to the backup" with no ramp; "increase retries".

**Example:** Illustrative numbers. Weak versus strong:
- Weak: "I would retry more times and, if that fails, point everything to the other provider."
- Strong: "First I stop the immediate retries, because they push 40 calls a second to about 53. Then backoff with jitter and a 10% retry budget. I send 10% of traffic to the second provider and check its quota, cost and answer validity before 25%. If its error rate is worse than the primary's or JSON validity drops by more than 2 points, I send traffic back and shed batch work instead."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Why does the fallback need a small ramp? It may have a lower limit (here 20 calls per second against 40 needed); a ramp finds that safely.
- How do you detect silent quality loss? Compare output validity and a golden test set on fallback traffic, and sample outputs for review; HTTP 200 does not tell you.
- Should clients retry 429s? Only after the `Retry-After` time and within a budget; otherwise slow down or shed.

**Common mistakes:**
- Increasing retries during a rate-limit incident.
- Switching 100% to a never-tested fallback.
- Ignoring cost and data-handling differences.
- No rollback criteria for the fallback.
