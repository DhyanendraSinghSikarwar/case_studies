# Shared resources

Small helper modules used by every case study. They are deliberately short and readable: each notebook first
computes a quantity by hand, then uses the helper once the mechanics are clear.

| File | Contents |
|---|---|
| `utils.py` | Repository-root discovery, standard case folders, per-case seeded RNG, money/percent/p-value formatting, table saving |
| `plotting.py` | The book's figure style (colour-blind-checked categorical palette in a fixed order, readable fonts, recessive grid), `save_fig`, small annotation helpers |
| `statistical_tests.py` | `describe_numeric` (a richer `describe()`), t-based and bootstrap confidence intervals, Wilson proportion intervals, effect sizes. Extended as later cases need more |
| `presentation.py` | `Deck`: a thin `python-pptx` wrapper with a fixed visual language (action titles, takeaway bar, KPI tiles, chart and table slides) |

## Using them from a notebook

Notebooks locate the repository root by walking up from the working directory, so they run from anywhere:

```python
from pathlib import Path
import sys
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "00_shared_resources").is_dir())
sys.path.insert(0, str(ROOT / "00_shared_resources"))
from utils import case_paths
```

## Conventions

- **Reproducibility:** `utils.SEED` is the book-wide seed; `rng_for_case(n)` gives each case its own stream.
- **Colours:** use `plotting.CATEGORICAL` in order and never cycle past the number of groups you need.
  `PRIMARY` is the default single-series colour, `HIGHLIGHT` marks the one thing the reader should look at.
- **p-values** are printed with `fmt_p` (never "0.000").
