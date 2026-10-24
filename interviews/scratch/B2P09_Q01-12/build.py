import re, subprocess, sys
P9 = open('/home/user/case_studies/interviews/Book2_GenAI/Book2_GenAI_Part09.md', encoding='utf-8').read().split('\n')
def hdr(n):
    for i, l in enumerate(P9):
        if l.startswith(f"### Q{n} "):
            assert P9[i+1].startswith("**Asked at:**")
            return l + "\n" + P9[i+1]
A = {}
A[1] = dict(
say="You evaluate the whole system (retrieval, prompt, model, tools, post-processing) on a versioned test set before release, then keep measuring on sampled production traffic after release, and you do not rely on a single model score.",
explain="""- **Why it differs from ordinary software tests:** outputs are open-ended and non-deterministic, there is rarely one correct string, so a unit-test `assert ==` does not work. You score with a mix of exact checks, rubric-based judges and humans, and you report a rate with an interval, not pass or fail.
- **Model vs system evaluation:** model eval asks "is this model good at the task?" (public benchmarks, or your own prompts with gold context). System eval asks "does the product work for users?" and includes the retriever, prompts, tools, guardrails and parsing. The example below shows the gap: the same generator scores 20/20 with gold context and 12/20 inside the system.
- **Build in layers, cheapest first:** deterministic checks (format, schema, exact answers, forbidden strings), then LLM judges for subjective criteria, then humans for calibration and edge cases (judge calibration is Q6, human design Q24).
- **Offline vs online:** offline (a frozen test set, run on every change) is repeatable and cheap, so it gates releases. Online (A/B tests, implicit feedback, sampled production traces scored by a judge) shows what real users do, including queries your set never sampled. Failures found online become new offline cases (Q30, Q15). OpenAI's evaluation guidance describes the same loop: continuous evaluation grown from logs (vendor docs, opened).
- **Start from error analysis, not from metrics:** read real traces, name the failure modes, then build evals for the ones that matter (Hamel Husain's FAQ, a practitioner view; see Q15).
- **Scope pointers:** retrieval vs generation metrics are in Part 6 Q10 and Q39, agent evaluation in Part 8 Q14, evaluating a fine-tuned model in Part 4 Q9, monitoring depth in Part 11.""",
example="Toy support bot, 20 cases (synthetic). With the gold document handed to the generator it answers 20/20, so a model-only eval says \"ship\". Run end to end with a retriever that finds the right document 70% of the time (assumed), it scores 12/20 in this run. On simulated traffic where 30% of queries are typos (assumed retrieval hit rate 0.4 on those), the pass rate is 0.62. The model was never the problem; the system eval and the online slice found it.",
code="q01.py",
follow="""- *Which do you build first?* A small set (20-50 cases from real failures is a common start, per Anthropic's agent-evals post, a vendor view) with deterministic checks; add judges only for criteria you cannot check in code.
- *What do you gate releases on?* Offline suite results with intervals (Q11, Q14); online metrics decide rollout and rollback (Q30).
- *Where does a public benchmark fit?* Only for picking candidate models; it is not a product eval (Q10).""",
mist="evaluating only the model with gold context; one aggregate number with no interval; building a set from imagined queries instead of logs; relying on an LLM judge nobody checked against human labels; no path for production failures to become test cases.")

