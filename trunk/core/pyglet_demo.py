import pyglet

SCREEN_X = 10
SCREEN_WIDTH = (SCREEN_X + 1) * 32
SCREEN_Y = 10
SCREEN_HEIGHT = (SCREEN_Y + 1) * 32

pyglet.resource.path = ['Resources']
pyglet.resource.reindex()
agent_image = pyglet.resource.image("Soldiers/soldier_blue.png")
tile = pyglet.resource.image("Grass.png")

colors = {
    'black': (0, 0, 0, 255),
    'blue': (0, 0, 255, 255),
    'light_steel_blue': (176, 224, 230, 255),
    'silver': (192, 192, 192, 255),
    'lime': (159, 248, 63, 255),
    'white': (255, 255, 255, 255)}

window = pyglet.window.Window(resizable=True)
window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
pyglet.gl.glClearColor(*colors['white'])  # Set background color to white


@window.event
def on_draw():
    window.clear()
    # pyglet.gl.glColor4f(0, 0, 0, 1.0)
    # pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (0, 0, 1,
    #                                                      100)))
    agent = pyglet.sprite.Sprite(img=agent_image, x=0, y=0)

    for y in range(0, SCREEN_Y):
        y_index = y * 32

        for x in range(0, SCREEN_X):
            x_index = x * 32
            loc = str(x) + ',' + str(y)
            grid = pyglet.sprite.Sprite(img=tile, x=x_index, y=y_index)
            pyglet.gl.glClearColor(*colors['black'])
            label = pyglet.text.Label(loc, font_size=10, x=x_index, y=y_index)

            grid.draw()
            label.draw()
    agent.draw()


if __name__ == '__main__':
    pyglet.app.run()
