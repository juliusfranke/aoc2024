import sys
from pathlib import Path

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    input, logic = file.read().strip().split("\n\n")

wires = {}
for inp in input.splitlines():
    key, value = inp.split(": ")
    wires[key] = int(value)
log = []

max_z = "z00"
for line in logic.splitlines():
    left, right = line.split(" -> ")
    p1, op, p2 = left.split(" ")
    log.append([p1, p2, op, right])
    if right[0] == "z" and int(right[1:]) > int(max_z[1:]):
        max_z = right


def calc(v1, v2, op):
    match op:
        case "AND":
            return int(v1 and v2)
        case "OR":
            return int(v1 or v2)
        case "XOR":
            return int(v1 != v2)


def try_logic(p1, p2, op, right, wires):
    if p1 not in wires.keys() or p2 not in wires.keys():
        return False
    wires[right] = calc(wires[p1], wires[p2], op)
    return True


def get_z(wires):
    z_i = 0
    num_ls = []
    while z_i <= int(max_z[1:]):
        k = f"z{z_i:02d}"
        num_ls.append(str(wires[k]))
        z_i += 1
    num_str = "".join(num_ls)
    num = int(num_str[::-1], 2)

    return num


in_out = ["x", "y", "z"]
sus = set()

for p1, p2, op, right in log:
    if op == "AND" and "x00" not in [p1, p2]:
        for _p1, _p2, _op, _ in log:
            if (right == _p1 or right == _p2) and _op != "OR":
                sus.add(right)
    if op == "XOR":
        for _p1, _p2, _op, _ in log:
            if (right == _p1 or right == _p2) and _op == "OR":
                sus.add(right)
    if right[0] == "z" and op != "XOR" and right != max_z:
        sus.add(right)
    if (
        op == "XOR"
        and right[0] not in in_out
        and p1[0] not in in_out
        and p2[0] not in in_out
    ):
        sus.add(right)

while log:
    log_remove = []
    for log_line in log:
        p1, p2, op, right = log_line
        if not try_logic(p1, p2, op, right, wires):
            continue
        log_remove.append(log_line)

    for l_r in log_remove:
        log.remove(l_r)


ans_1 = get_z(wires)
ans_2 = ",".join(sorted(sus))

print(f"1: {ans_1}")
print(f"2: {ans_2}")
