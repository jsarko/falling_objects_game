import pygame

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

# Move to helpers
def should_render(pos: tuple) -> bool:
    return True if pos.y < boundary_y[1] - 200 else False

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 150)
player_img = pygame.transform.scale(
    pygame.image.load("assets/pixel_bubz_64.png"), (150, 150)
) # Turtle pixel head

# object_pos = (600, boundary_y[0], 100, 100) # from_left from_top width height
object_pos = pygame.Vector2(screen.get_width() / 2, 0)
object_img = pygame.transform.scale(
    pygame.image.load("assets/frisbee_pixel.png"), (100, 100)
)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # Player
    # pygame.draw.circle(screen, "yellow", center=player_pos, radius=40)
    screen.blit(player_img, (player_pos.x, player_pos.y))

    # Falling object loop
    objs = []
    # Render falling objects
    if should_render(object_pos):
        # pygame.draw.rect(screen, "red", (*object_pos, 100, 100))
        screen.blit(object_img, (object_pos))
        
        # Apply gravity to falling objects
        if gravity:
            object_pos.y += 1

    # Movement

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_pos.x > (boundary_x[0] + 45): 
        player_pos.x -= PLAYER_SPEED * dt
        moving = -1

    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_pos.x < (boundary_x[1] - 43): 
        player_pos.x += PLAYER_SPEED * dt
        moving = 1
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()