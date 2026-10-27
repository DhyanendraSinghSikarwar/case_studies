import random


class Editor:
    """Two stacks: `done` holds the typed characters, `redo` holds undone ones."""
    def __init__(self):
        self.done, self.redo = [], []

    def run(self, cmd):
        if cmd.startswith("type "):
            self.done.append(cmd[5])
            self.redo.clear()                 # a new edit kills the redo branch
        elif cmd == "undo":
            if self.done:
                self.redo.append(self.done.pop())
        elif cmd == "redo":
            if self.redo:
                self.done.append(self.redo.pop())
        return "".join(self.done)


def editor_fast(cmds):
    e = Editor()
    return [e.run(c) for c in cmds]


def editor_brute(cmds):
    # reference: keep every text state in a list plus a pointer
    states, p, out = [""], 0, []
    for c in cmds:
        if c.startswith("type "):
            states = states[:p + 1] + [states[p] + c[5]]
            p += 1
        elif c == "undo":
            p = max(0, p - 1)
        elif c == "redo":
            p = min(len(states) - 1, p + 1)
        out.append(states[p])
    return out


class Browser:
    def __init__(self):
        self.cur, self.back_s, self.fwd_s = None, [], []

    def run(self, cmd):
        if cmd.startswith("visit "):
            if self.cur is not None:
                self.back_s.append(self.cur)
            self.cur = cmd[6:]
            self.fwd_s.clear()                # visiting clears forward history
        elif cmd == "back" and self.back_s:
            self.fwd_s.append(self.cur)
            self.cur = self.back_s.pop()
        elif cmd == "forward" and self.fwd_s:
            self.back_s.append(self.cur)
            self.cur = self.fwd_s.pop()
        return self.cur


def browser_fast(cmds):
    b = Browser()
    return [b.run(c) for c in cmds]


def browser_brute(cmds):
    pages, i, out = [], -1, []
    for c in cmds:
        if c.startswith("visit "):
            pages = pages[:i + 1] + [c[6:]]
            i += 1
        elif c == "back":
            i = max(0, i - 1)
        elif c == "forward":
            i = min(len(pages) - 1, i + 1)
        out.append(pages[i])
    return out


ed = ['type a', 'type b', 'type c', 'undo', 'undo', 'redo', 'type d', 'redo', 'undo']
exp = ['a', 'ab', 'abc', 'ab', 'a', 'ab', 'abd', 'abd', 'ab']
print("editor :", editor_fast(ed))
assert editor_fast(ed) == editor_brute(ed) == exp

br = ['visit x', 'visit y', 'visit z', 'back', 'back', 'forward', 'visit w', 'forward']
exp_b = ['x', 'y', 'z', 'y', 'x', 'y', 'w', 'w']
print("browser:", browser_fast(br), "-> ends on", browser_fast(br)[-1])
assert browser_fast(br) == browser_brute(br) == exp_b

# edge cases
assert editor_fast(['undo', 'redo']) == ['', '']                   # no-ops on empty
assert editor_fast(['type a', 'undo', 'undo', 'redo', 'redo']) == ['a', '', '', 'a', 'a']
assert editor_fast([]) == []
assert browser_fast(['visit a', 'back', 'forward', 'forward']) == ['a', 'a', 'a', 'a']
assert browser_fast(['visit a', 'visit b', 'back', 'visit c', 'forward', 'back', 'back']) == \
    ['a', 'b', 'a', 'c', 'c', 'a', 'a']

# seeded randomised cross-check
rng = random.Random(32)
for _ in range(1500):
    n = rng.randint(0, 14)
    cs = [rng.choice(['type a', 'type b', 'type c', 'undo', 'redo']) for _ in range(n)]
    assert editor_fast(cs) == editor_brute(cs), cs
    bs = [rng.choice(['visit p', 'visit q', 'visit r', 'back', 'forward']) for _ in range(n)]
    bs = ['visit h'] + bs     # the brute force needs a first page to exist
    assert browser_fast(bs) == browser_brute(bs), bs
print("1500 + 1500 seeded random command lists agree with the snapshot-list reference")
