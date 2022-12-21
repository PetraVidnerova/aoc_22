class Yell():
    def yell(self):
        pass


class NumberYell(Yell):
    def __init__(self, number):
        self.number = number

    def yell(self):
        return self.number

    def known(self):
        return True

    def fit_value(self, value):
        raise ValueError("operation not allowed, it's list")


class UnknownValue(Yell):
    def known(self):
        return False

    def fit_value(self, value):
        return value


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

    def known(self):
        return self.op1.known() and self.op2.known()

    def fit_value(self, value):
        known1 = self.op1.known()
        known2 = self.op2.known()

        if not known1 and not known2:
            raise NotImplementedError

        if known1 and known2:
            raise ValueError("operation not allowed - both uknown")

        if known1:
            value1 = self.op1.yell()
            if self.operation == "+":
                return self.op2.fit_value(value - value1)
            if self.operation == "-":
                return self.op2.fit_value(value1-value)
            if self.operation == "*":
                return self.op2.fit_value(value/value1)
            if self.operation == "/":
                return self.op2.fit_value(value1/value)
        if known2:
            value2 = self.op2.yell()
            if self.operation == "+":
                return self.op1.fit_value(value - value2)
            if self.operation == "-":
                return self.op1.fit_value(value2+value)
            if self.operation == "*":
                return self.op1.fit_value(value/value2)
            if self.operation == "/":
                return self.op1.fit_value(value2*value)


monkey_dict = {}

with open("input21.txt") as f:
    for line in f:
        line = line.strip()
        name, value = line.split(":")
        monkey_dict[name] = value.strip()


print(monkey_dict)

# create tree


def create_tree(monkey):
    if monkey == "humn":
        return UnknownValue()

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


root = monkey_dict["root"]
left, _, right = root.split(" ")

left_tree = create_tree(left)
right_tree = create_tree(right)

if left_tree.known():
    print(right_tree.fit_value(left_tree.yell()))

if right_tree.known():
    print(left_tree.fit_value(right_tree.yell()))

print("Game over")
