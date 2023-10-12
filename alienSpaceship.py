from random import randrange

import pygame

from laser import Laser


# Клас прибульців
class AlienSpaceship(pygame.sprite.Sprite):
    def __init__(self, pos, screen_height):
        super().__init__()

        self.screen_height = screen_height

        self.image = pygame.image.load('graphics/alien-spaceship-2x.png')
        self.rect = self.image.get_rect(center=pos)

        self.speed_x = randrange(1, 3)
        self.speed_y = randrange(1, 3)

        self.blasters = pygame.sprite.Group()
        self.blaster_cooldown = 1000
        self.blaster_time = pygame.time.get_ticks()
        self.ready = True

        self.blaster_sound = pygame.mixer.Sound('audio/fire.wav')
        self.blaster_sound.set_volume(0.05)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def blaster_shoot(self):
        if self.ready:
            self.blasters.add(Laser(self.rect.midbottom, self.screen_height, 10, 'red'))
            self.blaster_sound.play()
            self.blaster_time = pygame.time.get_ticks()
            self.ready = False

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.blaster_time >= self.blaster_cooldown:
                self.ready = True

    def update(self):
        self.recharge()
        self.move()
        self.blasters.update()
