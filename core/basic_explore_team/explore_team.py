from __future__ import print_function
# Team of agents that attempts to explore an area without being detected by enemies
import numpy as np
from psychsim.reward import *
from psychsim.pwl import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *

MAP_SIZE_X = 15  # X value of map dimension
MAP_SIZE_Y = 15  # Y value of map dimension

# Friendly agents
F_ACTORS = 2  # Number of agents in the team
F_START_LOC = ["1,0", "0,1"]  # Starting locations for each agent
F_GOAL_LOC = ["8,4", "1,4"]  # Objectives the agents need to visit to win

# Enemy agents
E_ACTORS = 1  # Number of agents in the team
E_START_LOC = ["5,5"]
E_PATROL_RANGE = 2


def f_get_current_x(world, actor):
    return world.getState(actor.name, 'x').domain()[0]


def f_get_current_y(world, actor):
    return world.getState(actor.name, 'y').domain()[0]


def f_get_start_x(index):
    return int((F_START_LOC[index]).split(",", 1)[0])


def f_get_start_y(index):
    return int((F_START_LOC[index]).split(",", 1)[1])


def f_get_goal_x(index):
    return int((F_GOAL_LOC[index]).split(",", 1)[0])


def f_get_goal_y(index):
    return int((F_GOAL_LOC[index]).split(",", 1)[1])


def e_get_current_x(world, actor):
    return world.getState(actor.name, 'x').domain()[0]


def e_get_current_y(world, actor):
    return world.getState(actor.name, 'y').domain()[0]


def e_get_start_x(index):
    return int((E_START_LOC[index]).split(",", 1)[0])


def e_get_start_y(index):
    return int((E_START_LOC[index]).split(",", 1)[1])


def find_distance(start_x, start_y, goal_x, goal_y):
    return abs(goal_x - start_x) + abs(goal_y - start_y)
    # return np.linalg.norm(np.array((start_x, start_y)) - np.array((goal_x, goal_y)))


def create_friendly_agents(world):
    for index in range(0, F_ACTORS):
        actor = Agent('Actor' + str(index))
        world.addAgent(actor)
        actor.setHorizon(2)

        # Set agent's starting location
        world.defineState(actor.name, 'x', int)
        world.setState(actor.name, 'x', f_get_start_x(index))
        world.defineState(actor.name, 'goal_x', int)
        world.setState(actor.name, 'goal_x', f_get_goal_x(index))

        world.defineState(actor.name, 'y', int)
        world.setState(actor.name, 'y', f_get_start_y(index))
        world.defineState(actor.name, 'goal_y', int)
        world.setState(actor.name, 'goal_y', f_get_goal_y(index))

        # # Scrapped
        # # Calculate and set Manhattan distance to the goal
        # world.defineState(actor.name, 'goal_dist', int)
        # dist = find_distance(get_start_x(index), get_start_y(index), get_goal_x(index), get_goal_y(index))
        # world.setState(actor.name, 'goal_dist', dist)
        # actor.setReward(minimizeFeature(stateKey(actor, 'goal_dist')), 1.)

        actor.setReward(minimizeDifference(stateKey(actor.name, 'x'), stateKey(actor.name, 'goal_x')), 1.)
        actor.setReward(minimizeDifference(stateKey(actor.name, 'y'), stateKey(actor.name, 'goal_y')), 1.)

        for enemies in range(0, E_ACTORS):
            enemy = 'Enemy' + str(index)
            actor.setReward(minimizeDifference(stateKey(actor.name, 'x'), stateKey(enemy, 'x')), -0.5)
            actor.setReward(minimizeDifference(stateKey(actor.name, 'y'), stateKey(enemy, 'y')), -0.5)

        # Visited flag for the goal locations
        world.setFeature(world.defineState(actor, F_GOAL_LOC[index], bool), False)
        actor.setReward(maximizeFeature(stateKey(actor, F_GOAL_LOC[index])), 1.)

        tree = {'if': equalRow(stateKey(actor.name, 'x'), str(f_get_goal_x(index))),
                True: {'if': equalRow(stateKey(actor.name, 'y'), str(f_get_goal_y(index))), True: True, False: False},
                False: False}
        world.addTermination(makeTree(tree))

        set_friendly_actions(world, actor, index)


