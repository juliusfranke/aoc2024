import sys
from pathlib import Path
from collections import defaultdict
from itertools import cycle
from typing import Tuple

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read()

data = data.splitlines()
max_y = len(data)
max_x = len(data[0])

obstacles = {i: defaultdict(bool) for i in range(max_y)}

start = None

for i in range(max_y):
    for j in range(max_x):
        c = data[i][j]
        if c == "#":
            obstacles[i][j] = True
        elif c == "^":
            start = (i, j)


def calc_path(start, obstacles, new: Tuple[int, int] | None = None):
    path = set()
    obst = set()
    y, x = start
    directions = cycle([[-1, 0, 0], [0, 1, 1], [1, 0, 2], [0, -1, 3]])
    direction = next(directions)
    path.add((y, x))
    cycle_start = False
    while True:
        forward_y = y + direction[0]
        forward_x = x + direction[1]
        idx = direction[2]
        if not 0 <= forward_y < max_y or not 0 <= forward_x < max_x:
            break
        if obstacles[forward_y][forward_x] or (
            new and forward_y == new[0] and forward_x == new[1]
        ):
            if new:
                if cycle_start and (forward_y, forward_x, idx) in obst:
                    return []
                elif forward_y == new[0] and forward_x == new[1]:
                    cycle_start = True
            obst.add((forward_y, forward_x, idx))
            direction = next(directions)
            continue
        y = forward_y
        x = forward_x
        path.add((y, x))
    return path


path = calc_path(start, obstacles)
ans_1 = len(path)
ans_2 = 0

print(f"1: {ans_1}")
for point in set(path):
    if not calc_path(start, obstacles, new=point):
        ans_2 += 1


print(f"2: {ans_2}")