A[2] = dict(
say="Sample real queries, cover the cases that matter on purpose, label them with clear rules, deduplicate, split once into dev and test, version the set by content, and check it never appears in your prompts, few-shot examples or training data.",
explain="""- **Source:** start from real user queries or logs (anonymised). Add synthetic cases only to fill gaps, and say so; synthetic questions tend to be easier and more uniform than real ones (the RAG-specific pitfalls are in Part 6 Q40).
- **Coverage, not just volume:** stratify by intent, difficulty, language, user segment and known failure modes; include edge cases, unanswerable questions and adversarial ones. Look for thin strata before labelling.
- **Labels:** write short guidelines, have two people label a sample, resolve disagreements, and keep the rationale. The label type should match what you will compute (a gold answer, a rubric verdict, relevant document ids).
- **Size:** it depends on the effect you must detect, not on a magic number. Guides cite 100-500 for golden sets (interview-prep guides, not a standard) and Anthropic suggests 20-50 real-failure tasks to start (vendor view). Few hundred cases give wide intervals on small gains (Q11, Q26).
- **Versioning:** hash the content, record the source and date, never edit a case silently; a changed set means a new version and old scores are not comparable.
- **Leakage:** keep the test split out of prompts, few-shot examples, fine-tuning data and judge calibration data. Check with n-gram or word-overlap searches and by keeping a never-looked-at final test split. Training-data decontamination is Part 2 Q30 and fine-tuning data is Part 4 Q34.""",
example="Synthetic log sample of 16 queries across four intents. Word-overlap deduplication (Jaccard >= 0.7) removed 1 exact rephrasing (\"how do I reset my password?\") but kept \"reset password please\", so cheap dedupe is imperfect and you still skim. Hash-based split gave 6 dev and 9 test. A planted check found that both few-shot examples in the prompt were also in the set, so those cases would flatter the score. Adding one case changed the version id from 7fb70dfa to e671e548.",
code="q02.py",
follow="""- *Dev vs test?* Tune prompts on dev; touch test only for the final comparison, otherwise you overfit the set.
- *Can an LLM write the questions?* Yes as a starting point, but check them by hand and keep real queries in the mix; model-written evals need human verification (Anthropic, vendor post).
- *How do you keep it fresh?* Add new failure cases from production on a schedule, as a new version, and keep a frozen regression slice (Q36).""",
mist="using the same examples in the prompt and in the test; building only from easy happy-path queries; no unanswerable or edge cases; editing cases without versioning; labelling with no guideline so labels are noisy.")

A[3] = dict(
say="These metrics compare the model's text to a reference by overlap of words (exact match, F1, BLEU, ROUGE) or by embedding similarity (BERTScore); they work when answers are short and constrained, and they fail for open-ended output because many different texts are equally correct.",
explain="""- **Exact match:** 1 if the normalised answer equals the reference. Good for short factual or classification answers; brittle to phrasing.
- **Token F1:** harmonic mean of word precision and recall against the reference (the SQuAD-style metric). Gives partial credit; still blind to meaning.
- **BLEU:** precision of n-grams with a brevity penalty, designed for machine translation. **ROUGE:** recall-oriented overlap (ROUGE-L uses the longest common subsequence), common for summaries.
- **BERTScore:** matches tokens by contextual-embedding similarity instead of exact words, so synonyms count; the authors tested it on 363 machine-translation and captioning systems (arXiv 1904.09675, abstract). It is still similarity to one reference, not truth.
- **Why they fail for LLM output:** one question has many valid phrasings, so a correct paraphrase scores low; and a wrong answer that copies most of the reference words scores high. Even in code, the Codex authors report that functionally inequivalent programs often had higher BLEU than equivalent ones (Codex paper body, read for this answer).
- **When they still fit:** extractive QA, classification labels, translation-style tasks with several references, or as a cheap regression signal. For open-ended tasks use rubric judges or humans (Q4, Q24).""",
example="Reference: \"Maria bought a car in 2019.\" A correct paraphrase (\"In 2019 Maria purchased an automobile.\") gets F1 0.50 and BLEU-2 0.32, while a wrong answer that changes only the year (\"... in 2021\") gets F1 0.83 and BLEU-2 0.82. The metric ranks the wrong answer above the right one. The toy soft match (a small synonym table standing in for embeddings, not a real BERTScore) lifts the paraphrase to 0.67 but also gives the wrong year 0.83, because the embedding view still hardly sees the changed fact.",
code="q03.py",
follow="""- *Is ROUGE useless?* No: it is a cheap proxy where outputs are constrained, but validate it against human ratings for your task before trusting it.
- *What do you use instead?* Deterministic checks where possible, otherwise a calibrated judge (Q4, Q6) plus human spot checks.
- *Why does BERTScore help only partly?* It forgives wording but not a changed number or entity; it measures closeness, not correctness.""",
mist="reporting BLEU for chatbots as quality; forgetting to normalise case, punctuation and articles before exact match; treating higher overlap as higher correctness; using one reference for tasks with many valid answers; comparing scores across different tokenisation or metric implementations.")

