### Q18 ⭐⭐ 🟢 Happy number. For a positive integer n, repeatedly replace it by the sum of the squares of its decimal digits. `n` is an integer with 1 <= n <= 2^31 - 1. Return `[happy, steps, cycle_len]`: `happy` is True if the sequence reaches 1; `steps` is the number of replacements needed to reach 1 from n (0 when n is 1) or -1 when n is not happy; `cycle_len` is the length of the cycle the sequence eventually enters (1 for a happy number, because 1 maps to itself; for the others it is a fixed length you should find). Detect the cycle with Floyd's tortoise and hare in O(1) space (and compare it with a set of seen values). Explain why the sequence cannot grow forever (for a number with 4 or more digits the digit-square sum is smaller than the number, and for any 10-digit input it is at most 810) so it must repeat, and name the cycle every unhappy number ends in. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a dictionary of seen values to positions on small inputs. Example: n=19 -> [True, 4, 1]; n=2 -> [False, -1, 8]; n=1 -> [True, 0, 1]; n=7 -> [True, 5, 1]; n=4 -> [False, -1, 8].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Cycle detection on a number sequence (Floyd's tortoise and hare), plus a small proof that the sequence is bounded.

**Say this first (1 line):** "The map n -> sum of squared digits eventually repeats, because it shrinks large numbers. A happy number reaches the fixed point 1; every other number ends in the same 8-cycle 4, 16, 37, 58, 89, 145, 42, 20. Floyd's two pointers find it in O(1) space."

**Brute force:** Keep a dict `seen[value] = position`. Stop when a value repeats; the cycle length is the current position minus the earlier one. O(steps) time and space. Simple and what I check against.

**Optimal:**
- Floyd: slow moves one step, fast moves two. Stop when fast is 1 or slow == fast. If it stopped on 1 the number is happy. Otherwise `fast` is now inside the cycle.
- Cycle length: from that point step until you return to it, counting.
- Steps (for a happy number): just apply the map again from n until 1.
- Why it must repeat: for a number with d digits the digit-square sum is at most 81 d. For d >= 4, 81 d < 10^(d-1) <= n, so the sum is smaller than n (I checked f(n) < n for every n from 1000 to 300,000 and the inequality for d up to 39). So every value drops below 1000 and then stays under 243 (at most 3 x 81). A 10-digit input (the 2^31-1 range) gives at most 810 after one step. A finite set of values forces a repeat.
- The cycle for unhappy numbers is [4, 16, 37, 58, 89, 145, 42, 20], length 8. I checked every n < 200,000: happy implies cycle length 1, and every other number has cycle length 8.

**Complexity:** Each step costs O(digits), about 10 for the input range. The number of steps is small (the first step brings any input under 811; the output shows the longest run I measured). O(1) extra space for Floyd; the dict version is O(steps).

**Dry run:** n = 19: 1 + 81 = 82, 64 + 4 = 68, 36 + 64 = 100, 1 + 0 + 0 = 1. That is 4 steps, happy, cycle length 1 (1 maps to 1). Floyd on 19: slow 19, fast 82. Move: slow 82, fast f(f(82)) = 100. Move: slow 68, fast f(f(100)) = f(1) = 1. Stop on 1. n = 2: 4, 16, 37, 58, 89, 145, 42, 20, 4: back to 4 after 8 steps, so [False, -1, 8].

