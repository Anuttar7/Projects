#Importing dependencies
import numpy as np
import argparse

#Adding the --gridworld argument
parser = argparse.ArgumentParser(description="Encoder")
parser.add_argument("--gridworld", required=True, help="File path to gridworld")
args = parser.parse_args()

with open(args.gridworld, "r") as file:
	grid = file.readlines()

grid = [grid[i].replace(" ", "") for i in range(len(grid))]
grid = [grid[i].replace("\n","") for i in range(len(grid))]


# Actions:		Directions:	Key State:		State Definition:
# 0: Move Forward	0: Up	 ^	k = 0:  Agent does	S := (i,j,d,k), where
# 1: Left Turn		1: Left  <		not have key	i: row number
# 2: Right Turn		2: Down	 v	k = 1:  Agent owns	j: column number
# 3: Turn Around	3: Right >		key		d: direction
#								k: has key or not


#Initialisations
m = len(grid)				#Number of rows in gridworld
n = len(grid[0])			#Number of columns in gridworld
numActions = 4				#Number of Actions
numDirections = 4			#Number of Directions
numStates = m * n * numDirections * 2	#Number of States

gamma = 1				#Discount Factor
R = -1 * np.ones((numStates, numActions, numStates))	#Reward Function (-1 for all states)
T = np.zeros((numStates, numActions, numStates))	#State Transition Probability Function


#Function for mapping state to a natural number (called state number)
def s_map (i, j, d, k):
	return 2*(numDirections*(n*i + j) + d) + k

map_ = {}
numValidStates = 0
for i in range(m):
	for j in range(n):
		for d in range(numDirections):
			for k in range(2):
				if (grid[i][j] == "W" or (grid[i][j] == "d" and k == 0)):
					continue
				map_[(i,j,d,k)] = numValidStates
				numValidStates += 1

#Creating State Transition Probability Function
#Transition from s -> s' s.t.:
#> s is not goal cell (so no transition from termial state)
#> s, s' are not Wall or door cell without key (so no transition from or to a wall)

