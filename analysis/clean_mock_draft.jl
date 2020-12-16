
# install the packages
using DelimitedFiles

# open the password file
mock_draft = readlines("../data/mock_draft.csv")
mock_draft = mock_draft[2:end]

player_data = [["player_name", "player_cost"]]
player = []

for q in mock_draft
	global player_data
	global player
	# loop through each line
	# if it is a new line then count the answers and start a new group
	if q == ""
		clean_data = [ strip(player[1]), strip(player[end-1])[2:end] ]
		append!(player_data, [clean_data])
		player = []
	# otherwise add the anser to the group 
	else
		append!(player, [q])
	end
end

writedlm("../data/player_costs.csv",  player_data, ',')
