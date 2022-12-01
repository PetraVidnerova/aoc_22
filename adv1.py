with open("input1.txt", "r") as f:
    sum_ = 0
    highest = 0
    for line in f:
        if not line.strip():
            if sum_ > highest:
                highest = sum_
            sum_ = 0
        else:
            sum_ += int(line)

print(highest)