A[4] = dict(
say="LLM-as-a-judge means using a strong model with a rubric to grade another model's output; pointwise scores one answer, pairwise picks the better of two, reference-based checks an answer against a gold answer, and you can trust any of them only after checking it against human labels.",
explain="""- **Pointwise:** judge scores one answer against a rubric (pass/fail or a small scale). Cheap, scales to production traces, no baseline needed; scores drift and cluster, and small differences vanish into ties.
- **Pairwise:** judge sees two answers and picks one (or ties). Better at ranking close candidates and A/B decisions; costs more per comparison, has position bias, and gives no absolute quality.
- **Reference-based:** judge compares the answer with a gold answer or gold facts. Strong when a correct reference exists; wrong or incomplete references punish correct answers.
- **When to use which:** pointwise or binary for production monitoring and gates, pairwise for choosing between two prompts or models, reference-based when you have gold answers. Details of pairwise design are in Q18.
- **What the research reports:** the MT-Bench paper (authors' setup: 80 multi-turn questions in 8 categories, 58 expert labellers) reports GPT-4 agreeing with human experts at 85% on non-tie votes versus 81% human-human agreement; the abstract summarises it as over 80% agreement. That is a result on their questions and setup, not a guarantee for yours.
- **Limits:** judges have biases (Q5), mistakes on math or facts they cannot check, and prompt sensitivity. Calibrate against humans (Q6) and keep humans on the hard cases. Prompt-level limits are in Part 3 Q32 and win rates for aligned models in Part 5 Q10.""",
example="Synthetic simulation, 20,000 pairs per row, judge noise of 0.9 on a 1-5 quality scale (assumed). When answer B is truly 1.0 better than A, the pairwise judge picks B 78% of the time, pointwise picks B 64% and ties 23%. At a 0.3 gap the numbers are 59% vs 43% with 31% ties. The toy gap comes from rounding to integers and ties, so treat it as mechanics, not a measured judge. Reference-based: with the right reference the correct answer \"Canberra\" is judged right; with a wrong reference (\"Sydney\") it is judged wrong.",
code="q04.py",
follow="""- *Which judge model?* The strongest affordable one from a different family than the generator (Q5), and keep it fixed and versioned.
- *Can the judge replace humans?* It can replace most routine grading once its TPR and TNR on a labelled set are acceptable; keep a human sample for drift.
- *Binary or 1-5?* Binary or a small scale is easier to calibrate (Q7).""",
mist="trusting a judge because it agrees with itself; using one pointwise 1-5 score for everything; never swapping order in pairwise; quoting the paper's 80% agreement as if it applied to your domain; changing the judge model mid-experiment and comparing the scores.")

