from random import randrange, choice

import pygame


# Клас аптечок
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, type):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.type = type

        self.health_power = pygame.image.load('graphics/health-power.png').convert_alpha()
        self.shield_power = pygame.image.load('graphics/shield-power.png').convert_alpha()
        self.powers = [self.health_power, self.shield_power]

        self.image = self.powers[self.type]
        self.rect = self.image.get_rect()

        self.rect.x = randrange(0, self.screen_width - self.rect.width)
        self.rect.y = randrange(-150, -100)

        self.speed_x = randrange(-2, 2)
        self.speed_y = randrange(2, 4)

        self.price = 5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top > self.screen_height + 60 or self.rect.left < -60 or self.rect.right > self.screen_width + 60:
            self.rect.x = randrange(0, self.screen_width - self.rect.width)
            self.rect.y = randrange(-150, -100)
            self.speed_x = randrange(-2, 2)
            self.speed_y = randrange(2, 4)
