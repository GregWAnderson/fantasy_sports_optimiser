import clean_projections 	as cp
import value_players 		as vp
import difflib


def input_retry(max_retries = 3, message = "Player: ", selection_list = None, replace_df = False, replacement_column = "", replacement_df = None ):
	retries = 0
	while retries < max_retries:
		try:
			choice = input(message)
			if choice not in selection_list:
				retries += 1
				raise ValueError
			else:
				if replace_df == True:
					replacement_df = replacement_df[ replacement_df[replacement_column] != choice ]
				else:
					pass
				return choice
				break
		except ValueError:
			print(f'{choice} is not in the list')
			try:
				print(f'Did you mean {difflib.get_close_matches(choice, replacement_df[replacement_column].unique())[0]}?')
			except:
				pass

# set the draft parameters
MAX_PLAYER = 13
players_drafted = 0
player_positions = {
		"PG": 2,
		"SG": 2,
		"SF": 2,
		"PF": 2,
		"C": 1,
	}
salary = 200

# clean the latest scraped projections
cp.clean_projections()
# merge projected scores with cost
players = vp.merge_data()

# start the draft
while (players_drafted < MAX_PLAYER) or salary > 0:
	# run the optimiser given the chanegd constraints
	vp.optimise(players, salary = salary, player_positions = player_positions)

	# select a player
	input_retry(max_retries = 3, message = "Player: ", selection_list = players.player_name.unique(), replace_df = True,
					replacement_df = players, replacement_column = "player_name")

	who = input_retry(max_retries = 3, message = "My team (y/n): ", selection_list = ["Y", "N", "y", "n"], replace_df = False)
	who = who.lower()
	if who == 'y':
		players_drafted+=1
		position = input_retry(max_retries = 3, message = "Position: ", selection_list = list(player_positions.keys()), replace_df = False)
		
		if player_positions.get(position) == 0:
			print(f'You stuffed up and took too many {position}')
		player_positions[position] = player_positions.get(position) - 1

		price = int(input_retry(max_retries = 3, message = "Price: ", selection_list =  map(str, range(1, salary)), replace_df = False))
		salary -= price

	print(f'salary remaining {salary}')

	if salary < 1:
		break



