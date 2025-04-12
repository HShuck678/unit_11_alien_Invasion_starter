import sys
import pygame
from pygame.sprite import Sprite, Group

class Ship(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        original_image = pygame.image.load("images/ship.png")
        # Scale the image down to 64x64 pixels (or adjust these numbers as needed)
        scaled_image = pygame.transform.scale(original_image, (64, 64))
        self.image = pygame.transform.rotate(scaled_image, 90)  # Rotate to face left
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centery = self.screen_rect.centery
        self.rect.right = self.screen_rect.right

        self.moving_up = False
        self.moving_down = False

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= 5
        if self.moving_down:
            # Check if moving down would put the ship past the screen bottom
            if self.rect.bottom + 5 <= self.screen_rect.bottom:
                self.rect.y += 5

    def blitme(self):
        self.screen.blit(self.image, self.rect)

class Bullet(Sprite):
    def __init__(self, screen, ship):
        super().__init__()
        self.screen = screen
        original_image = pygame.image.load("images/laserBlast.png")
        self.image = pygame.transform.rotate(original_image, 90)  # Rotate to face left
        self.rect = self.image.get_rect()
        # Make hitbox slightly smaller by adjusting the rect
        self.rect.inflate_ip(-4, -4)  # Reduces width and height by 4 pixels on each side
        self.rect.centery = ship.rect.centery
        self.rect.right = ship.rect.left
        self.speed = 7

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.rect.x -= self.speed

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)

class Alien(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("images/enemy_4.png")
        self.rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 800))
        pygame.display.set_caption("Alien Invasion Horizontal")
        self.bg_color = (30, 30, 30)

        self.ship = Ship(self.screen)
        self.bullets = Group()
        self.aliens = Group()

        self._create_fleet()

    def _create_fleet(self):
        alien = Alien(self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_y = self.screen.get_rect().height - 2 * alien_height
        number_aliens = available_space_y // (2 * alien_height)

        for alien_number in range(number_aliens):
            new_alien = Alien(self.screen)
            new_alien.rect.y = alien_height + 2 * alien_height * alien_number
            new_alien.rect.x = 100
            self.aliens.add(new_alien)

        self.fleet_direction = 1

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.ship.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = True
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.ship.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = False

    def _fire_bullet(self):
        if len(self.bullets) < 5:
            new_bullet = Bullet(self.screen, self.ship)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.right < 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    def _update_aliens(self):
        for alien in self.aliens.sprites():
            alien.rect.x += 1 * self.fleet_direction

        for alien in self.aliens.sprites():
            if alien.rect.right >= self.screen.get_rect().right or alien.rect.colliderect(self.ship.rect):
                self._reset_game()

    def _reset_game(self):
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.rect.centery = self.screen.get_rect().centery

    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
