#Importing Dependencies
import numpy as np
import argparse
import sys
import random
import pulp

#Adding Arguments
parser = argparse.ArgumentParser(description="Script.")
parser.add_argument("--mdp", required=True, help="Path to the MDP file")

#Create a mutually exclusive group for --algorithm and --policy
group = parser.add_mutually_exclusive_group()
group.add_argument("--algorithm", help="hpi or lp")
group.add_argument("--policy", help="Path to the policy file")

#Parse arguments
args = parser.parse_args()

#Error Handling
#if args.algorithm and args.algorithm != "hpi" and  args.algorithm != "lp" :
#	print("Error: Incorrect algorithm provided. Choose between hpi and lp only", file=sys.stderr)
#	sys.exit(1)

# Print the file
#if args.mdp:
#	print("MDP file path: ", args.mdp)
#	if args.algorithm:
#		print("Algorithm: ", args.algorithm)
#	elif args.policy:
#		print("Policy file path: ", args.policy)



#creating the MDP object
def createMDP():
	M = {"S": 0, "A": 0, "T": 0, "R":0, "gamma": 0}

	with open(args.mdp, "r") as file:
		content = file.readlines()

	n = int(content[0].split()[1])
	k = int(content[1].split()[1])

	M["S"] = np.array(range(n))
	M["A"] = np.array(range(k))
	M["T"] = np.zeros((n,k,n))
	M["R"] = np.zeros((n,k,n))
	M["gamma"] = float(content[-1].split()[1])

	for line in content:
		tokens = line.split()
		if (tokens[0] == "transition"):
			M["T"][int(tokens[1]), int(tokens[2]), int(tokens[3])] = float(tokens[5])
			M["R"][int(tokens[1]), int(tokens[2]), int(tokens[3])] = float(tokens[4])

	return M


#creating the policy
def create_policy ():
	with open(args.policy, "r") as file:
		content = file.readlines()
	policy = [int(line) for line in content]
	return policy


#Creating the MDP Solver class
#Default Algorithm Used: Linear Programming
class MDPSolver:
	def __init__ (self, M, algo, arg_policy = 0):
		self.initialisation(M)

		if algo == "hpi":
			self.hpi()
		else:
			self.lp()

		if arg_policy:
			arg_policy = create_policy()
			Vpi = self.policy_evaluation(arg_policy)
			[print(f"{Vpi[s]: 0.6f} {arg_policy[s]}") for s in self.S]
		else:
			[print(f"{self.optimal_V[s]: 0.6f} {self.optimal_policy[s]}") for s in self.S]

	def initialisation (self, M):
		self.S = M["S"]
		self.A = M["A"]
		self.T = M["T"]
		self.R = M["R"]
		self.gamma = M["gamma"]

		self.n = len(self.S)
		self.k = len(self.A)

		self.optimal_V = np.zeros(self.n)
		self.optimal_policy = np.zeros(self.n)

	def policy_evaluation(self, policy):
		V = np.zeros(self.n)
		tolerance = 10 ** -6
		while (True):
			old_V = V.copy()
			V = np.array([sum([self.T[s,policy[s],s_dash] * (self.R[s,policy[s],s_dash] + self.gamma*V[s_dash]) for s_dash in self.S]) for s in self.S])
			error = np.max(np.abs(V - old_V))
			if (error < tolerance):
				break
		return V

	def value_iteration (self):
		V = np.zeros(self.n)
		Q = np.zeros((self.n, self.k))
		policy = [random.choice(self.A) for s in self.S]
		tolerance = 10 ** -6
		while True:
			old_V = V.copy()
			Q = np.array([[sum([self.T[s,a,s_dash] * (self.R[s,a,s_dash] + self.gamma*V[s_dash]) for s_dash in self.S]) for a in self.A] for s in self.S])
			V = np.max(Q, axis=1)
			error = np.max(abs(V - old_V))
			if (error < tolerance):
				break
		self.optimal_policy = np.argmax(Q, axis=1)
		self.optimal_V = V

	def hpi (self):
		V = np.zeros(self.n)
		Q = np.zeros((self.n, self.k))
		policy = [random.choice(self.A) for s in self.S]
		tolerance = 10 ** -6
		while True:
			V = self.policy_evaluation(policy)
			Q = np.array([[sum([self.T[s,a,s_dash] * (self.R[s,a,s_dash] + self.gamma * V[s_dash]) for s_dash in self.S]) for a in self.A] for s in self.S])
			if (np.max(np.max(Q, axis=1) - V) < tolerance):
				break
			else:
				policy = np.argmax(Q, axis=1)
		self.optimal_V = V
		self.optimal_policy = policy

	def lp (self):
		model = pulp.LpProblem("Maximize_Z", pulp.LpMaximize)
		V = [pulp.LpVariable(f"x_{i}") for i in range(self.n)]
		model += -1 * sum(V), "Objective"
		for s in self.S:
			for a in self.A:
				x = sum([self.T[s,a,s_dash] * (self.R[s,a,s_dash] + self.gamma * V[s_dash]) for s_dash in np.array(np.nonzero(self.T[s,a])[0])])
				model += x <= V[s]
		model.solve(pulp.PULP_CBC_CMD(msg=False))

		self.optimal_V = np.array([V[s].varValue for s in self.S])
		Q = np.array([[sum([self.T[s,a,s_dash] * (self.R[s,a,s_dash] + self.gamma*self.optimal_V[s_dash]) for s_dash in self.S]) for a in self.A] for s in self.S])
		self.optimal_policy = np.argmax(Q, axis=1)

#Creating Instances
M = createMDP()
MDPSolver(M, args.algorithm, args.policy)
