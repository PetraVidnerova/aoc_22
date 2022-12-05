with open("input5.txt") as f:
    stacks = []
    moves = []
    is_stack = True
    for line in f:
        if line.strip():
            if is_stack:
                stacks.append(line)
            else:
                moves.append(line)
        else:
            is_stack = False

stacks = stacks[::-1]
stack_dict = {
    num: []
    for num in map(int, stacks[0].strip().split())
}

for line in stacks[1:]:
    for num, i in enumerate(range(0, len(line), 4)):
        if line[i+1:i+2].strip():
            stack_dict[num+1].append(line[i+1:i+2])


for line in moves:
    count = int(line[5:line.find("from")-1])
    source = int(line[line.find("from")+5:line.find("to")-1])
    dest = int(line[line.find("to")+3:])

    for _ in range(count):
        move = stack_dict[source].pop(-1)
        stack_dict[dest].append(move)

for st in stack_dict.values():
    print(st[-1], end="")

print()
