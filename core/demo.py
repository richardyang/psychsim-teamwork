from psychsim.reward import *
from psychsim.pwl import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *
import pyglet

# Initialize the Psychsim World
world = World()

################################
# 1. Creating an Agent
################################
# Create some Agents
actorA = Agent('Agent A')
actorB = Agent('Agent B')
# Add them to the World
world.addAgent(actorA)
world.addAgent(actorB)
# Set the number of steps to look-ahead
actor.setHorizon(5)

################################
# 2. Define the Agent and World States
################################
# Define the amount each Agent has
world.defineState(actorA.name,'pot',int)
world.defineState(actorB.name,'pot',int)

world.setState(actorA.name, 'pot', 0)
world.setState(actorB.name, 'pot', 0)

world.defineState(None,'pile_one',int)
world.defineState(None,'pile_two',int)

world.setState(None,'pile_one',1)
world.setState(None,'pile_two',4)


################################
# 3. Set Actions
################################
# Increment X position and set world dynamics
action = actorA.addAction({'verb': 'Take'})
tree = makeTree(incrementMatrix(stateKey(action['subject'], 'pot'), world))
world.setDynamics(stateKey(action['subject'], 'x'), action, tree)

# Rightmost boundary check, max X = map limit
tree = makeTree({'if': equalRow(stateKey(actor.name, 'x'), '5'),
                 True: False, False: True})
actor.setLegal(action, tree)


################################
# 4. Set Rewards
################################
# Set the Agent reward to minimize getting to goal
actor.setReward(minimizeDifference(stateKey(actor.name, 'x'), stateKey(actor.name, 'goal_x')),
                1.0)
actor.setReward(minimizeDifference(stateKey(actor.name, 'y'), stateKey(actor.name, 'goal_y')),
                1.0)

################################
# 5. Set Turn Order
################################
# Parallel action
# self.world.setOrder([set(self.world.agents.keys())])
# Sequential action
world.setOrder(world.agents.keys())

