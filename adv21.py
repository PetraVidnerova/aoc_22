class Yell():
    def yell(self):
        pass


class NumberYell(Yell):
    def __init__(self, number):
        self.number = number

    def yell(self):
        return self.number


class OperationYell(Yell):
    def __init__(self, op1, operation, op2):
        self.op1 = op1
        self.op2 = op2
        self.operation = operation

    def yell(self):
        print("operation", self.operation)
        if self.operation == "+":
            return self.op1.yell() + self.op2.yell()
        if self.operation == "-":
            return self.op1.yell() - self.op2.yell()
        if self.operation == "*":
            return self.op1.yell() * self.op2.yell()
        if self.operation == "/":
            return self.op1.yell() / self.op2.yell()


monkey_dict = {}

with open("input21.txt") as f:
    for line in f:
        line = line.strip()
        name, value = line.split(":")
        monkey_dict[name] = value.strip()


print(monkey_dict)

# create tree


def create_tree(monkey):
    value = monkey_dict[monkey]

    try:
        intvalue = int(value)
    except:
        intvalue = None

    if intvalue is not None:
        return NumberYell(intvalue)

    op1, operation, op2 = value.split(" ")
    op1 = create_tree(op1)
    op2 = create_tree(op2)
    return OperationYell(op1, operation, op2)


tree = create_tree("root")
print(tree)
print(tree.yell())
