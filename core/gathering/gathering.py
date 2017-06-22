from psychsim.reward import *
from psychsim.pwl import *
from psychsim.action import *
from psychsim.world import *
from psychsim.agent import *
import psychsim.probability
import pyglet
from pyglet.window import key
from threading import Thread

GATHERERS = 2
TURNS = 10000

class Gathering:
    def __init__(self):
        self.paused = False
        self.world = World()
        self.world.defineState(None, 'turns', int)
        self.world.setState(None, 'turns', 0)

        self.world.addTermination(makeTree({'if': thresholdRow(stateKey(None, 'turns'), TURNS),
                                    True: True, False: False}))

        self.agts = []
        self.create_agents()
        for i in range(1,4):
            for j in range(1,4):
                self.generate_food(i,j)

        # Parallel action
        #self.world.setOrder([set(self.world.agents.keys())])
        # Sequential action
        self.world.setOrder(self.world.agents.keys())

    def create_agents(self):
        # Create multiple agents
        for i in range(0,GATHERERS):
            actor = Agent('Actor'+str(i))
            self.world.addAgent(actor)
            actor.setHorizon(10)

            # States
            self.world.defineState(actor.name,'food',int)
            self.world.setState(actor.name,'food',0)
            self.world.defineState(actor.name,'x',int)
            self.world.defineState(actor.name,'y',int)

            # Start at different locations
            if i==0:
                self.world.setState(actor.name,'x',0)
                self.world.setState(actor.name,'y',0)
            else:
                self.world.setState(actor.name,'x',4)
                self.world.setState(actor.name,'y',4)

            # Nop
            '''
            action = actor.addAction({'verb': 'Wait'})
            tree = makeTree(incrementMatrix(stateKey(action['subject'], 'x'), 0.))
            self.world.setDynamics(stateKey(action['subject'], 'x'), action, tree)
            tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), 0.))
            self.world.setDynamics(stateKey(action['subject'], 'y'), action, tree)
            tree = makeTree(incrementMatrix('turns', 1.0))
            self.world.setDynamics(stateKey(None, 'turns'), action, tree)
            '''

            # Increment X position
            action = actor.addAction({'verb': 'MoveRight'})
            tree = makeTree(incrementMatrix(stateKey(action['subject'], 'x'), 1.))
            self.world.setDynamics(stateKey(action['subject'], 'x'), action, tree)
            tree = makeTree(incrementMatrix('turns', 1.0))
            self.world.setDynamics('turns', action, tree)

            # Rightmost boundary check
            tree = makeTree({'if': equalRow(stateKey(actor.name, 'x'), '4'),
                             True: False, False: True})
            actor.setLegal(action, tree)

            ##############################

            # Decrement X position
            action = actor.addAction({'verb': 'MoveLeft'})
            tree = makeTree(incrementMatrix(stateKey(action['subject'], 'x'), -1.))
            self.world.setDynamics(stateKey(action['subject'], 'x'), action, tree)
            tree = makeTree(incrementMatrix('turns', 1.0))
            self.world.setDynamics(stateKey(None, 'turns'), action, tree)

            # Leftmost boundary check, min X = 0
            tree = makeTree({'if': equalRow(stateKey(actor.name, 'x'), '0'),
                             True: False, False: True})
            actor.setLegal(action, tree)

            ##############################

            # Increment Y position
            action = actor.addAction({'verb': 'MoveUp'})
            tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), 1.))
            self.world.setDynamics(stateKey(action['subject'], 'y'), action, tree)
            tree = makeTree(incrementMatrix('turns', 1.0))
            self.world.setDynamics(stateKey(None, 'turns'), action, tree)

            # Downmost boundary check, max Y
            tree = makeTree({'if': equalRow(stateKey(actor.name, 'y'), '4'),
                             True: False, False: True})
            actor.setLegal(action, tree)

            ##############################

            # Decrement Y position
            action = actor.addAction({'verb': 'MoveDown'})
            tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), -1.))
            self.world.setDynamics(stateKey(action['subject'], 'y'), action, tree)
            tree = makeTree(incrementMatrix('turns', 1.0))
            self.world.setDynamics(stateKey(None, 'turns'), action, tree)

            # Upmost boundary check, min Y = 0
            tree = makeTree({'if': equalRow(stateKey(actor.name, 'y'), '0'),
                             True: False, False: True})
            actor.setLegal(action, tree)

            # Maximize your current food count
            #actor.setReward(maximizeFeature(stateKey(actor.name,'food')),1.0)

            # Models of belief
            actor.addModel('Selfish',R={},level=2,rationality=10.,selection='distribution')
            actor.addModel('Altruistic',R={},level=2,rationality=10.,selection='distribution')
            actor.addModel('Sadistic',R={},level=2,rationality=10.,selection='distribution')

            self.agts.append(actor)

    def generate_food(self, i ,j):
        location = Agent(str(i) + ',' + str(j))
        self.world.addAgent(location)
        location.setHorizon(1)

        self.world.defineState(location.name, 'food', bool)
        self.world.setState(location.name, 'food', True)
        self.world.defineState(location.name, 'x', int)
        self.world.setState(location.name, 'x', i)
        self.world.defineState(location.name, 'y', int)
        self.world.setState(location.name, 'y', j)
        nothing = location.addAction({
          'verb': 'nothing'
        })

        # Probability of spawning a food on the current tile
        action = location.addAction({
          'verb': 'generate'
        })
        tree = makeTree({
          'distribution': [(setTrueMatrix(stateKey(location.name, 'food')), 0.05), (setFalseMatrix(stateKey(location.name, 'food')), 0.95)]
        })
        self.world.setDynamics(stateKey(location.name, 'food'), action, tree)

        # Can't respawn food if food is already food there
        tree = makeTree({
          'if': trueRow(stateKey(location.name, 'food')),
          True: False,
          False: True
        })
        location.setLegal(action, tree)

        # Force food tile to run generate when there's no food
        tree = makeTree({
          'if': trueRow(stateKey(location.name, 'food')),
          True: True,
          False: False
        })
        location.setLegal(nothing, tree)

        # If an agent is on a food tile, give the agent the food
        for i in range(0,GATHERERS):
            action = location.addAction({
              'verb': 'food'+str(i)
            })
            tree = makeTree(setFalseMatrix(stateKey(location.name, 'food')))
            self.world.setDynamics(stateKey(location.name, 'food'), action, tree)
            tree = makeTree(incrementMatrix(stateKey(self.agts[i].name, 'food'),1))
            self.world.setDynamics(stateKey(self.agts[i].name, 'food'), action, tree)
            tree = makeTree({
                    'if': trueRow(stateKey(location.name, 'food')),
                    True: {'if': equalFeatureRow(stateKey(location.name, 'x'), stateKey(self.agts[i].name,'x')),
                                    True: {'if': equalFeatureRow(stateKey(location.name, 'y'), stateKey(self.agts[i].name,'y')),
                                                    True: True,
                                                    False: False
                                                    },
                                    False: False
                                    },
                    False: False
                    })
            location.setLegal(action, tree)

        # hack: prioritize giving food over no action
        location.setReward(achieveFeatureValue(stateKey(location.name,'food'),False),1.)


    def modeltest(self,trueModels,A,B,strongerBelief):
        agts = self.agts
        for i in range(2):
            me = agts[i]
            other = agts[1-i]
            for model in me.models.keys():
                if model is True:
                    name = trueModels[me.name]
                else:
                    name = model
                if name == 'Selfish':
                    me.setReward(maximizeFeature(stateKey(me.name,'food')),1.0,model)
                elif name == 'Altruistic':
                    me.setReward(maximizeFeature(stateKey(me.name,'food')),1.0,model)
                    me.setReward(maximizeFeature(stateKey(other.name,'food')),1.0,model)
                #elif name == 'Sadistic':
                #    me.setReward(minimizeFeature(stateKey(other.name,'money')),1.0,model)
                #    me.setReward(maximizeFeature(stateKey(other.name,'money')),1.0,model)

        weakBelief = 1.0 - strongerBelief
        belief = {'Selfish': weakBelief,'Altruistic': weakBelief}
        belief[A] = strongerBelief
        self.world.setMentalModel('Actor0','Actor1',belief)
        belief = {'Selfish': weakBelief,'Altruistic': weakBelief}
        belief[B] = strongerBelief
        self.world.setMentalModel('Actor1','Actor0',belief)

    def run_without_visual(self):
        while not self.world.terminated():
            result = self.world.step()
            self.world.explain(result, 2)
        self.evaluate_score()

    # Graphics
    def run_with_visual(self):
        pyglet.resource.path = ['../resources/gathering']
        pyglet.resource.reindex()

        SCREEN_WIDTH = 5 * 32
        SCREEN_HEIGHT = 5 * 32
        window = pyglet.window.Window(resizable=True)
        window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)

        tile_image = pyglet.resource.image("black.jpg")
        tiles_batch = pyglet.graphics.Batch()
        tiles = []
        for y in range(0, 5):
            for x in range(0, 5):
                tiles.append(pyglet.sprite.Sprite(
                    img=tile_image,
                    x=x * 32,
                    y=y * 32,
                    batch=tiles_batch)
                )

        goal_image = pyglet.resource.image("green.jpg")
        goals_batch = pyglet.graphics.Batch()
        goals = []
        for i in range(0, 5):
            goals_sub = []
            for j in range(0, 5):
                goals_sub.append(pyglet.sprite.Sprite(
                    img=goal_image,
                    x= i * 32 + 1999,
                    y= j * 32 + 1999,
                    batch=goals_batch)
                )
            goals.append(goals_sub)

        #agent_image = pyglet.resource.image("white.jpg")
        agent0_image = pyglet.resource.image("0.jpg")
        agent1_image = pyglet.resource.image("1.jpg")
        agents_batch = pyglet.graphics.Batch()
        agents = []
        for index in range(0, GATHERERS):
            if index == 0:
                agents.append(pyglet.sprite.Sprite(
                    img=agent0_image,
                    x=index * 32,
                    y=index * 32,
                    batch=agents_batch))
            else:
                agents.append(pyglet.sprite.Sprite(
                        img=agent1_image,
                        x=index * 32,
                        y=index * 32,
                        batch=agents_batch))



        @window.event
        def on_draw():
            window.clear()
            tiles_batch.draw()
            goals_batch.draw()
            agents_batch.draw()

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.P:
                self.paused = True
                print('Paused')
            if symbol == key.U:
                self.paused = False
                print('Resumed')

        def update(dt):
            if not self.paused:
                result = self.world.step()
                self.world.explain(result, 2)
            for i in range(1,4):
                for j in range(1,4):
                    val = self.world.getState(str(i)+','+str(j),'food').domain()[0]
                    #print str(i)+','+str(j)+':'+str(val)
                if self.world.terminated():
                    window.close()

            for i in range(0,GATHERERS):
                agents[i].x = int(self.world.getState('Actor' + str(i), 'x').domain()[0]) * 32
                agents[i].y = int(self.world.getState('Actor' + str(i), 'y').domain()[0]) * 32

            for i in range(1,4):
                for j in range(1,4):
                    val = self.world.getState(str(i)+','+str(j),'food').domain()[0]
                    if val:
                        goals[i][j].x = i * 32
                        goals[i][j].y = j * 32
                    else:
                        goals[i][j].x = i * 1999
                        goals[i][j].y = j * 1999

        pyglet.clock.schedule_interval(update, 0.1)
        # pyglet.app.run()
        Thread(target=pyglet.app.run()).start()
        # target=pyglet.app.run()

if __name__ == '__main__':
    run = Gathering()
    trueModels = {'Actor0': 'Selfish',
                  'Actor1': 'Selfish'}
    run.modeltest(trueModels,'Selfish','Selfish',1.0)
    run.run_with_visual()
