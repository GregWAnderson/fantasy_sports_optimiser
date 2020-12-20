import clean_projections 	as cp
import value_players 		as vp
import difflib

players_drafted = 0
max_player = 13

cp.clean_projections()

players = vp.merge_data()

player_positions = {
		"PG": 2,
		"SG": 2,
		"SF": 2,
		"PF": 2,
		"C": 1,
	}

salary = 200

while (players_drafted < max_player) or salary > 0:

	vp.optimise(players, salary = salary, player_positions = player_positions)

	# get player name
	player_tries = 0
	while player_tries < 3:
		try:
			player_pick = input("Player: ")
			if player_pick not in players.player_name.unique():
				player_tries += 1
				raise ValueError
			else:
				players = players[ players['player_name'] != player_pick ]
				break
		except ValueError:
			print(f'{player_pick} is not in the list or has been picked already')
			try:
				print(f'Did you mean {difflib.get_close_matches(player_pick, players.player_name.unique())[0]}?')
			except:
				pass

	
	who = input("My team (y/n): ").lower()
	if who == 'y':
		players_drafted+=1
		position = input("Position: ")
		if player_positions.get(position) == 0:
			print(f'You fucked up, and took too many {position}')
		player_positions[position] = player_positions.get(position) - 1

		price = int(input("Price: "))
		salary -= price

	print(f'salary remaining {salary}')

	if salary < 1:
		break



