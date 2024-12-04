import sys

day = 4
example = f"{day}_example.txt"
input = f"{day}_input.txt"
input = example if len(sys.argv) > 1 and sys.argv[1] == "example" else input


with open(input, "r") as file:
    data = file.read()

lines = data.splitlines()

x_max = len(lines[0])
y_max = len(lines)


def check_letter_1(i, j) -> int:
    count = 0
    forward = x_max - j >= 4
    up = i >= 3
    backward = j >= 3
    down = y_max - i >= 4
    if forward:
        word = lines[i][j : j + 4]
        count += int(word == "XMAS")
        if up:
            word = "".join([lines[i - a][j + a] for a in [0, 1, 2, 3]])
            count += int(word == "XMAS")
        if down:
            word = "".join([lines[i + a][j + a] for a in [0, 1, 2, 3]])
            count += int(word == "XMAS")
    if backward:
        word = "".join([lines[i][j - a] for a in [0, 1, 2, 3]])
        count += int(word == "XMAS")
        if up:
            word = "".join([lines[i - a][j - a] for a in [0, 1, 2, 3]])
            count += int(word == "XMAS")
        if down:
            word = "".join([lines[i + a][j - a] for a in [0, 1, 2, 3]])
            count += int(word == "XMAS")
    if up:
        word = "".join([lines[i - a][j] for a in [0, 1, 2, 3]])
        count += int(word == "XMAS")
    if down:
        word = "".join([lines[i + a][j] for a in [0, 1, 2, 3]])
        count += int(word == "XMAS")

    return count


def check_letter_2(i, j) -> int:
    word_1 = "".join([lines[i + a][j + a] for a in [-1, 0, 1]])
    if word_1 not in ["SAM", "MAS"]:
        return 0
    word_2 = "".join([lines[i - a][j + a] for a in [-1, 0, 1]])
    if word_2 not in ["SAM", "MAS"]:
        return 0
    return 1


sum_1 = 0
sum_2 = 0
for i in range(y_max):
    for j in range(x_max):
        letter = lines[i][j]
        if letter == "X":
            sum_1 += check_letter_1(i, j)
        if letter != "A" or not 0 < i < y_max - 1 or not 0 < j < x_max - 1:
            continue
        sum_2 += check_letter_2(i, j)
print(f"1: {sum_1}")
print(f"1: {sum_2}")
