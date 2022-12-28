elfes = []

with open("input23.txt", "r") as f:
    for i, line in enumerate(f):
        for j, field in enumerate(line.strip()):
            if field == "#":
                elfes.append((i, j))

directions = ["N", "S", "W", "E"]


def north(pos):
    x, y = pos
    if (
            (x-1, y-1) not in elfes and
            (x-1, y) not in elfes and
            (x-1, y+1) not in elfes
    ):
        x, y = x-1, y
    return x, y


def south(pos):
    x, y = pos
    if (
            (x+1, y-1) not in elfes and
            (x+1, y) not in elfes and
            (x+1, y+1) not in elfes
    ):
        x, y = x+1, y
    return x, y


def west(pos):
    x, y = pos
    if (
            (x-1, y-1) not in elfes and
            (x, y-1) not in elfes and
            (x+1, y-1) not in elfes
    ):
        x, y = x, y-1
    return x, y


def east(pos):
    x, y = pos
    if (
            (x-1, y+1) not in elfes and
            (x, y+1) not in elfes and
            (x+1, y+1) not in elfes
    ):
        x, y = x, y+1
    return x, y


moves = {
    "N": north,
    "S": south,
    "W": west,
    "E": east
}


def draw(elfes):
    xs = [x for x, y in elfes]
    ys = [y for x, y in elfes]

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    for i in range(minx, maxx+1):
        for j in range(miny, maxy+1):
            if (i, j) in elfes:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()
    print()


def find_new_positions(pos):
    new_positions = []
    for direction in directions:
        new_pos = moves[direction](pos)
        if new_pos != pos:
            new_positions.append(new_pos)
    return new_positions


for _ in range(10):
    #    draw(elfes)
    print(directions)
    # estimate positions
    new_elfes = []
    for i, j in elfes:
        new_positions = find_new_positions((i, j))
        if len(new_positions) == 0 or len(new_positions) == 4:
            new_elfes.append((i,  j))
        else:
            new_elfes.append(new_positions[0])

    # move
    for i, new_pos in enumerate(new_elfes):
        if new_elfes.count(new_pos) == 1:
            elfes[i] = new_pos

    first_dir = directions.pop(0)
    directions.append(first_dir)

# draw(elfes)

xs = [x for x, y in elfes]
ys = [y for x, y in elfes]

minx, maxx = min(xs), max(xs)
miny, maxy = min(ys), max(ys)

count = 0
for i in range(minx, maxx+1):
    for j in range(miny, maxy+1):
        if (i, j) not in elfes:
            count += 1
print(count)
