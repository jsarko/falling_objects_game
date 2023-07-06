import pygame
from models import FallingObject


def is_object_offscreen(obj: FallingObject, screen: pygame.Surface) -> bool:
    if obj.rect.y > screen.get_height():
        print(f"{obj}: is offscreen, destroying.")
        return True
    return False
