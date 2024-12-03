import re
import sys

day = 3
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = example if len(sys.argv) > 1 and sys.argv[1] == "example" else input


with open(input, "r") as file:
    data = file.read()

orig = data
# data = data.splitlines()


reg_1 = r"mul\((\d{1,3}),(\d{1,3})\)"
first = r"^(.*?)don't"
last = r"(?:.*)do((?!n't).*?)$"
do_dont = r"do([^n].*?)don't"

multiplications = re.findall(reg_1, data)

sum_1 = 0
for a, b in multiplications:
    sum_1 += int(a) * int(b)


first_find = re.findall(first, data)
last_find = re.findall(last, data)

dos = []
if len(first_find) > 0:
    first_find = first_find[0]
    data = data[len(first_find) :]
    dos.append(first_find)
if len(last_find) > 0:
    last_find = last_find[0]
    if "don't" not in last_find:
        data = data[: -len(last_find)]
        dos.append(last_find)


dos.extend([d for d in re.findall(do_dont, data)])

cleaned = "".join(dos)
mults = re.findall(reg_1, cleaned)
sum_2 = 0
for a, b in mults:
    sum_2 += int(a) * int(b)
print(f"1: {sum_1}")
print(f"2: {sum_2}")
