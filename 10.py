import sys
from typing import Dict, List, Tuple
from tqdm import tqdm
from pathlib import Path
from collections import deque, OrderedDict

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip().splitlines()


max_y = len(data)
max_x = len(data[0])
starts: List[Tuple] = []
for i in range(max_y):
    for j in range(max_x):
        if data[i][j] != "0":
            continue
        starts.append((i, j))

ans_1 = 0
ans_2 = 0


def recursive_search(pos: Tuple, num: int)->int:
    sum = 0
    for y, x in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
        new = (pos[0] + y, pos[1] + x)
        if not 0 <= new[0] < max_y or not 0 <= new[1] < max_x:
            continue
        new_num = int(data[new[0]][new[1]])
        if new_num == num + 1:
            if new in explored_1:
                continue
            explored_1.add(new)
            if new_num == 9:
                sum += 1
                continue
            sum += recursive_search(new, new_num)
    return sum


for start in starts:
    explored_1 = set()
    trails = recursive_search(start, 0)
    ans_1 += trails


print(f"1: {ans_1}")
print(f"2: {ans_2}")
