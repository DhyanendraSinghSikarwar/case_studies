import heapq, random
from collections import defaultdict

class NaiveTwitter:                      # brute force: one global list, scan newest to oldest, filter by author
    def __init__(self, feed_size): self.k = feed_size; self.all = []; self.f = defaultdict(set)
    def postTweet(self, user, tweet_id): self.all.append((user, tweet_id))
    def follow(self, a, b):
        if a != b: self.f[a].add(b)
    def unfollow(self, a, b): self.f[a].discard(b)
    def getNewsFeed(self, user):
        seen = self.f[user] | {user}
        return [t for u, t in reversed(self.all) if u in seen][:self.k]

class Twitter:
    def __init__(self, feed_size):
        self.k = feed_size
        self.clock = 0                              # global post number: the ONLY recency order
        self.tweets = defaultdict(list)             # user -> [(post number, tweet id)] oldest first
        self.following = defaultdict(set)           # user -> set of followees (never contains self)
    def postTweet(self, user, tweet_id):
        self.clock += 1
        self.tweets[user].append((self.clock, tweet_id))
    def follow(self, a, b):
        if a != b: self.following[a].add(b)         # set makes a double follow a no-op
    def unfollow(self, a, b):
        self.following[a].discard(b)                # not followed: no-op
    def getNewsFeed(self, user):
        heap = []
        for u in self.following[user] | {user}:     # f + 1 sources
            lst = self.tweets.get(u)
            if lst: heap.append((-lst[-1][0], u, len(lst) - 1))   # newest tweet of u; negative so the min-heap pops newest
        heapq.heapify(heap)
        out = []
        while heap and len(out) < self.k:           # k pops, each O(log f)
            negn, u, i = heapq.heappop(heap)
            out.append(self.tweets[u][i][1])
            if i:                                    # push u's next-older tweet
                heapq.heappush(heap, (-self.tweets[u][i - 1][0], u, i - 1))
        return out

def run(cls, init, ops):
    o = cls(*init)
    return [getattr(o, m)(*a) for m, a in ops]

ex = dict(init=[3], ops=[['postTweet', [1, 5]], ['getNewsFeed', [1]], ['follow', [1, 2]], ['postTweet', [2, 6]], ['getNewsFeed', [1]],
    ['postTweet', [2, 7]], ['postTweet', [1, 8]], ['getNewsFeed', [1]], ['unfollow', [1, 2]], ['getNewsFeed', [1]]])
want = [None, [5], None, None, [6, 5], None, None, [8, 7, 6], None, [8, 5]]
assert run(Twitter, **ex) == want == run(NaiveTwitter, **ex)
print('example ->', run(Twitter, **ex))

random.seed(19)
for case in range(800):
    k = random.randint(1, 5); ops = []; nxt = 100
    for _ in range(random.randint(0, 50)):
        r = random.random(); u = random.randint(1, 4); v = random.randint(1, 4)
        if r < 0.3: ops.append(['postTweet', [u, random.randint(0, 9)]])      # tweet ids repeat: they are labels, not an order
        elif r < 0.45: ops.append(['follow', [u, v]])
        elif r < 0.6: ops.append(['unfollow', [u, v]])
        else: ops.append(['getNewsFeed', [u]])
    assert run(Twitter, [k], ops) == run(NaiveTwitter, [k], ops), ops
print('800 random sequences match the naive reference')

# edge cases
t = Twitter(2)
assert t.getNewsFeed(1) == []                                  # nothing posted
t.follow(1, 1); t.postTweet(1, 9); assert t.getNewsFeed(1) == [9]   # self-follow does nothing: no duplicates
t.follow(1, 2); t.follow(1, 2); t.postTweet(2, 3); assert t.getNewsFeed(1) == [3, 9]
t.unfollow(1, 2); t.unfollow(1, 2); t.unfollow(1, 5); assert t.getNewsFeed(1) == [9]   # repeated / unknown unfollow is a no-op
t.follow(1, 2); assert t.getNewsFeed(1) == [3, 9]               # old tweets reappear on re-follow
t.postTweet(2, 1); t.postTweet(2, 0); assert t.getNewsFeed(1) == [0, 1]   # feed_size cap, ids 0 and 1 are not an order
# many tweets by one user: only k heap pops are needed
t = Twitter(3)
for i in range(10000): t.postTweet(1, i)
assert t.getNewsFeed(1) == [9999, 9998, 9997]
print('edge asserts ok')
