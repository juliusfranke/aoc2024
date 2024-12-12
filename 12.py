import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Set, Tuple

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else sys.argv[1]


with open(input, "r") as file:
    data = file.read().strip().splitlines()

max_y = len(data)
max_x = len(data[0])

plant_dict = defaultdict(list)
for i in range(max_y):
    for j in range(max_x):
        plant = data[i][j]
        plant_dict[plant].append((i, j))


def search(
    plant: str, loc: Tuple[int, int], plant_dict: Dict, visited: Set, sides: Dict
):
    curr = loc
    area = 1
    perim = 0
    sides[curr] = []
    for dy, dx, dir in [(0, 1, "W"), (-1, 0, "S"), (0, -1, "E"), (1, 0, "N")]:
        next = (curr[0] + dy, curr[1] + dx)
        if next in visited:
            continue
        if not 0 <= next[0] < max_y or not 0 <= next[1] < max_x:
            sides[curr].append(dir)
            perim += 1
            continue
        if next in plant_dict[plant]:
            visited.add(next)
            plant_dict[plant].remove(next)
            new_area, new_perim = search(plant, next, plant_dict, visited, sides)
            area += new_area
            perim += new_perim
        else:
            sides[curr].append(dir)
            perim += 1
    # print(area, perim)
    return area, perim


def go_dir(loc, dir):
    match dir:
        case "W":
            return (loc[0], loc[1] + 1)
        case "S":
            return (loc[0] - 1, loc[1])
        case "E":
            return (loc[0], loc[1] - 1)
        case "N":
            return (loc[0] + 1, loc[1])


sides_it = {"W": "N", "N": "E", "E": "S", "S": "W"}
two_sides_180 = {"W": "E", "E": "W", "N": "S", "S": "N"}
dirs = ["W", "S", "E", "N"]


def calc_sides(sides: Dict[Tuple[int, int], List[str]]):
    def __explore(loc) -> int:
        neighbors = {dir: go_dir(loc, dir) in sides for dir in dirs}
        neighbors = [key for key in neighbors.keys() if neighbors[key]]
        n = 0
        n_nb = len(neighbors)
        # no neighbors
        if n_nb == 0:
            return 4
        # one neighbork
        elif n_nb == 1:
            return 2
        elif n_nb == 2:
            if two_sides_180[neighbors[0]] == neighbors[1]:
                return 0
            if go_dir(go_dir(loc, neighbors[0]), neighbors[1]) not in sides.keys():
                return 2
            return 1
        elif n_nb == 3:
            for a, b in combinations(neighbors, 2):
                if two_sides_180[a] == b:
                    continue
                if go_dir(go_dir(loc, a), b) not in sides.keys():
                    n += 1
            return n
        elif n_nb == 4:
            for a, b in combinations(neighbors, 2):
                if two_sides_180[a] == b:
                    continue
                if go_dir(go_dir(loc, a), b) not in sides.keys():
                    n += 1
            return n
        else:
            raise Exception

    corners = 0

    for loc in sides.keys():
        corners += __explore(loc)
    return corners


ans_1 = 0
ans_2 = 0
area_dict = defaultdict(list)
for plant in plant_dict.keys():
    while len(plant_dict[plant]) > 0:
        loc = plant_dict[plant].pop(0)
        visited = set()
        visited.add(loc)
        sides = defaultdict(list)
        area, perim = search(plant, loc, plant_dict, visited, sides)
        area_dict[plant].append([area, perim])
        ans_1 += area * perim
        n_sides = calc_sides(sides)
        ans_2 += n_sides * area


print(f"1: {ans_1}")
print(f"2: {ans_2}")