def set_friendly_actions(world, actor, index):
    # Nop
    action = actor.addAction({'verb': 'Wait'})
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'x'), 0.))
    world.setDynamics(stateKey(action['subject'], 'x'), action, tree)
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), 0.))
    world.setDynamics(stateKey(action['subject'], 'y'), action, tree)

    # Increment X position
    action = actor.addAction({'verb': 'MoveRight'})
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'x'), 1.))
    world.setDynamics(stateKey(action['subject'], 'x'), action, tree)

    # Rightmost boundary check
    tree = makeTree({'if': equalRow(stateKey(actor.name, 'x'), str(MAP_SIZE_X)),
                     True: False, False: True})
    actor.setLegal(action, tree)

    ##############################

    # Decrement X position
    action = actor.addAction({'verb': 'MoveLeft'})
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'x'), -1.))
    world.setDynamics(stateKey(action['subject'], 'x'), action, tree)

    # Leftmost boundary check, min X = 0
    tree = makeTree({'if': equalRow(stateKey(actor.name, 'x'), '0'),
                     True: False, False: True})
    actor.setLegal(action, tree)

    ##############################

    # Increment Y position
    action = actor.addAction({'verb': 'MoveUp'})
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), 1.))
    world.setDynamics(stateKey(action['subject'], 'y'), action, tree)

    # Downmost boundary check, max Y
    tree = makeTree({'if': equalRow(stateKey(actor.name, 'y'), MAP_SIZE_Y),
                     True: False, False: True})
    actor.setLegal(action, tree)

    ##############################

    # Decrement Y position
    action = actor.addAction({'verb': 'MoveDown'})
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), -1.))
    world.setDynamics(stateKey(action['subject'], 'y'), action, tree)

    # Upmost boundary check, min Y = 0
    tree = makeTree({'if': equalRow(stateKey(actor.name, 'y'), '0'),
                     True: False, False: True})
    actor.setLegal(action, tree)


def create_enemy_agents(world):
    for index in range(0, E_ACTORS):
        actor = Agent('Enemy' + str(index))
        world.addAgent(actor)
        actor.setHorizon(2)

        # Set agent's starting location
        world.defineState(actor.name, 'x', int)
        world.setState(actor.name, 'x', e_get_start_x(index))

        world.defineState(actor.name, 'y', int)
        world.setState(actor.name, 'y', e_get_start_y(index))

        set_enemy_actions(world, actor, index)


def set_enemy_actions(world, actor, index):
    # Nop
    action = actor.addAction({'verb': 'Wait'})
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'x'), 0.))
    world.setDynamics(stateKey(action['subject'], 'x'), action, tree)
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), 0.))
    world.setDynamics(stateKey(action['subject'], 'y'), action, tree)

    # Increment X position
    action = actor.addAction({'verb': 'MoveRight'})
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'x'), 1.))
    world.setDynamics(stateKey(action['subject'], 'x'), action, tree)

    # Rightmost boundary check
    tree = makeTree({'if': equalRow(stateKey(actor.name, 'x'), str(e_get_start_x(index) + E_PATROL_RANGE)),
                     True: False, False: True})
    actor.setLegal(action, tree)

    ##############################

    # Decrement X position
    action = actor.addAction({'verb': 'MoveLeft'})
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'x'), -1.))
    world.setDynamics(stateKey(action['subject'], 'x'), action, tree)

    # Leftmost boundary check, min X = 0
    tree = makeTree({'if': equalRow(stateKey(actor.name, 'x'), str(e_get_start_x(index) - E_PATROL_RANGE)),
                     True: False, False: True})
    actor.setLegal(action, tree)

    ##############################

    # Increment Y position
    action = actor.addAction({'verb': 'MoveUp'})
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), 1.))
    world.setDynamics(stateKey(action['subject'], 'y'), action, tree)

    # Downmost boundary check, max Y
    tree = makeTree({'if': equalRow(stateKey(actor.name, 'y'), str(e_get_start_y(index) + E_PATROL_RANGE)),
                     True: False, False: True})
    actor.setLegal(action, tree)

    ##############################

    # Decrement Y position
    action = actor.addAction({'verb': 'MoveDown'})
    tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), -1.))
    world.setDynamics(stateKey(action['subject'], 'y'), action, tree)

    # Upmost boundary check, min Y = 0
    tree = makeTree({'if': equalRow(stateKey(actor.name, 'y'), str(e_get_start_y(index) - E_PATROL_RANGE)),
                     True: False, False: True})
    actor.setLegal(action, tree)


def printGrid(world):
    """
    Print out a grid to the console for visualization
    """
    print()
    for y in range(0, MAP_SIZE_Y):
        for x in range(0, MAP_SIZE_X):
            loc = str(x) + ',' + str(y)
            actorlocs = []
            for index in range(0, F_ACTORS):
                actorlocs.append(str(world.getState('Actor' + str(index), 'x').domain()[0]) + ',' + str(
                    world.getState('Actor' + str(index), 'y').domain()[0]))
            enemylocs = []
            for index in range(0, E_ACTORS):
                enemylocs.append(str(world.getState('Enemy' + str(index), 'x').domain()[0]) + ',' + str(
                    world.getState('Enemy' + str(index), 'y').domain()[0]))
            if loc in actorlocs:
                print('A', end="")
            elif loc in enemylocs:
                print('E', end="")
            elif loc == F_GOAL_LOC[0]:
                print('1', end="")
            elif loc == F_GOAL_LOC[1]:
                print('2', end="")
            else:
                print('o', end="")
        print()


if __name__ == '__main__':

    world = World()
    create_friendly_agents(world)
    create_enemy_agents(world)
    # Parallel action
    world.setOrder([set(world.agents.keys())])
    # Sequential action
    #world.setOrder(world.agents.keys())

    while not world.terminated():
        result = world.step()
        # world.explain(result, 2)
        # world.step({world.agents['Actor0']: Action({'verb': 'MoveRight'})})
        printGrid(world)
        # world.printState()

        # if allVisited(world):
        #    world.setFeature('complete', True)

    print('RUN COMPLETE!')
