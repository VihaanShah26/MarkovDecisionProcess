def drone_flight_planner (map,policies, values, delivery_fee, battery_drop_cost, dronerepair_cost, discount):

	# accessing the map using "map[y][x]"
	# accessing the policies using "policies[y][x]"
	# accessing the values using "values[y][x]"
	# y is between 0 and 5
	# x is between 0 and 5
	# function will return the value of the cell corresponding to the starting position of the drone
	# 

	#making all the rewards negative 
	battery_drop_cost = -battery_drop_cost
	dronerepair_cost = -dronerepair_cost

	start = [0,0]
	destination = [0,0]
		
	# finding the coordinates of the start and destination positions
	#initialise the values for exit states over here
	for j in range(6):
		for i in range(6):
			if map[j][i] == 1:
				start[0] = j
				start[1] = i
			if map[j][i] == 2:
				destination[0] = j
				destination[1] = i
				values[j][i] = delivery_fee
			if map[j][i] == 3: 
				values[j][i] = dronerepair_cost
	

	# helper function which will be called recursively 
	def helper(map, policies, values):
		convergence = 100000
		flag = 0
		# loop to iterate while the values have not converged 
		while convergence > 0.0000001:
			# if flag == 0: 
			# 	convergence = -10000
			# 	flag = 1
			convergence = 0
			for y in range(6):
				for x in range(6):
					if map[y][x] != 2 and map[y][x] != 3:
						utility, move = calculate_utility(map, values, y, x, battery_drop_cost, discount)
						# convergence = max(convergence, abs(utility - values[y][x]))
						convergence += abs(values[y][x] - utility)
						# print(convergence)
						values[y][x] = utility
						policies[y][x] = move
	# end of helper function 

	# calling the helper function -- running the program 
	helper(map, policies, values)

	return values[start[0]][start[1]]

# this function returns true if this move can be made and returns false if the move cannot be made 
def make_move(map, y, x, move):

	# move values --- 1 -> South, 2 -> West, 3 -> North, 4 -> East 
	if (move == 1 or move == 5) and y < 5: # if it is possible to move south 
		return True # it is a valid move 
	elif (move == 2 or move == 6) and x > 0: # if it is possible move west 
		return True
	elif (move == 3 or move == 7) and y > 0: # if it is possible move north 
		return True 
	elif (move == 4 or move == 8) and x < 5: # if it is possible move east
		return True 
	
	# if none of the moves are possible then return False 
	return False 

# this function is to calculate the utility based on 8 possible moves 
def calculate_utility(map, values, y, x, battery_drop_cost, discount):

	best_utility = -100000
	best_move = 0
	move = 1
	# move south with special propulsion off 
	if make_move(map, y, x, move):
		# 70% chance of going south 
		new_utility = 0.7 * (battery_drop_cost + (discount * values[y+1][x]))
		# 15% chance of going west
		if make_move(map, y, x, 2):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x-1]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going east 
		if make_move(map, y, x, 4):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x+1]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move
	else: 
		new_utility = 0.7 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going west
		if make_move(map, y, x, 2):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x-1]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going east 
		if make_move(map, y, x, 4):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x+1]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move

	# move west with special propuslsion off
	move = 2
	if make_move(map, y, x, move):
		# 70% chance of going west 
		new_utility = 0.7 * (battery_drop_cost + (discount * values[y][x-1]))
		# 15% chance of going north
		if make_move(map, y, x, 3):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y-1][x]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going south 
		if make_move(map, y, x, 1):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y+1][x]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move
	else: 
		# 70% chance of going west 
		new_utility = 0.7 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going north
		if make_move(map, y, x, 3):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y-1][x]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going south 
		if make_move(map, y, x, 1):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y+1][x]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move

	# move north with special propulsion off 
	move = 3
	if make_move(map, y, x, move):
		# 70% chance of going north 
		new_utility = 0.7 * (battery_drop_cost + (discount * values[y-1][x]))
		# 15% chance of going west
		if make_move(map, y, x, 2):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x-1]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going east 
		if make_move(map, y, x, 4):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x+1]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move
	else:
		# 70% chance of going north 
		new_utility = 0.7 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going west
		if make_move(map, y, x, 2):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x-1]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going east 
		if make_move(map, y, x, 4):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x+1]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move

	# move east with special propulsion off 
	move = 4
	if make_move(map, y, x, move):
		# 70% chance of going east 
		new_utility = 0.7 * (battery_drop_cost + (discount * values[y][x+1]))
		# 15% chance of going north
		if make_move(map, y, x, 3):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y-1][x]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going south 
		if make_move(map, y, x, 1):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y+1][x]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move
	else:
		# 70% chance of going east 
		new_utility = 0.7 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going north
		if make_move(map, y, x, 3):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y-1][x]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		# 15% chance of going south 
		if make_move(map, y, x, 1):
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y+1][x]))
		else: 
			new_utility += 0.15 * (battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move

	# move south with special propulsion on 
	move = 5
	if make_move(map, y, x, move):
		# 80% chance of going south 
		new_utility = 0.8 * (2*battery_drop_cost + (discount * values[y+1][x]))
		# 10% chance of going west
		if make_move(map, y, x, 2):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x-1]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going east 
		if make_move(map, y, x, 4):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x+1]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move
	else:
		# 80% chance of going south 
		new_utility = 0.8 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going west
		if make_move(map, y, x, 2):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x-1]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going east 
		if make_move(map, y, x, 4):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x+1]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move

	# move west with special propulsion on 
	move = 6
	if make_move(map, y, x, move):
		# 80% chance of going west 
		new_utility = 0.8 * (2*battery_drop_cost + (discount * values[y][x-1]))
		# 10% chance of going north
		if make_move(map, y, x, 3):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y-1][x]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going south 
		if make_move(map, y, x, 1):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y+1][x]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move
	else:
		# 80% chance of going west 
		new_utility = 0.8 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going north
		if make_move(map, y, x, 3):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y-1][x]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going south 
		if make_move(map, y, x, 1):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y+1][x]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move

	# move north with special propulsion on 
	move = 7
	if make_move(map, y, x, move):
		# 80% chance of going north 
		new_utility = 0.8 * (2*battery_drop_cost + (discount * values[y-1][x]))
		# 10% chance of going west
		if make_move(map, y, x, 2):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x-1]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going east 
		if make_move(map, y, x, 4):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x+1]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move
	else:
		# 80% chance of going north 
		new_utility = 0.8 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going west
		if make_move(map, y, x, 2):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x-1]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going east 
		if make_move(map, y, x, 4):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x+1]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move

	# move east with special propulsion on 
	move = 8 
	if make_move(map, y, x, move):
		# 80% chance of going east 
		new_utility = 0.8 * (2*battery_drop_cost + (discount * values[y][x+1]))
		# 10% chance of going north
		if make_move(map, y, x, 3):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y-1][x]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going south 
		if make_move(map, y, x, 1):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y+1][x]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move
	else:
		# 80% chance of going east 
		new_utility = 0.8 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going north
		if make_move(map, y, x, 3):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y-1][x]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		# 10% chance of going south 
		if make_move(map, y, x, 1):
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y+1][x]))
		else: 
			new_utility += 0.1 * (2*battery_drop_cost + (discount * values[y][x]))
		if new_utility > best_utility: 
			best_utility = new_utility
			best_move = move

	return [best_utility, best_move]