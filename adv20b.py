original = []
key = 811589153

with open("input20.txt", "r") as f:
    for line in f:
        original.append(int(line)*key)

print(original)


def mix(message, x):
    print("moving ", x)
    if x[1] == 0:
        return
    i = message.index(x)
    del message[i]

    i = i + x[1]
    message.insert(i % len(message), x)


original = list(enumerate(original))
message = original.copy()


for round in range(10):
    for x in original:
        mix(message, x)
    print(message)

i = 0
while message[i][1] != 0:
    i += 1

sum_ = 0
for x in i+1000, i+2000, i+3000:
    print(message[x % len(message)][1])
    sum_ += message[x % len(message)][1]

print(sum_)