A[5] = dict(
say="Judges favour the first slot (position bias), longer answers (verbosity bias) and text from their own model (self-preference); you measure each with a probe where the thing that should not matter is varied on equal-quality pairs, and mitigate by swapping order, controlling length, using a different judge family and calibrating against humans.",
explain="""- **Position bias:** the verdict changes when you swap the slots. The MT-Bench paper (Table 2, authors' setup) reports GPT-4 giving a consistent verdict after swapping in 65.0% of cases with the default prompt, with 30.0% biased toward the first slot; Claude-v1 was 23.8% consistent with 75.0% first-biased and GPT-3.5 46.2% consistent. Probe: judge every pair in both orders and count flips.
- **Verbosity bias:** longer answers win at equal quality. The same paper's \"repetitive list\" attack (padding an answer with rephrased list items, no new information) fooled the weaker judges; GPT-4 resisted much better. Probe: pad an answer with fluff and see if it wins; length-controlled scoring is one fix (length-controlled AlpacaEval reports Spearman with Arena rising from 0.94 to 0.98, authors' claim).
- **Self-preference:** a judge favours its own generations. The MT-Bench paper saw GPT-4 give itself a 10% higher win rate and Claude-v1 25%, but said the data could not settle whether this is self-enhancement; a later paper (arXiv 2404.13076, abstract) reports that models recognise their own outputs and that recognition correlates with preference. Probe: compare judges from different families on the same pairs.
- **Mitigations:** judge both orders and keep the verdict only if it agrees (otherwise a tie); control or penalise length; use a judge from another family or a panel of smaller judges from disjoint families (PoLL, authors' claim of less bias and lower cost); anchor with calibration against human labels (Q6).""",
example="Mock judge with planted biases (assumed: +0.25 first slot, +0.30 per 100 extra words, +0.40 for its own output) on equal-quality pairs, 20,000 each. The probes recover them: first slot wins 64% (50% would be unbiased), the padded answer wins 72%, the judge's own output wins 71%. Swap-and-agree removes the position effect (X wins 23%, Y 23%, tie 54%) but note it would not remove verbosity or self-preference, which hit both orders alike.",
code="q05.py",
follow="""- *Does swapping fix everything?* No, only position; length and self-preference need separate controls.
- *How often should you re-measure?* When you change the judge model, the prompt or the answer-length profile of your system.
- *Is a bigger judge less biased?* In the paper's table GPT-4 was more consistent than the others, but it still showed bias; measure yours.""",
mist="running one order only; reporting win rate without ties; letting the same model generate and judge; assuming bias numbers from a paper transfer to your prompts; padding-friendly rubrics that reward 'thoroughness'.")

A[6] = dict(
say="Label a sample by hand, run the judge on the same cases, and report agreement, Cohen's kappa, and TPR and TNR on a held-out split, so you know how often it catches passes and failures, before you trust its numbers.",
explain="""- **Split the labelled data:** one small part to pick few-shot examples and write the prompt (train), one to iterate on (dev), one untouched to report (test). Hamel Husain suggests roughly 10-20% / 40-45% / 40-45% and 100-200 labelled examples per failure mode (his practitioner guidance, not a standard).
- **Agreement alone misleads:** with 85% passes, a judge that always says pass agrees 85% of the time. Kappa corrects for chance: kappa = (po - pe) / (1 - pe). Two-annotator kappa details and the kappa paradox are Q25; code is Q39.
- **TPR and TNR:** TPR = share of human PASS the judge calls PASS; TNR = share of human FAIL the judge calls FAIL. For failure detection TNR is usually the number that matters, and it rests on the few failing cases, so it is noisy.
- **Use the rates to correct a metric:** with TPR and TNR you can estimate the true pass rate from the judge's observed rate: (observed + TNR - 1) / (TPR + TNR - 1). It only helps if the rates are measured well.
- **Iterate:** read the disagreements, fix the rubric or add anchored examples, re-measure on dev, and report once on test. Re-check when the model, prompt or traffic changes (Q45).""",
example="Synthetic data, 400 cases, 85% human-PASS, mock judge with assumed TPR 0.9 and TNR 0.7. On the test split (170 cases): agreement 0.86, kappa 0.49, TPR 0.90, TNR 0.65. An always-PASS judge gets the same 0.86 agreement but kappa 0.00. Honest weak result: correcting the judge's pass rate with dev-set TPR and TNR gave 0.926 against a human 0.865 (raw judge 0.824), because dev TNR (0.80) came from only 20 failing cases and test TNR was 0.65. The correction made it worse here; with few negatives, label more of them.",
code="q06.py",
follow="""- *What kappa is acceptable?* Rules of thumb exist (an interview guide cites 0.6 and 0.8 thresholds) but depend on the task; judge by TPR/TNR and by what a wrong verdict costs.
- *Why not use the dev set to report?* You tuned on it, so the number is optimistic.
- *How do you get more failing cases cheaply?* Oversample suspected failures when labelling, then reweight when you estimate prevalence.""",
mist="reporting only raw agreement; one split for everything; tuning the prompt on the test set; ignoring class imbalance; computing TPR/TNR from a handful of negatives and treating them as exact.")

