import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = image
    
    def update(self):
        raise NotImplementedError("Subclasses must implement the update method.")


class Player(GameObject):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
    
    def update(self):
        pass

class FallingObject(GameObject):
    def __init__(self, image, x, y):
        super().__init__()
    
    def update(self):
        pass

