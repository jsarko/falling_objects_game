import random

import pygame

from models import Player, FallingObject, Button, ImageButton
from events import CREATE_NEW_FALLING_OBJECT_EVENT
from helpers import is_object_offscreen

# pygame setup
pygame.init()
pregame = True
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
gravity = True
dt = 0
boundary_x = (0, 1280)
boundary_y = (0, 720)
PLAYER_SPEED = 700
falling_objs = []

# Init Assets
scoreboard = pygame.transform.scale(
    pygame.image.load("assets/sign.png").convert_alpha(), (100, 100)
)
bg = pygame.transform.scale(pygame.image.load(
    "assets/bg_jungle.jpg").convert_alpha(), (1280, 720))
font = pygame.font.SysFont('Comic Sans MS', 40, pygame.font.Font.bold)
player_image = pygame.transform.scale(
    pygame.image.load("assets/pixel_bubz_64.png").convert_alpha(), (120, 120)
)

# Initialize Player
player_start_pos = pygame.Vector2(
    screen.get_width() / 2, screen.get_height() - 200)
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


def start_game():
    global pregame
    pregame = False


start_button = Button(
    x=screen.get_width() / 2 - 100,
    y=screen.get_height() / 2 + 200,
    width=300,
    height=100,
    text="Start Game",
    font=font,
    text_color="black",
    bg_color="blue",
    hover_color="red",
    click_color="darkred",
    action=start_game)

player_button = ImageButton(
    x=screen.get_width() / 2 - 50,
    y=screen.get_height() / 2 - 50,
    width=120,
    height=120,
    image=player_image,
    action=lambda: print("Clicked player")
)


def pregame_loop(screen=screen, font=font):
    screen.fill("white")
    chose = pygame.font.Font.render(
        font, "Choose Player", True, "black")
    screen.blit(chose, (screen.get_width() / 2 -
                125, screen.get_height() / 2 - 300))

    # screen.blit(player.image, (screen.get_width() / 2 - 50,
    #                            screen.get_height() / 2 - 50))
    player_button.draw(screen)

    start_button.draw(screen)


def main_loop(screen=screen, font=font, falling_objs=falling_objs):
    screen.blit(bg, (0, 0))
    screen.blit(scoreboard, (40, 100))

    score = pygame.font.Font.render(
        font, str(player.score), True, "black")
    screen.blit(score, (75, 125))
    player.draw(screen)

    # Render Falling objects and check for obj events
    for obj in falling_objs:
        obj.update(dt)
        if is_object_offscreen(obj, screen):
            falling_objs.remove(obj)
        elif obj.is_collision(player):
            falling_objs.remove(obj)
            player.score += 1
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


while running:
    if pregame:
        pregame_loop()
    else:
        main_loop()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        start_button.handle_event(event)
        player_button.handle_event(event)
        if event.type == pygame.QUIT:
            running = False
        elif pregame is False:
            if event.type == CREATE_NEW_FALLING_OBJECT_EVENT:
                # Create a new FallingObject
                new_object = FallingObject(
                    x=random.randrange(screen.get_width()),
                    y=object_start_pos.y
                )
                falling_objs.append(new_object)

    # fill the screen with a color to wipe away anything from last frame

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(120) / 1000

pygame.quit()
