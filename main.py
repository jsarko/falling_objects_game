import random

import pygame

from models import Player, FallingObject
from events import CREATE_NEW_FALLING_OBJECT_EVENT
from helpers import is_object_offscreen

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
gravity = True
dt = 0
boundary_x = (0, 1280)
boundary_y = (0, 720)
PLAYER_SPEED = 500

falling_objs = []


# Initialize Player
player_start_pos = pygame.Vector2(
    screen.get_width() / 2, screen.get_height() - 150)
player_image = pygame.transform.scale(
    pygame.image.load("assets/pixel_bubz_64.png"), (150, 150)
)
player = Player(image=player_image, x=player_start_pos.x, y=player_start_pos.y)


# Initialize falling objects
object_start_pos = pygame.Vector2(
    random.randrange(screen.get_width()), 0
)
obj = FallingObject(
    x=object_start_pos.x,
    y=object_start_pos.y
)
obj.set_timer(1000)
falling_objs.append(obj)
# Main game loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == CREATE_NEW_FALLING_OBJECT_EVENT:
            # Create a new FallingObject
            new_object = FallingObject(
                x=random.randrange(screen.get_width()),
                y=object_start_pos.y
            )
            falling_objs.append(new_object)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # Draw Player

    # TODO: replace with player.draw()
    # screen.blit(player.image, player.rect)
    player.draw(screen)

    # Render Falling objects and check for obj events
    for obj in falling_objs:
        obj.update(dt)
        if is_object_offscreen(obj, screen):
            falling_objs.remove(obj)
        elif obj.is_collision(player):
            falling_objs.remove(obj)
        else:
            obj.draw(screen)

    # Movement
    keys = pygame.key.get_pressed()
    # LEFT key pressed AND player is in bounds
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.rect.x > (boundary_x[0] + 45):
        # TODO: replace with player.update()
        player.rect.x -= PLAYER_SPEED * dt
        moving = -1

    # RIGHT key pressed AND player is in bounds
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.rect.x < (boundary_x[1] - 43):
        player.rect.x += PLAYER_SPEED * dt
        moving = 1

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
