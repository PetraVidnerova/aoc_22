sum_ = 0
highest = [0, 0, 0]

with open("input1.txt", "r") as f:
    for line in f:
        if not line.strip():
            highest.append(sum_)
            highest = sorted(highest, reverse=True)[:3]
            sum_ = 0
        else:
            sum_ += int(line)

print(highest)
print(sum(highest))
