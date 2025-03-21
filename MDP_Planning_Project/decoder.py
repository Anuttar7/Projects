#Importing dependencies
import numpy as np
import subprocess
import argparse

parser = argparse.ArgumentParser(description="Decoder")
parser.add_argument("--mdp", required=True, help="Path to MDP file; give encoder.py here")
parser.add_argument("--value-policy", required=True, help="Optimal Policy; give planner.py here")
parser.add_argument("--gridworld", required=True, help="Path to gridworld file")
args = parser.parse_args()

with open(args.gridworld, "r") as file:
	test_file = file.readlines()

with open(args.value_policy, "r") as file:
	pol_file = file.readlines()

pol = [int(pol_file[i].split()[1]) for i in range(len(pol_file))]
val = [float(pol_file[i].split()[0]) for i in range(len(pol_file))]

grids = []
x = []
for line in test_file:
	if line == "Testcase\n":
		grids.append(x)
		x = []
	else:
		x.append(line)
grids.append(x)
del grids[0]
grids = [[grids[i][j].replace(" ", "") for j in range(len(grids[i]))] for i in range(len(grids))]
grids = [[grids[i][j].replace("\n", "") for j in range(len(grids[i]))] for i in range(len(grids))]


for q in range(len(grids)):
	m = len(grids[q])
	n = len(grids[q][0])
	map_ = {}
	temp = 0
	for i in range(m):
		for j in range(n):
			for d in range(4):
				for k in range(2):
					if not (grids[q][i][j] == "W" or grids[q][i][j] == "d" and k == 0):
						map_[(i,j,d,k)] = temp
						temp += 1

	i1 = -1
	j1 = -1
	d  = -1
	k  =  1
	for i in range(m):
		for j in range(n):
			if grids[q][i][j] == "v":
				i1 = i
				j1 = j
				d  = 2
			elif grids[q][i][j] == "<":
				i1 = i
				j1 = j
				d  = 1
			elif grids[q][i][j] == "^":
				i1 = i
				j1 = j
				d  = 0
			elif grids[q][i][j] == ">":
				i1 = i
				j1 = j
				d  = 3
			elif grids[q][i][j] == "k":
				k  = 0

	print(f"{pol[map_[(i1,j1,d,k)]]}")
