import random

def brute(board):
    def ok(cells):
        d = [c for c in cells if c != '.']
        return len(d) == len(set(d))
    for i in range(9):
        if not ok(board[i]) or not ok([board[r][i] for r in range(9)]):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            if not ok([board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)]):
                return False
    return True

def optimal(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = {}
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == '.':
                continue
            b = boxes.setdefault((r // 3, c // 3), set())
            if v in rows[r] or v in cols[c] or v in b:
                return False
            rows[r].add(v); cols[c].add(v); b.add(v)
    return True

base = ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
        "7...2...6", ".6....28.", "...419..5", "....8..79"]
good = [list(r) for r in base]
assert optimal(good) and brute(good)

bad_row = [list(r) for r in base]; bad_row[0][2] = '5'          # two 5s in row 0
bad_col = [list(r) for r in base]; bad_col[8][0] = '5'          # 5 twice in col 0
assert not optimal(bad_row) and not optimal(bad_col)
empty = [['.'] * 9 for _ in range(9)]
assert optimal(empty)

# the example in the prompt: a board with two '5' in the first row
assert optimal(bad_row) is False
# ok-looking trap: a rows-and-cols-only check misses a box clash
box_only = [['.'] * 9 for _ in range(9)]
box_only[0][0] = '7'; box_only[1][1] = '7'
assert optimal(box_only) is False

rng = random.Random(15)
agree = 0
for _ in range(500):
    b = [['.'] * 9 for _ in range(9)]
    for _ in range(rng.randint(0, 30)):
        b[rng.randrange(9)][rng.randrange(9)] = str(rng.randint(1, 9))
    assert optimal(b) == brute(b)
    agree += 1
print(agree, "random boards agree with brute force")
print(optimal(good), optimal(bad_row), optimal(bad_col), optimal(box_only))