for i in range(1, m-1):
	for j in range(1, n-1):
		if (grid[i][j] == "W" or grid[i][j] == "g"):
			continue
		for d in range(numDirections):
			for k in [0,1]:
				if (grid[i][j] == "d" and k == 0):
					continue

				# a = 0
				if d == 0:		#Facing Up
					if (grid[i-1][j] == "W" or (grid[i-1][j] == "d" and k == 0)):
						T[s_map(i,j,d,k), 0, s_map(i,j,d,k)] = 1
					elif (grid[i-2][j] == "W" or (grid[i-2][j] == "d" and k == 0)):
						if (k == 0 and grid[i-1][j] == "k"):
							T[s_map(i,j,d,0), 0, s_map(i-1,j,d,1)] = 1
						else:
							T[s_map(i,j,d,k), 0, s_map(i-1,j,d,k)] = 1
					elif (grid[i-3][j] == "W" or (grid[i-3][j] == "d" and k == 0)):
						if (k == 0 and grid[i-1][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i-1,j,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i-1,j,d,k)] = 0.5

						if (k == 0 and grid[i-2][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i-2,j,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i-2,j,d,k)] = 0.5
					else:
						if (k == 0 and grid[i-1][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i-1,j,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i-1,j,d,k)] = 0.5

						if (k == 0 and grid[i-2][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i-2,j,d,1)] = 0.3
						else:
							T[s_map(i,j,d,k), 0, s_map(i-2,j,d,k)] = 0.3

						if (k == 0 and grid[i-3][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i-3,j,d,1)] = 0.2
						else:
							T[s_map(i,j,d,k), 0, s_map(i-3,j,d,k)] = 0.2
				elif (d == 1):			#Facing Left
					if (grid[i][j-1] == "W" or (grid[i][j-1] == "d" and k == 0)):
						T[s_map(i,j,d,k), 0, s_map(i,j,d,k)] = 1
					elif (grid[i][j-2] == "W" or (grid[i][j-2] == "d" and k == 0)):
						if (k == 0 and grid[i][j-1] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j-1,d,1)] = 1
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j-1,d,k)] = 1
					elif (grid[i][j-3] == "W" or (grid[i][j-3] == "d" and k == 0)):
						if (k == 0 and grid[i][j-1] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j-1,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j-1,d,k)] = 0.5

						if (k == 0 and grid[i][j-2] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j-2,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j-2,d,k)] = 0.5
					else:
						if (k == 0 and grid[i][j-1] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j-1,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j-1,d,k)] = 0.5

						if (k == 0 and grid[i][j-2] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j-2,d,1)] = 0.3
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j-2,d,k)] = 0.3

						if (k == 0 and grid[i][j-3] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j-3,d,1)] = 0.2
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j-3,d,k)] = 0.2
				elif (d == 2):		#Facing Down
					if (grid[i+1][j] == "W" or (grid[i+1][j] == "d" and k == 0)):
						T[s_map(i,j,d,k), 0, s_map(i,j,d,k)] = 1
					elif (grid[i+2][j] == "W" or (grid[i+2][j] == "d" and k == 0)):
						if (k == 0 and grid[i+1][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i+1,j,d,1)] = 1
						else:
							T[s_map(i,j,d,k), 0, s_map(i+1,j,d,k)] = 1
					elif (grid[i+3][j] == "W" or (grid[i+3][j] == "d" and k == 0)):
						if (k == 0 and grid[i+1][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i+1,j,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i+1,j,d,k)] = 0.5

						if (k == 0 and grid[i+2][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i+2,j,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i+2,j,d,k)] = 0.5
					else:
						if (k == 0 and grid[i+1][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i+1,j,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i+1,j,d,k)] = 0.5

						if (k == 0 and grid[i+2][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i+2,j,d,1)] = 0.3
						else:
							T[s_map(i,j,d,k), 0, s_map(i+2,j,d,k)] = 0.3

						if (k == 0 and grid[i+3][j] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i+3,j,d,1)] = 0.2
						else:
							T[s_map(i,j,d,k), 0, s_map(i+3,j,d,k)] = 0.2
				elif (d == 3):		#Facing Right
					if (grid[i][j+1] == "W" or (grid[i][j+1] == "d" and k == 0)):
						T[s_map(i,j,d,k), 0, s_map(i,j,d,k)] = 1
					elif (grid[i][j+2] == "W" or (grid[i][j+2] == "d" and k == 0)):
						if (k == 0 and grid[i][j+1] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j+1,d,1)] = 1
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j+1,d,k)] = 1
					elif (grid[i][j+3] == "W" or (grid[i][j+3] == "d" and k == 0)):
						if (k == 0 and grid[i][j+1] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j+1,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j+1,d,k)] = 0.5

						if (k == 0 and grid[i][j+2] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j+2,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j+2,d,k)] = 0.5
					else:
						if (k == 0 and grid[i][j+1] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j+1,d,1)] = 0.5
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j+1,d,k)] = 0.5

						if (k == 0 and grid[i][j+2] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j+2,d,1)] = 0.3
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j+2,d,k)] = 0.3

						if (k == 0 and grid[i][j+3] == "k"):
							T[s_map(i,j,d,k), 0, s_map(i,j+3,d,1)] = 0.2
						else:
							T[s_map(i,j,d,k), 0, s_map(i,j+3,d,k)] = 0.2

				# a = 1
				T[s_map(i,j,d,k), 1, s_map(i,j,(d+1)%4,k)] = 0.9
				T[s_map(i,j,d,k), 1, s_map(i,j,(d+2)%4,k)] = 0.1

				# a = 2
				T[s_map(i,j,d,k), 2, s_map(i,j,(d+3)%4,k)] = 0.9
				T[s_map(i,j,d,k), 2, s_map(i,j,(d+2)%4,k)] = 0.1

				# a = 3
				T[s_map(i,j,d,k), 3, s_map(i,j,(d+1)%4,k)] = 0.1
				T[s_map(i,j,d,k), 3, s_map(i,j,(d+2)%4,k)] = 0.8
				T[s_map(i,j,d,k), 3, s_map(i,j,(d+3)%4,k)] = 0.1


#Printing Output
print(f"numStates {numValidStates}")
print(f"numActions {numActions}")
print(f"end somewhere idk")
[[[[[[[[[(not (grid[i][j] == "W" or (grid[i][j] == "d" and k == 0) or grid[i1][j1] == "W" or (grid[i1][j1] == "d" and k1 == 0))) and (T[s_map(i,j,d,k),a,s_map(i1,j1,d1,k1)] > 0) and print(f"transition {map_[(i,j,d,k)]} {a} {map_[(i1,j1,d1,k1)]} -1 {T[s_map(i,j,d,k), a, s_map(i1,j1,d1,k1)]}") for k1 in range(2)] for d1 in range(4)] for j1 in range(n)] for i1 in range(m)] for a in range(numActions)] for k in range(2)] for d in range(4)] for j in range(n)] for i in range(m)]
print(f"mdptype episodic")
print(f"discount {gamma}")

