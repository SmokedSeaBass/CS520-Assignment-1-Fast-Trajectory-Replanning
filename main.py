import random as rng
import math
import time
import statistics as stat

openList = []
closedList = []
counter = 0
knownWorld = []
timeStart = -1
timeFinish = -1

class Node:
	def __init__(self, h, state, pos):
		self.g = math.inf
		self.h = h
		self.f = self.g + self.h
		self.state = state
		self.search = 0
		self.xPos = pos[0]
		self.yPos = pos[1]
		self.pointer = None
	def __str__(self):
		return "Node (" + str(self.xPos) + ", " + str(self.yPos) + "): f = " + str(self.g) + "+" + str(self.h) + " = " + str(self.f)
	def __repr__(self):
			return "Node (" + str(self.xPos) + ", " + str(self.yPos) + "): f = " + str(self.g) + "+" + str(self.h) + " = " + str(self.f)

def main():
	basename = "grid-"
	times = []
	for i in range(1, 51):
		# print("Solving grid-" + str(i))
		timeStart = time.time()
		solve_grid(basename + str(i))
		times.append(time.time() - timeStart)
	# solve_grid("grid-easy")
	print("Average runtime: %s seconds" % (stat.mean(times)))
	return


def solve_grid(gridname):
	counter = 0
	data = import_grid(gridname)
	grid = data[0]
	startCell = data[1]
	goalCell = data[2]
	size = len(grid)
	graph = generate_graph(grid, startCell, goalCell)
	for i in range(size):									# TODO: make dynamic
		row = []
		for j in range(size):
			row.append(0)										# assume world to be unblocked
		knownWorld.append(row)
	while (startCell != goalCell):
		counter = counter + 1
		# print("counter: " + str(counter))

		startNode = graph[startCell[1]][startCell[0]]
		startNode.g = 0
		startNode.search = counter
		startNode.f = startNode.g + startNode.h
		startNode.pointer = None
		graph[startCell[1]][startCell[0]] = startNode
		# print("Start: " + str(startNode))

		goalNode = graph[goalCell[1]][goalCell[0]]
		goalNode.g = math.inf
		goalNode.search = counter
		goalNode.f = goalNode.g + goalNode.h
		graph[goalCell[1]][goalCell[0]] = goalNode
		# print("Goal: " + str(goalNode))

		openList.clear()
		closedList.clear()
		openList.append(tuple(startCell))		# add starting node to open list
		compute_path(goalCell, graph)
		if (not openList):
			# print("I cannot reach the target!")
			return
		pathTracer = graph[goalCell[1]][goalCell[0]]
		path = []
		while (pathTracer.pointer is not None):
			path.append(pathTracer)
			pathTracer = graph[pathTracer.pointer[1]][pathTracer.pointer[0]]
		path.reverse()
		for step in path:
			if (step.state == 1):		# blocked, prepare for new A*
				break
			for action in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
				if (step.xPos + action[0] >= 0 and step.xPos + action[0] < size
				and step.yPos + action[1] >= 0 and step.yPos + action[1] < size):
					knownWorld[step.yPos + action[1]][step.xPos + action[0]] = graph[step.yPos + action[1]][step.xPos + action[0]].state			# update known world
			startCell[0] = step.xPos	# move agent
			startCell[1] = step.yPos
	# print("I reached the target!")
	return

def compute_path(goal, graph):
	while (openList):
		currNode = minimum_f(openList, graph)
		if (graph[goal[1]][goal[0]].g <= currNode.f):
			break
		#print("examining " + str(currNode))
		openList.remove((currNode.xPos, currNode.yPos))
		closedList.append((currNode.xPos, currNode.yPos))
		legalActions = []
		for action in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
			if (currNode.xPos + action[0] >= 0 and currNode.xPos + action[0] < len(graph) 
			and currNode.yPos + action[1] >= 0 and currNode.yPos + action[1] < len(graph)
			and (currNode.xPos + action[0], currNode.yPos + action[1]) not in closedList):		# TODO: use dynamic limits
				legalActions.append(action)
		for action in legalActions:
			succ = graph[currNode.yPos + action[1]][currNode.xPos + action[0]]
			if ((succ.xPos, succ.yPos) in closedList or knownWorld[succ.yPos][succ.xPos] == 1):
				continue
			actionCost = getCost(currNode, succ, knownWorld)
			if (succ.search < counter):
				succ.g = math.inf
				succ.search = counter
			if (succ.g > currNode.g + actionCost):			# cost of any action is one
				succ.g = currNode.g + actionCost
				succ.pointer = (currNode.xPos, currNode.yPos)
				if ((succ.xPos, succ.yPos) in openList):
					openList.remove((succ.xPos, succ.yPos))
				succ.f = succ.g + heuristic((succ.xPos, succ.yPos), goal)
				openList.append((succ.xPos, succ.yPos))
			graph[succ.yPos][succ.xPos] = succ
	return

def minimum_f(nodeList, graph):
	if (not nodeList):
		return None
	minF = math.inf
	extremeG = math.inf		# -inf for choosing bigger g, +inf for choosing smaller g
	minNode = None
	for pos in nodeList:
		node = graph[pos[1]][pos[0]]
		if (node.h + node.g < minF or
		(node.h + node.g == minF and node.g < extremeG)):		# ">" for choosing larger G, "<" for choosing smaller G
			minF = node.h + node.g
			extremeG = node.g
			minNode = node
	if (minNode is None):
		print(nodeList)
	return minNode

def getCost(start, end, knownWorld):
	if (knownWorld[end.yPos][end.xPos] == 1):
		return math.inf
	return 1

def heuristic(startPos, finishPos):
	xDist = abs(finishPos[0] - startPos[0])
	yDist = abs(finishPos[1] - startPos[1])
	return xDist + yDist

def generate_graph(grid, start, goal):
	graph = []
	for y in range(len(grid)):        # TODO: make dynamic
		row = []
		for x in range(len(grid)):    # TODO: make dynamic
			node = Node(heuristic((x, y), goal), grid[y][x], (x, y))
			row.append(node)
		graph.append(row)
	return graph

def import_grid(filename):
	file = open(filename, "r")
	grid = []
	for line in file:
		if (line[0] == ":"):
			cells = line.split(":")
			start = list(map(int, cells[1].split(",")))
			goal = list(map(int, cells[2].split(",")))
			# print("start: " + str(start))
			# print("goal: " + str(goal))
			break
		row = []
		for i in range(len(line) - 1):
			s = line[i]
			row.append(int(s))
		grid.append(row)
	return (grid, start, goal)

if __name__ == "__main__":
	main()