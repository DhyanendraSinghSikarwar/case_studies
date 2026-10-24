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
| 3 | Prompting, structured outputs, function calling | 40 | ✅ (44 Qs) | ✅ | ✅ |
| 4 | Fine-tuning: SFT, LoRA/QLoRA, PEFT, distillation | 45 | ✅ (47 Qs) | ✅ | ✅ |
| 5 | Alignment: RLHF, DPO, safety, guardrails | 35 | ✅ (41 Qs) | ✅ | ✅ |
| 6 | RAG basics | 50 | ✅ (53 Qs) | ✅ | ✅ |
| 7 | Advanced RAG | 45 | ✅ (50 Qs) | ✅ | ✅ |
| 8 | Agents, tool use, MCP, multi-agent | 50 | ✅ (52 Qs) | ✅ | ✅ |
| 9 | LLM evaluation | 45 | ✅ (46 Qs) | ✅ | ✅ |
| 10 | Deployment: vLLM, quantization, latency/cost | 45 | ✅ (49 Qs) | ✅ | ✅ |
| 11 | LLMOps, security, prompt injection | 40 | ✅ (45 Qs) | ✅ | ✅ |
| 12 | GenAI system design + coding | 40 | ⬜ | ⬜ | ⬜ |

## Scope boundaries
Book 1 Part 9 owns light NLP/transformer intro; Book 4 owns generic MLOps/Docker/K8s; Book 6 owns GenAI scenarios. Book 2 is the deep treatment. Part 1 leaves PagedAttention, speculative decoding and quantization to Part 10, and decoding/sampling to Part 2.

## Environment notes (this session)
- WebSearch works; WebFetch is blocked (DNS), so sources are search snippets only and are labelled as such.
- torch/transformers may not be installed; code needing them must be marked `# not executed: <reason>`.

## Next step
Part 12 Wave A (GenAI system design + coding: build mini-RAG/agent from scratch; see plan.md), then Part 12 Wave B and review. Then Book 2 final pass (cross-reference check across Parts 1-12, header counts, question_index consistency) before starting Book 3. Parts 8-11 (52, 46, 49, 45 Qs) are complete and reviewed. Per-part scripts: copy scratch/B2P10_merge/merge.py and /tmp/claude-0/rev_b2p10/check.py with sed s/Part10/Part11/ (recreate check.py from an earlier part if /tmp is gone); Wave B brief template is scratch/B2P10_brief.md. Part 7 answers cross-reference Parts 8, 9 and 11 for depth; Part 8 must not repeat Part 7 Q13 (agentic RAG basics), Q31 (multi-hop loops) or Q47 (safe agentic RAG) but go deeper on agent architecture, memory, MCP and multi-agent. Part 6 notes: its answers are RAG-basics level with toy embeddings; Part 7 must go deeper on hybrid fusion, rerankers, GraphRAG, query rewriting and multi-hop without repeating Part 6 Q28-Q30. The user lifted the earlier agent pause with 'continue'. Reminders: apply lead edits AFTER the final scratch-to-file merge because the merge script replaces blocks wholesale; make the Example field mandatory in every Wave B brief; per-agent scratch files avoid concurrent-edit clobbering. Part 3 workflow that worked: each answer agent writes its range to scratch/<part>_Qxx-yy/answers.md and the lead merges by heading with scratch/B2P03_merge/merge.py (adapt the part number), which avoids concurrent-edit clobbering. Lesson from Part 2: parallel answer agents editing one file can clobber a boundary line (Q29 heading); run the heading/continuity check after every wave. WebFetch works now (some sites return 403/429); torch 2.14 CPU installed this session (pip install --index-url https://download.pytorch.org/whl/cpu torch).
