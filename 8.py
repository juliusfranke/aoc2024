import sys
from pathlib import Path
from math import gcd
from collections import defaultdict
from typing import DefaultDict, List

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().splitlines()

y_max = len(data)
x_max = len(data[0])

antennas: DefaultDict[str, List] = defaultdict(list)

for i in range(y_max):
    for j in range(x_max):
        symbol = data[i][j]
        if symbol != ".":
            antennas[symbol].append((i, j))


unique_1 = set()
unique_2 = set()
for symbol, locations in antennas.items():
    visited = set()
    for loc in locations:
        visited.add(loc)
        for o_loc in locations:
            if o_loc in visited:
                continue
            diff_y = o_loc[0] - loc[0]
            diff_x = o_loc[1] - loc[1]

            p1 = (loc[0] - diff_y, loc[1] - diff_x)
            if 0 <= p1[0] < y_max and 0 <= p1[1] < x_max:
                unique_1.add(p1)

            p2 = (o_loc[0] + diff_y, o_loc[1] + diff_x)
            if 0 <= p2[0] < y_max and 0 <= p2[1] < x_max:
                unique_1.add(p2)

            div = gcd(diff_y, diff_x)
            diff_y /= div
            diff_x /= div

            n = 0
            while True:
                y = loc[0] + n * diff_y
                x = loc[1] + n * diff_x
                if 0 <= y < y_max and 0 <= x < x_max:
                    unique_2.add((y, x))
                    n += 1
                else:
                    break
            n = -1
            while True:
                y = loc[0] + n * diff_y
                x = loc[1] + n * diff_x
                if 0 <= y < y_max and 0 <= x < x_max:
                    unique_2.add((y, x))
                    n -= 1
                else:
                    break


ans_1 = len(unique_1)
ans_2 = len(unique_2)

print(f"1: {ans_1}")
print(f"2: {ans_2}")
