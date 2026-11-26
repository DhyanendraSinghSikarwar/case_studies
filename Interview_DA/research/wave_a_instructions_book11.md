# Wave A instructions — Book 11 (Soft Skills, HR Round, GD & Career-Switch Story) question lists (plan.md Sections 8.3, 8.4)

You build the FROZEN QUESTION LIST for ONE part of Book 11. No answers: every question is followed by `<!-- ANSWER_PENDING -->`.

Read first: `plan.md` (Sections 1-6, 8.3, 8.4, 9, Book 11 table), `style_guide.md` (Sections 2, 3, 7, 8), `research/interview_processes.md` (HR, managerial, behavioural, Amazon Leadership Principle, GD rounds by company type), `research/market_skills_2026.md` (communication 73%, stakeholder management 44%, dashboards/reporting 75% of JDs; pay seen in JDs), the JD samples in `research/jd_sample_*.md`, and for format only the header of `Book10_Domain/Book10_Part08.md` and `research/index_rows/B10P08.md`. Do NOT copy their questions.

## Book 11 part map (stay inside YOUR scope; other agents own the other parts)
| Part | Topic | Target |
|---|---|---|
| 1 | "Tell me about yourself" and the career-switch story (HR → data analytics) | 40 |
| 2 | Why data analytics / why this company / why leave HR | 40 |
| 3 | Behavioural (STAR) questions | 90 |
| 4 | Communication: explaining data and findings to non-technical people (priority skill: 73% of JDs) | 80 |
| 5 | Stakeholder management and teamwork scenarios (weak vs strong answer) | 100 |
| 6 | Problem-solving, ownership, learning agility | 80 |
| 7 | Group discussion topics and how to perform (short; evidence mostly campus-era and thin) | 30 |
| 8 | HR round: salary negotiation, notice period, gaps, relocation, offers, joining | 60 |
| 9 | Interview-room situations (blanking, not knowing an answer, nervousness, difficult interviewers, virtual interviews) | 40 |
| 10 | Skill-improvement playbooks: communication, storytelling, business acumen, structured thinking, presentation, written emails, confidence (as questions: assessment, daily practice, 30-day plan, resources, how to show it); this is the skill-development part | 40 |
| 11 | Amazon Leadership Principles STAR bank (Amazon GCC rounds are mostly LP behavioural; project end-to-end walkthrough stays in Book 8 Part 8) | 30 |

Boundaries (do NOT duplicate; grep `question_index.md` for these before finalising):
- Book 0 FAQs (rows B0Q1-Q123) already answer career-switch strategy questions (how long, which role, salary expectations, "why leaving HR" in outline, how to explain HR experience, handling a technical question you do not know, certifications). Book 11 asks the INTERVIEW-ROOM version: the exact question as an interviewer words it, answerable aloud in 1-2 minutes with a weak vs strong contrast.
- Book 8 owns analysis scenarios: stakeholder requests (Part 2: vague asks, urgent reports), prioritisation and ethics (Part 7), project deep-dive "walk me through your project" (Part 8), staying current (Part 9). Book 11 Parts 4-6 ask the BEHAVIOURAL and COMMUNICATION angle ("tell me about a time...", "how do you handle a manager who...", "explain this to a non-technical VP"), not the analysis method.
- Book 7 owns business metrics and HR cases; Book 10 Part 1 owns HR analytics domain questions; Book 10 Part 8 owns learning a new domain; Book 12 will own resume, LinkedIn and job search.

## Hard rule on personal experience
Behavioural and story answers describe what the CANDIDATE did. The book cannot know the candidate's real experience. Every question must be answerable with a template the candidate fills with TRUE experience; the questions themselves must not presuppose invented facts. Ask for a type of experience ("a time you disagreed with a stakeholder"), and where the candidate may have none, include a "no direct experience" variant ("you have never worked in analytics, what would you do if...").

## Research (mandatory, before writing)
1. Use WebSearch (load with ToolSearch `select:WebSearch` if deferred). Run at least 6 distinct searches for your topic, e.g. "<topic> interview questions data analyst 2025/2026", "<topic> interview questions India career switcher", "<topic> HR round questions Bengaluru/Hyderabad", company-specific experiences. If rate-limited, wait and retry with narrower queries; note blocked pages (Glassdoor, AmbitionBox, Reddit, LinkedIn). Pages may not be fetchable: record snippet-only honestly.
2. Record every source in `research/Book11_PartNN_sources.md` in the format of `research/Book10_Part08_sources.md`: URL, use, type, recency, honest note whether fetched in full or snippet only. No invented sources or company claims; mark unverified; state sample size/limitations and your star reasoning.
3. If you cannot research (tools unavailable), STOP, write nothing, report why.

## Question rules
- Questions a real interviewer asks a 0-3 year data/business/MIS analyst, especially a career switcher from HR. Canonical wording, one question per entry, no duplicates inside the part; do not write questions owned by another part or book.
- Stars ⭐⭐⭐/⭐⭐/⭐ from the research; difficulty 🟢🟡🔴. Sort: stars descending, then 🟢→🔴. Numbering Q1..Qn continuous.
- Target is a minimum; fill gaps. Mix: the direct question as asked, follow-up probes, "weak vs strong" traps, a few situational role-play questions, and for numeric topics (salary, notice period buy-out, CTC structure) small inline numbers answerable in 5 minutes.
- Reader is a non-technical HR career switcher: use HR-flavoured situations (payroll queries, attendance, hiring, attrition, onboarding) where natural.
- Sensitive topics (salary, notice period, employment gaps, relocation, health, family, age, caste or gender questions): ask the interview question as it is really asked, and include how a candidate handles an inappropriate or illegal-sounding question politely. Legal specifics will be labelled "from memory, unverified, confirm with HR/legal" at answer time.

## Files you write (only these)
1. `Book11_SoftSkills/Book11_PartNN.md` (mkdir -p):
```
# Book 11 — Soft Skills, HR Round, GD & Career-Switch Story | Part N: <title> <difficulty emojis>

**Target:** <target> questions | **Actual:** <n> questions
**Scope:** <one line>

### Q1 ⭐⭐⭐ 🟢 <canonical question>
<!-- ANSWER_PENDING -->
```
(no footer; inline data lines go directly under the heading line, before the marker).
2. `research/Book11_PartNN_sources.md`.
3. `research/index_rows/B11PNN.md`: rows `| B11PNNQn | 11 | N | <question> |` with header `| Q-ID | Book | Part | Canonical question |` and separator, like `research/index_rows/B10P08.md`.
Touch no other file. Scratch dir: `/tmp/claude-0/-home-user-case-studies/f1f97a91-a687-5c91-adf9-6191d712464e/scratchpad/A11_PartNN`. Do not commit or push.

## Final reply (short)
Files, actual count vs target, searches/fetches, blocked sources, gap-fill count, overlaps you avoided with Books 0, 7, 8 and 10, anything uncertain.
