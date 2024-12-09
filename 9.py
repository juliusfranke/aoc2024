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
    data = file.read().strip()

line = []
storage_id = 0
idx = 0
ids_numbers = deque()
ids_numbers_2 = OrderedDict()
ids_dots = deque()
ids_dots_2: Dict[int, int] = {}
for i, number in enumerate(data):
    no = int(number)
    if i % 2 == 0:
        line.extend([storage_id for _ in range(no)])
        ids_numbers.extend([idx + k for k in range(no)])
        ids_numbers_2[idx] = no
        storage_id += 1
    else:
        line.extend(["." for _ in range(no)])
        ids_dots.extendleft([idx + k for k in range(no)])
        ids_dots_2[idx] = no
    idx += no

line_2 = line.copy()

last_dot = ids_dots.pop()
last_number = ids_numbers.pop()
while last_dot <= last_number:
    line[last_dot], line[last_number] = line[last_number], "."

    if len(ids_numbers) == 0 or len(ids_dots) == 0:
        break

    last_dot = ids_dots.pop()
    last_number = ids_numbers.pop()

for num_id, n_number in reversed(ids_numbers_2.items()):
    replace = None
    dot_id = None
    n_dots = 0
    for dot_id in sorted(ids_dots_2.keys()):
        if dot_id >= num_id:
            break
        n_dots = ids_dots_2[dot_id]
        if n_number <= n_dots:
            line_2[dot_id : dot_id + n_number], line_2[num_id : num_id + n_number] = (
                line_2[num_id : num_id + n_number],
                line_2[dot_id : dot_id + n_number],
            )
            replace = True
            break
    if replace and dot_id:
        ids_dots_2.pop(dot_id)
        if n_number < n_dots:
            ids_dots_2[dot_id+n_number] = n_dots - n_number


ans_1 = 0
ans_2 = 0

for i in range(len(line)):
    if line[i] == ".":
        break
    ans_1 += int(line[i]) * i

for i in range(len(line_2)):
    if line_2[i] == ".":
        continue
    ans_2 += int(line_2[i]) * i
print(f"1: {ans_1}")
print(f"2: {ans_2}")
