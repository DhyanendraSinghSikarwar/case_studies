# CLAUDE.md — ISB AMPBA Case-Study Workspace

This workspace builds 10 portfolio-grade analytics/AI projects modelled on ISB AMPBA capstones.

## Layout
```
isb_ampba/
├── CLAUDE.md                     # this file (workspace rules)
├── README.md                     # index + progress tracker
├── docs/ISB_AMPBA_Top10_CaseStudies_Plan.md   # master plan (methodology, alumni repos R1–R19, all specs)
├── case-studies/NN-<slug>.md     # one spec per project — the source of truth for what to build
├── templates/project-CLAUDE.md   # conventions copied into every project
├── projects/NN-<slug>/           # code lives here (one self-contained repo per case study)
├── claude-skills/                # skill sources (copy of the skills below)
├── install_skills.ps1 / .bat     # copies claude-skills/ -> .claude/skills/
└── .claude/skills/               # where Claude Code loads skills from
```

## First-run setup
If `.claude/skills/` does not exist or is missing any folder from `claude-skills/`, copy every folder from `claude-skills/` into `.claude/skills/` (create dirs), then tell the user to restart Claude Code so the skills load. Until then, read `claude-skills/<name>/SKILL.md` directly and follow it.

## Skills — use them, in this order
| Step | Skill | When |
|---|---|---|
| 1 | `ampba-new-project` | Start a case study: scaffold `projects/NN-<slug>/` from its spec |
| 2 | `ampba-data-sources` | Loading any dataset (UCI 350/502/144, yfinance, HF Amazon reviews, simulators) |
| 3 | `ampba-build-milestone` | Build one milestone (M1..M5) end-to-end, test, update README |
| 4 | `ampba-llm-agents` | Any LLM / RAG / LangGraph work (CS2, CS3, CS10) — mock-first |
| 5 | `ampba-review` | Mid-review (after M3) and final review (after M5) against acceptance criteria |
| 6 | `ampba-decision-memo` | Write DECISION_MEMO.md, MODEL_CARD.md, review deck outline |

## Workspace rules
1. The case-study spec in `case-studies/` is the contract. Do not drop modules, metrics or acceptance criteria; if one is infeasible, record why in the project README "Deviations" section.
2. One milestone per session/turn unless told otherwise. Stop after each milestone and report: what was built, test results, metrics, next milestone.
3. Every project follows `templates/project-CLAUDE.md` (copied into the project as its own CLAUDE.md).
4. Never fabricate results. Every number in README/memo must come from `outputs/summary.json` or `outputs/metrics.json` produced by code.
5. Reference repos (alumni work) are for design inspiration only — do not copy code verbatim; cite them in the project README "References".
6. Update the progress table in the root `README.md` when a milestone completes.
7. Windows + OneDrive: use pathlib, provide `tasks.py` as a `make` alternative, keep data/models/venv out of git and ideally out of OneDrive sync (`.venv` inside project is fine but gitignored).
