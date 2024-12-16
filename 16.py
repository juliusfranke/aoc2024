import sys
import heapq
import random
from typing import Dict, Tuple, List
from tqdm import tqdm
from pathlib import Path
from collections import defaultdict, deque, OrderedDict
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip().splitlines()


n_rows = len(data)
n_cols = len(data[0])

s_y, s_x = -1, -1
g_y, g_x = -1, -1
wall_y = []
wall_x = []
for i in range(n_rows):
    for j in range(n_cols):
        if data[i][j] == "S":
            s_y, s_x = i, j
        elif data[i][j] == "E":
            g_y, g_x = i, j
        elif data[i][j] == "#":
            patch = Rectangle((j - 0.5, i - 0.5), 1, 1)
            plt.gca().add_patch(patch)

directions = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
]


def a_star(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    maze: List[str],
) -> Tuple[float, List[List[Tuple[int, int]]]]:
    solutions: List = []
    best_cost = float("inf")
    came_from = {(start, (0, 1)): (None, None)}
    g_score = defaultdict(lambda: float("inf"))
    g_score[(start, (0, 1))] = 0

    open_set = []
    closed_set = []
    heapq.heappush(open_set, (0, start, (0, 1), [start]))

    while open_set:
        g_current, current, current_dir, path = heapq.heappop(open_set)
        closed_set.append(current)
        if current == goal:
            if g_current > best_cost:
                continue
            best_cost = g_current
            solutions.append(path)
        c_y, c_x = current
        for next_dir in directions:
            n_y, n_x = next_dir[0] + c_y, next_dir[1] + c_x
            if (n_y, n_x) in path:
                continue
            if n_y not in range(n_rows) or n_x not in range(n_cols):
                continue
            if maze[n_y][n_x] == "#":
                continue
            if current_dir == next_dir:
                g = g_current + 1
            else:
                g = g_current + 1001

            if g <= g_score[((n_y, n_x), next_dir)]:
                came_from[((n_y, n_x), next_dir)] = (current, current_dir)
                g_score[((n_y, n_x), next_dir)] = g
                heapq.heappush(
                    open_set,
                    (
                        g_score[((n_y, n_x), next_dir)],
                        (n_y, n_x),
                        next_dir,
                        path + [(n_y, n_x)],
                    ),
                )
    return (best_cost, solutions)


cost, solutions = a_star((s_y, s_x), (g_y, g_x), data.copy())

unique_pos = set()

for solution in solutions:
    for node in solution:
        unique_pos.add(node)
    x, y = [], []
    for point in solution:
        y.append(point[0])
        x.append(point[1])
    plt.plot(x, y)

plt.show()

ans_1 = cost
ans_2 = len(unique_pos)

print(f"1: {ans_1}")
print(f"2: {ans_2}")
