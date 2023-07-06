import random

import pygame

from models import FallingObject
from consts import FALLING_OBJ_IMAGES


def is_object_offscreen(obj: FallingObject, screen: pygame.Surface) -> bool:
    if obj.rect.y > screen.get_height():
        print(f"{obj}: is offscreen, destroying.")
        return True
    return False


def random_object_image() -> str:
    rand_n = random.randrange(len(FALLING_OBJ_IMAGES))
    return FALLING_OBJ_IMAGES[rand_n]
