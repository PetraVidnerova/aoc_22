map_fields = set()
blizzards = []

with open("input24.txt", "r") as f:
    for i, line in enumerate(f):
        for j, field in enumerate(line.strip()):
            if field != "#":
                map_fields.add((i, j))
            if field in "><^v":
                blizzards.append((field, (i, j)))
    rows = i+1
    cols = j+1


def move_blizzards(blizzards):
    new_blizzards = []
    for direction, (r, c) in blizzards:
        if direction == ">":
            r, c = r, c + 1
            if c == cols-1:
                c = 1
        elif direction == "<":
            r, c = r, c - 1
            if c == 0:
                c = cols-2
        elif direction == "v":
            r, c = r+1, c
            if r == rows-1:
                r = 1
        elif direction == "^":
            r, c = r - 1, c
            if r == 0:
                r = rows - 2
        else:
            raise ValueError("wrong dir")
        new_blizzards.append((direction, (r, c)))
    return new_blizzards


def next_steps(pos, blizzards):
    r, c = pos
    result = []
    for next_step in (
            (r, c+1),
            (r, c-1),
            (r+1, c),
            (r-1, c),
            (r, c)
    ):
        if next_step not in blizzards and next_step in map_fields:
            result.append(next_step)
    return result


START = (0, 1)
END = (rows-1, cols-2)


def draw(blizzards, fields, me):
    for i in range(rows):
        for j in range(cols):
            if (i, j) in blizzards:
                print("B", end="")
            elif (i, j) in me:
                print("E", end="")
            elif (i, j) in fields:
                print(".", end="")
            else:
                print("#", end="")
        print()


def find_way():
    global blizzards

    time = 0
    positions = set()
    positions.add(START)
    blizzards = blizzards

    while True:
        time += 1
        print(time)
#        draw(set([x[1] for x in blizzards]), map_fields, positions)
        blizzards = move_blizzards(blizzards)
        blizzards_set = set([x[1] for x in blizzards])
        new_positions = set()
        for pos in positions:
            for new_pos in next_steps(pos, blizzards_set):
                if new_pos == END:
                    return time
                new_positions.add(new_pos)
        positions = new_positions


print(find_way())
