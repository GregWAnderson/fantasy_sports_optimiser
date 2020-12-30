import urllib, json
import pandas as pd
import re
from itertools import permutations

from pulp import *

def merge_data():
	# read data
	player_points = pd.read_csv('../data/player_points.csv')
	player_costs = pd.read_csv('../data/player_costs.csv')

	player_costs = player_costs.groupby(['player_name']).mean()

	# join data
	player_df = player_points.merge(player_costs, on = 'player_name')

	# keep only necessary fields
	player_df = player_df[['position', 'player_name', 'player_cost', 'total_points']]

	# drop na's as this will effect the optimiser
	player_df = player_df.dropna()

	return(player_df)

def optimise(df, salary = 200, player_positions = {
		"PG": 2,
		"SG": 2,
		"SF": 2,
		"PF": 2,
		"C": 1,
	}):
	# set variables
	SALARY_CAP = salary

	pos_num_available = player_positions


	salaries = {}
	points = {}
	for pos in df.position.unique():
		available_pos = df[df.position == pos]
		salary = list(available_pos[["player_name","player_cost"]].set_index("player_name").to_dict().values())[0]
		point = list(available_pos[["player_name","total_points"]].set_index("player_name").to_dict().values())[0]
		salaries[pos] = salary
		points[pos] = point

	_vars = {k: LpVariable.dict(k, v, cat="Binary") for k, v in points.items()}

	#print(_vars)

	# run the optimisation model
	prob = LpProblem("Fantasy", LpMaximize)
	rewards = []
	costs = []
	position_constraints = []

	# Setting up the reward
	for k, v in _vars.items():
		costs += lpSum([salaries[k][i] * _vars[k][i] for i in v])
		rewards += lpSum([points[k][i] * _vars[k][i] for i in v])
		prob += lpSum([_vars[k][i] for i in v]) <= pos_num_available[k]
		
	prob += lpSum(rewards)
	prob += lpSum(costs) <= SALARY_CAP

	prob.solve()

	def summary(prob):
		div = '---------------------------------------\n'
		#print("Variables:\n")
		score = str(prob.objective)
		constraints = [str(const) for const in prob.constraints.values()]
		total_value = 0
		total_cost = 0
		master_cdf = pd.DataFrame()
		for v in prob.variables():
			score = score.replace(v.name, str(v.varValue))
			constraints = [const.replace(v.name, str(v.varValue)) for const in constraints]
			if v.varValue != 0:
				print(v.name, "=", v.varValue)
				clean_name = v.name.split('_')[1] + ' ' + v.name.split('_')[2] 
				cdf = df[df['player_name'] == clean_name]
				total_value += cdf.iloc[0]['total_points']
				total_cost += cdf.iloc[0]['player_cost']
				master_cdf = pd.concat([master_cdf, cdf])
		print()
		print(master_cdf)
		#print(div)
		#print("Constraints:")
		for constraint in constraints:
			constraint_pretty = " + ".join(re.findall("[0-9\.]*\*1.0", constraint))
			#if constraint_pretty != "":
				#print("{} = {}".format(constraint_pretty, eval(constraint_pretty)))
		#print(div)
		#print("Score:")
		#score_pretty = " + ".join(re.findall("[0-9\.]+\*1.0", score))
		#print("{} = {}".format(score_pretty, eval(score)))

		#print(f'Total cost: {total_cost}')
		#print(f'Total value: {total_value}')

	summary(prob)

