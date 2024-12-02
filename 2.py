from typing import Tuple
import numpy as np


def is_safe(line, tol) -> Tuple[bool, bool]:
    fix_idxs = []
    ar = np.array(line)
    diff = ar[:-1] - ar[1:]
    arg1_1 = np.sum(diff < 0)
    arg1_2 = np.sum(diff > 0)
    arg1 = np.logical_or(arg1_1 == diff.shape[0], arg1_2 == diff.shape[0])
    if arg1_1 == diff.shape[0] - 1:
        idx_1 = np.where(diff >= 0)[0]
        fix_idxs.append(idx_1)
        fix_idxs.append(idx_1 + 1)
    if arg1_2 == diff.shape[0] - 1:
        idx_1 = np.where(diff <= 0)[0]
        fix_idxs.append(idx_1)
        fix_idxs.append(idx_1 + 1)

    arg2_ar = np.logical_and(np.abs(diff) >= 1, np.abs(diff) <= 3)
    arg2 = np.sum(arg2_ar)

    if arg2 == diff.shape[0] - 1:
        idx_2 = np.where(arg2_ar == False)[0]
        fix_idxs.append(idx_2)
        fix_idxs.append(idx_2 + 1)

    arg = np.logical_and(arg1, arg2 == diff.shape[0])

    if not tol or not fix_idxs:
        return (arg, arg)
    for idx in np.unique(fix_idxs):
        n_line = line.copy()
        del n_line[idx]
        if is_safe(n_line, tol=False)[1]:
            return (arg, True)
    return (arg, arg)


example = "2_example.txt"
input = "2_input.txt"
input = input

with open(input, "r") as file:
    data = file.read()


array = [[int(number) for number in line.split(" ")] for line in data.splitlines()]

safe = 0
safe_tol = 0

for line in array:
    safe_i, safe_tol_i = is_safe(line, tol=True)
    safe += safe_i
    safe_tol += safe_tol_i

print(f"1: {safe}")
print(f"2: {safe_tol}")
