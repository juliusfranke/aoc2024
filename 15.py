import sys
from typing import Dict, List, Tuple
from tqdm import tqdm
from pathlib import Path
from collections import defaultdict, deque, OrderedDict

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    map, commands = file.read().strip().split("\n\n")

map = map.splitlines()
commands = commands.replace("\n", "")

rows = len(map)
cols = len(map[0])


rev = {">": "<", "^": "v", "<": ">", "v": "^"}


def parse(map):
    boxes = []
    walls = []
    lr = {}
    robot = None
    for i in range(rows):
        for j in range(cols):
            pos = map[i][j]
            match pos:
                case "O":
                    boxes.append((i, j))
                case "@":
                    robot = (i, j)
                case "#":
                    walls.append((i, j))
                case "[":
                    boxes.append((i, j))
                    lr[(i, j)] = [(i, j + 1), "["]
                case "]":
                    boxes.append((i, j))
                    lr[(i, j)] = [(i, j - 1), "]"]

    assert robot is not None
    return boxes, walls, robot, lr


boxes, walls, robot, lr = parse(map)



def move(pos, command):
    match command:
        case ">":
            next_pos = (pos[0], pos[1] + 1)
        case "^":
            next_pos = (pos[0] - 1, pos[1])
        case "<":
            next_pos = (pos[0], pos[1] - 1)
        case "v":
            next_pos = (pos[0] + 1, pos[1])
        case _:
            raise Exception
    return next_pos


def is_valid(pos) -> bool:
    if pos[0] not in range(rows) or pos[1] not in range(cols):
        return False

    if pos in walls:
        return False
    return True


def move_box(pos, command) -> List[Tuple[int, int]]:
    next_pos = move(pos, command)

    if not is_valid(next_pos):
        return []

    if next_pos in boxes:
        boxes_add = move_box(next_pos, command)
        if not boxes_add:
            return []
        return boxes_add

    return [next_pos]


def move_big_box(pos, command) -> List[List[Tuple[int, int]]]:
    next_pos_1 = move(pos, command)
    next_pos_2 = move(lr[pos][0], command)

    if not is_valid(next_pos_1) or not is_valid(next_pos_2):
        return []

    b2 = next_pos_2 in boxes
    if command in ["<", ">"]:
        if b2:
            add = move_big_box(next_pos_2, command)
            # print(add)
            if add:
                return [*add, [next_pos_1, next_pos_2]]
            else:
                return []

        else:
            return [[next_pos_1, next_pos_2]]

    b1 = next_pos_1 in boxes

    boxes_1, boxes_2 = [], []
    if b1:
        boxes_1 = move_big_box(next_pos_1, command)
        if not boxes_1:
            return []
    if b2 and not lr[next_pos_2][0] == next_pos_1:
        boxes_2 = move_big_box(next_pos_2, command)
        if not boxes_2:
            return []

    if not b1 and not b2:
        return [[next_pos_1, next_pos_2]]

    if boxes_1 or boxes_2:
        # print("--------")
        # print(boxes_1, boxes_2)
        return boxes_1 + boxes_2 + [[next_pos_1, next_pos_2]]
    else:
        return []


def move_robot(
    pos: Tuple[int, int], command: str, task_2: bool = False
) -> Tuple[int, int]:
    next_pos = move(pos, command)

    if not is_valid(next_pos):
        return pos
    if next_pos in boxes:
        if task_2:
            boxes_add = move_big_box(next_pos, command)
        else:
            boxes_add = move_box(next_pos, command)
        if not boxes_add:
            return pos
        if task_2:
            visited = set()
            for box_1, box_2 in boxes_add:
                if box_1 in visited and box_2 in visited:
                    continue
                visited.add(box_1)
                visited.add(box_2)
                p_box_1 = move(box_1, rev[command])
                p_box_2 = move(box_2, rev[command])

                boxes.remove(p_box_1)
                boxes.remove(p_box_2)
                boxes.append(box_1)
                boxes.append(box_2)

                lr.pop(p_box_1)
                lr.pop(p_box_2)

                if box_1[1] > box_2[1]:
                    lr[box_1] = [box_2, "]"]
                    lr[box_2] = [box_1, "["]
                else:
                    lr[box_1] = [box_2, "["]
                    lr[box_2] = [box_1, "]"]

        else:
            for box in boxes_add:
                boxes.append(box)
            boxes.remove(next_pos)
    return next_pos


def print_map(task_2: bool = False):
    map: str = ""
    for i in range(rows):
        for j in range(cols):
            if (pos := (i, j)) in boxes:
                if task_2:
                    map += lr[pos][1]
                else:
                    map += "O"
            elif pos == robot:
                map += "@"
            elif pos in walls:
                map += "#"
            else:
                map += "."
            # breakpoint()
        map += "\n"
    print(map)


# print_map()

for command in commands:
    robot = move_robot(robot, command)
# print_map()


ans_1 = sum([100 * i + j for (i, j) in boxes])
map_2 = []
for line in map:
    line_str = ""
    for char in line:
        match char:
            case "#":
                line_str += "##"
            case ".":
                line_str += ".."
            case "O":
                line_str += "[]"
            case "@":
                line_str += "@."
    map_2.append(line_str)

rows = len(map_2)
cols = len(map_2[0])

boxes, walls, robot, lr = parse(map_2)
# print_map(task_2=True)

for command in commands:
    robot = move_robot(robot, command, task_2=True)

# print_map(task_2=True)

ans_2 = sum([100 * i + j for (i, j) in boxes if lr[(i, j)][1] == "["])

print(f"1: {ans_1}")
print(f"2: {ans_2}")
