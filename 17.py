import sys
from typing import Dict, List
from pathlib import Path

day = Path(__file__).stem
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = input if len(sys.argv) == 1 else example


with open(input, "r") as file:
    data = file.read().strip()

registers, program_ = data.split("\n\n")

registers = [int(line.split(": ")[1]) for line in registers.splitlines()]
reg_dict: Dict[str, int] = {"A": registers[0], "B": registers[1], "C": registers[2]}
program = [int(opcode) for opcode in program_.split(": ")[1].split(",")]


def get_combo(operand, regs) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return regs["A"]
        case 5:
            return regs["B"]
        case 6:
            return regs["C"]
        case _:
            raise Exception


def run(program: List[int], a: int) -> List[int]:
    regs = {"A": a, "B": 0, "C": 0}
    i = 0
    output = []
    while i < len(program):
        opcode = program[i]
        operand = program[i + 1]
        match opcode:
            case 0:
                combo = get_combo(operand, regs)
                regs["A"] = regs["A"] // (1 << combo)
            case 1:
                regs["B"] ^= operand
            case 2:
                combo = get_combo(operand, regs)
                regs["B"] = combo % 8
            case 3:
                if regs["A"] == 0:
                    i += 2
                    continue
                i = operand
                continue
            case 4:
                regs["B"] = regs["B"] ^ regs["C"]
            case 5:
                combo = get_combo(operand, regs)
                output.append(combo % 8)
            case 6:
                combo = get_combo(operand, regs)
                regs["B"] = regs["A"] // (1 << combo)
            case 7:
                combo = get_combo(operand, regs)
                regs["C"] = regs["A"] // (1 << combo)

        i += 2
    return output


ans_1 = ",".join([str(o) for o in run(program, reg_dict["A"])])

find = program[::-1]


def run_2(a, d):
    if d == len(find):
        return a
    for i in range(8):
        out = run(program, a * 8 + i)
        if not (out and out[0] == find[d]):
            continue
        if res := run_2((a * 8 + i), d + 1):
            return res
    return 0


ans_2 = run_2(0, 0)

print(f"1: {ans_1}")
print(f"2: {ans_2}")
