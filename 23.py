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

comps = set()
conns = set()
for line in data:
    c1, c2 = line.split("-")
    comps.update((c1, c2))
    conns.update(((c1, c2), (c2, c1)))

print(conns)
ans_1 = 0
for k1, k2, k3 in combinations(comps, 3):
    if not {(k1, k2), (k2, k3), (k1, k3)} < conns:
        continue
    if "t" not in (k1[0] + k2[0] + k3[0]):
        continue
    ans_1 += 1

lans = [{k} for k in comps]

for lan in lans:
    for k1 in comps:
        if all((k1, k2) in conns for k2 in lan):
            lan.add(k1)

ans_2 = sorted(max(lans, key=len))


print(f"1: {ans_1}")
print(f"2: {','.join(ans_2)}")
