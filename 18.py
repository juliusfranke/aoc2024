import heapq
import sys
from typing import Callable, Dict, List, Tuple
from pathlib import Path
from collections import defaultdict

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
test = len(sys.argv) != 1
input = example if test else input
rows, cols = (7, 7) if test else (71, 71)
num_bytes = 12 if test else 1024

with open(input, "r") as file:
    data = file.read().strip().splitlines()


def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(
    came_from: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]
) -> List[Tuple[int, int]]:
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def a_star(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    obstcl: List[Tuple[int, int]],
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float],
):
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}

    open_set = []
    heapq.heappush(open_set, (0, start))

    g_score = defaultdict(lambda: float("inf"))
    g_score[start] = 0

    f_score = defaultdict(lambda: float("inf"))
    f_score[start] = heuristic(start, goal)

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)
        cx, cy = current

        for neighbor in [(cx + 1, cy), (cx, cy - 1), (cx - 1, cy), (cx, cy + 1)]:
            nx, ny = neighbor
            if nx not in range(cols) or ny not in range(rows):
                continue
            if neighbor in obstcl:
                continue
            tg = g_score[current] + 1
            if tg < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tg
                new_f_score = tg + heuristic(neighbor, goal)
                if neighbor in open_set:
                    open_set.remove((f_score[neighbor], neighbor))
                heapq.heappush(open_set, (new_f_score, neighbor))
                f_score[neighbor] = new_f_score
    return []


obstcls = []
for i in range(len(data)):
    obx, oby = data[i].split(",")
    obstcls.append((int(obx), int(oby)))


def print_map(obstcl: List[Tuple[int, int]], path: List[Tuple[int, int]]):
    map_str = ""
    for y in range(rows):
        for x in range(cols):
            if (x, y) in obstcl:
                map_str += "#"
                continue
            if (x, y) in path:
                map_str += "O"
                continue
            map_str += "."
        map_str += "\n"
    print(map_str)


obstcl_1 = obstcls[:num_bytes]
sol = a_star((0, 0), (cols - 1, rows - 1), obstcl_1, manhattan_distance)
ans_1 = len(sol) - 1

for i in range(num_bytes, len(data)):
    obstcl_2 = obstcls[:i]
    new = obstcl_2[-1]
    if new in sol:
        sol = a_star((0, 0), (cols - 1, rows - 1), obstcl_2, manhattan_distance)
    else:
        continue
    if not sol:
        ans_2 = str(obstcl_2[-1]).replace("(", "").replace(")", "").replace(" ", "")
        break
else:
    ans_2 = None


print(f"1: {ans_1}")
print(f"2: {ans_2}")
