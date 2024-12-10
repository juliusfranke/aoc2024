import sys
from typing import Callable, Dict, List, Tuple
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


def recursive_search(pos: Tuple, num: int, rule: Callable) -> int:
    sum = 0
    for y, x in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
        new = (pos[0] + y, pos[1] + x)
        if not 0 <= new[0] < max_y or not 0 <= new[1] < max_x:
            continue
        new_num = int(data[new[0]][new[1]])
        if new_num == num + 1:
            if rule(new, pos):
                continue
            # if new in explored_1:
            #     continue
            # explored_1.add(new)
            if new_num == 9:
                sum += 1
                continue
            sum += recursive_search(new, new_num, rule)
    return sum


def rule_1(new, pos) -> bool:
    if new in explored_1:
        return True
    explored_1.add(new)
    return False


def rule_2(new, pos) -> bool:
    return False
    # if (pos, new) in explored_2:
    #     return True
    # explored_2.add((pos, new))
    # return False


for start in starts:
    explored_1 = set()
    trails_1 = recursive_search(start, 0, rule_1)
    ans_1 += trails_1
    explored_2 = set()
    trails_2= recursive_search(start, 0, rule_2)
    ans_2 += trails_2


print(f"1: {ans_1}")
print(f"2: {ans_2}")
