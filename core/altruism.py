from psychsim.reward import *
from psychsim.pwl import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *
import psychsim.probability
import pyglet


world = World()
world.defineState(None,'round',int)
world.setState(None,'round',0)

banker = Agent('Banker')
world.addAgent(banker)
world.defineState(banker.name,'pool',int)
world.setState(banker.name,'pool',0)

distribute = banker.addAction({'verb': 'distribute'})

for i in range(4):
    actor = Agent('Agent'+str(i))
    world.addAgent(actor)
    actor.setHorizon(10)
    world.defineState(actor.name,'money',int)
    # Everyone starts with $200
    actor.setState('money',200)

    for i in range(20):
        money = i*10
        contrib = 'contribute '+str(money)
        action = actor.addAction({'verb':contrib})
        tree = makeTree(incrementMatrix(stateKey(None,'round'),1))
        world.setDynamics(stateKey(None,'round'),action,tree)

        tree = makeTree(incrementMatrix(stateKey(actor.name,'money'),money*-1))
        world.setDynamics(stateKey(actor.name,'money'), action, tree)

        tree = makeTree(incrementMatrix(stateKey(banker.name,'pool'),money))
        world.setDynamics(stateKey(banker.name, 'pool'), action, tree)

    tree = makeTree(addFeatureMatrix(stateKey(actor.name,'money'),stateKey(banker.name, 'pool'),0.4))
    world.setDynamics(stateKey(actor.name, 'money'),distribute,tree)

    actor.setReward(maximizeFeature(stateKey(actor.name, 'money')),1.0)
    actor.setReward(maximizeFeature(stateKey(banker.name, 'pool')),0.5)

world.addTermination(makeTree({'if': thresholdRow(stateKey(None,'round'),20),
                                True: True,
                                False: False}))
world.setOrder(['Agent0', 'Agent1', 'Agent2', 'Agent3', 'Banker'])
#world.setOrder([set(world.agents.keys())])

while not world.terminated():
    result = world.step()
    world.explain(result, 2)
    print('Banker pool: ' + str(world.getState('Banker', 'pool').domain()[0]))
