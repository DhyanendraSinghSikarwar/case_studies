# Book 2 Part 03 — Sources & research notes (Prompting, structured outputs, function calling)

Date: 2026-10-21. Target band per plan.md: Rs 30-80 LPA roles. No source states a salary band, so band fit is NOT verified for any report. WebSearch ran 7 queries (standard mode, US-only); WebFetch opened 9 pages (two Dataford pages returned 429). Stars blend topic frequency across guides with judgement; "Asked at" tags are company types unless a report names the company.

## Pages actually OPENED (WebFetch)
| Page | URL | Evidence type | Used for |
|---|---|---|---|
| techinterview.org: Why your agent returns broken JSON, and what interviews ask | https://www.techinterview.org/post/3233477302/structured-output-constrained-decoding-interview/ | prep article, no hiring company named | the four listed questions ("valid JSON but wrong numbers", logit-level constrained decoding, per-request schema compile latency/p99, when not to force a schema); failure modes of prompt-only JSON; XGrammar/Outlines/llguidance; cap retries at 1-2 and fail closed; Pydantic/Zod; guardrails vs format; Berkeley Function Calling Leaderboard. Q7, Q10, Q12, Q22, Q24, Q28, Q38-Q40, Q44 |
| DataCamp: prompt engineering interview questions | https://www.datacamp.com/blog/prompt-engineering-interview-questions | prep guide with Basic/Intermediate/Advanced labels; opening anecdote of an unnamed candidate asked about debugging a hallucinating RAG pipeline, an eval suite for subjective summarisation, and a tool-calling agent stuck in a loop | few-shot, CoT, decomposition, system vs user, structuring prompts, ambiguity, context engineering, output format, tool use, iteration, metrics, regression, LLM-judge, injection, versioning, monitoring, support-assistant design. Q1-Q6, Q16-Q18, Q21, Q27, Q32-Q35, Q41 |
| techinterview.org: What GenAI engineer interviews test | https://www.techinterview.org/post/3233476396/what-genai-engineer-interviews-test/ | prep article; names no company (says Meta, frontier labs and Series B startups run some version) | round structure; "how do you know a prompt change didn't make things worse" (golden set, regression, judge bias); ReAct loops can retry and compound errors. Q6, Q32 |
| InterviewBit: generative AI interview questions | https://www.interviewbit.com/generative-ai-interview-questions-and-answers/ | prep bank, no levels or companies | hallucination-reduction prompting, ReAct, CoT, few-shot, temperature/top-p. Q1, Q3, Q5, Q15 |
| OpenAI docs: function calling | https://developers.openai.com/api/docs/guides/function-calling | provider documentation (primary) | `tools` fields (`type`, `name`, `description`, `parameters`, `strict`), `tool_choice` (auto, required, forced function, `allowed_tools`, none), `parallel_tool_calls`, strict mode needs `additionalProperties: false` and all properties `required` (optional via null type), call loop with `call_id` and `function_call_output`, best practices (intern test, fewer than about 20 functions, enums). Q8, Q9, Q11, Q23, Q25, Q26, Q30, Q31, Q37 |
| Anthropic docs: tool use overview | https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/overview | provider documentation (primary) | `input_schema`, `tool_use`/`tool_result` blocks, `stop_reason: "tool_use"`, `tool_choice` with `disable_parallel_tool_use`, `strict: true`, client vs server tools, missing-required-parameter behaviour varies by model (may guess), tool search, token cost of tool definitions. Q8, Q9, Q11, Q17, Q25, Q26, Q30, Q31, Q37 |

## Seen via search results only (NOT opened)
| Item | URL | Evidence type | Used for |
|---|---|---|---|
| Dataford: Agentic AI Engineer role guide | https://dataford.io/roles/agentic-ai-engineer | aggregator claiming 127 candidate reports; page returned 429 on open, so figures come from a search snippet | prompt engineering tested in 49% of loops, tool use / function calling 47%, RAG 41%, median four rounds: used only as a frequency signal for stars; methodology unknown |
| Dataford practice questions on consistent structured outputs (HPE-labelled sample) | https://dataford.io/questions/how-would-you-design-and-optimize-prompts-to-ensure-consistent-structured-outputs-from-an-llm-api-for-hewlett-packard-enterprise-hpe-developer-workflows | sample/practice question, not a reported candidate question; 429 on open | Q7, Q33 topic confirmation only |
| Glassdoor Capgemini GenAI reviews (2025-26) | e.g. https://fr.glassdoor.ca/Entretien/Capgemini-Entretien-E3803-RVW95903382.htm | anonymous candidate reports, snippets only | topics reported: RAG, hallucination management, prompt engineering, evaluation metrics, LangChain/LangGraph; process often resume-based and shallower than big-tech loops. Q5, Q6 |
| Practitioner posts on tool-calling reliability (PromptLayer, dev.to, metacto) and CRITICTOOL (arXiv 2506.13977) | https://arxiv.org/pdf/2506.13977 | blogs and one research paper | tool hallucination vs key/value errors, endless retries after timeouts, retry budgets in app layer, idempotency keys, full trace capture. Q27-Q29 (low authority; treat as illustrative) |
| techinterview.org: ML engineer interview in the post-LLM era; faceprep prompt-engineering guide | https://www.techinterview.org/post/3233474925/ml-engineer-interview-post-llm-era/ | snippets | prompts as system-architecture decisions (where prompts live, versioning, A/B). Q33 |

## Question provenance
| Tag | Questions |
|---|---|
| prep-guide (opened) | Q1-Q7, Q10, Q12, Q15-Q18, Q21, Q22, Q24, Q32-Q35, Q38-Q41 |
| provider-docs (opened, primary) | Q8, Q9, Q11, Q23, Q25, Q26, Q30, Q31, Q37 (and the missing-parameter note in Q17) |
| practitioner / snippet level | Q27, Q28, Q29, Q44 (BFCL named in the structured-output article; no deeper source opened) |
| reported topics (anonymous, snippet level) | Q5, Q6, Q27 (Capgemini Glassdoor topics; DataCamp's unnamed-candidate anecdote) |
| expert gap-check (no source found; plan topic coverage and judgement) | Q13, Q14, Q19, Q20, Q36, Q42, Q43 |

## AI-era notes
- Prompting is now tested as system design (versioning, regression, evals), not just technique; reliable structured output and tool-calling reliability are the practical differentiators (Q6, Q7, Q10, Q27, Q28, Q38).
- Reasoning models change prompting advice (Q14, Q43); provider API details (parameter names, strict-mode rules, parallel-call behaviour) change fast, so answers must name the docs they were checked against and say to re-check.
- Reviewing LLM-written tool-calling code is a plausible AI-era round (Q37).

## Not found / blocked (honest)
- No first-hand candidate reports for Indian product companies (Flipkart, Swiggy, PhonePe) or big-tech labs on prompting or function calling; Glassdoor/Blind not reachable; no LeetCode Discuss post found. The Dataford aggregate could not be opened, so its numbers are snippet-level.
- Nothing found for Q13, Q14, Q19, Q20, Q36, Q42, Q43 beyond general guides: those answers must rely on well-known facts and runnable demos, not claims about what interviewers ask.
- Provider docs were opened on 2026-10-21 and will drift; the answers must say "check the current docs".
