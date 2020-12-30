import pandas as pd
import numpy as np
from itertools import chain

def try_join(l):
    try:
        return ' '.join(map(str, l))
    except TypeError:
        return np.nan

# return list from series of comma-separated strings
def chainer(s):
    return list(chain.from_iterable(s.str.split(',')))

def clean_projections():
	# read the csv file of raw player stats
	df = pd.read_csv('../data/player_projections.csv')

	# read the csv of the scoring system
	scoring = pd.read_csv('../data/scoring.csv')

	# conver the scoring from df to dict
	scoring_dict = {}
	for i in range(len(scoring.index)):
		scoring_dict[scoring.iloc[i][0]] = scoring.iloc[i][1]

	# set the columns of interest
	keep_columns = ['PLAYER', 'POS', 'PTS', 'TREB', 'AST', 'STL', 'BLK', 'TO', 'FGA', 'FGM', 'FTA', 'FTM']
	df = df[keep_columns]

	# Player names are both the name and positition, therefore we need to extract only the name
	df['PLAYER'] = df['PLAYER'].str.split(' ').str[0:2]
	df['PLAYER'] = [try_join(l) for l in df['PLAYER']]

	# calculate the total projected fantasy score
	cols_to_update = list(scoring_dict.keys())  
	# multiply the selected columns and update
	df[cols_to_update] = df[cols_to_update].mul(pd.Series(scoring_dict), axis=1)[cols_to_update]
	df['TOTAL_POINTS'] = df.sum(axis=1)

	# keep only the player, position and total points, where the position is not null
	df = df[['PLAYER', 'POS', 'TOTAL_POINTS']]
	df = df[df['POS'].notna()]

	# calculate lengths of splits
	lens = df['POS'].str.split(',').map(len)

	# players cna have multiple positions and therefore there needs to be one
	# record per player and position
	# create new dataframe, repeating or chaining as appropriate
	df = pd.DataFrame({'player_name': np.repeat(df['PLAYER'], lens),
	                    'total_points': np.repeat(df['TOTAL_POINTS'], lens),
	                    'position': chainer(df['POS'])})

	# save the data to a local store
	df.to_csv('../data/player_points.csv')

	return(df)