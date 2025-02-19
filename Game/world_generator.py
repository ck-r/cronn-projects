import Block
import random

MAX_DEPTH = 64
WORLD_LENGTH = 256
START_DEPTH = 32


def generate_world():
    surface = START_DEPTH
    for x in range(WORLD_LENGTH):
        y = MAX_DEPTH
        while y >= MAX_DEPTH - surface:
            if y == MAX_DEPTH - surface:
                Block.postaw_blok(Block.TRAWA, x, y)
            elif y > MAX_DEPTH - surface + random.randrange(2, 4):
                Block.postaw_blok(Block.KAMIEN, x, y)
            else:
                Block.postaw_blok(Block.ZIEMIA, x, y)
            y -= 1
        surface += random.randrange(-1, 2)
    for x in range(WORLD_LENGTH):
        Block.postaw_blok(Block.BEDROCK, x, MAX_DEPTH + 1)
