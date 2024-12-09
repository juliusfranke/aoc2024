import sys
from tqdm import tqdm
from pathlib import Path

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip()

line = []
idx = 0
for i, number in enumerate(data):
    no = int(number)
    if i % 2 == 0:
        line.extend([idx for _ in range(no)])
        idx += 1
    else:
        line.extend(["." for _ in range(no)])
last_i = 1
last_j = 0
# for i in range(1, len(line)):
for i in tqdm(range(1, len(line))):
    if i < last_i:
        continue
    if line[-i] == ".":
        continue
    if last_j >= len(line)-last_i:
        break
    for j in range(len(line) - i):
        if j <= last_j:
            continue
        if line[j] == ".":
            last_i = i
            last_j = j
            line[j] = line[-i]
            line[-i] = "."
            break
    


ans_1 = 0
ans_2 = 0

for i in range(len(line)):
    if line[i] == ".":
        break
    ans_1 += int(line[i]) * i

print(f"1: {ans_1}")
print(f"2: {ans_2}")
