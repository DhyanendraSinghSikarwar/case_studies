import os, sys
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0, 'scratch/B9P02_wavea')
from qs import Q, AS
order = {'🟢': 0, '🟡': 1, '🔴': 2}
S = sorted(Q, key=lambda q: (-q[0], order[q[1]]))   # stable
N = 50
n = len(S); c = [sum(1 for q in S if q[0] == s) for s in (3, 2, 1)]
assert n == N and sum(c) == N, (n, c)
assert [q[0] for q in S] == sorted([q[0] for q in S], reverse=True)
for s in (3, 2, 1):
    d = [order[q[1]] for q in S if q[0] == s]; assert d == sorted(d)
assert len({q[2] for q in S}) == N
for q in S:
    assert q[2].strip() and q[3] in AS and q[1] in order, q[2][:40]
    assert '<!--' not in q[2] and '|' not in q[2] and '\n' not in q[2]
    assert q[2].strip().endswith(('?', '.'))
def stars(s): return '⭐' * s
body = ''; rows = ''
for i, (s, d, t, a) in enumerate(S, 1):
    body += f"### Q{i} {stars(s)} {d} {t}\n**Asked at:** {AS[a]}\n<!-- ANSWER_PENDING -->\n\n"
    rows += f"| B9P02-Q{i} | 2 | {t} |\n"
hdr = f"""# Book 9 — Part 2: Communication, Data Storytelling and Stakeholder Management

**Topic:** How to explain, write, present and handle things as a data science, ML engineer or GenAI practitioner. Explaining models and statistics to non-technical people (random forest and boosted trees, regression, clustering, neural networks, LLMs, accuracy, precision and recall, AUC, p-values, confidence intervals, A/B results, correlation versus causation, overfitting, bias and fairness, probability forecasts, limitations, hallucination risk), storytelling with data (structure, charts, executive summaries, one-slide updates, null results, conflicting numbers, defending an analysis), written communication (status updates, emails, READMEs, design-doc summaries, incident reports, Slack escalations, documenting assumptions), stakeholder management (vague requests, expectations, saying no, scope changes, prioritising, delays, decisions, post-launch follow-up), presentation skills (openings, hostile questions, whiteboards, failed demos, time cuts, remote talks) and AI-era communication (explaining and disclosing AI-assisted analysis, reviewing AI-written work, explaining LLM limits).

**Target:** 50  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-31  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

**Scope note:** this part is editor guidance for the communication questions in data, ML and GenAI interviews. The answers in Wave B are templates, not scripts to memorise, and every one ends with a prompt to use your own real example. In this part the label Structure means the explanation or writing structure, and Strong sample answer means the spoken explanation or the short written sample (an email, an update, a summary). It gives no pay or negotiation figures and no legal advice. Behavioural stories ("tell me about a time") belong to Book 9 Part 1; numeric trade-off and stakeholder scenarios belong to Book 6 Part 6; metric definitions to Book 6 Part 1. This part asks "how would you explain, write, present or handle X". Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch result snippet or summary only (see research_notes/Book9_Part02_sources.md). The searches returned question banks (Dataford, Interview Query, TryExponent, Prepfully, Yardstick, Adaface), a few Towards Data Science pieces, general presentation-training pages and vendor LLM explainers. They agree on themes, not on wording, and none is a company rubric. 'Asked at' lines name guide families; 'commonly reported in public guides' is used only where a snippet supports the theme. Thin coverage: live-demo failures, remote presentations, Slack escalations, README writing, post-launch follow-up and the exact null-result and reconcile-two-dashboards framings; those lines say 'editor-designed' or name the nearest guidance. No company is named as asking a question except where a snippet listed it, and that listing is secondhand. Star counts and difficulty tags are editorial.

---

## A pattern for explaining anything to a non-technical person

This is editor guidance [G], not a company requirement. Public guides repeat the same core advice: check who is listening, tie the result to a decision, and use a concrete example (sources: research_notes/Book9_Part02_sources.md, snippets only). Treat the steps as a checklist for your own words, not a script.

1. **Name the decision.** Say what the listener has to decide or do, in one sentence. Everything else serves that.
2. **Answer first.** Give the conclusion or the plain-language meaning before any method.
3. **Use one familiar picture.** One analogy or one concrete example from their world. Not three.
4. **Give the number with its meaning.** Say what the figure means in people, orders or money, and how sure you are, in a range or in words such as "likely" and "not yet known".
5. **Say what it does not mean.** One common misreading and the correction, because that is where decisions go wrong.
6. **Name the limit and the safeguard.** Where it can fail, and what you will check or who reviews it.
7. **Check understanding and stop.** Ask "what would you want to know before you decide?" and leave room. Offer the detail, do not pour it out.

Worked example (illustrative; replace with your own): a p-value for a product manager. Decision: ship or not. Answer first: "The lift looks real but is small." Picture: "If the change did nothing, how often would we still see a gap this big by luck? The p-value answers that." Number: "About one time in twenty." Not meant: "It is not the chance the change works." Limit: "It says nothing about whether the lift is big enough to matter, so look at the range." Check: "Does the range change your decision?"

---

"""
open('Book9_SoftSkills/Book9_SoftSkills_Part02.md', 'w').write(hdr + body.rstrip('\n') + '\n')
open('scratch/B9P02_wavea/index_rows.txt', 'w').write(rows)
print(n, c)
