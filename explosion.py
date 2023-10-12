import pygame


# Клас вибуху
class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        explosion_surf_1 = pygame.image.load('graphics/explosion-sprite-1.png').convert_alpha()
        explosion_surf_2 = pygame.image.load('graphics/explosion-sprite-2.png').convert_alpha()
        explosion_surf_3 = pygame.image.load('graphics/explosion-sprite-3.png').convert_alpha()

        self.explosion_sprites = [explosion_surf_1, explosion_surf_2, explosion_surf_3]
        self.image = self.explosion_sprites[0]
        self.rect = self.image.get_rect(center=pos)

        self.sprite_index = 0
        self.explosion_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.explosion_time > 60:
            self.explosion_time = current_time
            self.sprite_index += 1
            if self.sprite_index == len(self.explosion_sprites):
                self.kill()
            else:
                pos = self.rect.center
                self.image = self.explosion_sprites[self.sprite_index]
                self.rect = self.image.get_rect(center=pos)
