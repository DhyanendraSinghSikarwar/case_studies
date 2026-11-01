import random

def brute(nums):
    s = set(nums)
    i = 1
    while i in s:
        i += 1
    return i

def optimal(nums):                    # modifies nums; O(1) extra space
    n = len(nums)
    for i in range(n):
        # keep swapping until slot i holds a value that cannot go home
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1

assert optimal([3, 4, -1, 1]) == 2
assert optimal([1, 2, 0]) == 3
assert optimal([7, 8, 9, 11, 12]) == 1
assert optimal([]) == 1
assert optimal([1]) == 2
assert optimal([2]) == 1
assert optimal([1, 1]) == 2              # duplicates must not loop forever
assert optimal([2, 2, 2, 2]) == 1
assert optimal([-5, 0]) == 1
assert optimal(list(range(1, 1001))) == 1001
assert optimal([10**9, 1]) == 2

# a tracing helper for the dry run
def trace(nums):
    nums = nums[:]
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
        print(" after i =", i, nums)
    return nums
print("dry run [3,4,-1,1]:")
trace([3, 4, -1, 1])

rng = random.Random(16)
for _ in range(1000):
    a = [rng.randint(-3, 9) for _ in range(rng.randint(0, 8))]
    assert optimal(a[:]) == brute(a), a
print("1000 random cases agree")
print(optimal([3, 4, -1, 1]), optimal([1, 2, 0]), optimal([7, 8, 9, 11, 12]))
