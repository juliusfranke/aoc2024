import sys
from pathlib import Path
from collections import defaultdict
import numpy as np

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip().splitlines()


# data = """1
# 2
# 3
# 2024""".splitlines()
data = np.array([int(num) for num in data])


def mix(nums, secret):
    return np.bitwise_xor(nums, secret)


def prune(secret):
    return np.mod(secret, 16777216)


def step(secret: np.ndarray):
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    secret = prune(mix(secret * 2048, secret))
    return secret


def rolling_window(a, size):
    shape = a.shape[:-1] + (a.shape[-1] - size + 1, size)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


prices = [np.mod(data, 10)]
changes = []
for i in range(2000):
    data = step(np.array(data))
    price = np.mod(data, 10)
    prices.append(price)
prices = np.array(prices)
change = prices[1:] - prices[:-1]

visited = set()


def search(change, prices):
    best = defaultdict(int)

    for i in range(0, change.shape[1]):
        visited = set()
        for j in range(len(change) - 3):
            price = prices[j + 4, i]
            seq = tuple(change[j : j + 4, i])
            if seq in visited:
                continue
            visited.add(seq)
            best[seq] += price
    return max(best.values())


ans_1 = sum(data)
ans_2 = search(change, prices)

print(f"1: {ans_1}")
print(f"2: {ans_2}")
