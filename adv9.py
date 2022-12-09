start = (0, 0)
head = (0, 0)
tail = (0, 0)

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


def move(direction, number):
    global head, tail, positions

    for _ in range(number):
        head = move_one(head, direction)

        tail_dir = distance(head, tail)
        for d in tail_dir:
            tail = move_one(tail, d)
        positions.add(tail)


with open("input9.txt", "r") as f:
    for line in f:
        direction, number = line.split()
        number = int(number)
        move(direction, number)

print(len(positions))
