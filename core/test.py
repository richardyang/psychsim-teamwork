from psychsim.reward import *
from psychsim.pwl import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *
import psychsim.probability

import pyglet


world = World()

actor = Agent('Agent')
world.addAgent(actor)
actor.setHorizon(10)

test = Agent('Test')
world.addAgent(test)
world.defineState(test.name,'lol',int)
test.setState('lol',1)
derp = test.addAction({'verb':'derp'})

world.defineState(actor.name,'money',int)
actor.setState('money',0)

world.defineState(None,'round',int,description='The current round')
world.setState(None,'round',0)

'''
##
action = actor.addAction({'verb':'test'})
tree = makeTree(incrementMatrix(stateKey(None,'round'),1))
world.setDynamics(stateKey(None,'round'),action,tree)

tree = makeTree(addFeatureMatrix(stateKey(actor.name,'money'),stateKey(None,'round')))
world.setDynamics(stateKey(actor.name,'money'),action,tree)
##
'''

action = actor.addAction({'verb':'a'})
tree = makeTree(incrementMatrix(stateKey(None,'round'),1))
world.setDynamics(stateKey(None,'round'),action,tree)
tree = makeTree(incrementMatrix(stateKey(actor.name,'money'),1))
world.setDynamics(stateKey(actor.name,'money'),action,tree)

action = actor.addAction({'verb':'b'})
tree = makeTree(incrementMatrix(stateKey(None,'round'),1))
world.setDynamics(stateKey(None,'round'),action,tree)
tree = makeTree(incrementMatrix(stateKey(actor.name,'money'),1))
world.setDynamics(stateKey(actor.name,'money'),action,tree)

#tree = makeTree({'if': differenceRow(stateKey(actor.name,'money'),stateKey(test.name,'lol'),0), True: True, False: False})
tree = makeTree({'if': differenceRow(stateKey(test.name,'lol'),stateKey(actor.name,'money'),0), True: True, False: False})
actor.setLegal(action,tree)


'''
action = actor.addAction({'verb':'right'})
tree = makeTree(incrementMatrix(stateKey(None,'round'),1))
world.setDynamics(stateKey(None,'round'),action,tree)
tree = makeTree(incrementMatrix(stateKey(actor.name,'money'),100))
world.setDynamics(stateKey(actor.name,'money'),action,tree)

action = actor.addAction({'verb':'left'})
tree = makeTree(incrementMatrix(stateKey(None,'round'),1))
world.setDynamics(stateKey(None,'round'),action,tree)
tree = makeTree({'distribution': [(incrementMatrix(stateKey(actor.name,'money'),50),0.6),
                                  (incrementMatrix(stateKey(actor.name,'money'),125),0.39),
                                  (incrementMatrix(stateKey(actor.name,'money'),1000000),0.01)]})
world.setDynamics(stateKey(actor.name,'money'),action,tree)
'''

actor.setHorizon(6)
actor.setAttribute('discount',1.)

world.addTermination(makeTree({'if': thresholdRow(stateKey(None,'round'),5),
                                True: True,
                                False: False}))

actor.setReward(maximizeFeature(stateKey(actor.name, 'money')),1.0)

world.setOrder([set(world.agents.keys())])

while not world.terminated():
    print(world.getState('Agent', 'money').domain()[0])
    result = world.step()
    world.explain(result, 2)
