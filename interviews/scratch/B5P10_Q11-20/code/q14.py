import random

random.seed(14)

def fib_three(n):
    """Optimal: bottom-up for the value (O(1) space) and recurrences for the two call counts."""
    a, b = 0, 1                       # fib(0), fib(1)
    for _ in range(n):
        a, b = b, a + b
    # naive calls: c(0) = c(1) = 1, c(k) = 1 + c(k-1) + c(k-2)
    c_prev, c_cur = 1, 1
    for _ in range(n - 1):
        c_prev, c_cur = c_cur, 1 + c_prev + c_cur
    naive = 1 if n < 2 else c_cur
    # memo calls: the first call is 1; each new k >= 2 makes two child calls; derived below, equals 2n - 1 for n >= 1
    memo = 1 if n == 0 else 2 * n - 1
    return [a, naive, memo]

def counted_recursions(n):
    """Oracle: run the two functions from the prompt and count their calls."""
    count = [0]
    def naive(k):
        count[0] += 1
        return k if k < 2 else naive(k - 1) + naive(k - 2)
    value = naive(n)
    naive_calls = count[0]
    count[0] = 0
    memo = {}
    def memoised(k):
        count[0] += 1
        if k < 2:
            return k
        if k in memo:
            return memo[k]
        memo[k] = memoised(k - 1) + memoised(k - 2)
        return memo[k]
    assert memoised(n) == value
    return [value, naive_calls, count[0]]

for n, want in [(0, [0, 1, 1]), (1, [1, 1, 1]), (2, [1, 3, 3]), (10, [55, 177, 19]), (25, [75025, 242785, 49])]:
    assert fib_three(n) == want, n
    assert counted_recursions(n) == want, n
print('5 prompt examples ok')

# walk-through: n = 2 (first call fib(2) -> fib(1), fib(0))
print('n=2 naive: fib(2) -> fib(1) base, fib(0) base = 3 calls; memo: same 3 calls, nothing cached yet')
# and n = 5 call table
print('k   fib(k)  naive_calls  memo_calls')
for k in range(0, 11):
    v, nv, mm = fib_three(k)
    print('%-3d %-7d %-12d %d' % (k, v, nv, mm))

# growth: naive ratio tends to the golden ratio, memo grows by 2 per step
ratios = [fib_three(k)[1] / fib_three(k - 1)[1] for k in (10, 20, 25)]
print('naive_calls(k)/naive_calls(k-1) at k=10,20,25:', [round(r, 4) for r in ratios], '(golden ratio 1.6180)')
print('naive_calls(k) = 2*fib(k+1) - 1 ?', all(fib_three(k)[1] == 2 * fib_three(k + 1)[0] - 1 for k in range(0, 26)))

# seeded random cross-check, n <= 20, plus every n
for n in range(0, 21):
    assert fib_three(n) == counted_recursions(n), n
for _ in range(300):
    n = random.randint(0, 20)
    assert fib_three(n) == counted_recursions(n)
print('all n in 0..20 and 300 random draws agree with the counted recursive functions')

# recursion limit: the memoised function is O(n) calls but also O(n) DEEP
def deep_memo(n):
    memo = {}
    def f(k):
        if k < 2:
            return k
        if k in memo:
            return memo[k]
        memo[k] = f(k - 1) + f(k - 2)
        return memo[k]
    return f(n)
try:
    deep_memo(5000)
    print('memo fib(5000): no error (unexpected)')
except RecursionError:
    print('memo fib(5000): RecursionError under the default limit; bottom-up gives', len(str(fib_three(5000)[0])), 'digits')
assert fib_three(0)[0] == 0 and fib_three(1)[0] == 1
print('edge cases ok')
