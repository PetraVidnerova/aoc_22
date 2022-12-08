import numpy as np

with open("input8.txt", "r") as f:
    grid = []
    for line in f:
        line = line.strip()
        grid.append(list(map(int, line)))

grid = np.array(grid, dtype=int)

height, width = grid.shape

score = np.ones_like(grid)

for i in range(height):
    for j in range(width):
        value = grid[i, j]
        # top
        index = i
        while True:
            if index == 0:
                break
            index -= 1
            if grid[index, j] >= value:
                break
        score[i, j] *= (i - index)
        #  down
        index = i
        while True:
            if index == height-1:
                break
            index += 1
            if grid[index, j] >= value:
                break
        score[i, j] *= (index - i)
        #  left
        index = j
        while True:
            if index == 0:
                break
            index -= 1
            if grid[i, index] >= value:
                break
        score[i, j] *= (j - index)
        # right
        index = j
        while True:
            if index == width - 1:
                break
            index += 1
            if grid[i, index] >= value:
                break
        score[i, j] *= (index - j)

print(score.max().max())
