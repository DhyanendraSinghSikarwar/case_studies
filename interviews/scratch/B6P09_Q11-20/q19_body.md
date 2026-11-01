**Say this first (1 line):** Whether the deployed model may keep running is not my call or the product team's: I would tell them it is a question for the privacy and compliance teams, bring them the facts they need (which records, which models, what retraining costs), prepare the retrain without the 15,000 patients now, and build a consent ledger so the next withdrawal is a filter, not a project.

**Clarifying questions:**
- What exactly was consented to, and what does withdrawal cover: future use, deletion of the raw records, or also models and derived data? That wording is for the privacy officer and legal to interpret.
- Does the model contain identifiable information (could it memorise records), or only aggregate patterns? It affects the risk discussion; I would ask the privacy team how they treat it.
- Where else do the 15,000 patients' data live: feature tables, embeddings, validation sets, logs, backups, vendors? We need an inventory.
- Is the 12.5% a one-off or a trend? A trend changes how we design the pipeline.
- Does the clinical safety side tolerate running the current model while the retrain is validated, or is switching it off safer for patients? That is for the clinical owner to decide.

**Approach:**
1. Do the arithmetic. 15,000 / 120,000 = 12.5%, so 105,000 records remain. The retrain is 3 days of compute plus a clinical re-validation; that is the cost of compliance, not a reason to delay the question.
2. Tell product plainly: I cannot say it is fine or not. I will take the options to privacy, compliance and the clinical owner this week, and give them a decision memo: (a) keep running until a retrained model is validated, with a stated end date; (b) switch to the previous model if one was trained without these patients; (c) pause the service. Each has a patient-safety cost and a privacy position; they choose.
3. Do the technical work in parallel. Start the retrain on the 105,000 now, in a staging area, so no time is lost whatever the decision is. Compare it with the current model on the validation set (also with withdrawn patients removed) to measure the performance change; with 87.5% of the data, a small change is plausible but must be measured.
4. Answer the data-side questions. List all copies and derived artefacts of the 15,000 patients' data, and the model versions trained on them. Questions to take to privacy and compliance: what must be deleted and by when, whether trained models count, what to tell clinicians and patients, what to record as evidence, and whether past analyses stay valid.
5. Design for cheap withdrawals. Keep a consent ledger (patient, purpose, status, effective date). Build the training table by joining that ledger at build time, record the manifest hash of each training set in the model registry, and keep lineage from raw data to features to model. A withdrawal then triggers a filter and a scheduled retrain, not an investigation.
6. Plan the retrain cadence. Retrain on a fixed schedule (for example monthly or quarterly) so that withdrawals are absorbed in routine releases, with the validation pack automated. Sharding the training data can reduce retrain work for rare withdrawals, but not for a batch like this (see the run).

**Metrics:**
- Withdrawn share = withdrawn records / training records = 12.5%.
- Time to honour = time from withdrawal request to the first deployed model without that patient (target set with the privacy team).
- Lineage coverage = records with consent status and lineage / all records (target 100%).
- Retrain performance delta = metric(retrained) - metric(current) on the same validation set, with an interval.
- Guardrails: no withdrawn id in any training manifest (checked by test), and clinical validation sign-off before release.

**Risks:**
- Assuming that removing rows from a table also removes their influence on a trained model; whether that is acceptable is a policy question.
- Missed copies: validation sets, exports and backups still containing the patients.
- Retraining quickly without re-validation, which trades a privacy risk for a safety risk.
- Hard-coding the answer ("keep running") when the rule might say otherwise.

**What the interviewer scores:**
- Strong: separates decisions (privacy, compliance, clinical) from the engineering work, and says so without stating rules as facts.
- Strong: gets 12.5% and 105,000, starts the retrain in parallel and measures the performance change.
- Strong: proposes a consent ledger joined at build time, manifest hashes and lineage.
- Weak: "it is fine, the model is anonymous", or "we must shut it down" with no questions asked.

**Example:** Illustrative. Weak versus strong:
- Weak: "The model does not store patient data, so it can keep running. I would just remove them next time."
- Strong: "I cannot decide that; the privacy and compliance teams and the clinical owner do. I will give them the options and the facts: 15,000 of 120,000 records, 12.5%, a 3-day retrain plus validation, and an inventory of every copy. I start the retrain on the 105,000 records now so we lose no time, and I will build a consent ledger joined at training time so a withdrawal is a filter and a scheduled retrain."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Can you "unlearn" instead of retraining? Approximate unlearning methods exist in the research literature (editor knowledge, not tested here); whether any is acceptable is a question for privacy and compliance, and validation is still needed.
- What if the retrained model is clearly worse? Report the delta to the clinical owner; options include more data from consented sources, or accepting a shorter-lived model; they decide.
- What do you log for audit? The ledger entry, the manifest hash of each training set, the model version, and the date of the deployed model that excludes the patient.

**Common mistakes:**
- Treating a privacy question as an engineering call.
- Deleting rows but leaving copies in features, validation sets or backups.
- Not recording which model was trained on which manifest.
- Planning for one withdrawal, not for a flow of them.
