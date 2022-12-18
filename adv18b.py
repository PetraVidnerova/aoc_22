lava = set()

with open("input18.txt", "r") as f:
    for line in f:
        lava.add(
            tuple(
                map(int, line.split(","))
            )
        )

min_x = min([x for (x, y, z) in lava])
max_x = max([x for (x, y, z) in lava])

min_y = min([y for (x, y, z) in lava])
max_y = max([y for (x, y, z) in lava])

min_z = min([z for (x, y, z) in lava])
max_z = max([z for (x, y, z) in lava])


def is_on_border(cube):
    x, y, z = cube
    if x <= min_x:
        return True
    if x >= max_x:
        return True
    if y <= min_y:
        return True
    if y >= max_y:
        return True
    if z <= min_z:
        return True
    if z >= max_z:
        return True
    return False


global_space = set()
global_free = set()


def free(cube):
    global global_space, global_free

    if cube in global_space:
        return False
    if cube in global_free:
        return True
    space = set()
    to_expand = [cube]
    while to_expand:
        x, y, z = to_expand.pop()
        for neighbour in [
                (x-1, y, z),
                (x+1, y, z),
                (x, y-1, z),
                (x, y+1, z),
                (x, y, z-1),
                (x, y, z+1)
        ]:
            if neighbour not in lava and is_on_border(neighbour):
                for x in space:
                    global_free.add(x)
                return True
            if neighbour not in lava and neighbour not in space:
                space.add(neighbour)
                to_expand.append(neighbour)
    for x in space:
        global_space.add(x)
    return False


free_sides = 0
for cube in lava:
    x, y, z = cube
    for neighbour in [
            (x-1, y, z),
            (x+1, y, z),
            (x, y-1, z),
            (x, y+1, z),
            (x, y, z-1),
            (x, y, z+1)
    ]:
        if not free(neighbour):
            print(neighbour, free(neighbour))
        if neighbour not in lava and free(neighbour):
            free_sides += 1

print(free_sides)

print(free_sides)
