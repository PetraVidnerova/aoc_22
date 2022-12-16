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
        self.clip()
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
            if low_i == -1:
                if low_i == -1 and low < p[0]:
                    low_inside = False
                    low_i = i
                elif low_i == -1 and low <= p[1]+1:
                    low_inside = True
                    low_i = i
            if high_i == -1:
                if high < p[0]-1:
                    high_inside = False
                    high_i = i
                elif high <= p[1]:
                    high_inside = True
                    high_i = i
            if low_i != -1 and high_i != -1:
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

        self.parts.insert(low_i, (low, high))
        i = low_i+1
        while i < len(self.parts) and self.parts[i][1] <= high:
            del self.parts[i]

    def clip(self):
        if not self.parts:
            return
        i = 0
        while True:
            if self.parts[i][1] < 0:
                del self.parts[i]
                continue
            if self.parts[i][0] < 0:
                self.parts[i] = (0, self.parts[i][1])
            break
        i = -1
        while True:
            if self.parts[i][0] > maxx:
                del self.parts[i]
                continue
            if self.parts[i][1] > maxx:
                self.parts[i] = (self.parts[i][0], maxx)
            break


def inspect_line(linenum):
    line = Intervals()

    ldist = distances - np.abs(sensors[:, 0]-linenum)

    close = (ldist >= 0).nonzero()[0]

    for c in close:
        s, d = sensors[c], distances[c]
        r = ldist[c]
        # start = max(0, s[1]-r)
        # end = min(maxy, s[1]+r)
        # line.add(start, end)
        line.add(s[1]-r, s[1]+r)

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
