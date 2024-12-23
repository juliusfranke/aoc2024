import sys
from typing import Dict
from tqdm import tqdm
from pathlib import Path
from itertools import combinations
from collections import defaultdict, deque, OrderedDict

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip().splitlines()

conns = defaultdict(list)
for line in data:
    c1, c2 = line.split("-")
    conns[c1].append(c2)
    conns[c2].append(c1)


ans_1 = 0
for k1, k2, k3 in combinations(list(conns.keys()), 3):
    if k1 not in conns[k2] or k1 not in conns[k3]:
        continue
    if k2 not in conns[k1] or k2 not in conns[k3]:
        continue
    if k3 not in conns[k1] or k3 not in conns[k2]:
        continue
    if "t" not in (k1[0] + k2[0] + k3[0]):
        continue
    ans_1 += 1

ans_2 = 0

print(f"1: {ans_1}")
print(f"2: {ans_2}")
