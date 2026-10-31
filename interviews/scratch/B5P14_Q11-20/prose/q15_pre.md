**Pattern:** Iterator adapter with a one-element look-ahead buffer. An iterator only goes forward, so to answer "what comes next?" without consuming it, I pull one element early and hold it.

**Say this first (1 line):** "I keep one buffered element, filled eagerly in the constructor and refilled after every `next`, so `peek` returns the buffer and `hasNext` is a plain sentinel check."

**Brute force:**
- `list(it)` once and keep an index. That breaks the rules (not allowed), uses O(n) memory, and cannot work on an infinite or lazy stream.

**Optimal:**
- A private sentinel object `_DONE` marks exhaustion. A sentinel, not `None`, because `None` can be a real element.
- `__init__`: `buf = next(it, _DONE)`.
- `peek()`: return `buf`. Calling it twice returns the same value.
- `next()`: save `v = buf`, refill `buf = next(it, _DONE)`, return `v`.
- `hasNext()`: `buf is not _DONE`.
- Why eager: the buffer always holds the next value or the sentinel, so `hasNext` needs no call into the underlying iterator and cannot raise or have side effects.
- The cost is one extra element of memory. The trade-off: the underlying iterator is advanced one step earlier than the caller's `next`, which matters if pulling an element has a side effect or is slow (a lazy variant fills the buffer on the first `peek` or `hasNext`; the code below shows the eager one, and the test confirms the constructor pulled exactly one element).

**Complexity:**
- Every method O(1) apart from the cost of the underlying `next(it)`.
- Space O(1) extra (one buffered element).

**Dry run:** first example, `[1, 2, 3]`.

| call | buf after | returns |
|---|---|---|
| constructor | 1 | |
| next() | v = 1, buf = 2 | 1 |
| peek() | 2 | 2 |
| next() | v = 2, buf = 3 | 2 |
| next() | v = 3, buf = _DONE | 3 |
| hasNext() | | False |

Second example `[7]`: peek 7, peek 7, hasNext True, next 7 (buf becomes `_DONE`), hasNext False.
