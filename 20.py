import sys
from typing import Dict, Tuple, Callable, List
from tqdm import tqdm
from pathlib import Path
from collections import Counter, deque, OrderedDict, defaultdict
import heapq
from itertools import combinations

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip().splitlines()

rows = len(data)
cols = len(data[0])

start: Tuple[int, int] = (-1, -1)
goal: Tuple[int, int] = (-1, -1)
obstcl: List[Tuple[int, int]] = []

for i in range(rows):
    for j in range(cols):
        if data[i][j] == "S":
            start = (i, j)
        elif data[i][j] == "E":
            goal = (i, j)
        elif data[i][j] == "#":
            obstcl.append((i, j))

print(f"{start=}")
print(f"{goal=}")


def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(
    came_from: Dict[Tuple[Tuple[int, int], int], Tuple[Tuple[int, int], int]],
    current: Tuple[int, int],
    n_cheat: int = 2,
) -> List[Tuple[int, int]]:
    total_path = [current]
    while (current, n_cheat) in came_from.keys():
        current, n_cheat = came_from[(current, n_cheat)]
        total_path.append(current)
    total_path.reverse()
    return total_path


def a_star(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    obstcl: List[Tuple[int, int]],
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float],
    allowed_cheat: int,
    break_cost: int | None,
):
    solutions = []
    open_set = []
    heapq.heappush(open_set, (0, start, 0, None, [start]))

    g_score = defaultdict(lambda: float("inf"))
    g_score[(start, 0, None)] = 0

    f_score = defaultdict(lambda: float("inf"))
    f_score[(start, 0, None)] = heuristic(start, goal)

    while open_set:
        _, current, n_cheat, cheat_start, path = heapq.heappop(open_set)
        if current == goal:
            solutions.append(path)
            return solutions
        cx, cy = current

        for neighbor in [(cx + 1, cy), (cx, cy - 1), (cx - 1, cy), (cx, cy + 1)]:
            nx, ny = neighbor
            cheating = n_cheat
            new_cheat_start = cheat_start
            if nx not in range(cols) or ny not in range(rows):
                continue
            if neighbor in path:
                continue
            if neighbor in obstcl:
                if n_cheat >= allowed_cheat:
                    continue
                if n_cheat == 0:
                    new_cheat_start = neighbor
                cheating += 1

            tg = g_score[(current, n_cheat, cheat_start)] + 1
            if break_cost and tg >= break_cost:
                continue
            if tg < g_score[(neighbor, cheating, new_cheat_start)]:
                g_score[(neighbor, cheating, new_cheat_start)] = tg
                new_f_score = tg + heuristic(neighbor, goal)
                heapq.heappush(
                    open_set,
                    (
                        new_f_score,
                        neighbor,
                        cheating,
                        new_cheat_start,
                        path + [neighbor],
                    ),
                )
                f_score[(neighbor, cheating, new_cheat_start)] = new_f_score
    return solutions


def print_map(obstcl: List[Tuple[int, int]], path: List[Tuple[int, int]]):
    map_str = ""
    for y in range(rows):
        for x in range(cols):
            o = (y, x) in obstcl
            p = (y, x) in path
            if o and p:
                map_str += "X"
                continue
            if o:
                map_str += "#"
                continue
            if p:
                map_str += "O"
                continue
            map_str += "."
        map_str += "\n"
    print(map_str)


baseline = a_star(start, goal, obstcl, manhattan_distance, 0, None)
assert len(baseline) == 1
path = baseline[0]
# for p1, p2 in combinations(path, 2):
#     if manhattan_distance(p1, p2) == 2:
#         print(p1, p2)
ans_1 = 0
ans_2 = 0
for i in range(len(path) - 2):
    for j in range(i + 2, len(path)):
        d = manhattan_distance(path[i], path[j])
        if d <= 20 and j - i - 1 - (d - 1) >= 100:
            ans_2 += 1
        if d == 2 and j - i - 2 >= 100:
            ans_1 += 1


# breakpoint()
# baseline_len = len(baseline[0])
# print(baseline_len)
# solutions = a_star(start, goal, obstcl, manhattan_distance, 1, baseline_len)
# # max_len = max([len(s) for s in solutions])
# print(baseline_len)

# print([len(s) - baseline_len for s in solutions])
# lengths = [s - max(lengths) for s in lengths]
# counter = Counter(lengths)
# print_map(obstcl, sol)
# breakpoint()


# ans_1 = sum([1 for s in solutions if len(s) - baseline_len <= -100])
print(f"1: {ans_1}")
print(f"2: {ans_2}")
