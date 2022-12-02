draws = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors"
}

rewards = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}


score = 0
with open("input2.txt", "r") as f:
    for line in f:
        opponent, player = line.strip().split()
        opponent = draws[opponent]
        player = draws[player]
        score += rewards[player]
        if player == opponent:
            score += 3
        elif (player, opponent) in (
                ("rock", "scissors"),
                ("paper", "rock"),
                ("scissors", "paper")
        ):
            score += 6

print(score)
