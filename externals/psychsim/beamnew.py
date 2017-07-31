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
TURNS = 50

myfile = open("ea_runs.txt","a")

class Gathering:
    def __init__(self,genome):

        self.weights = {}
        #self.weights['model'] = genome[0] # primary tendency, int 1,2,3
        # Genome for first agent
        self.weights['selfish_0'] = genome[1] # selfish strand, float 0.0-0.5
        self.weights['altruistic_0'] = genome[2] # altruistic strand, float 0.0-0.5
        self.weights['mean_0'] = genome[3] # mean strand, float 0.0-0.5
        self.weights['rationality_0'] = genome[4] # rationality, int 1-10
        self.weights['belief_0'] = genome[5] # belief level, int 0,1,2
        self.weights['belief_other'] = genome[6]

        '''
        # Genome for second agent
        self.weights['selfish_1'] = genome[7] # selfish strand, float 0.0-0.5
        self.weights['altruistic_1'] = genome[8] # altruistic strand, float 0.0-0.5
        self.weights['mean_1'] = genome[9] # mean strand, float 0.0-0.5
        self.weights['rationality_1'] = genome[10] # rationality, int 1-10
        self.weights['belief_1'] = genome[11] # belief level, int 0,1,2
        '''

        self.paused = False
        self.world = World()
        self.world.defineState(None, 'turns', int)
        self.world.setState(None, 'turns', 0)

        self.world.addTermination(makeTree({'if': thresholdRow(stateKey(None, 'turns'), TURNS),
                                    True: True, False: False}))

        self.agts = []
        self.tiles = []
        self.create_agents()
        for i in range(1,4):
            for j in range(1,4):
                self.generate_food(i,j)

        for action in self.agts[0].actions | self.agts[1].actions:
            tree = makeTree(incrementMatrix(stateKey(None,'turns'),1))
            self.world.setDynamics(stateKey(None,'turns'),action,tree)

        # Parallel action
        #self.world.setOrder([set(self.world.agents.keys())])
        #world.setOrder([set(['Agent0','Agent1']),'Agent2','Agent3'])
        #self.world.setOrder(set([tile.name for tile in self.tiles]),set([agent.name for agent in self.agts]))
        self.world.setOrder([set([tile.name for tile in self.tiles]),'Actor0','Actor1'])
        # Sequential action
        #self.world.setOrder(self.world.agents.keys())

    def create_agents(self):
        for i in range(0, GATHERERS):
            # Create multiple agents
            actor = Agent('Actor'+str(i))
            self.world.addAgent(actor)
            actor.setHorizon(3)
            self.agts.append(actor)

            # Active state (can be disabled by beam)
            self.world.defineState(actor.name, 'active',bool)
            self.world.setState(actor.name, 'active', False)


        for i in range(0, GATHERERS):
            actor = self.agts[i]
            if i == 0:
                other = self.agts[1]
                startx = 0
            else:
                other = self.agts[0]
                startx = 4
            # States
            self.world.defineState(actor.name,'food',int)
            self.world.setState(actor.name,'food',0)

            # Start at different locations
            self.world.defineState(actor.name,'x',int)
            self.world.defineState(actor.name,'y',int)
            self.world.setState(actor.name,'x',startx)
            self.world.setState(actor.name,'y',2)

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

            # Rightmost boundary check
            act = stateKey(actor.name,'active')
            tree = makeTree({'if': trueRow(act),
                            True: {'if': equalRow(stateKey(actor.name, 'x'), '4'),
                                True: False, False: True},
                            False: False})
            actor.setLegal(action, tree)

            # Check other agent
            #tree = makeTree({'if': differenceRow(stateKey(actor.name,'x'),stateKey(other.name,'x'),1), True: True, False: False})
            #actor.setLegal(action,tree)

            ##############################

            # Decrement X position
            action = actor.addAction({'verb': 'MoveLeft'})
            tree = makeTree(incrementMatrix(stateKey(action['subject'], 'x'), -1.))
            self.world.setDynamics(stateKey(action['subject'], 'x'), action, tree)

            # Leftmost boundary check, min X = 0
            tree = makeTree({'if': trueRow(act),
                            True: {'if': equalRow(stateKey(actor.name, 'x'), '0'),
                                True: False, False: True},
                            False: False})
            actor.setLegal(action, tree)

            # Check other agent
            #tree = makeTree({'if': differenceRow(stateKey(actor.name,'x'),stateKey(other.name,'x'),1), True: True, False: False})
            #actor.setLegal(action,tree)

            ##############################

            # Increment Y position
            action = actor.addAction({'verb': 'MoveUp'})
            tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), 1.))
            self.world.setDynamics(stateKey(action['subject'], 'y'), action, tree)

            # Downmost boundary check, max Y
            tree = makeTree({'if': trueRow(act),
                            True: {'if': equalRow(stateKey(actor.name, 'y'), '4'),
                                True: False, False: True},
                            False: False})
            actor.setLegal(action, tree)

            # Check other agent
            #tree = makeTree({'if': differenceRow(stateKey(actor.name,'y'),stateKey(other.name,'y'),1), True: True, False: False})
            #actor.setLegal(action,tree)

            ##############################

            # Decrement Y position
            action = actor.addAction({'verb': 'MoveDown'})
            tree = makeTree(incrementMatrix(stateKey(action['subject'], 'y'), -1.))
            self.world.setDynamics(stateKey(action['subject'], 'y'), action, tree)

            # Upmost boundary check, min Y = 0
            tree = makeTree({'if': trueRow(act),
                            True: {'if': equalRow(stateKey(actor.name, 'y'), '0'),
                                True: False, False: True},
                            False: False})
            actor.setLegal(action, tree)

            # Check other agent
            #tree = makeTree({'if': differenceRow(stateKey(actor.name,'y'),stateKey(other.name,'y'),1), True: True, False: False})
            #actor.setLegal(action,tree)

            ##############################

            # Beams
            action = actor.addAction({'verb': 'VerticalBeam'})
            tree = makeTree(setFalseMatrix(stateKey(other.name,'active')))
            self.world.setDynamics(stateKey(other.name,'active'),action,tree)
            tree = makeTree({'if': trueRow(act),
                            True: {'if': equalFeatureRow(stateKey(actor.name, 'x'), stateKey(other.name,'x')),
                                True: True, False: False},
                            False: False})
            #tree = makeTree({'if': equalFeatureRow(stateKey(actor.name,'x'),stateKey(other.name,'x')), True: True, False: False})
            actor.setLegal(action, tree)

            action = actor.addAction({'verb': 'HorizontalBeam'})
            tree = makeTree(setFalseMatrix(stateKey(other.name,'active')))
            self.world.setDynamics(stateKey(other.name,'active'),action,tree)
            tree = makeTree({'if': trueRow(act),
                            True: {'if': equalFeatureRow(stateKey(actor.name, 'y'), stateKey(other.name,'y')),
                                True: True, False: False},
                            False: False})
            #tree = makeTree({'if': equalFeatureRow(stateKey(actor.name,'y'),stateKey(other.name,'y')), True: True, False: False})
            actor.setLegal(action, tree)

            # Activate
            action = actor.addAction({'verb': 'Activate'})
            tree = makeTree(setTrueMatrix(stateKey(actor.name,'active')))
            self.world.setDynamics(stateKey(actor.name,'active'),action,tree)
            tree = makeTree({'if': trueRow(stateKey(actor.name,'active')),True: False, False: True})
            actor.setLegal(action, tree)

            # Maximize your current food count
            #actor.setReward(maximizeFeature(stateKey(actor.name,'food')),1.0)
            #me.setReward(maximizeFeature(stateKey(me.name,'food')),self.weights['selfish'])
            #me.setReward(maximizeFeature(stateKey(other.name,'food')),self.weights['altruistic'])
            #me.setReward(achieveFeatureValue(stateKey(other.name,'active'),False),self.weights['mean'])

            # Models of belief
            if i == 0:
                actor.addModel('Selfish',R={},level=self.weights['belief_0'],rationality=self.weights['rationality_0'],selection='distribution')
                actor.addModel('Altruistic',R={},level=self.weights['belief_0'],rationality=self.weights['rationality_0'],selection='distribution')
                actor.addModel('Mean',R={},level=self.weights['belief_0'],rationality=self.weights['rationality_0'],selection='distribution')
            elif i == 1:
                actor.addModel('Selfish',R={},level=2,rationality=10.,selection='distribution')
                actor.addModel('Altruistic',R={},level=2,rationality=10.,selection='distribution')
                actor.addModel('Mean',R={},level=2,rationality=10.,selection='distribution')


    def generate_food(self, i ,j):
        location = Agent(str(i) + ',' + str(j))
        self.tiles.append(location)
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
          'distribution': [(setTrueMatrix(stateKey(location.name, 'food')), 0.25), (setFalseMatrix(stateKey(location.name, 'food')), 0.75)]
        })

        #tree = makeTree(setTrueMatrix(stateKey(location.name, 'food')))
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
                #print me.models.keys()
                if model is True:
                    name = trueModels[me.name]
                else:
                    name = model
                if name == 'Selfish':
                    if i == 0:
                        me.setReward(maximizeFeature(stateKey(me.name,'food')),1.0,model)
                        me.setReward(maximizeFeature(stateKey(other.name,'food')),self.weights['altruistic_0'],model)
                        me.setReward(achieveFeatureValue(stateKey(other.name,'active'),False),self.weights['mean_0'],model)
                    elif i == 1:
                        me.setReward(maximizeFeature(stateKey(me.name,'food')),1.0,model)
                elif name == 'Altruistic':
                    if i == 0:
                        me.setReward(maximizeFeature(stateKey(me.name,'food')),self.weights['selfish_0'],model)
                        me.setReward(maximizeFeature(stateKey(other.name,'food')),1.0,model)
                        me.setReward(achieveFeatureValue(stateKey(other.name,'active'),False),0,model)
                    elif i == 1:
                        me.setReward(maximizeFeature(stateKey(me.name,'food')),1.0,model)
                        me.setReward(maximizeFeature(stateKey(other.name,'food')),1.0,model)
                elif name == 'Mean':
                    if i == 0:
                        me.setReward(maximizeFeature(stateKey(me.name,'food')),self.weights['selfish_0'],model)
                        me.setReward(maximizeFeature(stateKey(other.name,'food')),-1.0,model)
                        me.setReward(achieveFeatureValue(stateKey(other.name,'active'),False),1.0,model)
                    elif i == 1:
                        me.setReward(minimizeFeature(stateKey(other.name,'food')),1.0,model)
                        me.setReward(achieveFeatureValue(stateKey(other.name,'active'),False),1.0,model)
                        me.setReward(maximizeFeature(stateKey(me.name,'food')),0.5,model)

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
            #self.world.explain(result, 2)
        foodzero=self.world.getState('Actor0', 'food').domain()[0]
        foodone=self.world.getState('Actor1', 'food').domain()[0]
        myfile.write("Score: "+str(foodzero)+","+str(foodone)+"\n")
        return foodzero+foodone

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
                for i in range(0,GATHERERS):
                    print(self.world.getState('Actor' + str(i), 'food').domain()[0])
                self.world.explain(result, 2)
                turn = self.world.getState(None, 'turns')
                pyglet.image.get_buffer_manager().get_color_buffer().save('run/'+str(turn)+'.png')
            for i in range(1,4):
                for j in range(1,4):
                    val = self.world.getState(str(i)+','+str(j),'food').domain()[0]
                    #print str(i)+','+str(j)+':'+str(val)
                if self.world.terminated():
                    foodzero=self.world.getState('Actor0', 'food').domain()[0]
                    foodone=self.world.getState('Actor1', 'food').domain()[0]
                    #myfile.write(str(foodzero)+","+str(foodone))
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

        pyglet.clock.schedule_interval(update, 1.0)
        # pyglet.app.run()
        Thread(target=pyglet.app.run()).start()
        # target=pyglet.app.run()

