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

ans_1 = 0
ans_2 = 0

print(f"1: {ans_1}")
print(f"2: {ans_2}")