**Code:**
```python
import random

random.seed(1318)

def f(v):
    s = 0
    while v:
        v, d = divmod(v, 10)
        s += d * d
    return s

def happy(n):
    """Floyd: tortoise moves 1 step, hare 2; O(1) space. Then measure the cycle length from the meeting point."""
    slow, fast = n, f(n)
    while fast != 1 and slow != fast:
        slow, fast = f(slow), f(f(fast))
    x, c = fast, 1                          # fast is inside the cycle (or is 1)
    y = f(x)
    while y != x:
        y, c = f(y), c + 1
    steps = -1
    if fast == 1 or n == 1:
        steps, v = 0, n
        while v != 1:
            v, steps = f(v), steps + 1
    return [steps >= 0, steps, c]

def brute(n):
    """Dictionary of seen value -> position."""
    seen, v, i = {}, n, 0
    while v not in seen:
        seen[v] = i; i += 1
        v = f(v)
    return [1 in seen, seen.get(1, -1), i - seen[v]]

examples = [(19, [True, 4, 1]), (2, [False, -1, 8]), (1, [True, 0, 1]), (7, [True, 5, 1]), (4, [False, -1, 8])]
for n, exp in examples:
    got = happy(n)
    print(n, '->', got)
    assert got == exp and brute(n) == exp
print('trace of 19:', [19, f(19), f(f(19)), f(f(f(19))), f(f(f(f(19))))])

# exhaustive: every n < 200000 is happy or ends in the 8-cycle; list the cycle
for n in range(1, 200000):
    h, st, cl = happy(n)
    assert (cl == 1) if h else (cl == 8)
    assert [h, st, cl] == brute(n)
cyc, v = [], 4
while True:
    cyc.append(v); v = f(v)
    if v == 4: break
print('unhappy cycle:', cyc, '| checked every n < 200000: happy => cycle 1, unhappy => cycle of 8')

# why the sequence cannot grow: f(n) < n for n >= 1000 (checked), and the 10-digit bound
assert all(f(n) < n for n in range(1000, 300000))
assert all(81 * k < 10 ** (k - 1) for k in range(4, 40))
print('81*d < 10^(d-1) for every d >= 4; 10-digit bound 10*81 = 810; f(2^31-1) =', f(2 ** 31 - 1),
      ', f(1999999999) =', f(1999999999))
assert f(2 ** 31 - 1) <= 810 and max(f(n) for n in range(10 ** 9, 10 ** 9 + 1000)) <= 810

# longest run before a value repeats, over every n < 100000
def run_len(n):
    seen, v = set(), n
    while v not in seen:
        seen.add(v); v = f(v)
    return len(seen)
print('longest run before a repeat for n < 100000:', max(run_len(n) for n in range(1, 100000)), 'values')

# seeded random cross-check on large values too
for _ in range(500):
    n = random.choice([random.randint(1, 3000), random.randint(1, 2 ** 31 - 1)])
    assert happy(n) == brute(n)
print('random cross-check ok: 500 cases')

# edge asserts
assert happy(2 ** 31 - 1)[0] in (True, False)
assert happy(10) == [True, 1, 1] and happy(100) == [True, 1, 1] and happy(1) == [True, 0, 1]
print('edge asserts ok; 2^31-1 ->', happy(2 ** 31 - 1))
```

**Output (my run):**
```
19 -> [True, 4, 1]
2 -> [False, -1, 8]
1 -> [True, 0, 1]
7 -> [True, 5, 1]
4 -> [False, -1, 8]
trace of 19: [19, 82, 68, 100, 1]
unhappy cycle: [4, 16, 37, 58, 89, 145, 42, 20] | checked every n < 200000: happy => cycle 1, unhappy => cycle of 8
81*d < 10^(d-1) for every d >= 4; 10-digit bound 10*81 = 810; f(2^31-1) = 260 , f(1999999999) = 730
longest run before a repeat for n < 100000: 20 values
random cross-check ok: 500 cases
edge asserts ok; 2^31-1 -> [False, -1, 8]
```

**Edge cases:**
- n = 1: 0 steps, cycle 1.
- n = 10, 100: one step to 1.
- Largest input 2^31 - 1 is unhappy (result `[False, -1, 8]`).
- n = 4 (inside the unhappy cycle already): `[False, -1, 8]`.

**Follow-ups:**
- Why not just detect "reaches 4"? That works (the whole unhappy family goes through 4), but the proof that 4 is on every unhappy path is the same exhaustive check; Floyd or a set needs no such fact.
- Same technique elsewhere? Linked-list cycle (Floyd), and duplicate-number-as-cycle problems.
- Count happy numbers below N? Precompute with the map for each value; the map shrinks, so a memo works.

**Common mistakes:**
- Fast pointer started equal to slow, so the loop exits immediately.
- Assuming the sequence grows forever for big inputs.
- Forgetting n = 1 (already happy, 0 steps).
- Recomputing digits with strings in a hot loop without need (fine here, but say it).