A[7] = dict(
say="Judge one criterion at a time, use binary or a small scale with written definitions, give anchored pass and fail examples, ask for reasoning before the verdict, and demand a fixed machine-readable output that you parse strictly.",
explain="""- **One criterion per judge:** a single 'overall quality 1-5' judge cannot be debugged. Separate judges for faithfulness, relevance, tone, and so on tell you what failed (Hamel Husain recommends one focused judge per failure mode and binary pass/fail over 1-5 scales; practitioner guidance).
- **Binary or small scale:** define PASS and FAIL in plain words, including what to ignore. Wider scales cluster in the middle and are harder to calibrate (Q4, Q6).
- **Anchored examples:** two or three labelled examples (clear pass, clear fail, one borderline) fix the standard better than adjectives. Keep them out of your test set (Q2).
- **Reasoning before verdict:** ask for a short rationale first and the verdict last, which is also the approach in G-Eval (chain-of-thought plus form filling, authors' method) and in OpenAI's guidance to reason before scoring (vendor docs). The rationale also helps you debug disagreements.
- **Output format:** JSON with fixed keys in a fixed order, and a strict parser that rejects anything else and counts the rejections; retry once, then log as an error, never default to PASS.
- **Validate:** check the finished prompt against human labels (Q6). Prompt-level evaluation basics are in Part 3 Q32.""",
example="A faithfulness judge with a two-example rubric. The strict parser accepted a clean reply and a reply with prose around the JSON, and rejected three bad ones: verdict before reasoning, a drifted scale (\"4/5\"), and truncated JSON. The three-judge report (faithfulness PASS, relevance PASS, tone FAIL) points straight to the tone problem, which a single 1-5 score would hide. The mock judge here is canned text; it tests the format handling, not judging skill.",
code="q07.py",
follow="""- *Should the judge see the reference?* Only if the criterion needs it (correctness); for faithfulness give the context.
- *What about temperature?* Use temperature 0 and a pinned model version, and still expect small variation (Q27).
- *How many examples?* Enough to anchor the edge cases; more can bias the judge toward the examples' style.""",
mist="a rubric with several criteria mixed together; verdict before reasoning; 1-10 scales with no definitions; examples copied from the test set; defaulting unparseable outputs to PASS; not versioning the judge prompt.")

A[8] = dict(
say="Ragas faithfulness is the share of claims in the answer that the retrieved context supports, and answer relevance is how close the questions regenerated from the answer are to the original question; neither checks that the answer is correct or complete, which is how faithfulness can be 0.9 while users still complain.",
explain="""- **Faithfulness:** an LLM splits the answer into claims, checks each against the retrieved context, and the score is supported claims divided by total claims. The Ragas docs' example: a claim set where 1 of 2 is supported scores 0.5 (official docs, opened).
- **Answer (response) relevancy:** an LLM generates questions from the answer (default 3), and the score is the mean cosine similarity between each generated question's embedding and the original question's. The docs state it does not check factuality.
- **What they miss:** (1) faithful to wrong or stale context: a correct summary of the wrong document scores 1.0; (2) incompleteness: leaving out half the answer keeps relevance high; (3) retrieval failure: nothing here checks that the right chunks were fetched (Q16); (4) the verifier's own errors; (5) averaging: a mean hides a tail of bad answers.
- **Why 0.9 with complaints:** the metric asks 'is what you said supported?' not 'did you solve the problem?' Pair it with correctness or resolution labels, context metrics, and error analysis of complaints (Q15, Q17).
- **Scope:** the overview of generation metrics is in Part 6 Q39; here the point is how they break. The Ragas page for context recall was not opened for this answer.""",
example="Toy implementation (word overlap standing in for the LLM verdicts, bag-of-words cosine standing in for embeddings): the Einstein-style case gives 0.5, matching the docs' pattern. An answer faithful to a stale document (14 days, current policy 30) scores 1.0. Synthetic 10-answer set (assumed numbers): mean faithfulness 0.9, human-judged resolved rate 0.6, and 2 of the 8 perfectly faithful answers were not resolved. Relevance of an on-topic but partial answer is 0.69; an off-topic answer scores 0.0.",
code="q08.py",
follow="""- *Reference-free or with reference?* Faithfulness and response relevancy need no gold answer; correctness needs one.
- *Is faithfulness the same as hallucination rate?* Close but not equal: it is relative to the context, not to the world (Q9).
- *How do you debug a low score?* Read the unsupported claims; check whether retrieval or generation caused them (Q17).""",
mist="reading faithfulness as correctness; averaging without looking at the tail; ignoring that the verifier is an LLM that can be wrong; using relevance to judge completeness; treating one tool's metric name as a standard across libraries.")

