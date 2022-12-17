XMIN = 0
XMAX = 6

YMIN = 0
ymax = 0


class Rock():
    def __init__(self, lines):
        self.height = len(lines)
        self.width = len(lines[0])
        self.blocks = []
        for y in range(self.height):
            for x in range(self.width):
                if lines[y][x] == "#":
                    self.blocks.append((x, y))

    def position(self, x, y):
        y = y + self.height
        blocks = []
        for bx, by in self.blocks:
            blocks.append((x+bx, y-by))
        return blocks


rocks = [
    Rock(["####"]),
    Rock([
        ".#.",
        "###",
        ".#.",
    ]),
    Rock([
        "..#",
        "..#",
        "###"
    ]),
    Rock([
        "#",
        "#",
        "#",
        "#"
    ]),
    Rock([
        "##",
        "##",
    ])
]


def draw(tower, block):
    global ymax
    mymax = max([b[1] for b in block]+[ymax])
    for y in range(mymax, 0, -1):
        for x in range(0, XMAX+1):
            if (x, y) in tower:
                print("#", end="")
            elif (x, y) in block:
                print("@", end="")
            else:
                print(".", end="")
        print()
    print()


def is_full(tower, line_num):
    line = [(x, line_num) for x in range(XMAX+1)]
    if all([point in tower for point in line]):
        return True
    else:
        return False


def is_covered(tower, line_num):
    line = [(x, line_num) for x in range(XMAX+1)]
    if all([point in tower or (point[0], point[1]+1) in tower for point in line]):
        return True
    else:
        return False


def reduce_tower(tower, border):
    new_tower = set()
    for point in tower:
        if point[1] >= border:
            new_tower.add((point[0], point[1]-border))
    return new_tower


def hash(tower, ymax):
    hash_list = []
    for y in range(ymax+1):
        hash_list.append(["."]*7)
    for y in range(0, ymax+1):
        for x in range(0, XMAX+1):
            if (x, y) in tower:
                hash_list[y][x] = "#"
        hash_list[y] = "".join(hash_list[y])
    return "".join(hash_list)


with open("input17.txt") as f:
    directions = f.read().strip()

tower = set()
j = 0

states = set()
states_times = {}
states_heights = {}


height = ymax

i = 0
togo = 1000000000000
#togo = 2022
while i < togo:
    for xx in range(ymax, 0, -1):
        if is_covered(tower, xx):
            tower = reduce_tower(tower, xx)
            height += xx
            ymax = max([block[1] for block in tower])
            break

    #   draw(tower, [])
    x = 2
    y = ymax + 3

    tag = hash(tower, ymax)
    state = (tag, i % len(rocks), j % len(directions))
    if state not in states:
        states.add(state)
        states_times[state] = i
        states_heights[state] = height + ymax
    else:
        last_time = states_times[state]
        last_height = states_heights[state]

        period = i - last_time
        height_during_period = height + ymax - last_height

        left_time = togo - i
        repeat = left_time // period

        i += repeat*period
        height += repeat * height_during_period

    if i % 1000 == 0:
        print(f"i = {i} {ymax} {len(tower)} {len(states)}")
    block = rocks[i % len(rocks)]
    while True:

        #        draw(tower, block.position(x, y))
        direction = directions[j % len(directions)]
        j += 1

        if direction == "<":
            if x > 0:
                newx = x - 1
            else:
                newx = x
        elif direction == ">":
            if x + block.width < XMAX+1:
                newx = x + 1
            else:
                newx = x
        oldx, oldy = x, y
        # shif left/right
        if newx != x:
            if y > ymax:
                x = newx
            else:
                rock = block.position(newx, y)
                if all([block not in tower for block in rock]):
                    x = newx
 #       draw(tower, block.position(x, y))

        # move down
        if y > ymax+1:
            y = y - 1
        else:
            if y > 0:
                # try move to x, y-1
                rock = block.position(x, y-1)
                if all([block not in tower for block in rock]):
                    y = y-1

        # lay block
        if oldy == y:
            rock = block.position(x, y)
            for block in rock:
                tower.add(block)
            ymax = max([block[1] for block in tower])
            break
    i += 1

print(height+ymax)
draw(tower, [])
