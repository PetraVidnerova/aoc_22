import numpy as np

with open("input22.txt", "r") as f:
    lines = f.readlines()

n = len(lines[:-2])
m = max([len(x) for x in lines[:-2]])

field = np.zeros((n, m))
for i, line in enumerate(lines[:-2]):
    for j, x in enumerate(line):
        if x == " ":
            continue
        if x == ".":
            field[i, j] = 1
        elif x == "#":
            field[i, j] = 2

program_line = lines[-1]
program = [1]
while program_line:
    if program_line[0] == "\n":
        break
    if program_line[0] in ("R", "L"):
        program.append(program_line[0])
        program_line = program_line[1:]
        continue
    i = 0
    while program_line[i] not in ("R", "L", "\n"):
        i += 1
    program.append(int(program_line[:i]))
    program_line = program_line[i:]

print(field)
print(program)


def move(field, x, y, direction):
    m, n = field.shape

    def right(x, y):
        newx, newy = x, y+1
        if newy >= n:
            newy = 0
        return newx, newy

    def down(x, y):
        newx, newy = x+1, y
        if newx >= m:
            newx = 0
        return newx, newy

    def left(x, y):
        newx, newy = x, y-1
        if newy < 0:
            newy = n-1
        return newx, newy

    def up(x, y):
        newx, newy = x-1, y
        if newx < 0:
            newx = m-1
        return newx, newy

    if direction == 0:
        newx, newy = right(x, y)
        while field[newx, newy] == 0:
            newx, newy = right(newx, newy)
    elif direction == 1:
        newx, newy = down(x, y)
        while field[newx, newy] == 0:
            newx, newy = down(newx, newy)
    elif direction == 2:
        newx, newy = left(x, y)
        while field[newx, newy] == 0:
            newx, newy = left(newx, newy)
    elif direction == 3:
        newx, newy = up(x, y)
        while field[newx, newy] == 0:
            newx, newy = up(newx, newy)

    if field[newx, newy] == 2:
        return x, y, False
    else:
        return newx, newy, True


x, y = 0, 0
direction = 0

for command in program:
    print(command, ":", x, y, direction)
    if command == "R":
        direction = (direction + 1) % 4
        continue
    if command == "L":
        direction = (direction - 1) % 4
        continue
    steps = command
    for _ in range(steps):
        x, y, moved = move(field, x, y, direction)
        if not moved:
            break

print(x, y)

print(1000*(x+1)+4*(y+1)+direction)
