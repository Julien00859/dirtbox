import logging
import math
import random
import types

import matplotlib.pyplot as plt
import pyglet
from pyglet.window import key

from dirtbox import world

logging.basicConfig(level='DEBUG')
logging.getLogger('matplotlib').setLevel('INFO')
logging.getLogger('PIL').setLevel('INFO')

WIDTH, HEIGHT = (800, 608)
X, Y, Z = (0, 1, 2)
BLOCK_SIZE = 16
WORLD_WIDTH = 200

game_window = pyglet.window.Window(WIDTH, HEIGHT)
keys = key.KeyStateHandler()
game_window.push_handlers(keys)

logging.debug('Indexing resources')
pyglet.resource.path = ["K:/Projects/dirtbox/resources",]
pyglet.resource.reindex()

def anchor_low_left(res):
    res.anchor_x = 0
    res.anchor_y = res.height
    return res

logging.debug('Loading resources')
block_bedrock = anchor_low_left(pyglet.resource.image('bedrock.png'))
block_dirt = anchor_low_left(pyglet.resource.image('dirt.png'))
block_grass = anchor_low_left(pyglet.resource.image('grass_block_side.png'))
block_stone = anchor_low_left(pyglet.resource.image('stone.png'))

ui_batch = pyglet.graphics.Batch()
terrain_batch = pyglet.graphics.Batch()

game_state = types.SimpleNamespace()


@game_window.event
def on_draw():
    game_window.clear()
    ui_batch.draw()
    terrain_batch.draw()

def move(dt):
    if keys[key.LEFT]:
        for sprite in game_state.sprites:
            sprite.x += BLOCK_SIZE
    elif keys[key.RIGHT]:
        for sprite in game_state.sprites:
            sprite.x -= BLOCK_SIZE



def main():
    logging.debug('Creating world')
    game_state.world = world.create_world(
        world_width=WORLD_WIDTH,
        min_height=5 * BLOCK_SIZE,
        max_height=HEIGHT - 5 * BLOCK_SIZE,
        block_size=BLOCK_SIZE,
        world_function=world.DEFAULT_WORLD_FUNCTION
    )

    if logging.root.isEnabledFor(logging.DEBUG):
        plt.plot(game_state.world)
        plt.ylim(0, HEIGHT)
        plt.show()

    game_state.sprites = []
    a = game_state.sprites.append

    logging.debug('Creating sprites')
    for x in range(0, WORLD_WIDTH * BLOCK_SIZE, BLOCK_SIZE):
        height = game_state.world[x // BLOCK_SIZE]

        a(pyglet.sprite.Sprite(block_bedrock, x=x, y=0, batch=terrain_batch))
        for y in range(16, height - 3 * BLOCK_SIZE, BLOCK_SIZE):
            a(pyglet.sprite.Sprite(block_stone, x=x, y=y, batch=terrain_batch))
        a(pyglet.sprite.Sprite(block_dirt, x=x, y=height - 3 * BLOCK_SIZE, batch=terrain_batch))
        a(pyglet.sprite.Sprite(block_dirt, x=x, y=height - 2 * BLOCK_SIZE, batch=terrain_batch))
        a(pyglet.sprite.Sprite(block_grass, x=x, y=height - BLOCK_SIZE, batch=terrain_batch))

    logging.debug('Running')
    pyglet.clock.schedule_interval(move, 1 / 20.0)
    pyglet.app.run()

main()