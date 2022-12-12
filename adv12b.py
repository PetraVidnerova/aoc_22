field = []

S = (None, None)

with open("input12.txt") as f:
    line_num = 0
    for line in f:
        field.append(list(line.strip()))

        try:
            s = field[-1].index("S")
            S = (line_num, s)
            field[-1][s] = "a"
        except ValueError:
            pass

        try:
            z = field[-1].index("E")
            E = (line_num, z)
            field[-1][z] = "z"
        except ValueError:
            pass
        line_num += 1

print(field)
print(S)
print(E)

starting_fields = [
    (x, y)
    for x in range(len(field))
    for y in range(len(field[0]))
    if field[x][y] == "a"
]
visited = set()
visited.add(S)
length = 0


def possible(start, end):
    if end[0] < 0 or end[0] >= len(field):
        return False
    if end[1] < 0 or end[1] >= len(field[0]):
        return False
    val1 = ord(field[start[0]][start[1]])
    val2 = ord(field[end[0]][end[1]])
    if val2 - val1 > 1:
        return False
    return True


while True:
    if not starting_fields:
        raise ValueError("not reachable")
    if E in starting_fields:
        break
    length += 1
    new_starting = []
    for current in starting_fields:

        for next_field in (
                (current[0], current[1]+1),
                (current[0], current[1]-1),
                (current[0]+1, current[1]),
                (current[0]-1, current[1])
        ):
            if next_field not in visited and possible(current, next_field):
                new_starting.append(next_field)
                visited.add(next_field)
    starting_fields = new_starting

print(length)
