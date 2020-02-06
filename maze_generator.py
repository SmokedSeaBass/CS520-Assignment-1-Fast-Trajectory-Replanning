import random as rng

def main():
    gridDimensions = (101, 101)
    numberOfGrids = 50
    grid = [x[:] for x in [[-1] * gridDimensions[1]] * gridDimensions[0]]     # -1 = unvisited, 0 = unblocked, 1 = blocked
    pathStack = []
    currentCell = (rng.randint(0, gridDimensions[0]), rng.randint(0, gridDimensions[1]))
    if (rng.random() >= 0.3):
        grid[currentCell[1]][currentCell[0]] = 1
    else:
        grid[currentCell[1]][currentCell[0]] = 0
        pathStack.append(currentCell)


def find_unvisited_neighbor(cell, grid):
    for nCell in [(cell[0]+1, cell[1]), (cell[0], cell[1]+1), (cell[0]-1, cell[1]), (cell[0], cell[1]-1)]:
        if (grid[nCell[1]][nCell[0]] == -1):
            return nCell

if __name__ == "__main__":
    main()