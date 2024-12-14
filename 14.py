import sys
import numpy as np
from typing import Dict
import matplotlib.pyplot as plt
from tqdm import tqdm
import re
from pathlib import Path
from collections import deque, OrderedDict

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example
size = np.array([101, 103]) if len(sys.argv) == 1 else np.array([11, 7])

regex = r"p=(\d+),(\d+) v=([-]?\d+),([-]?\d+)"

with open(input, "r") as file:
    data = file.read().strip()


robots = re.findall(regex, data, re.MULTILINE)
P = []
V = []
for robot in robots:
    P.append([int(p) for p in robot[:2]])
    V.append([int(p) for p in robot[2:]])

P = np.array(P)
V = np.array(V)
F = np.mod(P + 100 * V, size)
# print(F)
middle = np.floor(size / 2)
quadrants = [0, 0, 0, 0]
r = [[], [], [], []]
for robot in F:
    if robot[0] == middle[0] or robot[1] == middle[1]:
        continue
    elif robot[0] < middle[0] and robot[1] < middle[1]:
        quadrants[0] += 1
        r[0].append(robot)
    elif robot[0] < middle[0] and robot[1] > middle[1]:
        quadrants[1] += 1
        r[1].append(robot)
    elif robot[0] > middle[0] and robot[1] < middle[1]:
        quadrants[2] += 1
        r[2].append(robot)
    else:
        quadrants[3] += 1
        r[3].append(robot)

ans_1 = np.prod(np.array(quadrants))
seconds = 0
position = P.copy()
min_norm = np.inf
while True:
    from_center = middle - position
    norm = np.linalg.norm(from_center)
    if norm < min_norm:
        min_norm = norm
        plt.scatter(position[:, 0], position[:, 1])
        plt.xlim([0, size[0]])
        plt.ylim([0, size[1]])
        plt.title(f"{seconds} seconds")
        plt.show()
        if min_norm < 650:
            break
    seconds += 1
    position = np.mod(position + V, size)

ans_2 = seconds

print(f"1: {ans_1}")
print(f"2: {ans_2}")
