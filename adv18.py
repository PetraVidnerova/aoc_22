lava = set()

with open("input18.txt", "r") as f:
    for line in f:
        lava.add(
            tuple(
                map(int, line.split(","))
            )
        )

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
        if neighbour not in lava:
            free_sides += 1

print(free_sides)
