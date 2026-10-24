# Book 2 Part 11 — Sources & research notes (LLMOps, monitoring, tracing, prompt versioning, security)

Date: 2026-10-24. Band per plan.md: Rs 30-80 LPA roles; no salary figures used. WebFetch returns a model-summarised view, so details are "as summarised". WebSearch hit a spend limit mid-session; one search succeeded after reset (a search before the limit returned nothing). No candidate-reported questions were found; "Asked at" tags are company types or "guide, not a candidate report".

## Pages OPENED (WebFetch)
| Page | URL | Type | Used for |
|---|---|---|---|
| OWASP GenAI Top 10 for LLM Apps | https://genai.owasp.org/llm-top-10/ | primary | 2025 list LLM01-LLM10 (Prompt Injection, Sensitive Information Disclosure, Supply Chain, Data and Model Poisoning, Improper Output Handling, Excessive Agency, System Prompt Leakage, Vector and Embedding Weaknesses, Misinformation, Unbounded Consumption) |
| OWASP project page | https://owasp.org/www-project-top-10-for-large-language-model-applications/ | primary | points to 2025 as current; older 1.1 |
| OWASP LLM10:2025 | https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/ | primary | DoS, denial of wallet, model extraction, functional replication; mitigations (limits, rate limits, logprob restriction, monitoring, watermarking) |
| Simon Willison, lethal trifecta | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | expert blog | three legs; avoid combining; guardrail products unreliable, "95%" is failing |
| Greshake et al. (arXiv 2302.12173) | https://arxiv.org/abs/2302.12173 | primary abstract | indirect prompt injection; scenarios; Bing Chat, code completion, GPT-4 apps |
| CaMeL (arXiv 2503.18813) | https://arxiv.org/abs/2503.18813 | primary abstract | control/data flow separation, capabilities; 77% of AgentDojo tasks with provable security vs 84% undefended (authors' claim) |
| Design Patterns for Securing LLM Agents (arXiv 2506.08837) | https://arxiv.org/abs/2506.08837 | primary abstract | exists; pattern names NOT seen in the abstract |
| Anthropic: mitigate jailbreaks and prompt injections | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks | vendor docs, full text | harmlessness screens, input validation, untrusted content in tool results, JSON-encoding, least privilege, screening tool output, repeat offenders, monitoring, red-teaming |
| OpenAI safety best practices | https://developers.openai.com/api/docs/guides/safety-best-practices | vendor docs | red-teaming, limit input length, HITL, input and output validation, moderation |
| Langfuse prompt management overview | https://langfuse.com/docs/prompt-management/overview | vendor docs | versioning, labels, client cache, link to traces |
| Langfuse prompt version control | https://langfuse.com/docs/prompt-management/features/prompt-version-control | vendor docs | production/latest labels, rollback by moving label, 404 on missing label, protected labels (plan-dependent) |
| Langfuse observability overview | https://langfuse.com/docs/observability/overview | vendor docs | trace contents, token and cost tracking, async batched export; page did not cover sampling, masking or OTel |
| LangSmith observability | https://docs.langchain.com/langsmith/observability | vendor docs | traces, annotation and feedback, automations, dashboards; thin detail |
| Arize Phoenix tracing | https://arize.com/docs/phoenix/tracing/llm-traces | vendor docs | OTLP, framework instrumentation, projects, sessions, annotations |
| Helicone gateway overview | https://docs.helicone.ai/gateway/overview | vendor docs | routing, failover, caching and custom rate limits listed; budgets not discussed |
| MLflow: what is LLM observability | https://mlflow.org/articles/what-is-llm-observability-a-guide-for-ai-ops-teams | vendor guide | monitoring checklist (inputs, outputs, traces, drift, cost, safety) |
| NIST AI RMF | https://www.nist.gov/itl/ai-risk-management-framework | primary | RMF 1.0 26 Jan 2023; functions Govern/Map/Measure/Manage (from image alt text); GenAI profile NIST-AI-600-1 26 Jul 2024; RMF being revised |
| artificialintelligenceact.eu | https://artificialintelligenceact.eu/ | secondary | confirms AI Act exists; did NOT state regulation number or application dates; Article 50 and sandbox dates (Aug 2026) mentioned only as page text |
| OTel GenAI semconv pages (spans, metrics) and the new repo | https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/ ; https://github.com/open-telemetry/semantic-conventions-genai | primary, moved notices | only learned the conventions MOVED to a separate repo; attributes and stability status NOT read |

## Search results only (not opened)
Udemy "AI, LLM & LLMOps: 240 Interview Questions" (paid MCQ course), W&B LLM observability guide, Patronus LLM observability tutorial, Comet LLMOps guide: snippets only, topic confirmation.

## Failed or blocked
EUR-Lex (empty page), MeitY DPDP page (403), OWASP LLM01 page (404), no fetch of Llama Guard, Datadog, NeMo, Garak, PyRIT, vendor pricing, Langfuse sampling/masking pages. No Glassdoor/Blind/Reddit reports surfaced.

## Provenance
Primary or vendor docs opened: Q1-Q31 (topic coverage from the pages above). Expert gap-check (no direct source): coding Q32-Q37 (tracing decorator, registry, PII redactor, injection detector, token bucket, canary), code review Q38, design Q39-Q45 (partly guide-supported). Candidate-reported: none.

## Unverified; Wave B must hedge or avoid
- EU AI Act and India DPDP Act specifics (dates, risk tiers, obligations, penalties, rules, cross-border provisions): keep general, defer to counsel.
- OpenTelemetry GenAI attribute names, span naming and stability (repo moved, not read).
- Version-specific OWASP list items (2025 edition only; check for newer).
- Vendor features and plan gating (Langfuse protected labels, LangSmith/Helicone budgets, sampling and masking support) and any vendor figures.
- CaMeL 77% vs 84% (authors' AgentDojo claim) and names of the design patterns in arXiv 2506.08837.
- Any detector accuracy, attack success rate or guardrail false-positive figures: only from the answers' own runs.
- Provider data-retention and training-use terms (vary by plan; check live terms).
- Anthropic/OpenAI guidance as of the pages read on 2026-10-24.


## Wave B/C addendum (2026-10-24)
- arXiv 2506.08837 pattern names: the abstract (re-opened by the lead) names no patterns. The Q45 answer agent read the HTML paper through a summarising fetch, which returned six patterns (action-selector, plan-then-execute, LLM map-reduce, dual LLM, code-then-execute, context-minimization); this matches the lead's recollection of the paper but was not read from raw text, so the names stay 'reported via a summariser, check the paper'. The frozen Q45 heading lists five of the six; the sixth patterns are covered in the answer.
