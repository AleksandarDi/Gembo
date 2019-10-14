import pygame
import math

projectile = pygame.image.load('Ball.png')


class Weapon(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((17, 17))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x - radius
        self.rect.y = y - radius

    def draw(self, window):
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        window.blit(projectile, (self.rect.x, self.rect.y))

    @staticmethod
    def ballPath(startX, startY, power, ang, time):
        angle = ang
        velX = math.cos(angle) * power
        velY = math.sin(angle) * power

        distX = velX * time
        distY = (velY * time) + ((-4.9 * (time ** 2)) / 2)

        newX = round(distX + startX)
        newY = round(startY - distY)

        return newX, newY
