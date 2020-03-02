import random as rng

def main():
	# Generation parameters
	gridDimensions = (101, 101)
	numberOfGrids = 50


	for i in range(numberOfGrids):
		print("Generating gridworld #" + str(i+1) + "...")
		# Initialize grid
		grid = [x[:] for x in [[-1] * gridDimensions[1]] * gridDimensions[0]]     # -1 = unvisited, 0 = unblocked, 1 = blocked
		# Initialize path stack (for backtracking from dead-ends)
		pathStack = []
		# Select initial cell
		currentCell = (rng.randint(0, gridDimensions[0]-1), rng.randint(0, gridDimensions[1]-1))

		# Iterate until all cells are visited
		while (True):
			if (rng.random() < 0.15):
				grid[currentCell[1]][currentCell[0]] = 1		# blocked
				currentCell = find_unvisited_in_branch(pathStack, grid, gridDimensions)
				if (currentCell is None):
					currentCell = find_random_unvisited(grid, gridDimensions)                   # assign randomly an unvisited cell
				if (currentCell is None):
					break                                                     	# grid is completely visited
			else:
				grid[currentCell[1]][currentCell[0]] = 0		# unblocked
				pathStack.append(currentCell)
				currentCell = find_unvisited_neighbor(currentCell, grid, gridDimensions)
				if (currentCell is None):
					currentCell = find_unvisited_in_branch(pathStack, grid, gridDimensions)     # backtrack in path
				if (currentCell is None):
					currentCell = find_random_unvisited(grid, gridDimensions)                   # assign randomly an unvisited cell
				if (currentCell is None):
					break                                                     	# grid is completely visited
		# choose start and goal locations
		start = (rng.randint(0, gridDimensions[0]-1), rng.randint(0, gridDimensions[1]-1))
		grid[start[1]][start[0]] = 2
		goal = (rng.randint(0, gridDimensions[0]-1), rng.randint(0, gridDimensions[1]-1))
		while (grid[goal[1]][goal[0]] == 2):
			goal = (rng.randint(0, gridDimensions[0]-1), rng.randint(0, gridDimensions[1]-1))
		grid[goal[1]][goal[0]] = 3
		# output to file
		print("Outputting gridworld #" + str(i+1) + " to file...")
		name = "grid-" + str(i+1)
		export_grid_to_file(grid, name, start, goal)
	return


def find_unvisited_neighbor(cell, grid, dimensions):
	#print("")
	neighbors = [(cell[0]+1, cell[1]), (cell[0], cell[1]+1), (cell[0]-1, cell[1]), (cell[0], cell[1]-1)]
	#print(str(neighbors))
	legalNeighbors = []
	for nCell in neighbors:
		if ((nCell[0] >= 0) and (nCell[0] < dimensions[0]) and (nCell[1] >= 0) and (nCell[1] < dimensions[1])):
			legalNeighbors.append(nCell)
	#print(str(legalNeighbors))
	if (not legalNeighbors):
		return None
	rng.shuffle(legalNeighbors)
	#print(str(legalNeighbors))
	for nCell in legalNeighbors:
		#print(str(nCell) + " tested")
		if (grid[nCell[1]][nCell[0]] == -1):
			return nCell
	return None

def find_unvisited_in_branch(stack, grid, dimensions):
	if (not stack):
		return None         # return None if the path is completely explored
	cell = find_unvisited_neighbor(stack.pop(), grid, dimensions)
	if (cell is None):
		return find_unvisited_in_branch(stack, grid, dimensions)
	return cell

def find_random_unvisited(grid, dimensions):
	for y in range(dimensions[1]):
		for x in range(dimensions[0]):
			if (grid[y][x] == -1):
				return (x,y)
	return None

def export_grid_to_file(grid, filename, start, goal):
	file = open(filename, "w")
	for row in grid:
		line = ""
		for cell in row:
			line = line + str(cell)
		line = line + "\n"
		file.write(line)
	line = ":" + str(start[0]) + "," + str(start[1])
	file.write(line)
	line = ":" + str(goal[0]) + "," + str(goal[1])
	file.write(line)
	file.close()
	return

if __name__ == "__main__":
	main()