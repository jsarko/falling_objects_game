import pygame
from events import CREATE_NEW_FALLING_OBJECT_EVENT


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        raise NotImplementedError(
            "Subclasses must implement the update method.")


class Player(GameObject):
    def __init__(self, image, x, y):
        super().__init__(x, y, image)

    def update(self):
        pass


class FallingObject(GameObject):
    def __init__(self, image, x, y):
        super().__init__(x, y, image)
        self.speed = 400

    def update(self, dt):
        self.rect.y += self.speed * dt

    @staticmethod
    def set_timer(ms):
        pygame.time.set_timer(CREATE_NEW_FALLING_OBJECT_EVENT, ms)
