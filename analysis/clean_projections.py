import pandas as pd
import numpy as np
from itertools import chain

def clean_projections():
	df = pd.read_csv('../data/player_projections.csv')
	scoring = pd.read_csv('../data/scoring.csv')

	scoring_dict = {}

	for i in range(len(scoring.index)):
		scoring_dict[scoring.iloc[i][0]] = scoring.iloc[i][1]

	keep_columns = ['PLAYER', 'POS', 'PTS', 'TREB', 'AST', 'STL', 'BLK', 'TO', 'FGA', 'FGM', 'FTA', 'FTM']

	df = df[keep_columns]

	df['PLAYER'] = df['PLAYER'].str.split(' ').str[0:2]

	def try_join(l):
	    try:
	        return ' '.join(map(str, l))
	    except TypeError:
	        return np.nan

	df['PLAYER'] = [try_join(l) for l in df['PLAYER']]

	cols_to_update = list(scoring_dict.keys())  # you might need cols_to_update = list(d.keys()) in python 3
	# multiply the selected columns and update
	df[cols_to_update] = df[cols_to_update].mul(pd.Series(scoring_dict), axis=1)[cols_to_update]

	df['TOTAL_POINTS'] = df.sum(axis=1)

	df = df[['PLAYER', 'POS', 'TOTAL_POINTS']]

	df = df[df['POS'].notna()]

	# return list from series of comma-separated strings
	def chainer(s):
	    return list(chain.from_iterable(s.str.split(',')))

	# calculate lengths of splits
	lens = df['POS'].str.split(',').map(len)

	# create new dataframe, repeating or chaining as appropriate
	df = pd.DataFrame({'player_name': np.repeat(df['PLAYER'], lens),
	                    'total_points': np.repeat(df['TOTAL_POINTS'], lens),
	                    'position': chainer(df['POS'])})

	df.to_csv('../data/player_points.csv')

	return(df)