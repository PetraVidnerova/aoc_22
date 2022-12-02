draws = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
}

rewards = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}

to_win = {
    "rock": "paper",
    "paper": "scissors",
    "scissors": "rock"
}

to_loose = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}


score = 0
with open("input2.txt", "r") as f:
    for line in f:
        opponent, player = line.strip().split()
        opponent = draws[opponent]
        if player == "X":  # to loose
            draw = to_loose[opponent]
            score += rewards[draw]
        elif player == "Y":  # draw
            score += rewards[opponent]
            score += 3
        elif player == "Z":
            draw = to_win[opponent]
            score += rewards[draw]
            score += 6

print(score)
