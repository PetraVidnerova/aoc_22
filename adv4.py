count = 0

with open("input4.txt") as f:
    for line in f:
        first, second = line.strip().split(",")
        first_low, first_high = map(int, first.split("-"))
        second_low, second_high = map(int, second.split("-"))

        if first_low <= second_low and first_high >= second_high:
            count += 1
        elif second_low <= first_low and second_high >= first_high:
            count += 1


print(count)
