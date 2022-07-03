from random import randrange, choice

import pygame


# Клас астероїдів
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.asteroid_img_1 = pygame.image.load('graphics/asteroid-1.png').convert_alpha()
        self.asteroid_img_2 = pygame.image.load('graphics/asteroid-2.png').convert_alpha()
        self.asteroids = [self.asteroid_img_1, self.asteroid_img_2]
        self.random_image = choice(self.asteroids)

        self.size = randrange(0, 10)
        self.price = 10

        if self.size > 5:
            self.random_image = pygame.transform.smoothscale(self.random_image, (self.random_image.get_width() * 2, self.random_image.get_height() * 2))
            self.price = 25

        self.image = self.random_image

        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, self.screen_width - self.rect.width)
        self.rect.y = randrange(-150, -100)

        self.speed_x = randrange(-3, 3)
        self.speed_y = randrange(2, 10)

        self.rotation = 0
        self.rotation_speed = randrange(-4, 4)
        self.update_time = pygame.time.get_ticks()

    def rotate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.update_time > 50:
            self.update_time = current_time
            self.rotation = (self.rotation + self.rotation_speed) % 360

            new_image = pygame.transform.rotate(self.random_image, self.rotation)
            old_center = self.rect.center

            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top > self.screen_height + 60 or self.rect.left < -60 or self.rect.right > self.screen_width + 60:
            self.rect.x = randrange(0, self.screen_width - self.rect.width)
            self.rect.y = randrange(-150, -100)
            self.speed_y = randrange(2, 10)
