sum = 0

with open("input3.txt") as f:
    for line in f:
        line = line.strip()
        length = len(line)
        first = set(line[:length//2])
        second = set(line[length//2:])
        key = first.intersection(second)
        for k in key:
            if k.islower():
                sum += ord(k) - ord('a') + 1
            elif k.isupper():
                sum += ord(k) - ord('A') + 27

print(sum)