A[9] = dict(
say="Hallucination checks split the answer into claims and test each against sources (entailment), verify that cited passages really support their claims, sample several answers and look for disagreement, and track how often the system abstains; each has blind spots, so combine them with human review.",
explain="""- **Claim decomposition plus entailment:** extract atomic claims, then ask an NLI model or LLM whether the source entails each. Output: share of grounded claims and the list of unsupported ones. Limits: decomposition errors, subtle numbers, and the checker's own mistakes; it checks against the source, not the world.
- **Citation verification:** check that each cited passage exists and supports the sentence that cites it. Catches fake and misattached citations; does not catch uncited claims.
- **Sampling consistency (SelfCheckGPT-style):** sample several answers and flag claims they disagree on, with no source needed (SelfCheckGPT, tested on GPT-3 WikiBio passages, abstract). Limit: a model can be consistently wrong, so agreement is not truth.
- **Abstention rate:** on unanswerable questions, how often the system says it does not know (and how often it wrongly abstains on answerable ones). A system that never abstains will hallucinate on them.
- **Connect to metrics:** faithfulness in Q8 is the claim-level version of the first check; context quality is Q16; separating retrieval from generation failures is Q17.""",
example="Synthetic source about a company. Four claims: 3 grounded, the invented \"900 employees\" flagged, grounded-claim rate 0.75. A citation check confirms the first two citations and fails the third. Sampling: an unsure mock model gave 400, 400, 400, 150, 900 (agreement 0.6, majority happens to be right); a confidently wrong mock gave 900 five times (agreement 1.0, truth 400), which is the case consistency checks miss. Abstention on 4 unanswerable cases: 1 of 4 = 0.25.",
code="q09.py",
follow="""- *Which one first?* Claim-level entailment against retrieved context, plus abstention on a labelled unanswerable set.
- *Black-box vs white-box?* Sampling checks work through an API; token-probability methods need logits.
- *How do you validate the detector?* Same way as any judge: human labels, TPR and TNR (Q6).""",
mist="treating consistency as correctness; checking the answer against itself; ignoring abstention; verifying only citation format and not content; trusting a detector never calibrated on your domain.")

