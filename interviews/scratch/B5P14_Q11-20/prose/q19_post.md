**Edge cases:**
- A user with no tweets and no followees: empty feed.
- `follow(a, a)`: ignored; own tweets still appear exactly once (tested).
- Follow twice, unfollow twice, unfollow a stranger: all harmless (tested).
- Re-following brings the old tweets back (tested).
- Fewer than `feed_size` tweets exist: return what there is.
- Tweet ids 0 and 1 posted after 3 and 9 must come first: ids are not an ordering (tested with random repeated ids too).
- A user with 10,000 tweets: only the last k are touched (tested).

**Follow-ups:**
- *Why not sort all tweets?* O(T log T) per feed. The merge touches only f + k entries.
- *`heapq.merge`:* `heapq.merge(*[reversed(lst) for lst in lists], key=..., reverse=...)` can do the same lazily; the explicit heap makes the "stop after k" and the index bookkeeping visible.
- *Thread-safety (stated concept only):* the global counter increment and the list append in `postTweet` must be one atomic step so post numbers match list order; a lock around each mutator, and readers need a consistent snapshot of the follow set.

**Common mistakes:**
- Using the tweet id as the recency order.
- Letting a user follow themselves and then showing their tweets twice.
- Pushing all tweets of all followees onto the heap (O(T log T)).
- Forgetting to include the user's own tweets.
- Keeping an unfollowed user's old tweets in the feed.
