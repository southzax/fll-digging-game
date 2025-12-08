# player.py - The player character (the archaeologist!)
# This file has the Man class that handles moving and drawing the player.

import pygame


class Man(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, screen):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.screen = screen
        img = pygame.image.load("img/player/MAN.png")
        self.image = pygame.transform.scale(
            img, (int(img.get_width() * scale), int(img.get_height() * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.direction = 1

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
