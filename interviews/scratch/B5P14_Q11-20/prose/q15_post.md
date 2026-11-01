**Edge cases:**
- Empty iterator: constructor leaves `buf = _DONE`, `hasNext` is False immediately.
- Elements that are `None`, 0 or `''` are real data (tested). This is the reason for a private sentinel.
- `peek` twice, `next` once: both peeks return the same value.
- A generator that can be iterated only once works, since nothing is copied and nothing is rewound (tested).
- The checker never calls `peek` or `next` when `hasNext` is False. In a real API I would raise `StopIteration` there.

**Follow-ups:**
- *Why not call `next` inside `hasNext`?* It would consume an element that `peek` or `next` later needs, or force a second buffer; eager fill keeps one rule: the buffer is always current.
- *Lazy buffering:* fill on first demand, with a `filled` flag. Useful when constructing the iterator must not touch the source. Costs a branch in every method.
- *Thread-safety (stated concept only):* `next` reads the buffer and refills it in two steps, so concurrent callers need a lock around the method body or they may receive the same element twice.

**Common mistakes:**
- Using `None` as the "done" marker and mishandling real `None` elements.
- Refilling the buffer in `peek`, which consumes data.
- Calling `list(it)` (explicitly disallowed).
- Forgetting to refill after `next`, so `peek` returns the element just consumed.
