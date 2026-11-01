**Say this first (1 line):** 6,000 rupees at 3 each buys 2,000 labels, a random sample gives about 60 examples of the 3% intent, so to reach 200 I would mix a small random slice with targeted sampling instead of buying 6,667 random labels.

**Clarifying questions:**
- Do all 10 intents matter equally, or is the rare one costly when missed? It decides whether 200 examples is worth the budget.
- How was the 3% measured, and from what period? It is a sample share, so the true share could be 2% or 4%.
- Can annotators handle Hinglish consistently, and what is their agreement? Noisy labels waste the budget.
- Do I have unlabelled tickets and an embedding or keyword search? That makes targeted sampling possible.
- Is there any existing label history, for example agent tags? Weak labels can seed the search.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data and labels 12, baseline 5, model 6, evaluation 6, rollout and monitoring 4, risks and cost 3):**
1. Clarify and frame: a classifier whose weakest intent is the rare one; the label budget is the main constraint.
2. Metrics and guardrails: per-intent recall and precision (macro average), with the rare intent reported alone, plus label agreement.
3. Data and labels: 6,000 / 3 = 2,000 labels. Random sample gives 2,000 x 0.03 = 60 rare examples (standard deviation about 7.6), and 40 to 80 if the true share is 2% to 4%. For 200 rare examples at random you need 200 / 0.03 = 6,667 labels, 20,001 rupees, 3.3 times the budget.
4. Baseline first: keyword rules and a TF-IDF plus logistic model on character n-grams (suits mixed Hinglish spelling), which also finds rare-intent candidates.
5. Model and trade-offs: plan 800 random labels (unbiased share and a clean test set) and 1,200 targeted ones from keyword or embedding search for the rare intent. At 30% precision of that pool that is about 360 rare examples; even at 15% it is 1,200 x 0.15 + 24 = 204. Then a small fine-tuned multilingual encoder or a prompted LLM with few-shot examples (editor knowledge: compare both on the same test set).
6. Evaluation: keep the random slice as the test set, label it twice on a subset to measure agreement, and report the rare intent with a range.
7. Rollout: shadow the classifier, send low-confidence tickets to humans, and use their corrections as new labels.
8. Monitoring and cost: weekly sample for the intent mix, retrain when a new intent appears, track label cost per rare example found.

**Metrics:**
- Rare-intent recall = rare tickets predicted rare / rare tickets in the random test slice (with its range).
- Label yield = rare examples found / labels bought.
- Guardrails: annotator agreement (for example Cohen's kappa), macro F1 across all 10 intents.

**Risks:**
- Targeted examples are not representative: use them for training only, never to estimate prevalence or test accuracy.
- The 800 random labels hold only about 24 rare tickets, so the rare-intent test is noisy.
- Keyword search finds only the easy phrasings.
- Hinglish spelling variants split the same intent.

**What the interviewer scores:**
- Strong: 2,000 labels, 60 expected, 6,667 and 20,001 needed, and a mixed plan with a test set kept random.
- Strong: says the 3% is a sample and shows 40 to 80.
- Weak: "label everything randomly" or "oversample" without noting the bias.

**Example:** Illustrative numbers. 6,000 / 3 = 2,000 labels; 2,000 x 0.03 = 60; 200 / 0.03 = 6,667 labels.
- Weak: "We will get 60 rare examples, that should be enough, we can use class weights."
- Strong: "A random sample gives about 60, with a range of 40 to 80 if the share is really 2 to 4 percent. To reach 200 I would spend 800 labels randomly for a clean test set and 1,200 on tickets found by keyword and embedding search. Even at 15 percent hit rate that gives about 204."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *How do you estimate prevalence after targeted labelling?* Only from the random slice, or by weighting by the inverse sampling probability.
- *Active learning?* Yes, after the first model: label the tickets near the decision boundary, then keep a random slice.

**Common mistakes:** Testing on the targeted sample. Quoting 3% as exact. Spending all labels before checking annotator agreement. Ignoring cost of a second annotator.
