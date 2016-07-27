import pyglet
from Tkinter import *


class BaseLoader:
    def __init__(self, master):
        master.wm_title("Scenario Config")
        labels = ["Map Size X", "Map Size Y", "Soldiers", "Enemies", "Bases"]  # Display text
        fields = []  # Fields for storing entries
        for i in range(0, 5):
            Label(master, text=labels[i]).grid(row=i)
            fields.append(Entry(master, width=5))
            fields[i].grid(row=i, column=1)

        labels = ["Soldier Rewards:", "S/G Dist", "S/E Dist",
                  "Base Rewards:", "H/E Dist", "H Cost",
                  "Helicopter Rewards:", "H/E Dist", "S/E Dist",
                  "Enemy Rewards:", "S/E Dist", "H/E Dist", "S/G Dist"]
        weights = [None] * 14

        for i in range(0, len(labels)):
            Label(master, text=labels[i]).grid(row=i+6)
            if i%3 or i==12:
                weights[i] = Entry(master, width=5)
                weights[i].grid(row=i+6, column=1)

        def save_configuration():
            # print("Size X: %s\nSize Y: %s\nSoldiers: %s\nEnemies: %s\nBases: %s" % ())
            newWindow = Toplevel(master)
            app = AdvancedLoader(newWindow, fields)

        def load_default():
            defaults = [8, 5, 1, 1, 1]
            for i in range(0, 5):
                fields[i].delete(0, 'end')
                fields[i].insert(0, defaults[i])

            default_weights = [None,0.5,-0.5,None,0.5,0.2,None,-1.0,1.0,None,0.5,0.6,-1.0]
            for i in range(0, len(labels)):
                if i % 3 or i == 12:
                    weights[i].delete(0, 'end')
                    weights[i].insert(0, default_weights[i])


        Button(master, text='Configure', command=save_configuration).grid(row=100, column=0, sticky=W, pady=4)
        Button(master, text='Default', command=load_default).grid(row=100, column=1, sticky=W, pady=4)


class AdvancedLoader:
    soldiers_count = 0
    enemies_count = 0
    bases_count = 0

    def __init__(self, master, fields):
        self.master = master
        soldiers_count = int(fields[2].get())
        enemies_count = int(fields[3].get())
        bases_count = int(fields[4].get())

        Label(master, text='x').grid(row=0, column=1)
        Label(master, text='y').grid(row=0, column=2)
        soldier_locations = []
        for i in range(0, soldiers_count):
            Label(master, text='Soldier' + str(i) + " Location:").grid(row=i + 1)
            soldier_x = Entry(master, width=5)
            soldier_x.grid(row=i + 1, column=1)
            soldier_y = Entry(master, width=5)
            soldier_y.grid(row=i + 1, column=2)
            location = [soldier_x, soldier_y]
            soldier_locations.append(location)

        enemy_locations = []
        for i in range(0, enemies_count):
            Label(master, text='Enemy' + str(i) + " Location:").grid(row=i + soldiers_count + 1)
            enemy_x = Entry(master, width=5)
            enemy_x.grid(row=i + soldiers_count + 1, column=1)
            enemy_y = Entry(master, width=5)
            enemy_y.grid(row=i + soldiers_count + 1, column=2)
            location = [enemy_x, enemy_y]
            enemy_locations.append(location)

        base_locations = []
        for i in range(0, bases_count):
            Label(master, text='Base' + str(i) + " Location:").grid(row=i + soldiers_count + enemies_count + 1)
            base_x = Entry(master, width=5)
            base_x.grid(row=i + soldiers_count + enemies_count + 1, column=1)
            base_y = Entry(master, width=5)
            base_y.grid(row=i + soldiers_count + enemies_count + 1, column=2)
            location = [base_x, base_y]
            base_locations.append(location)


