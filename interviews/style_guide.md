# style_guide.md

## 1. Star rating (plan.md §3)
| Rating | Rule |
|---|---|
| ⭐⭐⭐ | Appears in most loops at this level; skipping it is risky |
| ⭐⭐ | Appears regularly; expected for strong candidates |
| ⭐ | Senior/niche/differentiator; asked at specific companies or roles |

Order inside each part: ⭐⭐⭐ → ⭐⭐ → ⭐ (within same star: easy → hard). Difficulty tag 🟢 Easy / 🟡 Medium / 🔴 Hard where relevant.

## 2. Question-list format (Wave A)
```
### Q12 ⭐⭐⭐ 🟡 <Question text>
**Asked at:** <companies / company types>
<!-- ANSWER_PENDING -->
```
Part file header: title, part topic, target count, actual count, date. Numbering Q1…Qn continuous per part.

## 3. Answer template (Wave B, plan.md §4)
```
### Q<n> ⭐⭐⭐ 🟡 <Question>
**Asked at:** <company types>
**Say this first (1 line):** direct answer in plain words
**Then explain:**
- 2–5 key points (bullets/table), simple language
**Example:** real-world or numeric example
**Code:** (if practical; must be executed before inserting)
**Follow-ups:** 1–3 likely follow-ups with short answers
**Common mistakes:** what candidates get wrong
```
Book 1 additions: from-scratch code in NumPy where relevant; AI-era twist (LLM/GenAI follow-up, code-review of LLM output) where relevant.

## 4. Answer-style rules
- Sound like a strong candidate speaking in the interview: plain spoken language, short sentences.
- Order: 1-line direct answer → 2–5 simple points → example → code → follow-ups → common mistakes.
- Explain any jargon in one line. No textbook density, no filler.
- Prefer bullets/tables. Formulas only when they are what an interviewer expects.
- Every code snippet is run before insertion (Python/NumPy/pandas/scipy/sklearn); fix failures.
- Never reorder, renumber, or edit questions outside your assigned range.
