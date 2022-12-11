class Monkey:
    def __init__(self, items, operator, operand, test, true_monkey, false_monkey):
        self.items = items
        # operation
        self.operator = operator
        self.operand = operand

        self.test = test
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey

        self.inspect_count = 0
        self.factor = 1

    def recieve(self, item):
        self.items.append(item)

    def evaluate(self, value):
        other = self.operand if self.operand is not None else value
        if self.operator == "+":
            return value + other
        if self.operator == "-":
            return value - other
        if self.operator == "*":
            return value * other
        if self.operator == "/":  # should not be used
            return int(value / other)
        raise ValueError(f"Unknown operator {self.operator}")

    def process(self, monkeys):
        for item in self.items:
            self.inspect_count += 1
            item = self.evaluate(item)
            item = item % self.factor
            # item = int(item/3)
            if item % self.test == 0:
                monkeys[self.true_monkey].recieve(item)
            else:
                monkeys[self.false_monkey].recieve(item)
        self.items = []


monkeys = []

with open("input11.txt", "r") as f:
    lines = f.readlines() + [""]  # to force the append of the last monkey
    for line in lines:
        line = line.strip()
        if line.startswith("Monkey"):
            continue
        if line.startswith("Starting items:"):
            item_list = line.split(":")[-1]
            items = list(map(int, item_list.split(",")))
            continue
        if line.startswith("Operation:"):
            equation = line.split(":")[-1].strip()
            _, _, _, operator, operand = equation.split()
            try:
                operand = int(operand)
            except:
                operand = None
        if line.startswith("Test:"):
            test = int(line.split()[-1])
            continue
        if line.startswith("If true:"):
            true_monkey = int(line.split()[-1])
            continue
        if line.startswith("If false:"):
            false_monkey = int(line.split()[-1])
            continue

        if not line:
            monk = Monkey(
                items,
                operator, operand,
                test,
                true_monkey, false_monkey
            )
            monkeys.append(monk)

factor = 1
for monk in monkeys:
    factor *= monk.test

for monk in monkeys:
    monk.factor = factor

for r in range(10000):
    print("Round", r)
    for monk in monkeys:
        monk.process(monkeys)

    # for i, monk in enumerate(monkeys):
    #     print(f"Monk {i}: {monk.items}")


result = sorted([
    monk.inspect_count
    for monk in monkeys
])[-2:]

print(result[0]*result[1])