if __name__ == '__main__':
    master = Tk()
    app = BaseLoader(master)
    master.mainloop()

    #
    #
    # # TODO
    # # Friendly agents
    # F_ACTORS = 4  # Number of agents in the team
    # F_START_LOC = ["0,1","0,8","9,1","9,8"]  # Starting locations for each agent
    # F_GOAL_LOC = ["2,2","2,7","7,2","7,7"]  # Objectives the agents need to visit to win
    #
    # # Enemy agents
    # E_ACTORS = 4  # Number of agents in the team
    # E_START_LOC = ["2,2","2,7","7,2","7,7"]
    # E_PATROL_RANGE = 5
    #
    # # Distractor agents
    # D_ACTORS = 4
    # D_START_LOC = ["0,0","0,9","9,0","9,9"]  # Base location, also the start location of distractor
    #
    # # Reward weights - variables
    # BASE = [0.5, 0.2]  # Minimize distractor and enemy distance, minimize distractor cost
    # DISTRACTOR = [-1.0]  # Minimize agent and enemy distance
    # ENEMY = [0.5, 0.5,
    #          -1.0]  # Minimize agent and enemy distance, minimize enemy and distractor distance, minimize agent and goal distance
    # AGENT = [0.5, -0.5]  # Minimize agent and goal distance, maximize agent and enemy distance
    #
    #
    # def set_map_size(x, y):
    #     MAP_SIZE_X = x  # X value of map dimension
    #     MAP_SIZE_Y = y  # Y value of map dimension
    #     SCREEN_WIDTH = (MAP_SIZE_X) * 32
    #     SCREEN_HEIGHT = (MAP_SIZE_Y) * 32


    #
    #
    # # Begin pyglet visualization code #
    # pyglet.resource.path = ['../resources']
    # pyglet.resource.reindex()
    #
    # window = pyglet.window.Window(resizable=True)
    # window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
    #
    # tile_image = pyglet.resource.image("grass.png")
    # tiles_batch = pyglet.graphics.Batch()
    # tiles = []
    # for y in range(0, MAP_SIZE_Y):
    #     for x in range(0, MAP_SIZE_X):
    #         tiles.append(pyglet.sprite.Sprite(
    #             img=tile_image,
    #             x=x * 32,
    #             y=y * 32,
    #             batch=tiles_batch)
    #         )
    #
    # goal_image = pyglet.resource.image("target.png")
    # goals_batch = pyglet.graphics.Batch()
    # goals = []
    # for index in range(0, len(F_GOAL_LOC)):
    #     goals.append(pyglet.sprite.Sprite(
    #         img=goal_image,
    #         x=f_get_goal_x(index) * 32,
    #         y=f_get_goal_y(index) * 32,
    #         batch=goals_batch)
    #     )
    #
    # agent_image = pyglet.resource.image("soldier_blue.png")
    # agents_batch = pyglet.graphics.Batch()
    # agents = []
    # for index in range(0, F_ACTORS):
    #     agents.append(pyglet.sprite.Sprite(
    #         img=agent_image,
    #         x=f_get_start_x(index) * 32,
    #         y=f_get_start_y(index) * 32,
    #         batch=agents_batch)
    #     )
    #
    # enemy_image = pyglet.resource.image("soldier_red.png")
    # enemies_batch = pyglet.graphics.Batch()
    # enemies = []
    # for index in range(0, E_ACTORS):
    #     enemies.append(pyglet.sprite.Sprite(
    #         img=enemy_image,
    #         x=e_get_start_x(index) * 32,
    #         y=e_get_start_y(index) * 32,
    #         batch=enemies_batch)
    #     )
    #
    # distractor_image = pyglet.resource.image("heli.png")
    # base_image = pyglet.resource.image("base.png")
    # allies_batch = pyglet.graphics.Batch()
    # bases = []
    # distractors = []
    # for index in range(0, D_ACTORS):
    #     bases.append(pyglet.sprite.Sprite(
    #         img=base_image,
    #         x=d_get_start_x(index) * 32,
    #         y=d_get_start_y(index) * 32,
    #         batch=allies_batch)
    #     )
    #     distractors.append(pyglet.sprite.Sprite(
    #         img=distractor_image,
    #         x=d_get_start_x(index) * 32,
    #         y=d_get_start_y(index) * 32,
    #         batch=allies_batch)
    #     )
    #
    # @window.event
    # def on_draw():
    #     window.clear()
    #     tiles_batch.draw()
    #     goals_batch.draw()
    #     agents_batch.draw()
    #     enemies_batch.draw()
    #     allies_batch.draw()
    #
    # pyglet.app.run()