A[10] = dict(
say="Public benchmarks measure narrow, standardised abilities (knowledge, small coding functions, repository bug fixes, multi-turn chat quality, human preference), so they are useful for shortlisting models but a score says little about your users, your data or your system.",
explain="""- **MMLU:** 57 multiple-choice subject tasks testing knowledge; at publication most models were near chance and the largest GPT-3 about 20 points above (paper abstract). MMLU-Pro made it harder with 10 options and cleaner questions; the authors report accuracy drops of 16% to 33% and lower prompt sensitivity (authors' claim).
- **HumanEval:** 164 hand-written Python problems with an average of 7.7 unit tests each, scored by functional correctness (Codex paper). It tests small function writing, not software engineering (Q22).
- **SWE-bench:** 2,294 problems from real GitHub issues in 12 Python repos, scored by whether the patch passes the repository's tests; in the original paper the best model resolved 1.96% (abstract, long superseded). Current scores and Verified-subset figures change; check the live leaderboard.
- **MT-Bench:** 80 multi-turn questions across 8 categories, scored by an LLM judge. **Chatbot Arena:** crowdsourced pairwise human votes ranked statistically; the Arena paper cites over 240K votes at the time (details in Q19, Q20).
- **Why it is not a product eval:** different task mix, different prompts and data, contamination and saturation (Q21), implementation sensitivity, and no system effects. Hugging Face reported llama-65b at 0.637, 0.488 and 0.636 on MMLU from three implementations at that time (vendor blog), and Anthropic notes small format changes shift accuracy by about 5% (vendor post).
- **How to use:** shortlist models, then run your own golden set (Q2) on your system.""",
example="Two synthetic models with assumed per-task pass rates. On a benchmark mix of 70% math MCQs and 30% code, model X wins 0.84 vs 0.77. On a product mix (60% support chat, 30% extraction, 10% code) model Y wins 0.805 vs 0.64. Format sensitivity: a mock multiple-choice model that knows half the answers (assumed) and guesses with a bias to option A scores 0.702 when the gold answer is always A and 0.627 when the gold slot is random.",
code="q10.py",
follow="""- *Which benchmark is closest to a product?* Whichever shares your task and data; none replace your own eval.
- *Why do different tools report different MMLU numbers?* Prompt format, answer extraction and few-shot setup differ.
- *Is Arena a product eval?* It measures broad human preference on its users' prompts, not your task (Q20).""",
mist="picking a model by leaderboard rank alone; comparing numbers from different harnesses; assuming a high benchmark score means no regression on your task; quoting scores without the setting; ignoring contamination.")

A[11] = dict(
say="Not on this evidence: 82% vs 80% on 200 cases is a 4-case difference, the intervals overlap heavily, and even a paired test on the same cases usually cannot call it unless the two prompts almost never disagree.",
explain="""- **Interval for each score:** a Wilson 95% interval for 164/200 is about 0.761 to 0.867 and for 160/200 about 0.739 to 0.850, so they overlap a lot. Report a rate with an interval, not a bare number (Miller's 'Adding error bars to evals' frames evals as samples from a super-population; abstract).
- **Use the pairing:** both prompts ran on the same cases, so compare per case. Only discordant cases matter: b = new right and old wrong, c = old right and new wrong. A net +4 can come from 4 vs 0 or 34 vs 30.
- **Test:** exact McNemar test (binomial on b and c) or a paired bootstrap of the difference. The unpaired z-test ignores the pairing and is the wrong tool here (Q28; bootstrap code is Q38).
- **Trust small differences?** Little. Also repeated runs add noise (Q27), many comparisons add false positives (Q28), and sample size sets what you can detect (Q26).
- **Practical answer:** say you cannot conclude it is better; check the discordant cases, enlarge the set, or decide on other grounds (cost, latency, qualitative review).""",
example="Numbers from the run. Unpaired z = 0.51, p = 0.61. With the same +4 net wins: b=4, c=0 gives McNemar p = 0.125; b=6, c=2 gives 0.289; b=14, c=10 gives 0.541; b=34, c=30 gives 0.708. Even a 4-vs-0 result is not significant at 0.05. The paired bootstrap CI for 4-vs-0 came out (+0.005, +0.040), which excludes zero while exact McNemar says p = 0.125; with so few discordant cases the percentile bootstrap is too optimistic, so prefer the exact test there. Simulated power for a true +2 point gain (assumed 7% new-only wins, 5% old-only) at n = 200 was only 0.08.",
code="q11.py",
follow="""- *How many cases do you need?* Roughly, enough discordant cases to see the effect; see Q26.
- *What if the real gain is 2 points?* Then 200 cases will miss it most of the time, as the power simulation shows.
- *Can you just rerun?* Reruns reduce run noise but not case-sampling noise (Q27).""",
mist="comparing two intervals by eye for overlap; using an unpaired test on paired data; declaring a winner from a 2-point gap; running many variants and keeping the best (selection bias, Q28); ignoring run-to-run randomness.")

