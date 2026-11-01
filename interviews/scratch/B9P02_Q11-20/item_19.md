**Say this first (1 line):** Overfitting is memorising the practice questions instead of learning the subject, and I guard against it by testing on questions the model has never seen.

**Structure:** Use the "pattern for explaining anything" above.
1. Decision: why they care (the model must work on new customers, not just old ones).
2. Answer first: a model can look great on past data and fail on new data.
3. One picture: a student who memorises last year's exam answers and then meets new questions.
4. Number with meaning: "good on old data, much worse on new data" is the warning sign.
5. Not meant: a high score on past data does not prove it works.
6. Safeguard: keep some data hidden until the end, compare, keep the model simple enough, and monitor after launch.
7. Check: does that make sense?

**Strong sample answer (spoken):** Illustrative; replace with your own. "Imagine a student who memorises last year's exam, word for word. They score full marks on that paper, but on a new exam with different questions, they struggle. They learned the answers, not the subject. A model can do the same: it fits the past data so closely, including its quirks, that it fails on new cases. To guard against it, I hide part of the data until the end, like a surprise exam, and only trust the model if it does well on that too. I also keep the model as simple as the problem allows and check it again after launch. Does that picture make sense for your use case?"

**Weak version (and why it fails):** "The model has high variance and low bias, so it does not generalise." Correct to an engineer, meaningless to a business partner, who nods and learns nothing.

**What the interviewer scores:**
- Is the analogy accurate and everyday?
- Do you answer first, without jargon?
- Do you say what you actually do about it?
- Do you check understanding?
- Can you move to technical detail if asked?

**Make it yours:**
- Think of an analogy from your listener's own world (sales, cooking, sport) and test it for accuracy.
- Recall a time your model did well in training and worse on held-out data, and how you noticed.
- Write the one sentence for your safeguard using your real method.
- Say it aloud in under a minute.
- Be ready to explain the technical version too.

**Follow-ups:**
- Where does the analogy break down? "A student can understand; a model only finds patterns. I would say so if pushed."
- How would you explain it to a technical peer? "Gap between train and validation performance; regularisation, cross-validation, simpler models, more data."
- How do you know it is not overfitting after launch? "Monitor live performance against the held-out result."

**Common mistakes:**
- Jargon first.
- An analogy that implies the wrong thing.
- Naming the problem but no safeguard.
- Talking for five minutes.
- AI-era note: an AI-generated analogy may be generic; interviewers may ask for a second one, so understand why yours fits.
