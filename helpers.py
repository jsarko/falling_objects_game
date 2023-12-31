import random

import pygame

from models import FallingObject
from consts import FALLING_OBJ_IMAGES


def is_object_offscreen(obj: FallingObject, screen: pygame.Surface) -> bool:
    if obj.rect.y > screen.get_height():
        return True
    return False


def random_object_image() -> str:
    rand_n = random.randrange(len(FALLING_OBJ_IMAGES))
    return FALLING_OBJ_IMAGES[rand_n]


def start_game():
    print("Starting game")
    global pregame
    pregame = False
