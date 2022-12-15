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


distances = np.abs(sensors[:,0]-beacons[:,0]) + np.abs(sensors[:,1]-beacons[:,1])



line_buffer = np.empty(maxy+1, dtype=bool)

def inspect_line(linenum):
    line = line_buffer
    line.fill(True)

    ldist = distances - np.abs(sensors[:, 0]-linenum)

    close = (ldist>=0).nonzero()[0]

    for c in close:
        s, d = sensors[c], distances[c]
        r = ldist[c]
        start = max(0, s[1]-r)
        end = min(maxy, s[1]+r)
        line[start:end+1] = False
    if np.sum(line) > 0:
        return line.nonzero()[0][0]
    return -1

    
for line in range(0, maxx+1):
    if line % 1000 == 0:
        print("line ", line)
    idx = inspect_line(line)
    if idx != -1:
        print(line*4000000+idx)
        break
