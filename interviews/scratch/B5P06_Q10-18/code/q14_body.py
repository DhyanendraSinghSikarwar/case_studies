
def delete_node(node):
    """O(1). node is not the tail. Copy the successor's value in, then bypass the successor."""
    node.val = node.next.val
    node.next = node.next.next

def brute(arr, idx):                   # delete by index in a Python list
    return arr[:idx] + arr[idx + 1:]

# the four examples: the node to delete is chosen by its value
for arr, v, want in (([4, 5, 1, 9], 5, [4, 1, 9]), ([4, 5, 1, 9], 1, [4, 5, 9]),
                     ([1, 2], 1, [2]), ([0, 1, 2, 3], 0, [1, 2, 3])):
    head, nodes = from_array(arr)
    target = next(n for n in nodes if n.val == v)
    delete_node(target)
    assert to_array(head) == want == brute(arr, arr.index(v))
    print(arr, 'delete value', v, '->', want)

# what really happened: the given NODE OBJECT survives, the SUCCESSOR object is the one that left the list
head, nodes = from_array([4, 5, 1, 9])
node, successor = nodes[1], nodes[2]
other_ref = successor                  # someone else holds the successor
delete_node(node)
ids = node_ids(head)
assert id(node) in ids                 # the node we were given is still in the list (now holding 1)
assert id(successor) not in ids        # the successor object is gone from the list
assert other_ref.val == 1 and other_ref.next is nodes[3]   # but the stale reference still looks like a list node
print('given node still in list:', id(node) in ids, '| successor still in list:', id(successor) in ids,
      '| given node value now:', node.val)

# the tail cannot be deleted this way
head, nodes = from_array([1, 2, 3])
try:
    delete_node(nodes[-1])
except AttributeError as e:
    print('tail:', type(e).__name__, '-', e)
else:
    raise SystemExit('expected failure')

# seeded random cross-check: delete every non-tail position of random lists
random.seed(14)
for _ in range(300):
    n = random.randint(2, 15)
    arr = [random.randint(0, 4) for _ in range(n)]
    idx = random.randint(0, n - 2)
    head, nodes = from_array(arr)
    before = node_ids(head)
    delete_node(nodes[idx])
    assert to_array(head) == brute(arr, idx)
    assert node_ids(head) == before[:idx + 1] + before[idx + 2:]    # exactly one node object left: the successor
print('random cross-check ok (300 cases)')
