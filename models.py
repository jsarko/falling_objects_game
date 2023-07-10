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
        self.score = 0

    def update(self):
        pass


class FallingObject(GameObject):
    def __init__(self, x, y, image=""):
        super().__init__(x, y, self.get_image())
        self.speed = 200

    def get_image(self):
        from helpers import random_object_image
        img_path = random_object_image()
        img = pygame.transform.scale(
            pygame.image.load(img_path).convert_alpha(), (50, 50)
        )
        return img

    def update(self, dt: int) -> None:
        self.rect.y += self.speed * dt

    def is_collision(self, player: Player) -> bool:
        return self.rect.colliderect(player.rect)

    @staticmethod
    def set_timer(ms):
        pygame.time.set_timer(CREATE_NEW_FALLING_OBJECT_EVENT, ms)


class Button:
    def __init__(self, x, y, width, height, text, font, text_color, bg_color, hover_color, click_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.action = action
        self.hovered = False
        self.clicked = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.hovered = True
            else:
                self.hovered = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.clicked:
                self.clicked = False
                if self.action is not None:
                    self.action()

    def update(self):
        pass

    def draw(self, screen):
        if self.clicked:
            color = self.click_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.bg_color

        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class ImageButton(Button):
    def __init__(self, x, y, width, height, image, click_border_color=(255, 0, 0), action=None):
        super().__init__(x, y, width, height, "", None, None, None, None, None, action)
        self.image = image
        self.click_border_color = click_border_color

    def draw(self, screen):
        if self.clicked:
            pygame.draw.rect(screen, self.click_border_color, self.rect, 3)

        screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = not self.clicked
