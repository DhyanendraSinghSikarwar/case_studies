# BOOK2_EXECUTION_PLAN.md — How Book 2 (GenAI / LLM / RAG / Agentic AI) will be built

Follows plan.md §5 (Book 2 table), §11 (workflow) and style_guide.md. Book 1 is complete (14/14), so Book 2 is next.

## Instructions (what to do for each part)
1. **Wave A — questions.** Web research on the part's topic (Glassdoor, AmbitionBox, LeetCode Discuss, Blind, GfG, Medium, prep banks, engineering blogs). Save `research_notes/Book2_PartNN_sources.md` (question, source URLs actually seen, found-in-sources vs expert gap-check, blocked sources). Never invent sources. Check `question_index.md` to avoid duplicates. Write `Book2_GenAI/Book2_GenAI_PartNN.md` in the `ANSWER_PENDING` format, ordered ⭐⭐⭐→⭐ (easy→hard within a star), then append rows to `question_index.md`. Freeze the list.
2. **Wave B — answers.** Replace each `ANSWER_PENDING` with the style_guide.md template (say this first, explain, example, code, follow-ups, common mistakes). Run every code snippet before inserting; shown numbers must come from real runs. Never reorder or renumber.
3. **Wave C — review.** Completeness, accuracy, code re-run, star order, header counts, dedupe across parts; write `review_notes/Book2_PartNN_review.md`, then `review_Book2.md`.
4. Update the Progress Tracker in plan.md after each phase.

## Part checklist (target Qs from plan.md)
| Part | Topic | Target | Wave A | Wave B | Wave C |
|---|---|---|---|---|---|
| 1 | Transformer internals: attention, positional encoding, KV cache | 45 | ✅ (47 Qs) | ✅ | ✅ |
| 2 | Tokenization, pretraining, scaling laws, decoding | 40 | ✅ (44 Qs) | ✅ | ✅ |
| 3 | Prompting, structured outputs, function calling | 40 | ✅ (44 Qs) | ⬜ | ⬜ |
| 4 | Fine-tuning: SFT, LoRA/QLoRA, PEFT, distillation | 45 | ⬜ | ⬜ | ⬜ |
| 5 | Alignment: RLHF, DPO, safety, guardrails | 35 | ⬜ | ⬜ | ⬜ |
| 6 | RAG basics | 50 | ⬜ | ⬜ | ⬜ |
| 7 | Advanced RAG | 45 | ⬜ | ⬜ | ⬜ |
| 8 | Agents, tool use, MCP, multi-agent | 50 | ⬜ | ⬜ | ⬜ |
| 9 | LLM evaluation | 45 | ⬜ | ⬜ | ⬜ |
| 10 | Deployment: vLLM, quantization, latency/cost | 45 | ⬜ | ⬜ | ⬜ |
| 11 | LLMOps, security, prompt injection | 40 | ⬜ | ⬜ | ⬜ |
| 12 | GenAI system design + coding | 40 | ⬜ | ⬜ | ⬜ |

## Scope boundaries
Book 1 Part 9 owns light NLP/transformer intro; Book 4 owns generic MLOps/Docker/K8s; Book 6 owns GenAI scenarios. Book 2 is the deep treatment. Part 1 leaves PagedAttention, speculative decoding and quantization to Part 10, and decoding/sampling to Part 2.

## Environment notes (this session)
- WebSearch works; WebFetch is blocked (DNS), so sources are search snippets only and are labelled as such.
- torch/transformers may not be installed; code needing them must be marked `# not executed: <reason>`.

## Next step
Part 3 Wave B (answers for Q1-Q44), then Part 4 Wave A. Lesson from Part 2: parallel answer agents editing one file can clobber a boundary line (Q29 heading); run the heading/continuity check after every wave. WebFetch works now (some sites return 403/429); torch 2.14 CPU installed this session (pip install --index-url https://download.pytorch.org/whl/cpu torch).
