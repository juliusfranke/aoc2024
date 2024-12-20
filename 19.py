import sys
from typing import Dict, List
from tqdm import tqdm
from pathlib import Path
from functools import cache
from collections import defaultdict, deque, OrderedDict

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip().split("\n\n")

avl = [a for a in data[0].split(", ")]

designs = data[1].splitlines()

# print(avl, designs)
# cache = set(avl)

root = {}
for pat in avl:
    d = root
    for color in pat:
        if color not in d:
            d[color] = {}
        d = d[color]
    d[""] = None

print(len(designs))
# breakpoint()


curr: str

counts = defaultdict(int)


@cache
def outer(design) -> int:
    return rec_search(design, root)


def rec_search(design: str, r: Dict) -> int:
    terminate = "" in r
    if not design:
        if terminate:
            return 1
        return 0
    if terminate:
        n = outer(design)
    else:
        n = 0

    nxt = design[0]
    if nxt in r:
        return n + rec_search(design[1:], r[nxt])
    return n

    for pattern in avl:
        if design.count(pattern) == 0:
            continue
        sub_str = design.split(pattern)
        for sub in sub_str:
            if not rec_search(sub):
                break
        else:
            return True
    else:
        return False


# possible = [rec_search(design, avl, []) for design in designs]
possible = []
pbar = tqdm(designs)
# avl = sorted(avl, key=len, reverse=True)
ans_1 = 0
for design in pbar:
    if outer(design) > 0:
        ans_1 += 1
    # break
print(counts)

# rec_search("bwurrg", avl, [])

# ans_1 =
ans_2 = sum(map(outer, designs))

print(f"1: {ans_1}")
print(f"2: {ans_2}")