def run(genome):
    #print(genome)
    genome[0] = min(3,max(genome[0],1))
    genome[1] = min(0.5,max(genome[1],0))
    genome[2] = min(0.5,max(genome[2],0))
    genome[3] = min(0.5,max(genome[3],0))
    genome[4] = min(10,max(genome[3],1))
    genome[5] = min(2,max(genome[3],0))
    '''
    genome[6] = min(3,max(genome[0],1))
    genome[7] = min(0.5,max(genome[1],0))
    genome[8] = min(0.5,max(genome[2],0))
    genome[9] = min(0.5,max(genome[3],0))
    genome[10] = min(10,max(genome[3],1))
    genome[11] = min(2,max(genome[3],0))
    '''
    #print("Starting new run with "+str(genome))
    myfile.write(str(genome)+":")
    model = ""
    guessmodel = ""
    if genome[0] == 1:
        model='Selfish'
    elif genome[0] == 2:
        model='Altruistic'
    elif genome[0] == 3:
        model='Mean'

    if genome[0] == 1:
        guessmodel='Selfish'
    elif genome[0] == 2:
        guessmodel='Altruistic'
    elif genome[0] == 3:
        guessmodel='Mean'

    run = Gathering(genome)
    trueModels = {'Actor0': model,
                  'Actor1': 'Mean'}
    run.modeltest(trueModels,'Selfish',guessmodel,1.0)
    result = run.run_without_visual()
    return (result,)

