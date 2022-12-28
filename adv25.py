translate = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2
}

snafu = {
    2: "2",
    1: "1",
    0: "0",
    -1: "-",
    -2: "="
}


def translate_number(snafu):
    sum_ = 0
    for i, digit in enumerate(reversed(snafu)):
        sum_ += translate[digit] * 5**i
    return sum_


def translate_back(number):
    result = ""
    while number:
        rest = number % 5
        if rest in (0, 1, 2):
            result += snafu[rest]
            number = number // 5
        else:
            diff = 5 - rest
            result += snafu[-diff]
            number = (number // 5) + 1
    return result[::-1]


with open("input25.txt") as f:
    result = 0
    for line in f:
        result += translate_number(line.strip())

print(result)
print(translate_back(result))
