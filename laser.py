import pygame


# Клас лазерного пострілу
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, screen_height, speed, color_name):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill(color_name)
        self.rect = self.image.get_rect(center=pos)

        self.speed = speed

        self.screen_height = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.screen_height + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()
