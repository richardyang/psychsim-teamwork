# TODO
MAP_SIZE_X = 10  # X value of map dimension
MAP_SIZE_Y = 10  # Y value of map dimension
SCREEN_WIDTH = (MAP_SIZE_X) * 32
SCREEN_HEIGHT = (MAP_SIZE_Y) * 32

# Friendly agents
F_ACTORS = 4  # Number of agents in the team
F_START_LOC = ["0,1","0,8","9,1","9,8"]  # Starting locations for each agent
F_GOAL_LOC = ["2,2","2,7","7,2","7,7"]  # Objectives the agents need to visit to win

# Enemy agents
E_ACTORS = 4  # Number of agents in the team
E_START_LOC = ["2,2","2,7","7,2","7,7"]
E_PATROL_RANGE = 5

# Distractor agents
D_ACTORS = 4
D_START_LOC = ["0,0","0,9","9,0","9,9"]  # Base location, also the start location of distractor

# Reward weights - variables
BASE = [0.5, 0.2]  # Minimize distractor and enemy distance, minimize distractor cost
DISTRACTOR = [-1.0]  # Minimize agent and enemy distance
ENEMY = [0.5, 0.5,
         -1.0]  # Minimize agent and enemy distance, minimize enemy and distractor distance, minimize agent and goal distance
AGENT = [0.5, -0.5]  # Minimize agent and goal distance, maximize agent and enemy distance
