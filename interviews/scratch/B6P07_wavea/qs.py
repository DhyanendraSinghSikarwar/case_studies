# Question data for Book 6 Part 7. Tuple: (stars, difficulty, scenario text, asked-key). All numbers are invented illustrative numbers.
# Prices are invented round figures per million tokens in one unnamed currency unit, not any vendor's prices.
import math
NS = "; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened"
ED = "No public page found for this exact scenario, editor-designed; the theme is adjacent to "
AS = {
 'G': "GenAI and LLM-engineer interview guides (InterviewBit, Hyring, Let's Code, recrew, Pensero and Towards AI 2026 pages list RAG, hallucination mitigation, evaluation and cost or latency topics; one guide reports a prompt about a RAG answer that is wrong although the right document exists, and another a smaller-model-for-narrow-tasks answer pattern)" + NS,
 'R': "RAG-debugging pages (Latitude, Educative, Redis, Fiddler and ChatRAG pages on locating the failing stage, stale indexes, retrieval recall versus faithfulness and reranking); practitioner and vendor material rather than a confirmed interview bank" + NS,
 'E': "LLM-evaluation pages (Manning's AI model evaluation chapter and an arXiv judge-bias study listing position, verbosity and self-preference bias, Arize and Langfuse pages on offline versus online evaluation, an LLM-as-judge survey); practitioner and academic material rather than an interview bank" + NS,
 'C': "LLM cost and routing pages (getmaxim cost and semantic-cache guides, tianpan and system-design.space pages on routing and cascades, a Towards Data Science article on saving tokens in agentic AI, a Towards AI piece on AI system-design interview patterns); practitioner material, no confirmed interview bank" + NS,
 'A': "Agent cost and loop-control material (solo.io and getmaxim pages on iteration and token ceilings for agent loops, a Towards Data Science article on agent token costs, an Exponent-sourced 2026 guide that mentions a candidate-reported agent-with-RAG token-cost design prompt)" + NS,
 'I': "Indic-language and tokenizer material (an ACL Anthology LoResLM 2026 paper on informal and romanised Hindi tokenization, an arXiv study of tokenizer efficiency across the 22 official Indian languages, a HackerNoon opinion piece on the cost of building AI for Indian languages); research and commentary pages rather than an interview bank" + NS,
 'P': "PII and compliance material (tianpan, Kunal Ganglani, Gravitee and barkingiguana pages on logs, retention, redaction and data residency, and a vendor piece on DPDP readiness for LLM traffic); vendor and practitioner pages, not regulator guidance or an interview bank" + NS,
 'X': "Eval-contamination and feedback-bias material (a tianpan post on eval-set contamination and production leakage, an arXiv paper on contamination in closed-source LLMs, an RLHF survey and the sycophancy literature summarised in secondary pages); research and practitioner pages rather than an interview bank" + NS,
}
def wil(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d
    h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
Q = []
def add(s, d, t, a):
    if a.startswith('ED:'):
        AS.setdefault(a, ED + a[3:] + NS.replace('; commonly reported in public guides for', '; related topics appear in public guides for').replace('search snippets only, not opened', 'no page for the exact framing; search snippets only, not opened'))
    Q.append((s, d, t, a))
PIN, POUT = 3, 15   # illustrative price per million input / output tokens

# ================= 3 stars =================
# A1 RAG audit
assert 55+20+15+10 == 100 and 55+15 == 70
add(3, '🟢', "A RAG assistant gives wrong answers even though the right document is in the index. You audit a sample of 100 failed answers and find 55 where the correct chunk was not in the top 5 retrieved, 20 where it was in the top 5 but the model ignored it, 15 where an outdated document was retrieved instead, and 10 with other causes. Which stage do you fix first, what do you measure next, and what do you tell the product owner about a 100-answer sample?", 'R')
# A2 hallucination rate
lo, hi = wil(36, 300); assert 36/300 == 0.12 and 0.087 < lo < 0.089 and 0.160 < hi < 0.163
add(3, '🟢', "A legal-summary assistant is suspected of hallucinating, and 36 of 300 randomly sampled answers contain at least one claim the source does not support. Compute the measured rate with a 95% Wilson interval, and say what the number does and does not tell you about answers outside the sample. How would you define a hallucination for the annotators, and what target would you propose?", 'G')
# A3 cost blow-up
per_call = 2000*PIN/1e6 + 400*POUT/1e6
assert round(per_call, 6) == 0.012 and round(per_call*50000*30) == 18000 and 18000 == 3*6000
add(3, '🟢', "A support chatbot makes 50,000 calls a day, each with 2,000 input and 400 output tokens, at illustrative prices of 3 per million input tokens and 15 per million output tokens. The monthly budget was 6,000 for a 30-day month. Compute the actual monthly cost and name the first three levers you would pull, with a rough saving for each.", 'C')
# A4 latency
assert round(0.8 + 300/40, 1) == 8.3
add(3, '🟢', "A chat feature has a time to first token of 0.8 seconds and generates 40 tokens per second, and typical answers are 300 tokens long. Users say it feels slow, and the product budget is 5 seconds end to end. Compute the time to the last token and the time to the first visible text with streaming, and say which of the two a user feels and what you would cut.", 'G')
# A5 over-refusal
assert 3000/98000 > 0.0306 and 3000/98000 < 0.0307 and 1800/2000 == 0.9 and 1800/(1800+3000) == 0.375 and 2000+98000 == 100000
add(3, '🟢', "A safety filter sits in front of an assistant. Of 100,000 weekly queries, 2,000 are truly harmful and 98,000 are benign, and the filter blocks 1,800 of the harmful queries and 3,000 of the benign ones. Compute the block rate on benign queries, the recall on harmful queries and the share of all blocks that are correct, and say how you would tune the filter.", 'ED:guardrail and over-refusal topics in GenAI guides')
# A6 injection
assert 17/200 == 0.085
add(3, '🟡', "A support bot that can issue refunds reads customer emails, and a red team plants hidden instructions in 200 test emails. In 17 of them (8.5% of the 200, a measured sample) the bot issued a refund it should not have. What do you do in the first hour, and what structural change would you make instead of only editing the prompt?", 'ED:prompt-injection and guardrail topics in GenAI guides')
# A7 upgrade regression
assert 430-40+55 == 445 and 430/500 == 0.86 and 445/500 == 0.89
add(3, '🟡', "A provider releases a new model version, and your 500-prompt regression suite shows the pass count rising from 430 (86%) to 445 (89%). Looking prompt by prompt, 40 that passed before now fail and 55 that failed before now pass. Is this a safe upgrade, what do you examine in the 40 regressions, and what rollout do you use?", 'ED:model-upgrade and regression-evaluation topics in LLMOps material')
# A8 judge position bias
add(3, '🟡', "An LLM judge picks the better of two answers, and when you rerun 100 pairs with the answer order swapped it picks the same underlying answer in only 68 of the 100 pairs. What does this say about the judge, how do you reduce the problem, and how should the remaining disagreement be treated in the win rate you report?", 'E')
# A9 fine-tune vs RAG
assert 12*2000 == 24000 and 12*300 == 3600
add(3, '🟡', "A team proposes fine-tuning a model on 4,000 policy documents because answers about new policies are wrong. About 600 of the documents change in a typical month, a retraining run costs 2,000 and re-indexing the changed documents for retrieval costs about 300 a month, both illustrative. Compute the yearly cost of monthly retraining against monthly re-indexing, and give your recommendation with the conditions that would change it.", 'G')
# A10 vendor vs self-host
api = 2000*PIN + 400*POUT
assert api == 12000 and 15000/api == 1.25
add(3, '🟡', "A company sends 2,000 million input and 400 million output tokens a month to an API priced at illustrative 3 and 15 per million tokens. A self-hosted option costs a fixed 15,000 a month for GPUs and staff and can absorb up to twice the current volume. Compute the API bill and the break-even volume as a multiple of today's, and list the non-cost questions you would raise.", 'ED:vendor-API versus self-host and LLM cost material')
# A11 canary
p1, p2 = 15/1000, 36/9000; pp = 51/10000; se = math.sqrt(pp*(1-pp)*(1/1000+1/9000)); z = (p1-p2)/se
assert abs(p1-0.015) < 1e-12 and abs(p2-0.004) < 1e-12 and z > 4 and 1000+9000 == 10000
add(3, '🟡', "A new prompt version v12 is canaried on 1,000 requests while the old version v11 serves 9,000, and JSON parse failures are 15 of 1,000 (1.5%) on v12 and 36 of 9,000 (0.4%) on v11. Compute whether the difference is larger than sampling noise, and state your rollback rule and who decides.", 'ED:prompt versioning and rollout topics in LLMOps material')
# A12 non-determinism
assert 156/200 == 0.78 and 166/200 == 0.83 and abs(math.sqrt(0.8*0.2/200)-0.0283) < 0.0001
add(3, '🟡', "On an extraction task a prompt scored 156 of 200 (78%) in one run and 166 of 200 (83%) in another run of the same model and prompt, because of sampling at temperature 0.7. A teammate wants to ship a new prompt that scored 83% in a single run. What is the run-to-run noise, and how do you design the comparison?", 'ED:non-determinism and temperature topics in GenAI guides')
# A13 long context vs retrieval
assert 100000*PIN/1e6*20000 == 6000 and round(6000*PIN/1e6*20000) == 360
add(3, '🟡', "Each query could stuff a 100,000-token document set into the prompt or retrieve 6,000 tokens, at an illustrative 3 per million input tokens and 20,000 queries a day. Compute the daily input cost of each approach, and say what accuracy and latency evidence you would want before choosing.", 'ED:long-context versus RAG topics in GenAI guides')
# A14 multilingual
assert round(150*1.3) == 195 and 150*4 == 600 and round(600/195, 2) == 3.08 and 88-74 == 14 and round(14/88, 3) == 0.159
add(3, '🟡', "A bot answers in English and Hindi. An illustrative tokenizer gives 1.3 tokens per English word and 4 per Hindi word, a 150-word answer is generated in each language, and on 200 graded answers per language correctness is 74% for Hindi against 88% for English. Compute tokens and relative output cost per answer, the absolute and relative correctness gaps, and what you would do.", 'I')
# A15 agent loop
steps_other = 19400*6; steps_cap = 600*25; tot = steps_other + steps_cap
assert 600/20000 == 0.03 and 600+19400 == 20000 and tot == 131400 and round(steps_cap/tot, 3) == 0.114
add(3, '🔴', "An agent task is capped at 25 steps, and 600 of 20,000 tasks (3%) hit the cap while the other 19,400 average 6 steps. Compute the share of all steps spent by the capped tasks, and explain how you would find why they loop and what hard controls you would add beyond the cap.", 'A')
# A16 semantic cache
assert 1000000*0.35 == 350000 and round(350000*0.012) == 4200 and 28/400 == 0.07 and round(350000*0.07) == 24500
add(3, '🔴', "A semantic cache with a similarity threshold of 0.92 serves 35% of 1,000,000 monthly calls (350,000 hits) at an illustrative 0.012 saved per hit. A human review of 400 sampled hits finds 28 wrong answers, for example a different product with a similar name. Compute the savings, the sample wrong-answer rate and the count of wrong cached answers projected if the sample is representative, and say how you would change the cache.", 'C')
# A17 PII
assert 500000*0.02 == 10000
add(3, '🔴', "Conversation logs store full prompts for 400 days, and a scan of 500,000 stored conversations finds phone numbers or emails in 2% of them, which is 10,000 conversations. Support staff and an analytics vendor can read the logs. What do you do now, what do you change in the logging design, and how do you handle the 10,000 existing conversations?", 'P')
# A18 offline vs online
add(3, '🔴', "Over three releases the offline pass rate on a 1,000-question set rose from 82% to 86% (4 points absolute), but the online resolution rate moved only from 61% before the three releases to 61.5% after, on 20,000 conversations a month in each period. List the reasons the two can diverge, say which check you do first, and how you would build an online metric you trust.", 'E')

# ================= 2 stars =================
# temperature
assert 100000*0.03 == 3000 and 100000*0.005 == 500
add(2, '🟢', "An invoice-extraction call at temperature 0.7 returns invalid JSON on 3% of 100,000 daily calls, and at temperature 0 it does so on 0.5%. Compute the daily invalid counts at each setting, and explain what else besides lowering temperature you would do to make outputs parse reliably and what lowering it costs.", 'ED:temperature and structured-output topics in GenAI guides')
# shadow
assert 700000*0.10 == 70000 and round(70000*0.0153, 1) == 1071.0
add(2, '🟢', "Before switching models you plan to shadow 10% of 700,000 weekly calls on the candidate at an illustrative 0.0153 per call, while the old model still answers users. Compute the weekly shadow cost, and say what you can and cannot learn from shadow traffic compared with an A/B test.", 'ED:rollout and shadow-traffic topics in LLMOps material')
# fine-tune small
assert 5000000*0.004 == 20000 and 5000000*0.0005 == 2500 and 20000-2500 == 17500 and round(13000/17500, 2) == 0.74
add(2, '🟢', "A ticket classifier uses a large model at 0.004 per call for 5,000,000 calls a month. A fine-tuned small model would cost 0.0005 per call after a one-off 13,000 for labels and training (all illustrative), and scored 2 points lower in absolute accuracy on a 500-ticket test set. Compute the monthly saving and payback in months, and say what accuracy trade you would need agreed.", 'G')
# prompt caching
pc = lambda h: (h*4000*PIN*0.1/1e6 + (1-h)*4000*PIN/1e6 + 500*PIN/1e6) * 1e6
assert round(pc(0)) == 13500 and round(pc(0.6)) == 7020
add(2, '🟢', "A request has a 4,000-token fixed prefix and 500 variable tokens at an illustrative 3 per million input tokens, with cached prefix tokens billed at 10% of that rate, over 1,000,000 calls a month. Compute the monthly input cost with no caching and with a 60% cache hit rate on the prefix, and say how you would restructure prompts to raise the hit rate.", 'C')
# prompt bloat
assert (3500-800)*2000000*PIN/1e6 == 16200
add(2, '🟢', "A system prompt grew from 800 to 3,500 tokens over ten small edits, and the service makes 2,000,000 calls a month at an illustrative 3 per million input tokens. Compute the extra monthly input cost caused by the growth, and describe how you would version, review and trim the prompt without breaking behaviour.", 'ED:prompt versioning and prompt-length topics in GenAI guides')
# citations
assert 120/150 == 0.8 and 15/150 == 0.1 and 120+15+15 == 150
add(2, '🟢', "An assistant that cites sources is audited on 150 citations: 120 exist and support the claim, 15 exist but do not support it, and 15 point to documents that do not exist. Compute the share of each outcome, and say how you would reduce fabricated and unsupported citations and track them over time.", 'ED:grounding and citation topics in RAG-debugging pages')
# retries
assert round(8000*3000*PIN/1e6) == 72 and round(8000*3*3000*PIN/1e6) == 216 and 100000*0.08 == 8000
add(2, '🟢', "A client times out on 8% of 100,000 daily calls (8,000 calls) and retries up to 3 times, resending the full 3,000-token prompt each time, billed at an illustrative 3 per million input tokens even for timed-out calls. Compute the extra daily cost if every one of those calls succeeds on its first retry, and the upper bound if all 3 retries are used by every one, and say what you would change.", 'C')
# stale index
assert 90/2 == 45 and 45/1200 == 0.0375
add(2, '🟡', "An internal policy assistant re-indexes its 1,200 documents once a week, and about 90 documents change in a typical week at random times. Compute the average number of documents that are stale at a random moment, as a count and as a share of the index, and say how you would guarantee freshness for the documents that matter most.", 'R')
# reranker
assert 186/300 == 0.62 and 222/300 == 0.74 and 900+120 == 1020 < 1200
add(2, '🟡', "A retrieval stage reaches recall at 5 of 62% on 300 labelled queries (186 queries), and adding a reranker lifts it to 74% (222 queries) while adding 120 ms to a path that already takes 900 ms against a 1,200 ms budget. Is the 12-point absolute gain worth it, and what else do you check before shipping the reranker?", 'R')
# batching
per = {1: 50, 4: 42, 8: 35, 16: 25}; agg = {b: b*v for b, v in per.items()}
assert agg == {1: 50, 4: 168, 8: 280, 16: 400} and round(2.5/(280*3600/1e6), 2) == 2.48
assert max(b for b, v in per.items() if v >= 30) == 8
add(2, '🟡', "A GPU serves one request at 50 tokens per second per user, 42 at batch size 4, 35 at batch size 8 and 25 at batch size 16, and the product needs at least 30 tokens per second per user. Compute aggregate throughput at each batch size, choose the batch size, and compute the cost per million output tokens at an illustrative 2.5 per GPU-hour for your choice.", 'ED:batching and throughput topics in GenAI guides')
# TTFT pipeline
assert 100+250+150+400 == 900 and 250+150+400 == 800 > 700
add(2, '🟡', "A RAG request runs input moderation (100 ms), retrieval (250 ms), reranking (150 ms) and then model time to first token (400 ms) one after another, and the time-to-first-token budget is 700 ms. Compute the current time to first token and its value if moderation runs in parallel with retrieval, and say what else you would cut.", 'G')
# thumbs bias
assert 2400/3000 == 0.8 and 150/200 == 0.75 and round(2400*0.25) == 600
add(2, '🟡', "Only 3,000 of 100,000 weekly chats get a vote, and 2,400 of those votes (80%) are thumbs-up. An audit of 200 randomly chosen thumbs-up answers finds 150 correct (75%), and a teammate wants to fine-tune on all thumbs-up answers. Compute how many wrong answers the 2,400 would contain if the audit rate held, and explain what is wrong with the plan.", 'X')
# upgrade cost
old = 2000*3/1e6 + 400*15/1e6; new = 2000*4.5/1e6 + 280*22.5/1e6
assert round(old, 4) == 0.012 and round(new, 4) == 0.0153 and round(new/old - 1, 3) == 0.275 and 400*0.7 == 280
add(2, '🟡', "A new model version prices both input and output tokens at 1.5 times the old version but writes answers that are 30% shorter than the old length (400 down to 280 tokens). A call has 2,000 input tokens, and old prices are an illustrative 3 and 15 per million. Compute old and new cost per call and the relative change, and say how you weigh it against a measured 2-point absolute gain in resolution rate.", 'ED:model-upgrade cost and quality trade-off topics in LLMOps material')
# contamination
assert 117+165 == 282 and 282/300 == 0.94 and 120+180 == 300 and 117/120 == 0.975 and round(165/180, 3) == 0.917
add(2, '🟡', "A 300-question golden set drawn from production logs scores 94% (282 correct), but 120 of the questions were later copied into few-shot examples and fine-tuning data. On those 120 the model got 117 right, and on the 180 untouched questions it got 165. Compute the score on each part, and say what you report and how you rebuild the set.", 'X')
# kappa
a_, b_, c_, d_ = 110, 50, 30, 10; n_ = a_+b_+c_+d_
po = (a_+b_)/n_; pj = (a_+c_)/n_; ph = (a_+d_)/n_; pe = pj*ph + (1-pj)*(1-ph); kap = (po-pe)/(1-pe)
assert n_ == 200 and po == 0.8 and pj == 0.7 and ph == 0.6 and abs(kap-0.5652) < 0.001
add(2, '🟡', "A pass/fail LLM judge is compared with human labels on 200 outputs: both pass on 110, both fail on 50, the judge passes and the human fails on 30, and the judge fails and the human passes on 10. Compute raw agreement, the judge's pass rate against the human pass rate, and Cohen's kappa, and say whether you would trust the judge to gate releases.", 'E')
# routing
assert round(70000*0.002 + 30000*0.012) == 500 and round(100000*0.012) == 1200 and round(70000*(0.94-0.90)) == 2800
add(2, '🟡', "A router sends 70% of 100,000 daily queries to a small model at 0.002 per call and the rest to a large model at 0.012. The small model passes 90% of its routed queries, and the large model would have passed 94% of those same queries. Compute daily cost against sending everything to the large model, and the extra failures per day caused by routing, and say how you would validate the router.", 'C')
# cascade
assert round(0.8 + 0.4*2.5, 2) == 1.8 and round(0.8 + 2.5, 1) == 3.3 > 3.0
add(2, '🟡', "A cascade tries a small model first (0.8 seconds) and escalates to a large model (2.5 seconds) when confidence is low, and 60% of requests are accepted by the small model. Compute the mean latency of the cascade against always calling the large model, and the latency of an escalated request against a 3.0-second p95 budget, and say what that implies for the p95.", 'C')
# romanised
assert 160/200 == 0.8 and 104/200 == 0.52 and round((0.8-0.52)/0.8, 2) == 0.35
add(2, '🟡', "A retrieval system answers Hindi queries, and recall at 5 is 160 of 200 Devanagari-script queries (80%) but 104 of 200 romanised queries (52%). Compute the absolute and relative gap, and say how you would diagnose and close it without hurting the Devanagari queries.", 'I')
# conversation growth
tot_in = sum(1000 + 300*(t-1) for t in range(1, 21))
assert tot_in == 77000 and round(tot_in*PIN/1e6, 3) == 0.231 and 20*1000 == 20000
add(2, '🟡', "A chat product resends the whole history on every turn, with a 1,000-token system prompt and 300 new tokens added per turn, and the input at turn t counts the system prompt plus the t-1 earlier turns. Over a 20-turn conversation compute the total input tokens sent and their cost at an illustrative 3 per million, compare with 20,000 tokens if no history were resent, and propose a context-management policy.", 'C')
# streaming guardrail
assert round(400/40 + 0.1, 1) == 10.1 and round(50/40 + 0.1, 2) == 1.35
add(2, '🟡', "An output PII filter must see text before the user does. Answers average 400 tokens at 40 tokens per second, the filter takes 0.1 seconds per check, and you can ignore the time to first token. Compute when the first text appears if the whole answer is buffered and if it is checked in 50-token chunks, and describe the risk you accept with chunking.", 'ED:output guardrail and streaming topics in GenAI guides')
# upload injection
assert 1000/50000 == 0.02 and 83 < 1000*5/60 < 84
add(2, '🔴', "Users can upload PDFs that are added to a shared knowledge base, and a scanner flags 1,000 of 50,000 uploads (2%) as possibly containing hidden instructions. A manual review takes 5 minutes per flagged file. Compute the review hours, and explain why scanning alone is not enough and what architecture limits the damage when a poisoned document is retrieved.", 'ED:indirect prompt-injection topics in GenAI guides')
# agent writes
lo, hi = wil(20, 500); assert 20/500 == 0.04 and 0.025 < lo < 0.027 and 0.060 < hi < 0.062 and 780 <= round(30000*lo) + 10 and round(30000*hi) < 1900
add(2, '🔴', "In 500 staged runs, each with one write action, an agent took a wrong write action in 20 (4%, a measured sample). Production will make 30,000 write actions a month. Compute a 95% Wilson interval for the wrong-action rate and the implied monthly range, and say which permissions, approvals and rollback you would add.", 'ED:agent wrong-action and tool-permission topics in GenAI guides')
# deletion
assert 3000/2000000 == 0.0015 and 35-30 == 5
add(2, '🔴', "A user exercises a right to have personal data deleted. It sits in raw chat logs, in 3,000 of 2,000,000 chunks in a vector index, in an evaluation dataset and in 35-day rolling backups, and your internal deletion target is 30 days. Compute the share of the index affected and the gap between the target and the backup retention, and lay out a deletion plan that is honest about what cannot be erased immediately.", 'P')
# regression n
n_req = math.ceil((1.959964 + 0.841621)**2 * (0.8*0.2 + 0.75*0.25) / 0.05**2)
assert 1090 <= n_req <= 1092
add(2, '🔴', "You want a regression suite to detect a drop in pass rate from 80% to 75% (5 points absolute) with 95% confidence and 80% power, using separate prompt samples for the two versions. Compute the number of prompts needed per version with the normal approximation, compare it with your 200-prompt suite, and say how scoring both versions on the same prompts would help.", 'ED:regression-suite sizing in LLM evaluation pages')
# judge sampling
assert 1000000*0.05 == 50000 and 50000*0.01 == 500 and 50000*0.02 == 1000 and 100/0.02 == 5000
add(2, '🔴', "An LLM judge costs 0.01 per scored answer, and production makes 1,000,000 answers a month at 0.012 each. A failure mode hits 2% of answers. Compute the cost of scoring a 5% random sample, the expected number of failures in that sample, and how many answers you must score to expect at least 100 failures, and say what you would sample instead of a plain random draw.", 'E')

# ================= 1 star =================
# sycophancy
assert 140-90 == 50 and 70-45 == 25 and 90/200 == 0.45 and 140/200 == 0.7
add(1, '🟢', "On 200 prompts that contain a false premise, an assistant corrects the premise in 90 (45%) and goes along with it in the rest. After a prompt change it corrects 140 of the same 200 (70%). Compute the change in percentage points and the number of extra corrected prompts, and say why a thumbs-up signal might reward the old behaviour.", 'X')
# deprecation
assert round(2000*3*0.0153, 1) == 91.8
add(1, '🟢', "A provider will retire the model snapshot you use in 90 days. You have a 2,000-prompt regression suite, want 3 runs per candidate to handle sampling noise, and a candidate costs an illustrative 0.0153 per call. Compute the evaluation cost for one candidate, and describe the migration plan, including what you do if the new version regresses on some prompts.", 'ED:model-upgrade and deprecation topics in LLMOps material')
# judge drift
add(1, '🟡', "A judge model version is updated, and the same 300 saved answers are rescored: the mean score falls from 4.2 to 3.8 on a 5-point scale, and 90 of the 300 answers (30%) change by one point or more. How do you tell judge drift from product drift, and how do you keep a time series of scores comparable?", 'E')
# lost in the middle
assert (92+71+85) == 248 and round(248/300, 3) == 0.827 and 92-71 == 21
add(1, '🟡', "A document-QA test places the answer passage at the start, middle or end of a long context, with 100 questions in each position, and accuracy is 92%, 71% and 85% respectively. Compute overall accuracy and the middle-versus-start gap in points, and say what you would change about how retrieved passages are ordered or whether to use long context at all.", 'ED:long-context versus RAG topics in GenAI guides')
# agent budget
tail = 1000*160000; rest = 99000*20000
assert round(tail/(tail+rest), 4) == 0.0748 and (tail - 1000*80000) == 80_000_000 and round(80_000_000/(tail+rest), 4) == 0.0374
add(1, '🟡', "Median agent tasks use 20,000 tokens, and of 100,000 tasks a month, 1,000 sit in the tail at 160,000 tokens while the other 99,000 are assumed to use exactly the median. Compute the tail's share of all tokens, and the saving from a hard per-task cap of 80,000 tokens as a share of all tokens, then say what happens to the tasks that hit the cap.", 'A')
# unit economics
calls = 5000*1500 + 95000*60
assert calls == 13200000 and round(calls*0.012) == 158400 and 100000*5 == 500000 and round(1500*0.012) == 18 and 5000*18 == 90000 and 5000*5 - 90000 == -65000
add(1, '🟡', "A feature earns 5 per user per month. Of 100,000 users, 5,000 heavy users make 1,500 calls a month and the other 95,000 make 60 calls each, at an illustrative 0.012 per call. Compute total monthly cost, the cost per heavy user, and the margin on heavy users alone, and propose pricing or limits.", 'C')
# synthetic eval
lo, hi = wil(78, 100); assert 0.685 < lo < 0.695 and 0.845 < hi < 0.855 and round(500*lo) in (344, 345) and round(500*hi) in (424, 425)
add(1, '🟡', "A team generates 500 synthetic test questions from its documents with an LLM, and humans review a random 100 of them and find 78 valid. Compute the sample valid rate with a 95% Wilson interval and the projected range of valid questions among the 500, and say how you would use the set.", 'ED:synthetic evaluation data topics in LLM evaluation pages')
# residency
assert 90/500 == 0.18 and round(20000*0.18) == 3600
add(1, '🟡', "A vendor API processes prompts outside the country, and a sample of 500 of the 20,000 daily prompts finds personal data in 90 of them (18%, a measured sample). Compute the projected daily count of prompts with personal data, and compare redaction, a regional endpoint, self-hosting and contractual terms, saying what you need from legal.", 'P')
# self-host utilisation
tph = 2000*3600
assert tph == 7_200_000 and round(20/(tph/1e6), 2) == 2.78 and round(20/(0.3*tph/1e6), 2) == 9.26 and round(20/(tph/1e6)/15, 3) == 0.185
add(1, '🔴', "A self-hosted node costs an illustrative 20 per hour and can generate 2,000 tokens a second at full load. Compute the cost per million output tokens at 100% and at 30% utilisation, compare with an API at an illustrative 15 per million output tokens, and find the utilisation at which the node breaks even.", 'ED:vendor-API versus self-host and LLM cost material')
# multilingual wilson
le, he = wil(91, 100); lh, hh = wil(78, 100)
assert 0.83 < le < 0.85 and hh > 0.84 and le < hh and 91-78 == 13
add(1, '🔴', "English answers are graded correct on 91 of 100 test questions and Hindi answers on 78 of 100, using different graders. Compute 95% Wilson intervals for both, say whether the 13-point absolute gap looks real, and list the confounds in the comparison.", 'I')
# rule of three
assert 3/300 == 0.01 and round(1 - 0.05**(1/300), 5) == 0.00994
add(1, '🔴', "A jailbreak test suite of 300 attacks is run against a hardened assistant and none succeed. Compute the approximate 95% upper bound on the per-attempt success rate with the rule of three and with the exact formula, and say what you can claim to a risk committee and what you cannot.", 'ED:red-teaming and jailbreak topics in GenAI guides')
# abstention
ec = lambda ans, acc: ans*(1-acc)*20 + (1-ans)*4
assert round(ec(0.8, 0.92), 2) == 2.08 and round(ec(0.55, 0.97), 2) == 2.13
add(1, '🔴', "A model answers a question only if its confidence is above a threshold; at threshold 0.7 it answers 80% of questions with 92% accuracy, and at 0.9 it answers 55% with 97% accuracy (accuracy measured among answered questions). A wrong answer costs 20, a human escalation costs 4 and a correct answer costs 0, all illustrative. Compute the expected cost per question at each threshold, and say how sensitive the choice is to the wrong-answer cost.", 'ED:abstention and hallucination-reduction topics in GenAI guides')
