import sys
from typing import List

day = 5
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = example if len(sys.argv) > 1 and sys.argv[1] == "example" else input


with open(input, "r") as file:
    data = file.read()

rules, updates = data.split("\n\n")
rules = rules.splitlines()
updates_str = updates.splitlines()

rules_rev = {}
for rule in rules:
    n1, n2 = rule.split("|")
    n1, n2 = int(n1), int(n2)
    if n2 not in rules_rev.keys():
        rules_rev[n2] = [n1]
    else:
        rules_rev[n2].append(n1)
updates = []
for update in updates_str:
    updates.append([int(no) for no in update.split(",")])


def fix_intersection(update, intersection, idx):
    for error in intersection:
        update.remove(error)
        update.insert(idx, error)


def check_intersection(update):
    a1 = True
    intersections = [None, None]
    for i in range(len(update) - 1):
        remaining = update[i+1:]
        current = update[i]
        if current not in rules_rev.keys():
            continue
        not_allowed = rules_rev[current]
        intersection = set(remaining).intersection(not_allowed)
        if intersection:
            a1 = False
            intersections = [i, intersection]
            break
    return a1, intersections


def check_update(update) -> List[int]:
    a1 = True
    a2 = 0
    a2_list = update.copy()
    a1, intersections = check_intersection(update)
    while intersections[1]:
        fix_intersection(a2_list, intersections[1], intersections[0])
        _, intersections = check_intersection(a2_list)
        a2 = a2_list[(len(a2_list) - 1) // 2]
    
    if a1:
        return [update[(len(update) - 1) // 2], a2]
    else:
        return [0, a2]


ans_1 = 0
ans_2 = 0
for update in updates:
    a1, a2 = check_update(update)
    ans_1 += a1
    ans_2 += a2

print(f"1: {ans_1}")
print(f"2: {ans_2}")
