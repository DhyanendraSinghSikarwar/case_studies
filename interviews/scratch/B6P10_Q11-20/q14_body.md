**Say this first (1 line):** Little's law gives 60,000 calls over 8 hours = 2.08 calls a second x 180 seconds = 375 mean concurrent calls, which is 15 servers at full load, but I would plan about 18 to 22 because arrivals are random and the evenly-spread assumption hides a real peak.

**Clarifying questions:**
- Which tasks must the bot do (balance, card block, loan enquiry) and which must go to a human? Scope decides how risky an error is.
- How is the language mix: Hindi, Tamil, and mixed-language (code-switched) speech such as Hinglish? I need recorded test calls from each group, not just text.
- Is the 3-minute mean call length stable, and what share of calls end in a handoff? A longer or heavier tail raises concurrency (L = arrival rate x duration).
- What audio quality arrives (mobile, noisy, speaker phone)? Speech recognition errors dominate bad calls.
- Which identity or payment actions are allowed by voice? Ask compliance and legal what must be verified and recorded; I will not assume rules.

**Approach:**
1. Clarify and frame. Goal: resolve the top intents by voice with low friction and a safe handoff. Define "contained" (resolved without a human) and "safe" (no wrong action).
2. Metrics and guardrails. Containment, task success, word error rate by language, reply latency (the 1.5-second budget), handoff rate, repeat-call rate within 24 hours, customer satisfaction. Guardrails: wrong-action rate, authentication failures, abandon rate.
3. Data and labels. Collect consented, de-identified call audio with human transcripts per language, including code-mixed speech and noisy lines. Label intents and outcomes. Budget transcription by language, not in total, so minority languages are not starved.
4. Baseline first. A menu-style flow with a general speech-recognition model and an intent classifier for the top 5 intents; measure word error rate per language on a held-out set.
5. Model and trade-offs. Streaming speech recognition, an intent or dialogue model (a small model first, a larger language model only where needed), then streaming speech synthesis. Capacity by Little's law: 375 concurrent calls, 15 servers at 25 calls each at full load, 18 at the 99.9th percentile of random fluctuation, 22 with 30% headroom (see the code). Split the 1.5 seconds across recognition, understanding and synthesis.
6. Evaluation. Offline: word error rate and intent accuracy per language and per noise level; scripted test calls for sensitive intents. Online: a small share of live calls with easy handoff to a human, comparing containment and satisfaction against the human-only path.
7. Launch and experiment plan. Pilot one language and 2 intents on 5% of the window, then add languages when the per-language metrics clear a bar agreed with operations. Load-test to the planned concurrency before each ramp.
8. Monitoring, retraining and risks. Daily word error rate and latency by language; sampled call review; retrain recognition on corrected transcripts; alert on handoff and abandon spikes; fall back to a human line when servers saturate.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 6, 4, 11, 6, 5, 5.

**Metrics:**
- Concurrent calls L = arrival rate x mean duration = (60,000 / 28,800 s) x 180 s = 375.
- Servers = ceil(concurrent calls / calls per server): 15 at full load for the mean; more for the tail and for headroom.
- Word error rate per language = (substitutions + deletions + insertions) / words in the reference transcript.
- Containment = calls resolved without a human / all calls; wrong-action rate = wrong actions / actions taken.
- p95 reply latency = 95th percentile time from the caller finishing speaking to the first audio of the reply.

**Risks:**
- Little's law gives an average. Random fluctuation and uneven arrivals (a busy hour, salary day, an outage that triggers calls) push real concurrency above 375.
- Minority-language and mixed-language callers get worse recognition, so an overall average hides unfair service; always report per language.
- Voice cloning and fraud: a voice is a weak identity proof; ask compliance and security what verification is required.
- Recording and storing calls: consent, retention and privacy rules are for compliance and legal to confirm.
- A bot that traps callers in loops; always offer a human.

**What the interviewer scores:**
- Strong: 375 concurrent calls and 15 servers, then says that is the mean and adds headroom for variance and peaks.
- Strong: per-language evaluation, a latency split across the speech pipeline, and an easy human handoff.
- Strong: a staged rollout by language and intent, with load tests.
- Weak: one overall accuracy number, no per-language data, no capacity margin.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "I would use a large speech model that supports Indian languages, and 15 servers will do."
- Strong: "60,000 calls in 8 hours is about 2.1 calls a second, and a 3-minute call makes that 375 concurrent calls, so 15 servers only at full load. With random arrivals I would plan 18, and 22 with 30% headroom. I would measure word error rate separately for Hindi, Tamil and code-mixed callers on noisy lines, pilot one language on 5% of calls, and always keep a path to a human."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if calls get longer after launch? Concurrency scales with duration: 4-minute calls give 500 concurrent calls and 20 servers at full load, so watch mean call length as a capacity metric.
- How would you handle code-mixed speech? Collect and transcribe code-mixed audio, evaluate on it explicitly, and consider language-identification per utterance before routing.
- How do you control cost? Route simple intents to a small model, cap call length, and measure cost per contained call against the human-handled cost.

**Common mistakes:**
- Using calls per day divided by 24 hours when 60% fall in an 8-hour window.
- Forgetting that Little's law needs the arrival rate in the same time unit as the duration.
- Sizing at 100% utilisation with no headroom.
- Reporting a single overall word error rate.
