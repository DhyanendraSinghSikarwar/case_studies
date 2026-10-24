# Q24 toy tiered moderation. SYNTHETIC posts from templates; "LLM tier" is a mock with a fixed error rate. Numbers are toy-only.
import random, re, hashlib
random.seed(11)
BAD_SPAM = ["buy cheap pills now", "win free money click link", "earn cash fast click here"]
BAD_HATE = ["those people are vermin", "they should all vanish, subhuman scum"]
OK = ["lovely weather today", "check my cooking video", "the match was great", "i hate waiting in traffic", "click the link in my bio for my recipe"]
def leet(s): return s.replace("e", "3").replace("a", "4").replace("o", "0")
def make(n, attacked=False):
    out = []
    for _ in range(n):
        r = random.random()
        if r < 0.06: t, y = random.choice(BAD_SPAM), "spam"
        elif r < 0.09: t, y = random.choice(BAD_HATE), "hate"
        else: t, y = random.choice(OK), "ok"
        if attacked and y != "ok" and random.random() < 0.6: t = leet(t)
        out.append((t, y))
    return out
HASHES = {hashlib.sha1(b"win free money click link").hexdigest()}        # known-bad exact hash list
def norm(t): return t.replace("3", "e").replace("4", "a").replace("0", "o")
SPAMW = {"free": .4, "money": .3, "cash": .3, "pills": .5, "click": .2, "buy": .2}
HATEW = {"scum": .5, "vermin": .5, "subhuman": .6}
def cheap_score(t):                                                         # tier 2 classifier stand-in: keyword weights per category
    sp = min(1, sum(v for k, v in SPAMW.items() if k in t)); ha = min(1, sum(v for k, v in HATEW.items() if k in t))
    return (sp, "spam") if sp >= ha else (ha, "hate")
def llm_tier(t, y, cat):  # mock LLM with policy in prompt: right 92% of the time on gray-zone items (ASSUMED error rate)
    truth = (y == cat)
    return truth if random.random() < 0.92 else (not truth)
def pipeline(posts, use_norm, lo=0.2, hi=0.6, fail_open=True, llm_down=False):
    res, llm_calls = [], 0
    for t, y in posts:
        x = norm(t) if use_norm else t
        if hashlib.sha1(x.encode()).hexdigest() in HASHES: res.append((y, "remove:spam")); continue
        s, cat = cheap_score(x)
        if s >= hi: res.append((y, "remove:" + cat))
        elif s < lo: res.append((y, "allow"))
        else:
            llm_calls += 1
            if llm_down: res.append((y, "allow" if fail_open else "queue"))
            else: res.append((y, ("remove:" + cat) if llm_tier(x, y, cat) else "allow"))
    return res, llm_calls
def report(res):
    for cat in ("spam", "hate"):
        tp = sum(1 for y, a in res if y == cat and a == "remove:" + cat); n = sum(1 for y, a in res if y == cat)
        rem = sum(1 for y, a in res if a == "remove:" + cat)
        print(f"  {cat}: recall {tp}/{n} = {tp / n:.2f}   precision {tp}/{rem} = {tp / max(1, rem):.2f}")
clean, adv = make(2000), make(2000, attacked=True)
for name, posts, un in [("clean traffic", clean, False), ("attacked (leet-speak), no normalisation", adv, False), ("attacked, with normalisation", adv, True)]:
    r, calls = pipeline(posts, un); print(name, "| LLM calls:", calls, "of", len(posts)); report(r)
r, _ = pipeline(clean, False, llm_down=True, fail_open=True); print("LLM tier down, fail-open: bad posts allowed:", sum(1 for y, a in r if y != "ok" and a == "allow"))
r, _ = pipeline(clean, False, llm_down=True, fail_open=False); print("LLM tier down, fail-closed (queue): items sent to human:", sum(1 for y, a in r if a == "queue"))
