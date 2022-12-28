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

with open("advice22.txt", "r") as f:
    lines = f.readlines()
    n = int(lines[0])
    cube = []
    for line in lines[1:5]:
        row = []
        for col in line.rstrip("\n"):
            if col == " ":
                row.append(0)
            else:
                row.append(int(col))
        cube.append(row)
    rotation = []
    for line in lines[5:]:
        row = []
        for col in line.split():
            row.append(int(col))
        rotation.append(row)

cube = np.array(cube)
rotation = np.array(rotation)
print(cube)
print(rotation)


def get_rotation(i):
    x, y = (cube == i).nonzero()
    return rotation[x[0], y[0]]


def get_side(i):
    x, y = (cube == i).nonzero()
    return x[0]*n, y[0]*n, rotation[x, y]


extras = {
    i: get_side(i)[0:2]
    for i in range(1, 7)
}


sides = {
    i: get_side(i)
    for i in range(1, 7)
}

sides = {
    i: np.rot90(field[x: x+n, y: y+n], rot) if rot else field[x:x+n, y:y+n]
    for i, (x, y, rot) in sides.items()
}


transitions = {}

transitions.update({
    (1, -1, y): (4, n-1, y)
    for y in range(n)
})
transitions.update({
    (1, n, y): (2, 0, y)
    for y in range(n)
})
transitions.update({
    (1, x, -1): (5, 0, x)
    for x in range(n)
})

transitions.update({
    (1, x, n): (6, 0, n-1-x)
    for x in range(n)
})

###
transitions.update({
    (2, -1, y): (1, n-1, y)
    for y in range(n)
})
transitions.update({
    (2, n, y): (3, 0, y)
    for y in range(n)
})
transitions.update({
    (2, x, -1): (5, x, n-1)
    for x in range(n)
})

transitions.update({
    (2, x, n): (6, x, 0)
    for x in range(n)
})
###
transitions.update({
    (3, -1, y): (2, n-1, y)
    for y in range(n)
})
transitions.update({
    (3, n, y): (4, 0, y)
    for y in range(n)
})
transitions.update({
    (3, x, -1): (5, n-1, n-1-x)
    for x in range(n)
})
transitions.update({
    (3, x, n): (6, n-1, x)
    for x in range(n)
})
###
transitions.update({
    (4, -1, y): (3, n-1, y)
    for y in range(n)
})
transitions.update({
    (4, n, y): (1, 0, y)
    for y in range(n)
})
transitions.update({
    (4, x, -1): (5, n-1-x, 0)
    for x in range(n)
})
transitions.update({
    (4, x, n): (6,  n-1-x, n-1)
    for x in range(n)
})
###
transitions.update({
    (5, -1, y): (1, y, 0)
    for y in range(n)
})
transitions.update({
    (5, n, y): (3, n-1-y, 0)
    for y in range(n)
})
transitions.update({
    (5, x, -1): (4, n-1-x, 0)
    for x in range(n)
})
transitions.update({
    (5, x, n): (2, x, 0)
    for x in range(n)
})
###
transitions.update({
    (6, -1, y): (1, n-1-y, n-1)
    for y in range(n)
})
transitions.update({
    (6, n, y): (3, y, n-1)
    for y in range(n)
})
transitions.update({
    (6, x, -1): (2, x, n-1)
    for x in range(n)
})
transitions.update({
    (6, x, n): (4, n-1-x, n-1)
    for x in range(n)
})

translate_direction = {
    (1, 5): 1,
    (5, 1): 0,
    (6, 1): 2,
    (1, 6): 1,
    (5, 3): 0,
    (3, 5): 3,
    (3, 6): 3,
    (6, 3): 2,
    (4, 5): 0,
    (5, 4): 0,
    (4, 6): 2,
    (6, 4): 2
}


def move(cube, side, x, y, direction):

    def right(side, x, y):
        newx, newy = x, y+1
        if (side, newx, newy) in transitions:
            side, newx, newy = transitions[(side, newx, newy)]
        return side, newx, newy

    def down(side, x, y):
        newx, newy = x+1, y
        if (side, newx, newy) in transitions:
            side, newx, newy = transitions[(side, newx, newy)]
        return side, newx, newy

    def left(side, x, y):
        newx, newy = x, y-1
        if (side, newx, newy) in transitions:
            side, newx, newy = transitions[(side, newx, newy)]
        return side, newx, newy

    def up(side, x, y):
        newx, newy = x-1, y
        if (side, newx, newy) in transitions:
            side, newx, newy = transitions[(side, newx, newy)]
        return side, newx, newy

    if direction == 0:
        newside, newx, newy = right(side, x, y)
    elif direction == 1:
        newside, newx, newy = down(side, x, y)
    elif direction == 2:
        newside, newx, newy = left(side, x, y)
    elif direction == 3:
        newside, newx, newy = up(side, x, y)

    print("->", newside, newx, newy)
    if cube[newside][newx, newy] == 2:
        return side, x, y, False, direction
    else:
        if (side, newside) in translate_direction:
            direction = translate_direction[(side, newside)]
        return newside, newx, newy, True, direction


def draw(field, position):
    for i, line in enumerate(field):
        for j, col in enumerate(line):
            if position == (i, j):
                print("S", end="")
            elif col == 0:
                print(" ", end="")
            elif col == 1:
                print(".", end="")
            elif col == 2:
                print("#", end="")
        print()


x, y = 0, 0
direction = 0
side = 1

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
        side, x, y, moved, direction = move(sides, side, x, y, direction)
        if not moved:
            break
    # if get_rotation(side) == 1:
    #     xx = y
    #     yy = n-1-x
    # elif get_rotation(side) == 2:
    #     xx = n-1-x
    #     yy = n-1-y
    # else:
    #     xx, yy = x, y
    # ex, ey = extras[side]
    # draw(field, (xx+ex, yy+ey))
    # input()

print(side, x, y)

ex, ey = extras[side]

x += ex
y += ey

print(x, y, direction)

print(1000*(x+1)+4*(y+1)+direction)
