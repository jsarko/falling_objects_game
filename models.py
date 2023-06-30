from pygame import Vector2

class BaseObject:
    self.pos = pygame.Vector2(
        screen.get_width() / 2, 
        screen.get_height() /2
    )

    def move(self):
        pass
    
    def draw(self):
        pass

class Player(BaseObject):
    self.player_pos = pygame.Vector2(
        screen.get_width() / 2, 
        screen.get_height() - 150
    )
    self.player_img = pygame.transform.scale(
        pygame.image.load("assets/pixel_bubz_64.png"), 
        (150, 150)
    )