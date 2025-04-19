#Hadley Shuck
#Testing a new thing
#4/19/2025
import random
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Defense")

# Hide the mouse cursor
pygame.mouse.set_visible(False)

# Load and transform images
ROCKET_IMAGE = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load("images/ship2(no bg).png"), (50, 50)), 180
)
ENEMY_IMAGE = pygame.transform.scale(pygame.image.load("images/enemy_4.png"), (40, 40))
BULLET_IMAGE = pygame.transform.scale(pygame.image.load("images/beams.png"), (10, 5))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Rocket(pygame.sprite.Sprite):
    """A class to manage the player's rocket."""
    def __init__(self):
        """Initialize the rocket and set its starting position."""
        super().__init__()
        self.image = ROCKET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.right = WIDTH
        self.rect.centery = HEIGHT // 2
        self.speed = 5
    def update(self, *args, **kwargs):
        """Update the rocket's vertical position based on key input."""
        keys = kwargs.get('keys', None)
        if keys:
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed


class Enemy(pygame.sprite.Sprite):
    """A class to represent a moving enemy ship."""

    def __init__(self, x, y, speed):
        """Initialize the enemy with a position and speed."""
        super().__init__()
        self.image = ENEMY_IMAGE
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed

    def update(self, *args, **kwargs):
        """Update the rocket's vertical position based on key input."""
        keys = kwargs.get('keys', None)
        if keys:
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed


class Bullet(pygame.sprite.Sprite):
    """A class to manage bullets fired from the rocket."""

    def __init__(self, x, y, speed):
        """Create a bullet object at the rocket's current position."""
        super().__init__()
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self, *args, **kwargs):
        """Move the bullet leftward and remove it if off-screen."""
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


class Button:
    """A class to create and manage a clickable play button."""

    def __init__(self, x, y, width, height, text, font_size=30):
        """Initialize the button with position, size, and label."""
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 200, 0)
        self.text = text
        self.font = pygame.font.SysFont("Arial", font_size)
        self.text_image = self.font.render(text, True, WHITE)
        self.text_rect = self.text_image.get_rect(center=self.rect.center)

    def draw(self, surface):
        """Draw the button on the screen."""
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_image, self.text_rect)

    def is_clicked(self, mouse_pos):
        """Return True if the button is clicked."""
        return self.rect.collidepoint(mouse_pos)


def create_enemy_fleet(rows, cols, spacing_x, spacing_y, speed):
    """Generate a group of enemy ships in a grid formation."""
    enemies = pygame.sprite.Group()
    for row in range(rows):
        for col in range(cols):
            x = col * spacing_x
            y = row * spacing_y + 50
            enemy = Enemy(x, y, speed)
            enemies.add(enemy)
    return enemies


def reset_game(rocket, bullets, all_sprites, enemy_speed):
    """Reset the game state to its initial configuration."""
    rocket.rect.right = WIDTH
    rocket.rect.centery = HEIGHT // 2
    bullets.empty()
    enemies = create_enemy_fleet(3, 5, 80, 60, enemy_speed)
    all_sprites.empty()
    all_sprites.add(rocket)
    all_sprites.add(enemies)
    return enemies


def draw_hud(score, font):
    """Render and display the current score."""
    score_image = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_image, (10, 10))


def main():
    """Main game loop."""
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 36)

    rocket = Rocket()
    bullets = pygame.sprite.Group()
    enemy_speed = 1
    enemies = create_enemy_fleet(3, 5, 80, 60, enemy_speed)
    rocket = Rocket()  # Create a Rocket object
    all_sprites = pygame.sprite.Group()  # Create an empty sprite group
    all_sprites.add(rocket)             # Add the rocket to the group
    all_sprites.add(enemies)

    play_button = Button(WIDTH // 2 - 60, HEIGHT // 2 - 25, 120, 50, "Play")

    game_active = False
    score = 0

    while True:
        SCREEN.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif not game_active and event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(mouse_pos):
                    game_active = True
                    enemies = reset_game(rocket, bullets, all_sprites, enemy_speed)
                    score = 0
            elif game_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(rocket.rect.left, rocket.rect.centery, 7)
                    bullets.add(bullet)
                    all_sprites.add(bullet)

        if game_active:
            keys = pygame.key.get_pressed()
            rocket.update(keys)
            bullets.update()
            enemies.update()

            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            score += len(hits)

            for enemy in enemies:
                if enemy.rect.right >= WIDTH or enemy.rect.colliderect(rocket.rect):
                    game_active = False

            all_sprites.draw(SCREEN)
            draw_hud(score, font)
        else:
            play_button.draw(SCREEN)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
