import numpy as np
from collections import Counter

example = "1_example.txt"
input = "1_input.txt"

with open(input,"r") as file:
    data = file.read()

data = data.splitlines()

array = np.array([line.split("   ") for line in data],dtype=int).T
left_list = array[0].copy()
right_list = array[1].copy()
array[0].sort()
array[1].sort()
distance = np.sum(np.abs(array[0]-array[1]))
print(f"1.1: {distance}")
counts_right = Counter(right_list)
similarity = np.sum([number*counts_right[number] if number in counts_right.keys() else 0 for number in left_list])
print(f"1.2: {similarity}")
