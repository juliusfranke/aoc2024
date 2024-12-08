import sys
from pathlib import Path
import numpy as np

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


def isvalid(numbers, target, concat=False, concat_num: int | None = None):
    num = numbers[-1]
    if len(numbers) == 1:
        if np.isclose(target, num):
            return True
        else:
            return False
    if target - num >= 0:
        # print("subtraction")
        if isvalid(numbers[:-1], target - num, concat=concat):
            return True
    if target % num == 0:
        # print("dividing")
        if isvalid(numbers[:-1], target // num, concat=concat):
            return True
    if concat:
        num_str = str(num)
        target_str = str(target)
        if len(target_str) > len(num_str) and all(
            [num_str[-i - 1] == target_str[-i - 1] for i in range(len(num_str))]
        ):
            if isvalid(numbers[:-1], int(target_str[: -len(num_str)]), concat=True):
                return True
    return False


with open(input, "r") as file:
    data = file.read()

data = data.splitlines()
lines = []
for line in data:
    a = line.split(": ")
    result = int(a[0])
    numbers = [int(b) for b in a[1].split(" ")]
    lines.append([result, numbers])

ans_1 = 0
ans_2 = 0

for line in lines:
    valid_1 = isvalid(line[1], line[0])
    if valid_1:
        ans_1 += line[0]
    valid_2 = isvalid(line[1], line[0], concat=True)
    if valid_2:
        ans_2 += line[0]


print(f"1: {ans_1}")
print(f"2: {ans_2}")
