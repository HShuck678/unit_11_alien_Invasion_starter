import sys
import pygame
#Testing
from rocket import Rocket
from bullet import Bullet
from alien import Alien
if __name__ == '__main__':
    pass
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_UP, K_DOWN

pygame.init()


SCREEN_WIDTH = 700  
SCREEN_HEIGHT = 400 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Horizontal Alien Invasion")
        self.clock = pygame.time.Clock()

        self.rocket = Rocket(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            self.rocket.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.rocket.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.rocket.moving_down = True
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.rocket.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.rocket.moving_down = False

    def _fire_bullet(self):
        if len(self.bullets) < 5:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.right < 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    def _update_aliens(self):
        self.aliens.update()

        for alien in self.aliens.sprites():
            if alien.rect.right >= self.rocket.rect.left:
                self._reset_game()
            if alien.rect.right >= self.screen.get_width():
                self._reset_game()

    def _reset_game(self):
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.rocket.center_rocket()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_y = self.screen.get_height() - (2 * alien_height)
        number_aliens_y = available_space_y // (2 * alien_height)

        for alien_number in range(number_aliens_y):
            alien = Alien(self)
            alien.rect.y = alien_height + 2 * alien_height * alien_number
            alien.rect.x = 0
            self.aliens.add(alien)

    def _update_screen(self):
        self.screen.fill((30, 30, 30))
        self.rocket.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

  
    ship.update()


    DISPLAYSURF.fill((0, 0, 0))


    ship.blitme()


    pygame.display.update()