def demo(genome):
    #print(genome)
    genome[0] = min(3,max(genome[0],1))
    genome[1] = min(0.5,max(genome[1],0))
    genome[2] = min(0.5,max(genome[2],0))
    genome[3] = min(0.5,max(genome[3],0))
    genome[4] = min(10,max(genome[3],1))
    genome[5] = min(2,max(genome[3],0))
    genome[6] = min(3,max(genome[0],1))
    genome[7] = min(0.5,max(genome[1],0))
    genome[8] = min(0.5,max(genome[2],0))
    genome[9] = min(0.5,max(genome[3],0))
    genome[10] = min(10,max(genome[3],1))
    genome[11] = min(2,max(genome[3],0))

    #print("Starting new run with "+str(genome))
    myfile.write(str(genome)+":")
    models = []
    if genome[0] == 1:
        models.append('Selfish')
    elif genome[0] == 2:
        models.append('Altruistic')
    elif genome[0] == 3:
        models.append('Mean')

    if genome[6] == 1:
        models.append('Selfish')
    elif genome[6] == 2:
        models.append('Altruistic')
    elif genome[6] == 3:
        models.append('Mean')

    run = Gathering(genome)
    trueModels = {'Actor0': models[0],
                  'Actor1': models[1]}
    run.modeltest(trueModels,'Selfish','Mean',1.0)
    result = run.run_with_visual()
    return (result,)

