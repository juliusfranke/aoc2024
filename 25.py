from itertools import combinations, permutations, product
import sys
from typing import Dict
from tqdm import tqdm
from pathlib import Path
from collections import deque, OrderedDict

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip().split("\n\n")

locks = []
keys = []
for block in data:
    heights = []
    lines = block.splitlines()

    if lines[0][0] == "#":
        for j in range(len(lines[0])):
            if len(heights) == j+1:
                continue
            for i in range(1,len(lines)):
                if lines[i][j] == ".":
                    heights.append(i-1)
                    break
        locks.append(heights)
    elif lines[0][0] == ".":
        for j in range(len(lines[0])):
            if len(heights) == j+1:
                continue
            for i in range(1,len(lines)):
                if lines[i][j] == "#":
                    heights.append(6-i)
                    break
        keys.append(heights)
    print(heights)

            


ans_1 = 0
for lock, key in product(locks, keys):
    for l, k in zip(lock, key):
        if l+k > 5:
            break
    else:
        ans_1+=1
    print(lock, key)
        

    # print(block.splitlines())

# print(data)

ans_2 = 0

print(f"1: {ans_1}")
print(f"2: {ans_2}")
