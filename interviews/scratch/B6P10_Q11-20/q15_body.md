**Say this first (1 line):** Resume vectors are 2,000,000 x 768 x 4 bytes = 6.144 GB (decimal), or 1.536 GB at 1 byte per value, which fits one machine's memory, so the hard parts are label quality, ranking beyond similarity and fairness, not storage.

**Clarifying questions:**
- What is a good match: a recruiter shortlisting, an interview, or a hire? Different signals, different delays, and the target decides the label.
- Who sees the shortlist and does a human always decide? Automated rejection raises the stakes; I would design for decision support.
- How fresh must it be (new resume or new job appears in minutes)? It decides between a nightly batch and an online index.
- Which attributes may be used or must be excluded? Ask compliance and legal about fairness and protected-attribute rules; I will not state what is required.
- Are resumes multilingual or in mixed formats? Parsing and language coverage affect recall for some candidates.

**Approach:**
1. Clarify and frame. Goal: for each job, 200 good candidates in under 300 ms, with no hidden unfairness. Two stages: retrieve candidates by embedding similarity plus hard filters (location, skills, experience range), then re-rank.
2. Metrics and guardrails. Recall at 200 against recruiter-confirmed good candidates, ranking quality (NDCG at 10), recruiter time to shortlist, interview rate. Guardrails: selection rates by group (reviewed with compliance), latency p95, share of resumes ever shown.
3. Data and labels. Labels are noisy: recruiter clicks, shortlists, interviews. They reflect which candidates recruiters were shown (exposure bias) and past preferences (bias). Use graded labels (viewed, shortlisted, interviewed) and keep a random exploration slice if the product owner agrees.
4. Baseline first. Keyword and filter search (BM25-style) plus rules. Measure recall at 200 against labelled jobs; any embedding model must beat it.
5. Model and trade-offs. Embeddings (768 dimensions) for retrieval, a re-ranker with structured features. Storage: 6.144 GB in float32, 1.536 GB in int8 (see the code); the int8 shortlist overlapped the float32 shortlist well in a small synthetic test, but re-check on real data. Compute: 1,536,000,000 multiply-adds per brute-force query, which is why an approximate nearest-neighbour index or precomputing per job matters. Trade-off: recall versus latency versus memory.
6. Evaluation. Offline on held-out jobs with recruiter-confirmed matches; slice by seniority, language, city and group (as agreed with compliance); check for proxy features. Online: interleaving or an A/B test on recruiter time to shortlist and interview rate.
7. Launch and experiment plan. Shadow results shown beside the existing search, then 10% of recruiters, then wider. Gate on latency and the fairness review.
8. Monitoring, retraining and risks. Monitor index freshness, recall on a fixed set, selection rates, complaints. Retrain embeddings when the label distribution changes; document how candidates can correct their data.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 5, 6, 4, 10, 6, 5, 5.

**Metrics:**
- Raw storage = vectors x dimensions x bytes per value: 2,000,000 x 768 x 4 = 6,144,000,000 bytes = 6.144 GB (decimal); at 1 byte, 1.536 GB.
- Recall at 200 = recruiter-confirmed matches inside the shortlist / all confirmed matches for that job.
- NDCG at 10 = discounted gain of the top 10 divided by the best possible; recruiter time to shortlist.
- Selection-rate ratio between groups = selection rate of group A / selection rate of group B, reviewed with compliance (a monitoring signal, not a legal test).
- Guardrails: p95 latency under 300 ms, index age, complaint rate.

**Risks:**
- Learning past bias: if past hires favoured one group, labels teach the model to repeat it. Ask compliance and legal what testing and documentation are required.
- Proxy features (name, college, postcode, gaps) leaking sensitive attributes.
- Exposure bias: candidates never shown never get labels.
- Over-compressed vectors dropping rare skills; test recall per segment.
- Candidates gaming keywords; fake or duplicate resumes.

**What the interviewer scores:**
- Strong: 6.144 GB and 1.536 GB, then says storage is not the bottleneck and moves to labels and ranking.
- Strong: two-stage retrieve-and-rerank with a keyword baseline.
- Strong: fairness as design and monitoring, with compliance asked about the rules, not asserted.
- Weak: "embed everything and take the nearest 200", with no labels, bias or evaluation.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "I would use a big language model to score every resume against every job."
- Strong: "The vectors are 6.144 GB in float32 and 1.536 GB in 1-byte form, so they fit in memory. Brute force is about 1.5 billion multiply-adds a query, so I would use an approximate index with hard filters to get a few thousand candidates, then re-rank 200. I would measure recall against recruiter-confirmed matches, compare with a keyword baseline, check selection rates by group with compliance, and keep a human making every decision."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Would you store job vectors too? Yes, 150,000 x 768 x 4 = 0.4608 GB, and precomputing the shortlist per job nightly can cover most traffic; new jobs use an online query.
- How do you cope with sparse labels? Use weaker signals (views, saves) with lower weight, and use recruiter feedback on shown results to refresh the re-ranker.
- How do you test fairness with no sensitive attributes in the data? Ask compliance and legal what may be collected for testing and how; do not infer protected attributes without their guidance.

**Common mistakes:**
- Quoting megabytes or gigabytes without saying decimal versus binary.
- Treating click or shortlist labels as ground truth.
- Putting fairness only at the end, or stating legal rules as facts.
- Ignoring hard filters and going straight to nearest neighbours.
