# Wave B instructions — Book 11 (Soft Skills, HR Round, GD & Career-Switch Story) answers

You answer a frozen question range. Read `plan.md` (Sections 4, 5, 8.5), `style_guide.md` (Sections 10 and 11), this file, and `research/Book11_PartNN_sources.md` for YOUR part (resolve or label every "uncertain" item it lists). Tone/layout reference: finished chunks in `Book08_Scenarios/answers_chunks/` and `Book10_Domain/answers_chunks/`.

## Who you write for
A non-technical HR professional switching to data analytics, facing HR, managerial and behavioural rounds. Plain words, spoken-aloud style (how a calm, confident candidate would actually say it), no corporate jargon, no memorised-sounding paragraphs. Every answer teaches the candidate HOW to build their own answer.

## HARD RULE: never invent the candidate's experience
The book cannot know what the candidate really did. Every personal-story answer is therefore:
1. a TEMPLATE the candidate fills with TRUE experience (use `[square-bracket placeholders]`), and
2. an ILLUSTRATIVE example (clearly headed "Illustrative example, replace with your own true story") that borrows an HR-analytics situation (payroll error, attendance report, attrition data, hiring tracker, onboarding) with small invented numbers, and
3. an explicit line: "Say this only if it is true for you. If you have no direct example, use the no-experience version below."
Never write "In my previous role I increased X by 30%" as if it were fact. Never fabricate statistics, company policies, laws, salary benchmarks or interview reports.

## What you produce
- Read your range from `Book11_SoftSkills/Book11_PartNN.md` (read-only; do NOT edit it). Copy each heading AND any inline-data lines under it EXACTLY.
- Write ONE chunk file `Book11_SoftSkills/answers_chunks/B11P<NN>_Q<from>-<to>.md` (mkdir -p): for each question in your range IN ORDER, the exact heading line (+ data body) copied unchanged, then the full answer. No preamble. Never renumber/reorder/drop/rewrite questions. Touch no other file. Do not commit.
- Scratch folder: `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/B11P<NN>_Q<from>-<to>` (yours only). Run `python3 script.py` for any arithmetic.

## Answer templates
Common header for every answer:
```
### Q<n> ⭐⭐⭐ 🟢 <question — copied exactly>
(data lines copied exactly, if any)
**Asked at:** <only what Book11_PartNN_sources.md / research/interview_processes.md supports; otherwise "commonly asked (no company-specific report found)">
**What the interviewer is checking:** <1 line>
**Say this in the interview:** <1-2 plain-spoken lines: the shape of a good answer>
```
A) Story / behavioural / situational question (Parts 1, 2, 3, 5, 6, 9, 11 and most of 4, 8):
```
**Weak answer (what not to say):** <1-3 short sentences, realistic>
**Why it is weak:** <1 line>
**Strong answer (template, speak it in your own words):** <60-130 words aloud, with [placeholders]>
**Illustrative example, replace with your own true story:** <a short worked example in an HR-analytics situation with small invented numbers>
**STAR breakdown:** Situation: ... Task: ... Action: ... Result: ... (one line each; for non-story questions replace with the structure that fits, for example Point, Reason, Example, Link back to the role)
**If you have no direct experience:** <the honest alternative: a related example, a class or project, or "how I would handle it" with the steps>
```
B) Concept / how-to / skill-playbook question (Part 10, parts of 4, 7, 8, 9):
```
**Explain simply:** 2-5 bullets
**Plan / steps:** numbered steps; for playbook questions give assessment, daily practice, 30-day plan, free resources and how to show it, as the question asks
**Worked example or script:** <a short model answer, role-play script or example with numbers computed by code where numeric>
```
Then always:
```
**Likely follow-ups:** 1-3 with short answers
**Common mistakes:** <what beginners get wrong>
```
About 180-380 words per answer; shorter for easy ones. No filler. NEVER use em dashes (use commas, colons, semicolons, parentheses).

## Part-specific notes
- Part 7 (GD): evidence is thin and mostly campus-era; say honestly that lateral hires seldom get a GD. Give structure, phrases, sample points on the topic, and etiquette; do not claim any company runs a GD unless the sources file does.
- Part 8 (HR round): all salary, CTC, hike and notice-period figures in questions are EXERCISE inputs; compute every figure with a script; state rounding. Real pay bands: only from `research/market_skills_2026.md` and `plan.md` Section 2 (JDs mostly Rs 3.5-9 LPA, non-random sample, unverified). Labour-law, notice-period enforceability, offer-revocation and background-verification specifics: awareness only, "from memory, unverified, confirm with HR/legal". Never advise lying, inflating a current salary or hiding a competing offer; give honest, tactful scripts.
- Parts 5, 9, and any question about inappropriate personal questions (age, marital status, family, religion): give a polite deflection script and say specifics of law are "from memory, unverified, confirm with HR/legal".
- Part 10 (playbooks): resources and podcasts/courses/communities only if you are confident they exist; label "from memory, unverified, check the link". Do not claim effectiveness statistics. Include a self-check test, daily practice and a 30-day plan where the question asks.
- Part 11 (Amazon LP bank): the list and wording of the principles comes from memory, labelled "from memory, unverified, check Amazon's own page". Tie each answer to the named principle; show STAR with a measurable Result; never claim to know Amazon's scoring; remind that stories must be true and must say "I", not "we".
- Part 1 and 2: give a 60-90 second spoken structure (present, past, future / link to the role), an HR-to-analytics bridge, and what to leave out; no invented achievements.

## Verification and honesty rules
- Compute every number by code; where a question's inline data is inconsistent or its premise is wrong, say so, solve the sensible version and list it in your final report.
- Real-world facts (laws, company policies, interview formats, salary norms, platform names) are NOT verified (no web): principle only, labelled "from memory, unverified". Never state a statistic as fact; numbers in questions are invented exercise inputs (the Part 8 questions Q13 and Q31 use invented offer figures: treat them as exercise inputs).
- "Asked at" must follow the sources file; prep-site claims stay marked unverified.
- Verification scripts stay in the scratch folder; do not paste them into answers.

## Reporting
Final reply (short): chunk path, number of answers, questions with premise problems (IDs and what you changed), what was verified by script, anything unverified.
