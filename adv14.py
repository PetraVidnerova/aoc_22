blocks = set()
bottomline = 0


def parse_line(line):
    global blocks, bottomline

    points = []
    for point in line.split("->"):
        x, y = map(int, point.split(","))
        points.append((x, y))

    start = 0
    end = 1
    while end < len(points):
        s = points[start]
        e = points[end]
        if s[0] == e[0]:
            if s[1] > e[1]:
                s, e = e, s
            if e[1] > bottomline:
                bottomline = e[1]
            for i in range(s[1], e[1]+1):
                blocks.add((s[0], i))
        elif s[1] == e[1]:
            if s[0] > e[0]:
                s, e = e, s
            if s[1] > bottomline:
                bottomline = s[1]
            for i in range(s[0], e[0]+1):
                blocks.add((i, s[1]))
        start, end = start+1, end+1


def fall(x, y):
    if y > bottomline:
        return True
    for next_pos in (
            (x, y+1),
            (x-1, y+1),
            (x+1, y+1)
    ):
        if next_pos not in blocks:
            return fall(*next_pos)
    blocks.add((x, y))
    return False


with open("input14.txt", "r") as f:
    for line in f:
        parse_line(line)


bottomline += 2
source = (500, 0)

i = 0
while True:
    if fall(*source):
        break
    i += 1

print("END")
print(i)
