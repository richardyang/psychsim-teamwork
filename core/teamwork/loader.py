from Tkinter import *

master = Tk()
master.wm_title("Scenario Config")
Label(master, text="Map Size X").grid(row=0)
Label(master, text="Map Size Y").grid(row=1)
Label(master, text="Soldiers").grid(row=2, column=0)
Label(master, text="Enemies").grid(row=3, column=0)
Label(master, text="Bases").grid(row=4, column=0)

size_x = Entry(master)
size_y = Entry(master)
soldiers = Entry(master)
enemies = Entry(master)
bases = Entry(master)

size_x.grid(row=0, column=1)
size_y.grid(row=1, column=1)
soldiers.grid(row=2, column=1)
enemies.grid(row=3, column=1)
bases.grid(row=4, column=1)


def save_configuration():
    print("Size X: %s\nSize Y: %s\nSoldiers: %s\nEnemies: %s\nBases: %s" % (
    size_x.get(), size_y.get(), soldiers.get(), enemies.get(), bases.get()))

def load_default():
    size_x.insert(0, '5')

Button(master, text='Preview', command=save_configuration).grid(row=7, column=0, sticky=W, pady=4)
Button(master, text='Default', command=load_default).grid(row=7, column=1, sticky=W, pady=4)


mainloop( )

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


