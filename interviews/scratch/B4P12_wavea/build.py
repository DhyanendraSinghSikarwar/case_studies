import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0,'scratch/B4P12_wavea')
from qs import QS
order={'🟢':0,'🟡':1,'🔴':2}
QS=sorted(QS,key=lambda q:(-q[0],order[q[1]]))   # stable: stars 3,2,1; easy to hard inside a star
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
print(n,c)
assert n==45, n
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
assert sum(c)==45 and all(q[1] in order for q in QS)
assert len({q[2] for q in QS})==45
for s in (3,2,1):
    d=[order[q[1]] for q in QS if q[0]==s]
    assert d==sorted(d),(s,d)
# ---- set tags
SETS={'F':('Fraud detection platform (card and UPI-style payments)'),'R':('Recommender platform (video home feed)'),
 'D':('Demand forecasting platform (retail replenishment)'),'C':('Regulated credit-risk platform (bank-owned GCC, India)'),
 'L':('LLM-serving boundary (internal assistant, hosted model)'),'E':('Edge and on-device inference (field app)')}
tag=re.compile(r'^\[Set ([A-Z]), Q(\d) of (\d), (\d+) min, (\d+) pts\]')
got={}
for s,d,q,a in QS:
    m=tag.match(q)
    if m:
        k,i,of,mi,pt=m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5))
        assert of==4 and k in SETS
        assert i not in got.setdefault(k,{}),(k,i)
        got[k][i]=(mi,pt)
assert set(got)==set(SETS)
for k,v in got.items():
    assert sorted(v)==[1,2,3,4],(k,v)
    assert sum(p for m_,p in v.values())==100,(k,v)
    assert [v[i][1] for i in (1,2,3,4)]==[10,20,30,40]
setq=sum(len(v) for v in got.values())
assert setq==24 and n-setq==21
mins={k:sum(m_ for m_,p in v.values()) for k,v in got.items()}
# ---- cross-reference check against Part01..11 headings
heads={}
for p in range(1,12):
    t=open(f'Book4_MLOps/Book4_MLOps_Part{p:02d}.md',encoding='utf-8').read()
    heads[p]={int(x) for x in re.findall(r'^### Q(\d+) ',t,re.M)}
    assert heads[p],p
refs=set()
for s,d,q,a in QS:
    for m in re.finditer(r'Part (\d+) Q(\d+)',q):
        P,Q=int(m.group(1)),int(m.group(2)); refs.add((P,Q))
        assert P in heads and Q in heads[P],('unresolved',P,Q)
    assert not re.search(r'Part 12 Q',q)
print('refs resolved',len(refs))
rows=''.join(f"| {k} | {SETS[k]} | 4 | {mins[k]} min | 100 |\n" for k in sorted(SETS))
hdr=f"""# Book 4 — Part 12: Cost, scaling, security and MLOps system design (with timed mock sets)

**Topic:** cost control without price figures (FinOps tagging and attribution, showback and chargeback, right-sizing, idle GPUs, spot and preemptible capacity, batching, quantisation, caching, scale-to-zero, storage tiering, egress, unit economics and budgeting), scaling and capacity arithmetic (queues, backpressure, autoscaling, load shedding), security (secrets, least-privilege IAM, model and image supply chain, network isolation, PII and India data residency, model theft and extraction, policy as code, the agent and prompt-injection boundary at platform level), reliability (SLOs, rollback, disaster recovery, multi-Region, incident response), organisation (build versus buy, platform versus embedded teams, maturity, ML technical debt) and six timed end-to-end MLOps system-design sets (fraud detection, recommender, demand forecasting, regulated credit risk, LLM-serving boundary, edge and on-device)

**Target:** 45  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-26  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

How the sets work: there are 6 sets of 4 questions ({setq} of the {n} questions); the other {n-setq} questions are standalone. Each set question is tagged `[Set F, Q1 of 4, 6 min, 10 pts]`. Questions are listed by star rating (⭐⭐⭐ first) as the book requires, so the four questions of a set are scattered through the file; to run a set as a mock, collect its tag. Inside a set, Q1 is the clarify-and-requirements warm-up (10 pts), Q2 the core design or capacity step (20 pts), Q3 the data, operations or governance step (30 pts) and Q4 the hard integrative step with failure, cost and security (40 pts): 100 points per set, 40 to 45 minutes. Suggested scoring per question: 30 percent for clarifying questions and stated assumptions, 30 percent for a design that meets the stated numbers (check the arithmetic), 20 percent for naming the failure modes, security and cost consequences, 10 percent for the runnable check (a short Python simulation, validator or table with assertions), 10 percent for a crisp spoken summary in under 60 seconds. Bands: 85 to 100 strong hire-style answer, 70 to 84 solid with gaps, 50 to 69 needs the weak parts reviewed, below 50 redo the linked earlier parts. Time budgets and bands are practice targets set by this book, not any company's published rules.

| Set | Theme | Questions | Time | Points |
|---|---|---|---|---|
{rows}
Scope note: this part integrates, it does not reteach. Part 1 owns Git and pytest; Part 2 Docker; Part 3 Kubernetes and Helm; Part 4 DVC, MLflow and registry; Part 5 pipelines and orchestration; Part 6 serving mechanics, latency, shadow, canary and rollout; Part 7 CI/CD and promotion gates; Part 8 monitoring, drift and alerting; Part 9 feature stores, Kafka and Spark; Part 10 AWS and SageMaker depth; Part 11 Azure ML, Vertex AI and cross-cloud comparison; Book 1 owns ML theory; Book 2 owns LLM and RAG internals and prompt-injection technique; Book 3 SQL; Book 6 product and business metrics. This part owns cost, scaling, security, reliability and organisation decisions across the stack and end-to-end design. Every prompt names the earlier question it builds on (cited as Part N Qn) and all {len(refs)} distinct references were checked by script against the headings of Book4_MLOps_Part01 to Part11. Part 12 is the last part of Book 4.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book4_Part12_sources.md). No page was found that reports exact system-design or FinOps questions asked by a named company, so 'Asked at' tags name source types (ML system-design guides and courses, FinOps prep lists, regulator and law-firm explainers, OWASP summaries, maturity-model posts, job-posting patterns), not verified company reports; set contents are expert designs. All numbers in the prompts are invented, no prices or salary figures are used, and Indian regulatory statements (RBI FREE-AI of 13 Aug 2025, DPDP Act and Rules, RBI payment-data direction, SEBI cloud framework) come from adviser snippets and are hedged 'check the regulator's site and current law'. Wave B may run only: Python cost and capacity arithmetic in abstract units, queue, autoscaling, spot and failover simulations with seeds, the simplified IAM evaluator sketch scratch/B4P10_wavea/iam_eval_sketch.py (it does not model all IAM rules), secret and pickle scanners, policy YAML validators (pyyaml and pydantic), hash-chained logs, signature checks, threat-model and controls tables, and a small ONNX export and quantisation. No cloud calls, no credentials, no prices.

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q.strip()}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt=''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->')==45 and txt.count('**Asked at:**')==45
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt
assert txt.count('\n### Q')==45
open('Book4_MLOps/Book4_MLOps_Part12.md','w',encoding='utf-8',newline='\n').write(txt)
rows_i=''.join(f"| B4P12-Q{i} | 12 | {q.strip()} |\n" for i,(s,d,q,a) in enumerate(QS,1))
open('scratch/B4P12_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows_i)
print(n,c,mins)
