import numpy as np

with open("input8.txt", "r") as f:
    grid = []
    for line in f:
        line = line.strip()
        grid.append(list(map(int, line)))

grid = np.array(grid, dtype=int)

height, width = grid.shape

visible_trees = 0

for i in range(height):
    for j in range(width):
        value = grid[i, j]
        visible = (
            np.all(grid[:i, j] < value) +
            np.all(grid[i+1:, j] < value) +
            np.all(grid[i, :j] < value) +
            np.all(grid[i, j+1:] < value)
        )
        if visible:
            visible_trees += 1

print(visible_trees)
