**Pattern:** K-way merge with a heap (Part 8 Q10 style). Each user's tweets are already in posting order, so the feed is a merge of newest-first lists that stops after `k` items.

**Say this first (1 line):** "Recency is one global post counter; each user keeps a list in posting order, and the feed is a heap merge of the newest-first lists of the user and followees, stopped after feed_size pops."

**Brute force:**
- One global list of all tweets. For a feed, scan from newest to oldest, keep tweets whose author is the user or a followee, stop after `k`. O(total tweets) per feed in the worst case (it is the oracle).

**Optimal:**
- `clock`: global post number, +1 per `postTweet`. Tweet ids are labels (the example posts 5, 6, 7, 8 but another run could post 9, 2, 5), so recency comes only from the counter.
- `tweets[user]`: list of `(post number, tweet id)`, oldest first. `following[user]`: set of followees, never containing the user.
- `follow(a, b)`: ignore when `a == b`; set add (twice is the same as once). `unfollow(a, b)`: `discard` (a no-op when not followed). Past and future tweets of `b` leave and re-enter the feed at once, because the feed is computed from the current follow set.
- `getNewsFeed(u)`: sources = followees plus `u`. Push `(-newest post number, user, index of newest)` for every source that has tweets, heapify. Pop up to `k` times: take the tweet, then push that user's next-older tweet. Ties cannot occur because post numbers are unique.

**Complexity:**
- `postTweet`, `follow`, `unfollow`: O(1) average.
- `getNewsFeed`: O(f) to build and heapify, plus up to k pops and pushes at O(log f) each: O(f + k log f), independent of how many tweets exist. With k <= 20 this is tiny.
- Space O(tweets + follow edges).
- Stated concept: a real service pre-computes feeds. Fan-out on write pushes each new tweet into every follower's stored feed (fast reads, slow posts for users with millions of followers); fan-out on read merges at request time as here (cheap writes, costly reads); large systems mix the two, using fan-out on write for ordinary users and fan-out on read for celebrity accounts.

**Dry run:** first example, `feed_size = 3`.

| call | state | returns |
|---|---|---|
| postTweet(1, 5) | tweet 5 gets post number 1 | None |
| getNewsFeed(1) | sources {1}: [5] | [5] |
| follow(1, 2) | following[1] = {2} | None |
| postTweet(2, 6) | post number 2 | None |
| getNewsFeed(1) | heap (-1, user 1), (-2, user 2): pop 6, pop 5 | [6, 5] |
| postTweet(2, 7) | post number 3 | None |
| postTweet(1, 8) | post number 4 | None |
| getNewsFeed(1) | newest per source: user 1 -> 8 (4), user 2 -> 7 (3). pop 8, pop 7, push user 2's 6 (2) vs user 1's 5 (1): pop 6 | [8, 7, 6] |
| unfollow(1, 2) | following[1] = {} | None |
| getNewsFeed(1) | only user 1: 8, 5 | [8, 5] |
