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


with open("input17.txt") as f:
    directions = f.read().strip()


tower = set()
j = 0

for i in range(2022):
    #    draw(tower, [])
    x = 2
    y = ymax + 3

    print(f"i = {i}")
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
            rock = block.position(newx, y)
            if all([block not in tower for block in rock]):
                x = newx
 #       draw(tower, block.position(x, y))

        # move down
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

print(ymax)