A[12] = dict(
say="pass@k is the probability that at least one of k sampled solutions passes the tests; the unbiased estimator draws n >= k samples, counts c correct, and computes 1 - C(n-c, k) / C(n, k) per problem, then averages across problems.",
explain="""- **Definition and estimator:** the Codex paper defines pass@k as the expectation over problems of 1 - C(n-c, k)/C(n, k), and used n = 200 samples with k <= 100 (paper body, read for this answer). The estimate is exact for the probability that a random size-k subset of your n samples contains a pass, which is unbiased for the true pass@k.
- **Why not generate exactly k and count?** That works but is noisy; many samples and the formula give a lower-variance estimate for every k at once. The stable code multiplies terms instead of computing huge binomials.
- **The biased shortcut:** estimating pass@k as 1 - (1 - p_hat)^k with the empirical pass@1 is biased. The paper says it consistently underestimates and the gap does not fully close even for n > 5k (Appendix A and Figure 13). Another meaning of 'best of k' bias: if you pick the best sample using the tests and report it as pass@1, you reported pass@k under the wrong name; pass@k is only honest when you say k and the tests are the selector, which is not available in a product.
- **pass^k (all k succeed):** the probability that every one of k trials passes, about p^k for independent trials, estimated by C(c, k)/C(n, k). It is the reliability view. Anthropic's agent-evals post gives 75% per trial as about 42% pass^3 (vendor post). pass@k rises with k, pass^k falls.
- **Reported results:** the Codex abstract reports 28.8% solved with a single sample and 70.2% with 100 samples per problem (authors' setting, HumanEval). Implementation is Q13; agent use is Part 8 Q51.""",
example="Problem with n = 10 samples, c = 3 correct: pass@1 = 0.300 and pass@5 = 0.917. Bias, exact expectation over c for true p = 0.3, n = 10, k = 5: true pass@5 = 0.8319; the unbiased estimator averages 0.8319; the naive 1 - (1 - p_hat)^5 averages 0.7597. A per-trial success of 0.75 gives pass@3 = 0.984 but pass^3 = 0.422. Across three synthetic problems with (n, c) = (10, 10), (10, 7), (10, 2): mean pass@3 = 0.842, mean pass^3 = 0.431.",
code="q12.py",
follow="""- *Which should a product report?* If the user sees one answer, pass@1 or pass^k; pass@k only when a verifier picks among k.
- *Does pass@k assume independent samples?* The estimator assumes the n samples are drawn independently from the model; temperature and sampling must allow that.
- *HumanEval is small; how do you report uncertainty?* Bootstrap over problems (Q38).""",
mist="using 1 - (1 - p_hat)^k; reporting pass@100 as if it were what users get; computing the binomials directly and overflowing; using n = k so the estimate is noisy; mixing pass@k and pass^k.")

out = []
for n in range(1, 13):
    a = A[n]
    out.append(hdr(n))
    out.append(f"**Say this first (1 line):** {a['say']}\n")
    out.append(f"**Then explain:**\n{a['explain']}\n")
    out.append(f"**Example:** {a['example']}\n")
    src = open(f"code/{a['code']}", encoding='utf-8').read().rstrip('\n')
    assert '```' not in src
    r = subprocess.run([sys.executable, '-I', f"code/{a['code']}"], capture_output=True, text=True, cwd='.')
    assert r.returncode == 0, (n, r.stderr)
    out.append("**Code:** (mock LLM judges and toy synthetic data; numpy/stdlib only)")
    out.append("```python\n" + src + "\n```")
    out.append("**Output (my run):**\n```\n" + r.stdout.rstrip('\n') + "\n```\n")
    out.append(f"**Follow-ups:**\n{a['follow']}\n")
    out.append(f"**Common mistakes:** {a['mist']}\n")
open('answers.md', 'w', encoding='utf-8').write("\n".join(out))
