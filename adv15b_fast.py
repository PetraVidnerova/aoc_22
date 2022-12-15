import numpy as np

sensors = []
beacons = []

maxx = 4000000
maxy = 4000000

# maxx = 20
# maxy = 20

with open("input15.txt", "r") as f:
    for line in f:
        sensor, beacon = line.split(":")
        x = int(sensor[sensor.find("x=")+2:sensor.find(",")])
        y = int(sensor[sensor.find("y=")+2:])
        sensors.append((x, y))
        x = int(beacon[beacon.find("x=")+2:beacon.find(",")])
        y = int(beacon[beacon.find("y=")+2:])
        beacons.append((x, y))

sensors = np.array(sensors)
beacons = np.array(beacons)


def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


distances = np.abs(sensors[:, 0]-beacons[:, 0]) + \
    np.abs(sensors[:, 1]-beacons[:, 1])


class Intervals():
    def __init__(self):
        self.parts = []

    def is_member(self, low, high):
        for p in parts:
            if low >= p[0] and high <= p[1]:
                return True
        return False

    def covers(self):
        if len(self.parts) == 1:
            return False  # assume it is not on border
        if len(self.parts) > 2 or len(self.parts) == 0:
            raise ValueError("something wrong", len(self.parts))
        return True

    def value(self):
        return self.parts[0][1]+1

    def add(self, low, high):
        low_inside = False
        high_inside = False
        low_i = -1
        high_i = -1
        for i, p in enumerate(self.parts):
            if low < p[0]:
                low_inside = False
                low_i = i
                break
            elif low <= p[1]+1:
                low_inside = True
                low_i = i
                break
        for i, p in enumerate(self.parts):
            if high < p[0]-1:
                high_inside = False
                high_i = i
                break
            elif high <= p[1]:
                high_inside = True
                high_i = i
                break
        if low_i == -1:
            self.parts.append((low, high))
            return
        if high_i == -1:
            high_i = len(self.parts)
        if low_inside and high_inside and low_i == high_i:
            return
        if not low_inside and not high_inside:
            self.parts.insert(low_i, (low, high))
            return
        low = min(low, self.parts[low_i][0])
        if high_inside:
            high = self.parts[high_i][1]
        new_parts = [
            p
            for p in self.parts
            if p[1] < low
        ]
        new_parts.append((low, high))
        new_parts += [
            p
            for p in self.parts
            if p[0] > high
        ]
        self.parts = new_parts


def inspect_line(linenum):
    line = Intervals()

    ldist = distances - np.abs(sensors[:, 0]-linenum)

    close = (ldist >= 0).nonzero()[0]

    for c in close:
        s, d = sensors[c], distances[c]
        r = ldist[c]
        start = max(0, s[1]-r)
        end = min(maxy, s[1]+r)
        line.add(start, end)

    if line.covers():
        return line.value()
    return -1


for line in range(0, maxx+1):
    if line % 10000 == 0:
        print("line ", line)
    idx = inspect_line(line)
    if idx != -1:
        print(line*4000000+idx)
        break
