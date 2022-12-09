start = (0, 0)
snail = [(0, 0) for i in range(10)]


positions = set()
positions.add(start)


def distance(head, tail):
    v = head[0] - tail[0]
    h = head[1] - tail[1]

    if abs(v) < 2 and abs(h) < 2:
        return ""

    response = ""
    if v < 0:
        response += "U"
    if v > 0:
        response += "D"
    if h > 0:
        response += "R"
    if h < 0:
        response += "L"

    return response


def move_one(obj, direction):
    if direction == "R":
        return (obj[0], obj[1]+1)
    elif direction == "L":
        return (obj[0], obj[1]-1)
    elif direction == "U":
        return (obj[0]-1, obj[1])
    elif direction == "D":
        return (obj[0]+1, obj[1])


def move_tail(head, tail):
    tail_dir = distance(head, tail)
    for d in tail_dir:
        tail = move_one(tail, d)
    return tail


def move(direction, number):
    global head, tail, positions

    for _ in range(number):
        snail[0] = move_one(snail[0], direction)

        for i in range(len(snail)-1):
            snail[i+1] = move_tail(snail[i], snail[i+1])
        positions.add(snail[-1])


with open("input9.txt", "r") as f:
    for line in f:
        direction, number = line.split()
        number = int(number)
        move(direction, number)

print(len(positions))
