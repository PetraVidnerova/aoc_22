with open("input6.txt", "r") as f:
    input_ = f.read().strip()


for i in range(len(input_)-14):
    letters = input_[i:i+14]
    if len(letters) == len(set(letters)):
        break

print(i+14)
