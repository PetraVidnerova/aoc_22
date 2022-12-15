sensors = []
beacons = []

with open("input15.txt", "r") as f:
    for line in f:
        sensor, beacon = line.split(":")
        x = int(sensor[sensor.find("x=")+2:sensor.find(",")])
        y = int(sensor[sensor.find("y=")+2:])
        sensors.append((x, y))
        x = int(beacon[beacon.find("x=")+2:beacon.find(",")])
        y = int(beacon[beacon.find("y=")+2:])
        beacons.append((x, y))


def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


line = 2000000
empty_fields = set()

for sensor, beacon in zip(sensors, beacons):
    distance = manhattan(sensor, beacon)
    cursor = sensor[0]
    while manhattan((cursor, line), sensor) <= distance:
        if (cursor, line) != beacon:
            empty_fields.add(cursor)
        cursor += 1
    cursor = sensor[0]-1
    while manhattan((cursor, line), sensor) <= distance:
        if (cursor, line) != beacon:
            empty_fields.add(cursor)
        cursor -= 1

print(len(empty_fields))
