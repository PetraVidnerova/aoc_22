with open("input6.txt", "r") as f:
    input_ = f.read().strip()


for i in range(len(input_)-4):
    letters = input_[i:i+4]
    if len(letters) == len(set(letters)):
        break

print(i+4)
