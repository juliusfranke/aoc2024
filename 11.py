import sys
from tqdm import tqdm
from pathlib import Path
from collections import defaultdict

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip()

stones = defaultdict(int)
for num in data.split(" "):
    stones[int(num)] += 1


def blink():
    nums = list(stones.items())
    for num, amount in nums:
        if num == 0:
            stones[1] += amount
        elif len(str(num)) % 2 == 0:
            num_str = str(num)
            num_l = int(num_str[len(num_str) // 2 :])
            num_r = int(num_str[: len(num_str) // 2])
            stones[num_l] += amount
            stones[num_r] += amount
        else:
            stones[num * 2024] += amount
        stones[num] -= amount
        if stones[num] == 0:
            stones.pop(num)


for _ in tqdm(range(25)):
    blink()

ans_1 = sum([n for n in stones.values()])

for _ in tqdm(range(50)):
    blink()

ans_2 = sum([n for n in stones.values()])

print(f"1: {ans_1}")
print(f"2: {ans_2}")
