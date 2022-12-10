X = 1
cycle = 0

screen = [
    40*["-"]
    for _ in range(6)
]


def update_result(cycle, X):
    global screen

    line = (cycle-1) // 40
    column = (cycle-1) % 40

    if abs(X-(column)) < 2:
        pixel = "#"
    else:
        pixel = "."

    screen[line][column] = pixel


def process_line(line):
    global cycle, X

    cycle += 1
    update_result(cycle, X)
    if line.startswith("addx"):
        cycle += 1
        update_result(cycle, X)
        _, number = line.split()
        X += int(number)


with open("input10.txt", "r") as f:
    for line in f:
        process_line(line.strip())

for line in screen:
    for char in line:
        print(char, end="")
    print()
