def mysplit(inner_string):
    start = 0
    end = 0
    members = []
    while start < len(inner_string):
        if inner_string[start] == "[":
            bracket = 1
            while bracket > 0:
                end += 1
                if inner_string[end] == "[":
                    bracket += 1
                if inner_string[end] == "]":
                    bracket -= 1
            end += 1
        else:
            while end < len(inner_string) and inner_string[end] != ",":
                end += 1
        members.append(inner_string[start:end])
        end += 1
        start = end
    return members


def convert(line):
    line = line.strip()
    if line[0] == "[" and line[-1] == "]":
        members = mysplit(line[1:-1])
        result = []
        for m in members:
            result.append(convert(m))
        return result
    else:
        return int(line)


def compare(left, right):
    # both ints
    if type(left) == int and type(right) == int:
        if left == right:
            return 0
        elif left < right:
            return -1
        else:
            return 1

    if type(left) == int:
        left = [left]
    if type(right) == int:
        right = [right]

    # both lists
    if len(left) == 0 and len(right) == 0:
        return 0
    elif len(left) == 0:
        return -1
    elif len(right) == 0:
        return 1
    else:
        result = compare(left[0], right[0])
        if result == 0:
            return compare(left[1:], right[1:])
        else:
            return result


score = 0
with open("input13.txt") as f:
    is_left = True
    index = 1
    lines = f.readlines() + [""]
    for line in lines:
        line = line.strip()
        if line:
            if is_left:
                left = convert(line)
                is_left = False
            else:
                right = convert(line)
                is_left = True
        else:  # empty line
            if compare(left, right) < 0:
                score += index
            index += 1

print(score)
