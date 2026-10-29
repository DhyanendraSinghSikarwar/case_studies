### Q2 ⭐⭐⭐ 🟢 Number of 1 bits. `n` is an integer with 0 <= n < 2^32. Return `[popcount, naive_iterations, kernighan_iterations]`: the number of 1 bits in `n`; the number of times the loop `while m: m >>= 1` runs (examining one bit per round, starting from m = n); and the number of times the loop `while m: m &= m - 1` runs. Explain why `m & (m - 1)` clears exactly the lowest set bit, why the Kernighan loop count equals the popcount, and why the naive count equals `n.bit_length()`. Also compare with `bin(n).count('1')` and `int.bit_count()` (added in Python 3.10; on older versions it does not exist) and say which one you would write in an interview and why you still need to know the loop. In the answer include a dry run on the first example and a seeded random cross-check of your solution against bin(n).count('1') and n.bit_length() on small inputs. Example: n=11 -> [3, 4, 3]; n=0 -> [0, 0, 0]; n=2147483648 -> [1, 32, 1]; n=4294967295 -> [32, 32, 32]; n=1 -> [1, 1, 1].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened) | Python integer documentation (docs.python.org fetch failed, not opened; behaviour verified by running Python 3.13; the version in which int.bit_count appeared is editor knowledge, not checked against a page)

**Pattern:** Bit counting with the lowest-set-bit trick (Brian Kernighan).

**Say this first (1 line):** "m & (m - 1) clears exactly the lowest set bit, so looping until m is 0 runs once per set bit. Shift-and-test runs once per bit position up to the highest set bit, which is bit_length. Return [popcount, naive, kernighan]."

**Brute force:** Shift right one bit at a time and test the low bit (or `bin(n).count('1')`). The loop `while m: m >>= 1` runs `bit_length` times: up to 32 for a 32-bit input.

**Optimal:**
- Kernighan: `m &= m - 1` per round. Subtracting 1 flips the lowest set bit to 0 and every 0 below it to 1; the bits above are unchanged. AND-ing with the original keeps the bits above, and the flipped region becomes all 0 (the lowest set bit was 1 in m but 0 in m - 1, and the lower bits were 0 in m). So exactly one set bit disappears per round.
- So the iteration count equals the popcount: each round removes one set bit and nothing else, and the loop stops at 0.
- Naive count: `m >>= 1` drops the lowest bit each time, and m reaches 0 exactly when all `bit_length` bits are gone. So the count is `n.bit_length()` (0 for n = 0).
- Compare: `bin(n).count('1')` is simple and fine. `int.bit_count()` is the one I write in an interview: it is a one-call popcount, written in C. It was added in Python 3.10 (editor knowledge, not checked against the docs); on an older version it raises AttributeError. I ran it on 3.13 and it matches in every test below. I still need the loop: interviewers ask "do it without the built-in", and the loop is the base of other tricks (power of two is `n & (n - 1) == 0`).
- Python note: the input is 0 <= n < 2**32 for a reason. For a negative number both loops never terminate, because Python ints have infinitely many leading 1 bits (shown capped at 100 rounds below). If you must handle negatives, mask first: `n & 0xFFFFFFFF`.

**Complexity:** Naive: O(bit_length), at most 32 rounds. Kernighan: O(popcount), at most 32 rounds, best on sparse numbers. Space O(1). With a fixed 32-bit bound both are O(1); the difference matters for sparse or big values (for example 2**1000 + 1 needs 2 Kernighan rounds, about 1000 naive rounds).

**Dry run:** `n = 11 = 1011`.
- m = 1011, m - 1 = 1010, m & (m - 1) = 1010 (lowest 1 gone). Round 1.
- m = 1010, m - 1 = 1001, AND = 1000. Round 2.
- m = 1000, m - 1 = 0111, AND = 0000. Round 3. Stop. Popcount 3.
- The shift loop: 1011 -> 101 -> 10 -> 1 -> 0, 4 rounds = bit_length. Result `[3, 4, 3]`.

