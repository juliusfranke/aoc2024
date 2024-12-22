import sys
from functools import cache
from typing import Dict, List
from tqdm import tqdm
from pathlib import Path
import heapq
from collections import defaultdict, deque, OrderedDict
from itertools import combinations, pairwise, permutations

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip().splitlines()


adj_num = {
    "A": [("^", "3"), ("<", "0")],
    "0": [(">", "A"), ("^", "2")],
    "1": [(">", "2"), ("^", "4")],
    "2": [(">", "3"), ("^", "5"), ("<", "1"), ("v", "0")],
    "3": [("^", "6"), ("<", "2"), ("v", "A")],
    "4": [(">", "5"), ("^", "7"), ("v", "1")],
    "5": [(">", "6"), ("^", "8"), ("<", "4"), ("v", "2")],
    "6": [("^", "9"), ("<", "5"), ("v", "3")],
    "7": [(">", "8"), ("v", "4")],
    "8": [(">", "9"), ("<", "7"), ("v", "5")],
    "9": [("<", "8"), ("v", "6")],
}

adj_dir = {
    "<": [(">", "v")],
    "v": [(">", ">"), ("^", "^"), ("<", "<")],
    ">": [("^", "A"), ("<", "v")],
    "^": [(">", "A"), ("v", "v")],
    "A": [("<", "^"), ("v", ">")],
}


def bfs(u, v, g):
    open = deque([(u, [])])
    seen = {u}
    shortest = None
    res = []
    while open:
        current, path = open.popleft()
        if current == v:
            if shortest is None:
                shortest = len(path)
            if len(path) == shortest:
                res.append("".join(path + ["A"]))
            continue
        if shortest and len(path) >= shortest:
            continue
        for dir, neighbor in g[current]:
            seen.add(neighbor)
            open.append((neighbor, path + [dir]))
    return res


@cache
def dfs(seq, level, i=0):
    g = adj_num if i == 0 else adj_dir
    res = 0
    seq = "A" + seq
    for u, v in pairwise(seq):
        paths = bfs(u, v, g)
        if level == 0:
            res += min(map(len, paths))
        else:
            res += min(dfs(path, level - 1, 1) for path in paths)
    return res


ans_1 = sum(dfs(code, 2) * int(code[:3]) for code in data)
ans_2 = sum(dfs(code, 25) * int(code[:3]) for code in data)


print(f"1: {ans_1}")
print(f"2: {ans_2}")
