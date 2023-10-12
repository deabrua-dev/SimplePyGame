from random import choice, randrange
from sys import exit

import pygame

from alienSpaceship import AlienSpaceship
from asteroid import Asteroid
from explosion import Explosion
from player import Player
from power import PowerUp


# Клас Гри
class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        player_sprite = Player(self.screen_width, self.screen_height)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.asteroids = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.explosions = pygame.sprite.Group()

        self.alien_timer = pygame.time.get_ticks()

        self.alien_direction_x = 1
        self.alien_direction_y = 1

        self.heart_red = pygame.image.load('graphics/heart-red-3x.png').convert_alpha()
        self.heart_grey = pygame.image.load('graphics/heart-grey-3x.png').convert_alpha()
        self.shield_surf = pygame.image.load('graphics/shield-3x.png').convert_alpha()

        self.score = 0

        self.font = pygame.font.Font('fonts/JetBrainsMonoNL-Bold.ttf', 70)
        self.font_top = pygame.font.Font('fonts/JetBrainsMonoNL-Bold.ttf', 50)
        self.font_mid = pygame.font.Font('fonts/JetBrainsMonoNL-Bold.ttf', 30)
        self.font_bot = pygame.font.Font('fonts/JetBrainsMonoNL-Bold.ttf', 20)

        self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
        self.explosion_sound.set_volume(0.04)
        self.game_active = False

        self.music = pygame.mixer.Sound('audio/music.mp3')
        self.music.set_volume(0.2)
        self.music.play(loops=-1)

    # Контроль гри
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] and self.game_active:
            self.game_active = False
            self.end()
        elif keys[pygame.K_TAB] and not self.game_active:
            self.game_active = True
            self.score = 0
            self.setup_objects()

    # Виклик меню
    def main_menu(self):
        back_surf = pygame.Surface((790, 590))
        back_surf.set_alpha(5)
        back_surf.fill('grey87')

        back_rect = back_surf.get_rect(topleft=(5, 5))
        screen.blit(back_surf, back_rect)
        if self.score == 0:
            game_name_surf = self.font.render('SOLO', False, 'gold')
            game_name_rect = game_name_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2))

            go_play_next_surf = self.font_bot.render('Press Tab to play...', False, 'gray89')
            go_play_next_rect = go_play_next_surf.get_rect(center=(self.screen_width / 2,
                                                                   self.screen_height / 2 +
                                                                   game_name_rect.height / 2))

            screen.blit(game_name_surf, game_name_rect)
            screen.blit(go_play_next_surf, go_play_next_rect)
        else:
            score_surf = self.font_mid.render(f'Your score: {self.score}', False, 'White')
            score_rect = score_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2))

            game_over_surf = self.font_top.render('Game Over', False, 'White')
            game_over_rect = game_over_surf.get_rect(center=(self.screen_width / 2,
                                                             self.screen_height / 2 - score_rect.height - 10))
            go_play_next_surf = self.font_bot.render('Press Tab to play...', False, 'gray89')
            go_play_next_rect = go_play_next_surf.get_rect(center=(self.screen_width / 2,
                                                                   self.screen_height / 2 + score_rect.height))

            screen.blit(game_over_surf, game_over_rect)
            screen.blit(score_surf, score_rect)
            screen.blit(go_play_next_surf, go_play_next_rect)

    # Відображення рівня здоров'я гравця
    def display_health_bar(self):
        x_offset = 10
        for i in range(3):
            screen.blit(self.heart_grey, (x_offset + 10, self.screen_height - self.heart_grey.get_height() - 10))
            x_offset += self.heart_grey.get_width() + 1
        x_offset = 10
        for i in range(self.player.sprite.lives):
            screen.blit(self.heart_red, (x_offset + 10, self.screen_height - self.heart_red.get_height() - 10))
            x_offset += self.heart_red.get_width() + 1
        x_offset = 10
        for i in range(self.player.sprite.shield):
            screen.blit(self.shield_surf, (x_offset + 10, self.screen_height - self.shield_surf.get_height() - 10))
            x_offset += self.shield_surf.get_width() + 1

    # Відображення кількості поінтів гравця
    def display_score(self):
        score_surf = self.font_mid.render(f'Score: {self.score}', False, 'White')
        score_rect = score_surf.get_rect(topleft=((self.screen_width - score_surf.get_width() - 10),
                                                  (self.screen_height - score_surf.get_height() - 10)))
        screen.blit(score_surf, score_rect)

    # Малюємо щит навколо корабля гравця
    def draw_shield(self):
        if self.player.sprite.shield > 0:
            pygame.draw.circle(screen, 'cyan3', (self.player.sprite.rect.center),
                               self.player.sprite.rect.width, width=2)

    # Створення ігрових обїектів
    def setup_objects(self):
        self.asteroid_setup()
        self.power_ups_setup()
        self.alien_setup()

    # Створення астероідів
    def asteroid_setup(self):
        for i in range(0, 5):
            asteroid = Asteroid(self.screen_width, self.screen_height)
            self.asteroids.add(asteroid)

    # Створення аптечок
    def power_ups_setup(self):
        for i in range(0, 2):
            power = PowerUp(self.screen_width, self.screen_height, randrange(0, 2))
            self.power_ups.add(power)

    # Підвищення рівня щита гравця
    def add_shield(self):
        print('Plus Ultra!!!')
        if self.player.sprite.shield < 3:
            self.player.sprite.shield += 1
        power = PowerUp(self.screen_width, self.screen_height, randrange(0, 2))
        self.power_ups.add(power)

    # Підвищення рівня здоров'я гравця
    def add_live(self):
        print('Add one heart')
        if self.player.sprite.lives < 3:
            self.player.sprite.lives += 1
        power = PowerUp(self.screen_width, self.screen_height, randrange(0, 2))
        self.power_ups.add(power)

    # Створення кораблів прибульців
    def alien_setup(self):
        x_offset = 96
        y_offset = 75
        for i in range(0, 5):
            alien = AlienSpaceship((x_offset, y_offset), self.screen_height)
            self.aliens.add(alien)
            x_offset += (alien.rect.width + 100)
            if i < 2:
                y_offset += 25
            else:
                y_offset -= 25

    # Виклик пострілу в прибульців
    def alien_shot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.alien_timer >= 400:
            self.alien_timer = current_time
            if self.aliens.sprites():
                alien = choice(self.aliens.sprites())
                alien.blaster_shoot()

    # Перевірка позицій прибульців, та коригування напрямку ії руху
    def aliens_position_check(self):
        for alien in self.aliens:
            if alien.rect.left <= -50 or alien.rect.right >= self.screen_width + 50:
                alien.speed_x = -alien.speed_x
            if alien.rect.bottom >= self.screen_height / 2 or alien.rect.top <= 10:
                alien.speed_y = -alien.speed_y

    # Перевірка колізій об'єктів
    def collision_checks(self):
        # Колізіі пострілів з бластера гравця з астероїдами та прибульцями
        if self.player.sprite.blasters:
            for blast in self.player.sprite.blasters:
                asteroids_hit = pygame.sprite.spritecollide(blast, self.asteroids, True)
                if asteroids_hit:
                    for asteroid in asteroids_hit:
                        self.score += asteroid.price
                    exp = Explosion(blast.rect.center)
                    self.explosions.add(exp)
                    blast.kill()
                    self.explosion_sound.play()
                    asteroid = Asteroid(self.screen_width, self.screen_height)
                    self.asteroids.add(asteroid)

                aliens_hit = pygame.sprite.spritecollide(blast, self.aliens, True)
                if aliens_hit:
                    self.score += (100 * len(aliens_hit))
                    exp = Explosion(blast.rect.center)
                    self.explosions.add(exp)
                    blast.kill()
                    self.explosion_sound.play()
                    alien = AlienSpaceship((randrange(50, 750), randrange(50, 100)), self.screen_height)
                    self.aliens.add(alien)

        # Колізії гравця з астероїдами, аптечками та прибульцями
        if self.player.sprite:
            player_asteroid_hit = pygame.sprite.spritecollide(self.player.sprite, self.asteroids, True)
            if player_asteroid_hit:
                for hit in player_asteroid_hit:
                    if self.player.sprite.shield > 0:
                        self.player.sprite.shield -= 1
                    elif self.player.sprite.lives > 0:
                        self.player.sprite.lives -= 1

                    if self.player.sprite.lives > 0:
                        print("-1 live")
                        exp = Explosion(hit.rect.center)
                        self.explosions.add(exp)
                        self.explosion_sound.play()
                        asteroid = Asteroid(self.screen_width, self.screen_height)
                        self.asteroids.add(asteroid)
                    else:
                        self.end()
                        print("Dead")
                    hit.kill()

            player_alien_hit = pygame.sprite.spritecollide(self.player.sprite, self.aliens, True)
            if player_alien_hit:
                for hit in player_alien_hit:
                    if self.player.sprite.shield > 0:
                        self.player.sprite.shield -= 1
                    elif self.player.sprite.lives > 0:
                        self.player.sprite.lives -= 1
                    if self.player.sprite.lives > 0:
                        print("-1 live")
                        exp = Explosion(hit.rect.center)
                        self.explosions.add(exp)
                        self.explosion_sound.play()
                        alien = AlienSpaceship((randrange(50, 750), randrange(50, 100)), self.screen_height)
                        self.aliens.add(alien)
                    else:
                        self.end()
                        print("Dead")
                    hit.kill()

            player_power_up_hit = pygame.sprite.spritecollide(self.player.sprite, self.power_ups, True)
            if player_power_up_hit:
                for hit in player_power_up_hit:
                    if hit.type == 1:
                        self.add_shield()
                    elif hit.type == 0:
                        self.add_live()
                    hit.kill()

        # Колізії пострілів прибульців з астероїдами та кораблем гравця
        if self.aliens:
            for alien in self.aliens:
                for blast in alien.blasters:
                    asteroid_alien_blaster_hit = pygame.sprite.spritecollide(blast, self.asteroids, True)
                    if asteroid_alien_blaster_hit:
                        exp = Explosion(blast.rect.center)
                        self.explosions.add(exp)
                        self.explosion_sound.play()
                        blast.kill()
                        asteroid = Asteroid(self.screen_width, self.screen_height)
                        self.asteroids.add(asteroid)
                player_alien_blaster_hit = pygame.sprite.spritecollide(self.player.sprite, alien.blasters, True)
                if player_alien_blaster_hit:
                    for hit in player_alien_blaster_hit:
                        exp = Explosion(hit.rect.center)
                        self.explosions.add(exp)
                        self.explosion_sound.play()
                        hit.kill()
                        if self.player.sprite.shield > 0:
                            self.player.sprite.shield -= 1
                        elif self.player.sprite.lives > 0:
                            self.player.sprite.lives -= 1
                        if self.player.sprite.lives > 0:
                            print("-1 live")
                            hit.kill()
                        else:
                            self.end()
                            hit.kill()
                            print("Dead")

    # Функція обнулення гри
    def end(self):
        self.explosion_sound.play()
        self.game_active = False
        self.player.sprite.lives = 3
        self.player.sprite.shield = 3
        self.player.sprite.rect.midbottom = (self.screen_width / 2, self.screen_height - 50)
        for blast in self.player.sprite.blasters:
            blast.kill()
        for asteroid in self.asteroids.sprites():
            asteroid.kill()
        for power_up in self.power_ups.sprites():
            power_up.kill()
        for alien in self.aliens.sprites():
            for blast in alien.blasters:
                blast.kill()
            alien.kill()
        for explosion in self.explosions.sprites():
            explosion.kill()

    # Функції роботи гри
    def run(self):
        if self.game_active:
            self.get_input()

            self.player.update()
            self.player.sprite.blasters.draw(screen)
            self.player.draw(screen)

            self.asteroids.update()
            self.asteroids.draw(screen)

            self.power_ups.update()
            self.power_ups.draw(screen)

            self.aliens_position_check()
            self.aliens.update()
            self.alien_shot()
            for alien in self.aliens:
                alien.blasters.draw(screen)
            self.aliens.draw(screen)

            self.collision_checks()

            self.explosions.update()
            self.explosions.draw(screen)

            self.display_score()
            self.display_health_bar()
            self.draw_shield()
        else:
            self.get_input()
            self.main_menu()


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('SOLO')
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    game = Game(WIDTH, HEIGHT)
    space = pygame.image.load('graphics/space.png').convert_alpha()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(space, (0, 0))
        game.run()

        pygame.display.flip()
        clock.tick(60)
