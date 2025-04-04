import sys
import pygame
#Testing
if __name__ == '__main__':
    pass
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_UP, K_DOWN

pygame.init()


SCREEN_WIDTH = 700  
SCREEN_HEIGHT = 400 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Ship:
    
    def __init__(self, screen):
               
        self.screen = screen
        self.screen_rect = screen.get_rect()

        
        try:
            self.image = pygame.image.load('ship.png')
            self.image = pygame.transform.rotate(self.image, -90) 
        except pygame.error:
            print("Error: Could not load image. Make sure 'images/ship.bmp' exists.")
            sys.exit()

        self.rect = self.image.get_rect()

        
        self.rect.midleft = self.screen_rect.midleft

       
        self.moving_up = False
        self.moving_down = False

        
        self.speed = 5

    def update(self):
        
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.speed

    def blitme(self):
       
        self.screen.blit(self.image, self.rect)


ship = Ship(DISPLAYSURF)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                ship.moving_up = True
            elif event.key == K_DOWN:
                ship.moving_down = True
        elif event.type == KEYUP:
            if event.key == K_UP:
                ship.moving_up = False
            elif event.key == K_DOWN:
                ship.moving_down = False

  
    ship.update()


    DISPLAYSURF.fill((0, 0, 0))


    ship.blitme()


    pygame.display.update()

