sum = 0

with open("input3.txt") as f:
    lines = [
        line
        for line in f.read().split("\n")
        if line
    ]
    for i in range(0, len(lines), 3):
        a, b, c = set(lines[i]), set(lines[i+1]), set(lines[i+2])
        key = a.intersection(b).intersection(c)
        for k in key:
            if k.islower():
                sum += ord(k) - ord('a') + 1
            elif k.isupper():
                sum += ord(k) - ord('A') + 27

print(sum)
