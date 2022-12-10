X = 1
cycle = 0

result = {
    cycle: None
    for cycle in (20, 60, 100, 140, 180, 220)
}


def update_result(cycle, X):
    global result

    if cycle in result.keys():
        result[cycle] = cycle * X


def process_line(line):
    global cycle, X

    cycle += 1
    update_result(cycle, X)
    if line.startswith("addx"):
        cycle += 1
        update_result(cycle, X)
        _, number = line.split()
        X += int(number)


with open("input10.txt", "r") as f:
    for line in f:
        process_line(line.strip())

print(sum(result.values()))
