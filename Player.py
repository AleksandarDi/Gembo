from Platforms import *

character1R = pygame.image.load('Ghost/IdleR.png')
character1L = pygame.image.load('Ghost/IdleL.png')
character1Right = [pygame.image.load('Ghost/RunR0.png'), pygame.image.load('Ghost/RunR1.png'),
                   pygame.image.load('Ghost/RunR2.png'), pygame.image.load('Ghost/RunR3.png'),
                   pygame.image.load('Ghost/RunR4.png'), pygame.image.load('Ghost/RunR5.png')]
character1Left = [pygame.image.load('Ghost/RunL0.png'), pygame.image.load('Ghost/RunL1.png'),
                  pygame.image.load('Ghost/RunL2.png'), pygame.image.load('Ghost/RunL3.png'),
                  pygame.image.load('Ghost/RunL4.png'), pygame.image.load('Ghost/RunL5.png')]
character1Death = [pygame.image.load('Ghost/DeathR0.png'), pygame.image.load('Ghost/DeathR1.png'),
                   pygame.image.load('Ghost/DeathR2.png'), pygame.image.load('Ghost/DeathR3.png'),
                   pygame.image.load('Ghost/DeathR4.png'), pygame.image.load('Ghost/DeathR5.png')]
character1LDeath = [pygame.image.load('Ghost/DeathL0.png'), pygame.image.load('Ghost/DeathL1.png'),
                    pygame.image.load('Ghost/DeathL2.png'), pygame.image.load('Ghost/DeathL3.png'),
                    pygame.image.load('Ghost/DeathL4.png'), pygame.image.load('Ghost/DeathL5.png')]
character2R = pygame.image.load('Alien/IdleR.png')
character2L = pygame.image.load('Alien/IdleL.png')
character2Right = [pygame.image.load('Alien/RunR0.png'), pygame.image.load('Alien/RunR1.png'),
                   pygame.image.load('Alien/RunR2.png'), pygame.image.load('Alien/RunR3.png'),
                   pygame.image.load('Alien/RunR4.png'), pygame.image.load('Alien/RunR5.png')]
character2Left = [pygame.image.load('Alien/RunL0.png'), pygame.image.load('Alien/RunL1.png'),
                  pygame.image.load('Alien/RunL2.png'), pygame.image.load('Alien/RunL3.png'),
                  pygame.image.load('Alien/RunL4.png'), pygame.image.load('Alien/RunL5.png')]
character2Death = [pygame.image.load('Alien/DeathR0.png'), pygame.image.load('Alien/DeathR1.png'),
                   pygame.image.load('Alien/DeathR2.png'), pygame.image.load('Alien/DeathR3.png'),
                   pygame.image.load('Alien/DeathR4.png'), pygame.image.load('Alien/DeathR5.png')]
character2LDeath = [pygame.image.load('Alien/DeathL0.png'), pygame.image.load('Alien/DeathL1.png'),
                    pygame.image.load('Alien/DeathL2.png'), pygame.image.load('Alien/DeathL3.png'),
                    pygame.image.load('Alien/DeathL4.png'), pygame.image.load('Alien/DeathL5.png')]
vec = pygame.math.Vector2
platforms = pygame.sprite.Group()
for plat in PLATFORM_LIST_LEFT:
    p = Platform(*plat)
    platforms.add(p)
for plat in PLATFORM_LIST_RIGHT:
    p = Platform(*plat)
    platforms.add(p)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.pos = vec(x, y)
        self.width = width
        self.height = height
        self.health = 100
        self.healthbarWidth = 32
        self.sp = 5
        self.vel = vec(0, 0)
        self.healthbarColor = (0, 255, 0)
        self.healthbarImage = pygame.Surface((self.healthbarWidth, 3))
        self.healthbar = self.healthbarImage.get_rect()
        self.image = pygame.Surface((29, 45))
        self.rect = self.image.get_rect()
        self.rect.x = x - 1
        self.rect.y = y + 1
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.deathCount = 0
        self.side = True
        self.characterRight = []
        self.characterLeft = []
        self.characterIdleR = []
        self.characterIdleL = []

    # Checks for collisions and helps with jumping
    def collide(self, spriteGroup, IhitMyHead):
        global blockSubtract, characterSubtract
        blockSubtract = 0
        characterSubtract = 0
        hits = pygame.sprite.spritecollide(self, spriteGroup, False)
        if self.vel.y != 0:
            if len(hits) == 1:
                if self.vel.y < 0 and (self.rect.bottom > hits[0].rect.bottom):
                    self.vel.y = 0
                    IhitMyHead = True
                    blockSubtract = hits[0].rect.bottom
                    characterSubtract = self.rect.top
                else:
                    self.pos.y = hits[0].rect.top - 45
                    self.vel.y = 0
                    self.isJump = False
            elif len(hits) > 1:
                if self.vel.y < 0 and (self.rect.bottom > hits[0].rect.bottom):
                    self.vel.y = 0
                    IhitMyHead = True
                    blockSubtract = hits[0].rect.bottom
                    characterSubtract = self.rect.top
                elif hits[0].rect.top > hits[1].rect.top:
                    self.pos.y = hits[1].rect.top - 45
                    self.vel.y = 0
                    self.isJump = False
                else:
                    self.pos.y = hits[0].rect.top - 45
                    self.vel.y = 0
                    self.isJump = False
            else:
                if self.vel.y < 25:
                    self.vel.y = self.vel.y + 0.5 * 10
                self.pos.y += self.vel.y
        elif self.vel.y == 0 and not hits:
            self.vel.y = self.vel.y + 0.5 * 10
        if IhitMyHead:
            self.pos.y += blockSubtract - characterSubtract

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -20

    def draw(self, window):
        # Draw character and moving animation
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.right:
            self.side = True
            window.blit(self.characterRight[self.walkCount // 5], (self.pos.x, self.pos.y))
            self.walkCount += 1
        elif self.left:
            self.side = False
            window.blit(self.characterLeft[self.walkCount // 5], (self.pos.x, self.pos.y))
            self.walkCount += 1
        else:
            if self.side:
                window.blit(self.characterIdleR, (self.pos.x, self.pos.y))
            else:
                window.blit(self.characterIdleL, (self.pos.x, self.pos.y))
        # Update position
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y + 1
        # draw Health bar
        self.healthbarImage = pygame.Surface((self.healthbarWidth, 3))
        self.healthbar = self.healthbarImage.get_rect()
        self.healthbar.x = self.pos.x
        self.healthbar.y = self.pos.y - 6
        outerLayer = pygame.Surface((31, 5))
        blackness = outerLayer.get_rect()
        blackness.x = self.pos.x - 1
        blackness.y = self.pos.y - 7
        pygame.draw.rect(window, (0, 0, 0), blackness)
        pygame.draw.rect(window, self.healthbarColor, self.healthbar)

    # Draws the death animation
    def drawDeath(self, window, charD):
            characterDeath = charD
            window.blit(characterDeath[self.deathCount], (self.pos.x, self.pos.y))
            self.pos.y += 2
            pygame.display.update()
            self.deathCount += 1


class PlayerSprites(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