if __name__ == '__main__':
    #print(run([1,0.5,0.5,-0.5,10,2,1,0.5,0.5,-0.5,10,2]))
    print(demo([1,0.5,0.5,-0.5,10,2,1,0.5,0.5,-0.5,10,2]))
    print(demo([3,0.5,-0.5,0.5,10,2,3,0.5,-0.5,0.5,10,2]))


    '''
    runone = True
    runall = False

    if runall:
        #myfile.write("7/14\n")
        models = ['Selfish','Altruistic','Mean']
        for zero in range(0,3):
            for one in range(0,3):
                for i in range(0,3):
                    for j in range(0,3):
                        truezero=models[zero]
                        trueone=models[one]
                        beliefzero=models[i]
                        beliefone=models[j]
                        #myfile.write(truezero[0]+","+trueone[0]+","+beliefzero[0]+","+beliefone[0]+",")
                        #myfile.write("Food: 100%\n")
                        #myfile.write("True Models: "+truezero+","+trueone+"\n")
                        #myfile.write("Belief Models: "+beliefzero+","+beliefone+"\n")
                        #myfile.write("Confidence: 1.0\n")
                        run = Gathering()
                        trueModels = {'Actor0': truezero,
                                      'Actor1': trueone}
                        run.modeltest(trueModels,beliefzero,beliefone,1.0)
                        run.run_without_visual()
                        #myfile.write("\n")
    elif runone:
        run = Gathering()
        trueModels = {'Actor0': 'Selfish',
                      'Actor1': 'Mean'}
        run.modeltest(trueModels,'Selfish','Mean',1.0)
        run.run_with_visual()
    '''