**Code:**
```python
import random

random.seed(1202)

def naive_loop(n):
    m, it = n, 0
    while m:
        m >>= 1
        it += 1
    return it

def kernighan_loop(n):
    m, it = n, 0
    while m:
        m &= m - 1       # clears the lowest set bit
        it += 1
    return it

def solve(n):
    k = kernighan_loop(n)
    return [k, naive_loop(n), k]    # popcount == kernighan iterations

def brute(n):
    s = bin(n)[2:]
    return [s.count('1'), len(s) if n else 0, s.count('1')]

examples = [(11, [3, 4, 3]), (0, [0, 0, 0]), (2147483648, [1, 32, 1]), (4294967295, [32, 32, 32]), (1, [1, 1, 1])]
for n, want in examples:
    assert solve(n) == want == brute(n)
    print(n, '->', solve(n))

# dry run of n = 11 = 0b1011
m = 11
while m:
    print(f'  m={m:04b}  m-1={m-1:04b}  m&(m-1)={m & (m-1):04b}')
    m &= m - 1

# seeded cross-check against bin().count and bit_length (and int.bit_count, present on this Python 3.13)
for _ in range(5000):
    n = random.choice([random.randrange(2**32), random.randrange(40), 2**random.randrange(32), 2**random.randrange(1, 33) - 1])
    r = solve(n)
    assert r == brute(n)
    assert r[0] == bin(n).count('1') == n.bit_count()
    assert r[1] == n.bit_length()
print('random cross-check ok: 5000 cases')
# exhaustive on 0..2**16
for n in range(2**16):
    assert solve(n) == brute(n) and n.bit_length() == solve(n)[1] and n.bit_count() == solve(n)[0]
print('exhaustive 0..65535 ok')

# why the 0 <= n < 2**32 bound matters: both loops never end for negative n in Python.
# Bounded demonstration (stop after 100 rounds):
def rounds_capped(n, step, cap=100):
    m, it = n, 0
    while m and it < cap:
        m = step(m); it += 1
    return it, m
print('naive on -1, capped at 100:', rounds_capped(-1, lambda m: m >> 1))
print('kernighan on -1, capped at 100:', rounds_capped(-1, lambda m: m & (m - 1)))
print('masked version of -1 :', kernighan_loop(-1 & 0xFFFFFFFF))
print('edge asserts ok')
```

**Output (my run):**
```
11 -> [3, 4, 3]
0 -> [0, 0, 0]
2147483648 -> [1, 32, 1]
4294967295 -> [32, 32, 32]
1 -> [1, 1, 1]
  m=1011  m-1=1010  m&(m-1)=1010
  m=1010  m-1=1001  m&(m-1)=1000
  m=1000  m-1=0111  m&(m-1)=0000
random cross-check ok: 5000 cases
exhaustive 0..65535 ok
naive on -1, capped at 100: (100, -1)
kernighan on -1, capped at 100: (100, -1267650600228229401496703205376)
masked version of -1 : 32
edge asserts ok
```

**Edge cases:**
- n = 0: both loops run 0 times, popcount 0.
- n = 2**31 (a single high bit): 1 Kernighan round, 32 naive rounds. This is the case that shows the difference.
- n = 2**32 - 1 (all ones): all three numbers are 32.
- Negative input: infinite loop (shown capped). Mask to 32 bits first if the contract allows negatives.

**Follow-ups:**
- Power of two (Q12)? `n > 0 and n & (n - 1) == 0` (one set bit).
- Count set bits for 0..n? DP: `bits[i] = bits[i >> 1] + (i & 1)`, or `bits[i & (i - 1)] + 1`.
- Hamming distance of two numbers (Q13)? `(x ^ y).bit_count()`.

**Common mistakes:**
- Writing `m & m - 1`: precedence is fine in Python (`-` binds tighter than `&`), but it reads as a bug, so use brackets.
- Looping `for _ in range(32)` and testing `(n >> i) & 1` and calling that Kernighan.
- Running either loop on a negative number.
- Claiming `bit_count` exists "in all Python 3": it does not before 3.10.
