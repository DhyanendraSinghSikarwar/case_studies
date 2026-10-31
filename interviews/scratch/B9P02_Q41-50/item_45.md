**Say this first (1 line):** I would write a one-page summary built for the decision, with the recommendation, the trade-off, the risks and the cost first, and link every claim to the section of the design document where engineers can check the detail.

**Structure:** Two layers that point to each other (editor guidance [G]).
1. Top line: what is being proposed and what decision or approval is needed, in two sentences.
2. Why: the problem and the benefit in business terms, with the number that matters and how sure we are.
3. The main alternative considered and why it lost, in one or two lines.
4. Cost, timeline and dependencies, and the top risks with the safeguard for each.
5. Open questions and what is explicitly out of scope.
6. Links: each statement points to its section number so engineers can verify it.
Keep it to one page. Have an engineer read it for accuracy before it goes out, and keep the same terms and numbers as the design document.

**Strong sample answer (spoken):** Illustrative; replace with your own. "I would write the summary like this. 'We propose moving the recommendation model to a nightly batch job, replacing the live calls. This needs your approval for two engineers for six weeks. It cuts serving cost and removes a weekly outage risk. The trade-off is that recommendations will be up to a day old; we think that is acceptable for this use and will check with a test. We considered a streaming design but it costs more and adds little here. Main risk: the nightly job fails and shows stale results; we will alert and fall back to the previous day. Details in sections three and five.' Then I would ask the tech lead to read it and tell me if anything is simplified in a way that is wrong."

**Weak version (and why it fails):** Pasting the design doc's introduction, or dropping all caveats to make it sound clean. Executives still do not know what is asked of them, and engineers see an inaccurate summary and stop trusting it.

**What the interviewer scores:**
- Decision-first structure and a clear ask.
- Translation of technical choices into cost, risk and benefit.
- Accuracy: caveats and trade-offs survive.
- Traceability to the source document.
- Using a technical reviewer.

**Make it yours:**
- Pick a real design doc or project write-up you know.
- Write the two-sentence top line and the one number that matters.
- Choose the one trade-off you would not leave out.
- Ask a colleague to check that the summary is accurate for them.
- Do not summarise a document you have not read in full.

**Follow-ups:**
- What do you cut? "Method detail, history and rejected options beyond the main one, but I link them."
- How do you stay accurate? "I use the document's own terms and numbers and have an engineer review it."
- What if executives want even less? "One sentence plus the ask, with the page available behind it."

**Common mistakes:**
- Leaving out the trade-off so it reads as risk-free.
- Writing in the document's order, not the decision's.
- Changing numbers or terms.
- Using jargon the readers will not know.
- Skipping a technical review.
