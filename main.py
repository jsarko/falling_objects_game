import random

import pygame

from models import Player, FallingObject, Button, ImageButton
from events import CREATE_NEW_FALLING_OBJECT_EVENT
from helpers import is_object_offscreen

# pygame setup
pygame.init()
pregame = True
postgame = False
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
gravity = True
dt = 0
boundary_x = (0, 1280)
boundary_y = (0, 720)
PLAYER_SPEED = 700
falling_objs = []
start_time = 0
time_limit = 20  # seconds
global remaining_time
remaining_time = time_limit

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
countdown = pygame.transform.scale(pygame.image.load(
    "assets/hanging_sign.png").convert_alpha(), (150, 150)
)

# Init music
pregame_music = pygame.mixer.music.load("assets/pregame_music.mp3")
# main_music = pygame.mixer.usic.load("assets/main_music.mp3")

# current_track = pregame_music
pygame.mixer.music.play()

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
    global start_time
    pregame = False
    start_time = pygame.time.get_ticks()
    pygame.mixer.music.load("assets/main_music.mp3")
    pygame.mixer.music.play()


def replay_game():
    global pregame
    global postgame
    global remaining_time
    remaining_time = time_limit
    pregame = not pregame
    postgame = not postgame
    pygame.mixer.music.load("assets/pregame_music.mp3")
    pygame.mixer.music.play()


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

replay_button = Button(
    x=screen.get_width() / 2 - 100,
    y=screen.get_height() / 2 + 200,
    width=300,
    height=100,
    text="Play Again",
    font=font,
    text_color="black",
    bg_color="blue",
    hover_color="red",
    click_color="darkred",
    action=replay_game)

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


def postgame_loop(screen=screen, font=font):
    screen.fill("white")
    final_score = pygame.font.Font.render(
        font, f"Final Score: {player.score}", True, "black")
    screen.blit(final_score, (screen.get_width() / 2 -
                125, screen.get_height() / 2 - 300))

    replay_button.draw(screen)


def main_loop(screen=screen, font=font, falling_objs=falling_objs):
    # TODO: Move blits to GameObject.draw(). Add center bool param to draw() that will center the object
    # on screen in regards to the objects size. Add optional offset param as well that takes x, y values.

    # TODO: Add method to center a rect within another rect

    screen.blit(bg, (0, 0))
    screen.blit(scoreboard, (40, 100))
    screen.blit(countdown, (screen.get_width() / 2 - 75, -30))

    # TODO: Move to separate function
    global remaining_time
    remaining_time = time_limit - \
        (pygame.time.get_ticks() - start_time) // 1000
    countdown_text = f"{remaining_time // 60}:{'0' if len(str(remaining_time)) == 1 else ''}{remaining_time % 60}"
    time = pygame.font.Font.render(font, str(countdown_text), True, "black")
    screen.blit(time, (screen.get_width() / 2 - 40, 40))

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
    if postgame:
        postgame_loop()
    elif pregame:
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
        elif pregame is False and postgame is False:
            if postgame:
                replay_button.handle_event(event)
            if event.type == CREATE_NEW_FALLING_OBJECT_EVENT:
                # Create a new FallingObject
                new_object = FallingObject(
                    x=random.randrange(screen.get_width()),
                    y=object_start_pos.y
                )
                falling_objs.append(new_object)

    if (remaining_time < 0
        and not pregame
            and not postgame):
        pygame.mixer.music.load("assets/postgame_music.mp3")
        pygame.mixer.music.play()
        postgame = True
    # fill the screen with a color to wipe away anything from last frame

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(120) / 1000

pygame.quit()
