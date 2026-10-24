# Book 2 Part 12 — Sources & research notes (GenAI system design + coding)

Date: 2026-10-24. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch works this session but returns a model-summarised view ("as summarised"). No candidate-reported questions (Glassdoor, Blind, AmbitionBox, LeetCode Discuss) were found; every source is a prep guide, vendor or engineering blog, paper or regulator page.

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| GenAI System Design Interview worked examples (myengineeringpath) | https://myengineeringpath.dev/genai-engineer/system-design-interview/ | prep guide | 6-step framework; examples: RAG support chatbot, content moderation, code review agent; practice list incl. legal contract summaries, e-commerce hybrid search, enterprise Q&A with citations, telehealth triage, meeting summariser |
| KDnuggets: how to answer AI system design questions | https://www.kdnuggets.com/how-to-answer-ai-system-design-interview-questions | prep guide | 7-step framework (clarify, estimate, architecture, deep dive, trade-offs, failure modes, evolution); examples: ChatGPT, support AI, Copilot, code reviewer, legal assistant, voice assistant |
| PracHub GenAI system design guide | https://prachub.com/resources/generative-ai-system-design-interviews-how-to-design-llm-applications-that-work-in-production | prep guide | eight evaluation signals, 50-minute flow, common mistakes, example list (legal/medical RAG, document-processing, refund agent, model router) |
| BIRD paper | https://arxiv.org/abs/2305.03111 | primary abstract | 12,751 pairs, 95 DBs, 37 domains, 33.4 GB; 40.08% vs human 92.96% (2023, dated) |
| Spider paper | https://arxiv.org/abs/1809.08887 | primary abstract | 10,181 questions, 5,693 SQL, 200 DBs, 138 domains; cross-database generalisation |
| Twig voice latency budget | https://www.twig.so/blog/voice-ai-agents-latency-budget-800ms | vendor blog | per-stage table is the author's estimate; page's totals only work with overlap; vendor TTS and endpointing claims unverified; barge-in, speculative tool lookups |
| RouteLLM paper | https://arxiv.org/abs/2406.18665 | primary abstract | "more than 2x" cost cut claim, authors' own; no exact figures in abstract |
| RBI press release 61018 (FREE-AI) | https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=61018 | regulator | 13 Aug 2025; committee set 26 Dec 2024; seven Sutras, 26 recommendations, six pillars (principles not listed on page) |

## Search results only (snippets, not opened)
- Text-to-SQL: RSL-SQL, E-SQL, GenLink (reported about 66-67% BIRD, 88-90% Spider with GPT-4-class models; not comparable); DEV Community and vendor SQL-guard posts (read-only execution, treat generated SQL as untrusted, schema retrieval importance); THOR/VLDB workshop paper.
- Voice: AWS Builder Center, Cresta, tianpan.co posts, AssemblyAI, simbavoice (targets 300-800 ms vs 800-1500 ms; vendor numbers conflict).
- IDP/BFSI: Cygnet.One, SmartDev case study, eCorpIT India BFSI guide (vendor claims: about 90% straight-through, 95-99% accuracy; RBI video-KYC and DPDP mentions unverified; e-invoice IRN threshold claim unverified).
- RBI FREE-AI secondary coverage: KPMG India, Storyboard18, Drishti IAS, Outlook Money.
- DPDP Rules 2025: Mondaq, JSA Prism, Conventus, iPleaders (notified 13 Nov 2025; core duties 18 months later; 72-hour breach report; INR 250 crore ceiling reported). Official text not read.
- Semantic cache: InstCache arXiv 2411.13820 (GPTCache mismatch about 30% at 0.9), several practitioner blogs with conflicting thresholds.
- Routing: FrugalGPT and RouteLLM secondary write-ups (up to 98% and 85% cost cuts are secondary claims).
- E-commerce assistant: MACS arXiv preprint (catalogue-grounded multi-agent), ZenML LLMOps DB entry citing DoorDash, vendor blogs.
- Legal RAG: Stanford RegLab "Hallucination-Free?" via VentureBeat, LawNext, LLRX (17-33% for two tools, 43% GPT-4; disputed by vendor).
- Moderation: tianpan.co tiered pipeline post, techinterview.org LLD, Zefr/AAMAS paper (vendor figure about 12% contextual violations unverified).
- Indic/code-mixed ASR: HiACC corpus, Gnani.ai and Deepgram blogs (WER ranges are vendor figures), arXiv 2503.07522.
- Prep lists: Let's Code, Hyring, Simplilearn, DesignGurus, Educative, Audible/Payhip book listings (paid products).

## Failed or blocked
igotanoffer.com (403). No Indian company-specific GenAI design interview reports found (Flipkart, Swiggy, Razorpay, GCC searches returned generic guides). RBI FREE-AI full report PDF and DPDP Gazette text not read.

## Provenance of the 40 questions
- Guide-supported designs: framework, estimation, model selection, knowledge assistant, shopping assistant, voice agent, code reviewer, meeting summariser, legal/medical RAG, moderation, multi-tenant SaaS, agent-assist, text-to-SQL, IDP.
- Regulator/vendor-supported (India): bank chatbot, KYC/IDP, multilingual assistant, claims/underwriting agent.
- Expert gap-check only: coding questions (mini-RAG, agent harness, sqlite text-to-SQL, semantic cache, SSE streaming, memory manager, router, call harness, template engine, eval run, ACL retrieval, batch runner), serving-layer code review, incident review, air-gapped design, critique exercise, fallback ladder, executive launch brief.
- Candidate-reported: none.

## Unverified; Wave B must hedge or avoid
- Any benchmark number beyond the BIRD/Spider dataset sizes (leaderboard accuracies, "human 92.96%" is 2023-era).
- Voice per-stage latencies and vendor endpointing/TTS claims; human turn-taking thresholds and their academic attributions.
- Router and cascade savings (FrugalGPT, RouteLLM) and semantic-cache mismatch rates and recommended thresholds.
- Stanford legal-hallucination percentages (secondary, disputed, possibly updated).
- DPDP specifics (dates, 72-hour report, penalty ceiling, log retention), RBI directions (video KYC, deepfake rules, e-invoice IRN) and FREE-AI recommendation details beyond the press-release facts; defer to counsel.
- IDP accuracy, straight-through rate and cost-saving claims; ASR WER ranges for Hinglish.
- Prices, GPU throughput and provider limits: use labelled assumptions or own runs only.
- Vendor feature claims (Llama Guard, ShieldGemma, SQL guard products, LangChain features).
