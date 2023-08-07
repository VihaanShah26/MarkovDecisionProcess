# Markov Decision Process

## Goal
Create a path planner to help a pizza chain deliver food to their customers using drones 

## Background 
The pizza place is based in a small town sized 6 blocks from North to South and 6 blocks from East to West. 

Rival pizza places own some of the blocks and will shoot down the drone if it flies above these blocks. 

The pizza place has to pay to charge the drone's battery so the shotter the flight time, the better. 

The town is extremely windy so the drone may not always move in the direction it intends to. When the drone tries to move in a particular direction, it has a 70% chance of going in that direction and a 30% chance of going on either side due to the wind (15% each side). The drone also has a special propulsion system which doubles the battery consumption but gives the drone an 80% chance of going in the direction it intends and 10% chance of going on either of the sides. 

Special Propulsion off: 

<img width="383" alt="image" src="https://github.com/VihaanShah26/MarkovDecisionProcess/assets/79374408/23b6f2e9-60a1-418c-9f98-176f6a33abac">

Special Propulsion on: 

<img width="379" alt="image" src="https://github.com/VihaanShah26/MarkovDecisionProcess/assets/79374408/58f67502-7f7d-4ae4-834d-01d22904ceba">

The drones can move in 4 directions - North, South, East, West. When the drones reach boundaries, if they try moving out of the map, they bounce against the boundaries. 

The town has 1 pizza place, 1 customer and any number of rivals. 

## Program 
The program will take as input a bidimensional structure called map of size 6x6 which contains the locations of the pizza place, customer and rivals. They are represented as follows: 

0 - Empty Block 

1 - The Pizza Shop 

2 - Customer 

3 - Rival Pizza Places 

The program also takes as input an empty bidimensional structure of size 6x6 called policies which must be populated by the drone's best action in each block. The actions the drone can take are represented as follows: 

1 - South with special propulsion OFF 

2 - West with special propulsion OFF 

3 - North with special propulsion OFF 

4 - East with special propulsion OFF 

5 - South with special propulsion ON 

6 - West with special propulsion ON 

7 - North with special propulsion ON 

8 - East with special propulsion ON

Other inputs - "delivery_fee" which is the reward for successfully delivering the pizza, "battery_drop_cost" which is the cost of the drone moving one block without special propulsion, "dronerepair_cost" which is the cost of replacing a drone that is shot down by a rival and "discount" which is the discounting factor of rewards as the drone takes longer to deliver the pizza. 

The function returns the expected utility of the job. It modiefies the "policies" structure by entering the optimal policy in each block and the "values" structure by entering the expected utility of each block under optimal policy. 

In case of ties, priority is given as special propulsion off > special propulsion on and South > West > North > East. 
