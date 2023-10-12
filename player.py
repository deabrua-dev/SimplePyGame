import pygame
from laser import Laser


# Клас гравця
class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.spaceship_engines_on = pygame.image.load('graphics/spaceship-engines-on.png').convert_alpha()
        self.spaceship_engines_off = pygame.image.load('graphics/spaceship-engines-off.png').convert_alpha()

        self.image = self.spaceship_engines_off
        self.rect = self.image.get_rect(midbottom=(screen_width / 2, screen_height - 50))

        self.right_move = None
        self.left_move = None

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.lives = 3
        self.shield = 3

        self.speed_x = 7
        self.speed_y = 10

        self.blasters = pygame.sprite.Group()
        self.blaster_cooldown = 500
        self.blaster_time = 0
        self.ready = True

        self.blaster_sound = pygame.mixer.Sound('audio/fire.wav')
        self.blaster_sound.set_volume(0.1)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.top > 5:
            self.rect.y -= self.speed_y
            self.image = self.spaceship_engines_on
        elif keys[pygame.K_s] and self.rect.bottom < self.screen_height - 10:
            self.rect.y += self.speed_y
            self.image = self.spaceship_engines_off
        elif keys[pygame.K_a] and self.rect.left > 5:
            self.rect.x -= self.speed_x
            self.image = self.spaceship_engines_on
        elif keys[pygame.K_d] and self.rect.right < self.screen_width - 10:
            self.rect.x += self.speed_x
            self.image = self.spaceship_engines_on
        else:
            self.image = self.spaceship_engines_off

        if keys[pygame.K_SPACE] and self.ready:
            self.blaster_shoot()
            self.ready = False
            self.blaster_time = pygame.time.get_ticks()
            self.blaster_sound.play()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.blaster_time >= self.blaster_cooldown:
                self.ready = True

    def blaster_shoot(self):
        self.blasters.add(Laser(self.rect.topright, self.screen_height, -15, 'cyan2'))
        self.blasters.add(Laser(self.rect.topleft, self.screen_height, -15, 'cyan2'))

    def update(self):
        self.get_input()
        self.recharge()
        self.blasters.update()
