import sys
import re
from pathlib import Path
import numpy as np

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example

regex = r"=?([+-]?\d+)"
cost = np.array([3, 1])

with open(input, "r") as file:
    data = file.read().strip().split("\n\n")

ans_1 = 0
ans_2 = 0


def calc_n(a_x, a_y, b_x, b_y, p_x, p_y) -> int:
    num_1 = p_y * a_x - p_x * a_y
    den_1 = b_y * a_x - b_x * a_y
    if num_1 % den_1 != 0:
        return 0
    n_b = num_1 // den_1
    num_2 = p_x - n_b * b_x
    den_2 = a_x
    if num_2 % den_2 != 0:
        return 0
    n_a = num_2 // den_2
    return 3 * n_a + n_b


for block in data:
    m = re.findall(regex, block, re.MULTILINE)
    if len(m) != 6:
        raise Exception

    a_x, a_y, b_x, b_y, p_x, p_y = [int(num) for num in m]
    ans_1 += calc_n(a_x, a_y, b_x, b_y, p_x, p_y)
    ans_2 += calc_n(a_x, a_y, b_x, b_y, 10000000000000 + p_x, 10000000000000 + p_y)


print(f"1: {ans_1}")
print(f"2: {ans_2}")
