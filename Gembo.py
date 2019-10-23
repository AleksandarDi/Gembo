from Player import *
from Weapon import *
import random

# JUMPING HAS SMALL BUGS
# Setup code
global level, background, tiles, tilesX, tilesY, platforms
pygame.init()
pygame.display.set_caption("GEMBO")
win = pygame.display.set_mode((1200, 600), pygame.DOUBLEBUF)
menuBackground = pygame.image.load('MenuBackground.jpg')
myFont = pygame.font.SysFont('Comic Sans MS', 30)
largeFont = pygame.font.SysFont('Comic Sans MS', 50)
clock = pygame.time.Clock()
timer = pygame.time
fps = 27


# Menu loop
def MenuLoop():
    global level
    menuTrue = True
    showInstructions = False
    level = 1
    while menuTrue:
        clock.tick(fps)
        image = pygame.Surface((170, 30))
        startRect = image.get_rect()
        instructionsRect = image.get_rect()
        instructionsRect.x = 498
        instructionsRect.y = 360
        startRect.x = 498
        startRect.y = 310
        img = pygame.Surface((110, 30))
        goBackRect = img.get_rect()
        goBackRect.x = 1080
        goBackRect.y = 5
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.MOUSEBUTTONUP:
                if startRect.collidepoint(pygame.mouse.get_pos()) and not showInstructions:
                    menuTrue = False
                    MainLoop()
                if instructionsRect.collidepoint(pygame.mouse.get_pos()):
                    showInstructions = True
                if goBackRect.collidepoint(pygame.mouse.get_pos()) and showInstructions:
                    showInstructions = False
        if not showInstructions:
            drawMenuWindow()
        else:
            drawInstructionsWindow()


def MainLoop():
    # Main Loop
    global player, player1, players, player2, weapon, true, playerTime, isPlayerOne, shoot, hasShotOnce, shootTime, \
        power, angle, assignRole, isRightWall, isLeftWall, hitMyHead, startingPointForProjectileX, \
        startingPointForProjectileY, timeForPlayer, playerSpriteHead, playerSpriteBody, level, tilesY, tilesX, \
        strength, platforms
    # Setting the players starting health, character and position
    if level == 1:
        PlanetOneSetup()
    elif level == 2:
        PlanetTwoSetup(player1.wins, player2.wins)
    elif level == 3:
        if player1.wins != 2 or player2.wins != 2:
            PlanetThreeSetup(player1.wins, player2.wins)
    isPlayerOne = True
    shoot = False
    hasShotOnce = False
    shootTime = 0
    power = 0
    angle = 0
    assignRole = False
    isRightWall = False
    isLeftWall = False
    hitMyHead = False
    startingPointForProjectileX = weapon.x
    startingPointForProjectileY = weapon.y
    timeForPlayer = 10.3
    true = True
    start_time = timer.get_ticks() / 1000
    # Start main game loop
    while true:
        clock.tick(fps)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()
        # If a player falls off the map he dies
        if player.pos.y > 600:
            if isPlayerOne:
                player1.health = 0
                player2.wins += 1
                EndLoop()
            else:
                player2.health = 0
                player1.wins += 1
                EndLoop()
        elif not shoot:
            # PLAYER MOVING RIGHT
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.pos.x < 1200 - player.width - 5:
                hits = pygame.sprite.spritecollide(player, platforms, False)
                if len(hits) <= 1:
                    isRightWall = False
                    isLeftWall = False
                    player.pos.x += player.sp
                    player.right = True
                    player.left = False
                if len(hits) > 1:
                    if hits[0].rect.top > hits[1].rect.top:
                        if hits[1].rect.left < player.rect.right:
                            isRightWall = True
                    elif hits[0].rect.left < player.rect.right:
                        isRightWall = True
                    if isLeftWall:
                        isRightWall = False
                        player.pos.x += player.sp
                        player.right = True
                        player.left = False
            # PLAYER MOVING LEFT
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.pos.x > 0:
                hits = pygame.sprite.spritecollide(player, platforms, False)
                if len(hits) <= 1:
                    isRightWall = False
                    isLeftWall = False
                    player.pos.x -= player.sp
                    player.right = False
                    player.left = True
                if len(hits) > 1:
                    if hits[1].rect.top > hits[0].rect.top:
                        if hits[1].rect.right > player.rect.left:
                            isLeftWall = True
                    elif hits[0].rect.right > player.rect.left:
                        isLeftWall = True
                    if isRightWall:
                        isLeftWall = False
                        player.pos.x -= player.sp
                        player.right = False
                        player.left = True
            else:
                player.right = False
                player.left = False
            # SHOOTING
            # Line from weapon to mouse
            weapon.x = player.pos.x + 20
            weapon.y = player.pos.y + 30
            line = [(weapon.x, weapon.y), pygame.mouse.get_pos()]
            if keys[pygame.K_SPACE] and not player.isJump and not shoot and not hasShotOnce:
                startingPointForProjectileX = weapon.x
                startingPointForProjectileY = weapon.y
                pos = pygame.mouse.get_pos()
                shoot = True
                hasShotOnce = True
                if math.sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2) / 4 > 100:
                    power = 100 * strength
                else:
                    power = math.sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2) / 4 * strength
                angle = findAngle(pos)
            # JUMPING
            if not player.isJump and timer.get_ticks() / 1000 - start_time < timeForPlayer:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    player.jump(platforms)
                    player.isJump = True
                    player.right = False
                    player.left = False
                    player.walkCount = 0
        elif shoot:
            projectileCollide = pygame.sprite.spritecollide(weapon, platforms, False)
            playerCollide = pygame.sprite.spritecollide(weapon, players, False)
            # Check if the projectile has hit the enemy player and damage him
            if playerCollide:
                damage = 20
                healthCut = 7
                timeForPlayer = 5.4
                shoot = False
                start_time = timer.get_ticks() / 1000
                if isPlayerOne:
                    if playerCollide[0].rect[1] == player2.rect[1]:
                        damage = 40
                        healthCut = 13
                    player2.health -= damage
                    player2.healthbarWidth -= healthCut
                    if 40 < player2.health < 70:
                        player2.healthbarColor = (255, 255, 0)
                    if player2.health <= 40:
                        player2.healthbarColor = (255, 0, 0)
                    if player2.health <= 0:
                        player1.wins += 1
                        while player2.deathCount <= 5:
                            redrawGameWindow()
                            if player2.side:
                                player2.drawDeath(win, character2Death)
                            else:
                                player2.drawDeath(win, character2LDeath)
                        EndLoop()
                        true = False
                else:
                    if playerCollide[0].rect[1] == player1.rect[1]:
                        damage = 40
                        healthCut = 13
                    player1.health -= damage
                    player1.healthbarWidth -= healthCut
                    if 40 < player1.health < 70:
                        player1.healthbarColor = (255, 255, 0)
                    if player1.health <= 40:
                        player1.healthbarColor = (255, 0, 0)
                    if player1.health <= 0:
                        player2.wins += 1
                        while player1.deathCount <= 5:
                            redrawGameWindow()
                            if player1.side:
                                player1.drawDeath(win, character1Death)
                            else:
                                player1.drawDeath(win, character1LDeath)
                        EndLoop()
                        true = False
            # If the projectile collides with a wall reset
            elif projectileCollide:
                timeForPlayer = 5.4
                start_time = timer.get_ticks() / 1000
                shoot = False
            # If projectile has not collided with anything keep moving
            elif weapon.y < 600 - weapon.radius and 0 < weapon.x < 1200:
                shootTime += 0.3
                po = Weapon.ballPath(startingPointForProjectileX, startingPointForProjectileY, power, angle, shootTime)
                weapon.x = po[0]
                weapon.y = po[1]
            # If projectile out of screen reset and switch player
            else:
                timeForPlayer = 5.4
                shoot = False
                start_time = timer.get_ticks() / 1000
        # Checks which players turn it is and assigns him the role - Reset the shoot, start time, player time
        if assignRole:
            shootTime = 0
            hasShotOnce = False
            isPlayerOne = not isPlayerOne
            timeForPlayer = 10.3
            players.empty()
            if isPlayerOne:
                player = player1
                playerSpriteHead = PlayerSprites(player2.rect.x, player2.rect.y, 29, 22.5)
                playerSpriteBody = PlayerSprites(player2.rect.x, player2.rect.y + 22.5, 29, 22.5)
                players.add(playerSpriteHead)
                players.add(playerSpriteBody)
            else:
                player = player2
                playerSpriteHead = PlayerSprites(player1.rect.x, player1.rect.y, 29, 22.5)
                playerSpriteBody = PlayerSprites(player1.rect.x, player1.rect.y + 22.5, 29, 22.5)
                players.add(playerSpriteHead)
                players.add(playerSpriteBody)
            assignRole = False
            start_time = timer.get_ticks() / 1000
            if level == 2:
                strength = random.uniform(0.5, 1.5)
        # Set the time for a player
        playerTime = int(timeForPlayer - (timer.get_ticks() / 1000 - start_time))
        if timer.get_ticks() / 1000 - start_time > timeForPlayer and not shoot and not player.isJump:
            assignRole = True
        # Redraw the main game window
        redrawGameWindow()


def drawMenuWindow():
    win.blit(menuBackground, (0, 0))
    textSurface = myFont.render("Start Game", False, (255, 255, 255))
    win.blit(textSurface, (500, 300))
    textSurface = myFont.render("How to play", False, (255, 255, 255))
    win.blit(textSurface, (500, 350))
    pygame.display.update()


def drawInstructionsWindow():
    # Go Back
    win.blit(menuBackground, (0, 0))
    goBackCommand = myFont.render("Go Back", False, (255, 255, 255))
    win.blit(goBackCommand, (1080, 5))
    # Player 1 and Player 2
    playerOne = myFont.render("Player One - Ghost", False, (255, 255, 255))
    win.blit(playerOne, (200, 10))
    win.blit(character1R, (300, 60))
    playerTwo = myFont.render("Player Two - Alien", False, (255, 255, 255))
    win.blit(playerTwo, (600, 10))
    win.blit(character2R, (700, 60))
    # Commands for playing
    commands = myFont.render("Commands", False, (255, 255, 255))
    win.blit(commands, (10, 90))
    leftRightCommand = myFont.render("A,D or Left and Right Arrow key to move left and right", False, (255, 255, 255))
    win.blit(leftRightCommand, (20, 140))
    jumpCommand = myFont.render("W or Arrow key Up to jump", False, (255, 255, 255))
    win.blit(jumpCommand, (20, 170))
    shootCommand = myFont.render("Space bar to shoot", False, (255, 255, 255))
    win.blit(shootCommand, (20, 200))
    mouseCommand = myFont.render("Point the mouse for direction of shooting", False, (255, 255, 255))
    win.blit(mouseCommand, (20, 230))
    # Game play
    gamePlay = myFont.render("Game Play:", False, (255, 255, 255))
    win.blit(gamePlay, (10, 280))
    textForGamePlay = myFont.render("Use the controls to move and to shoot. Each player has 10 seconds to make a move.",
                                    False, (255, 255, 255))
    win.blit(textForGamePlay, (20, 310))
    textForGamePlay = myFont.render("When the time runs out it's the next players turn. After a player fires a shot",
                                    False, (255, 255, 255))
    win.blit(textForGamePlay, (20, 340))
    textForGamePlay = myFont.render("he has 5 seconds to run away and hide.", False, (255, 255, 255))
    win.blit(textForGamePlay, (20, 370))
    textForGamePlay = myFont.render("When firing a shot, the speed with which the ball moves depends on the position",
                                    False, (255, 255, 255))
    win.blit(textForGamePlay, (20, 400))
    textForGamePlay = myFont.render("of the mouse. The ball moves faster if the mouse is further from the attacking",
                                    False, (255, 255, 255))
    win.blit(textForGamePlay, (20, 430))
    textForGamePlay = myFont.render("player's side. The fight goes on until one of the players runs out of health.",
                                    False, (255, 255, 255))
    win.blit(textForGamePlay, (20, 460))
    textForGamePlay = largeFont.render("Have Fun Playing!", False, (255, 255, 255))
    win.blit(textForGamePlay, (500, 520))
    pygame.display.update()


def redrawGameWindow():
    win.blit(background, (0, 0))
    win.blit(tiles, (tilesX, tilesY))
    if player1.health > 0:
        player1.draw(win)
    if player2.health > 0:
        player2.draw(win)
    weapon.draw(win)
    player.collide(platforms, hitMyHead)
    # Draws the score
    textSurface = myFont.render(str(playerTime), False, (255, 255, 255))
    win.blit(textSurface, (1150, 30))
    textSurface = myFont.render(str(player1.wins), False, (255, 255, 255))
    win.blit(textSurface, (430, 10))
    textSurface = myFont.render(str(player2.wins), False, (255, 255, 255))
    win.blit(textSurface, (690, 10))
    # draws whose turn it is
    if isPlayerOne:
        textSurface = myFont.render("Ghost", False, (255, 255, 255))
        win.blit(textSurface, (530, 10))
    else:
        textSurface = myFont.render("Alien", False, (255, 255, 255))
        win.blit(textSurface, (530, 10))
    if level == 2:
        strengthbarImage = pygame.Surface(((strength * 100) - 50, 20))
        strengthbar = strengthbarImage.get_rect()
        strengthbar.x = 10
        strengthbar.y = 20
        strengthbarColor = (0, 255, 0)
        outerLayer = pygame.Surface((102, 22))
        blackness = outerLayer.get_rect()
        blackness.x = 9
        blackness.y = 19
        pygame.draw.rect(win, (0, 0, 0), blackness)
        pygame.draw.rect(win, strengthbarColor, strengthbar)
        textSurface = myFont.render("Power", False, (255, 255, 255))
        win.blit(textSurface, (115, 6))
    pygame.display.update()


def PlanetOneSetup():
    global player, player1, players, player2, weapon, playerSpriteHead, playerSpriteBody, tilesX, tilesY, strength, \
            background, tiles, platforms
    player1 = Player(75, 333, 29, 45)
    player2 = Player(1017, 240, 29, 45)
    player1.characterIdleR = character1R
    player1.characterIdleL = character1L
    player1.characterLeft = character1Left
    player1.characterRight = character1Right
    player2.characterIdleR = character2R
    player2.characterIdleL = character2L
    player2.characterLeft = character2Left
    player2.characterRight = character2Right
    player = player1
    strength = 1
    # clear the players from the sprite in case they are both added so no self collision is done
    players = pygame.sprite.Group()
    # at the beginning of the game add the second player for collision with the ball because player one starts first
    playerSpriteHead = PlayerSprites(player2.rect.x, player2.rect.y, 29, 22.5)
    playerSpriteBody = PlayerSprites(player2.rect.x, player2.rect.y + 22.5, 29, 22.5)
    players.add(playerSpriteHead)
    players.add(playerSpriteBody)
    weapon = Weapon(player.pos.x + 20, player.pos.y + 30, 9)
    tilesX = 0
    tilesY = 54
    background = pygame.image.load('Background.jpg')
    tiles = pygame.image.load('Tiles.png')
    platforms = pygame.sprite.Group()
    for plat in PLATFORM_LEVEL1_LIST_LEFT:
        p = Platform(*plat)
        platforms.add(p)
    for plat in PLATFORM_LEVEL1_LIST_RIGHT:
        p = Platform(*plat)
        platforms.add(p)


def PlanetTwoSetup(p1Wins, p2Wins):
    global player, player1, players, player2, weapon, playerSpriteHead, playerSpriteBody, tilesY, platforms, tiles, \
        background, strength
    player1 = Player(194, 356, 29, 45)
    player2 = Player(924, 130, 29, 45)
    player1.wins = p1Wins
    player2.wins = p2Wins
    player1.characterIdleR = character1R
    player1.characterIdleL = character1L
    player1.characterLeft = character1Left
    player1.characterRight = character1Right
    player2.characterIdleR = character2R
    player2.characterIdleL = character2L
    player2.characterLeft = character2Left
    player2.characterRight = character2Right
    player = player1
    # remove the players from the sprite in case they are both added so no self collision is done
    players = pygame.sprite.Group()
    # at the beginning of the game add the second player for collision with the ball because player one starts first
    playerSpriteHead = PlayerSprites(player2.rect.x, player2.rect.y, 29, 22.5)
    playerSpriteBody = PlayerSprites(player2.rect.x, player2.rect.y + 22.5, 29, 22.5)
    players.add(playerSpriteHead)
    players.add(playerSpriteBody)
    weapon = Weapon(player.pos.x + 20, player.pos.y + 30, 9)
    strength = random.uniform(0.5, 1.5)
    tiles = pygame.image.load('Level2.png')
    background = pygame.image.load('Planet2.png')
    tilesY = 0
    platforms.empty()
    for platf in PLATFORM_LEVEL2_LIST_LEFT:
        p = Platform(*platf)
        platforms.add(p)
    for platf in PLATFORM_LEVEL2_LIST_RIGHT:
        p = Platform(*platf)
        platforms.add(p)


def PlanetThreeSetup(p1Wins, p2Wins):
    global player, player1, players, player2, weapon, playerSpriteHead, playerSpriteBody, tilesY, platforms, tiles, \
        background, strength
    player1 = Player(29, 380, 29, 45)
    player2 = Player(1025, 181, 29, 45)
    player1.wins = p1Wins
    player2.wins = p2Wins
    player1.characterIdleR = character1R
    player1.characterIdleL = character1L
    player1.characterLeft = character1Left
    player1.characterRight = character1Right
    player2.characterIdleR = character2R
    player2.characterIdleL = character2L
    player2.characterLeft = character2Left
    player2.characterRight = character2Right
    # Set the gravity for the third planet
    player1.gravity = 0.2
    player2.gravity = 0.2
    # reset strength back to normal
    strength = 1
    player = player1
    # remove the players from the sprite in case they are both added so no self collision is done
    players = pygame.sprite.Group()
    # at the beginning of the game add the second player for collision with the ball because player one starts first
    playerSpriteHead = PlayerSprites(player2.rect.x, player2.rect.y, 29, 22.5)
    playerSpriteBody = PlayerSprites(player2.rect.x, player2.rect.y + 22.5, 29, 22.5)
    players.add(playerSpriteHead)
    players.add(playerSpriteBody)
    weapon = Weapon(player.pos.x + 20, player.pos.y + 30, 9)
    tiles = pygame.image.load('Level3.png')
    background = pygame.image.load('Planet3.png')
    platforms.empty()
    for platf in PLATFORM_LEVEL3_LIST_LEFT:
        p = Platform(*platf)
        platforms.add(p)
    for platf in PLATFORM_LEVEL3_LIST_RIGHT:
        p = Platform(*platf)
        platforms.add(p)


def drawEndScreen():
    win.blit(background, (0, 0))
    win.blit(tiles, (tilesX, tilesY))
    if player1.health > 0:
        player1.draw(win)
        textSurface = myFont.render("Congratulations Ghost", False, (255, 255, 255))
        win.blit(textSurface, (450, 60))
    if player2.health > 0:
        player2.draw(win)
        textSurface = myFont.render("Congratulations Alien", False, (255, 255, 255))
        win.blit(textSurface, (450, 60))
    textSurface = myFont.render("Press N for the next planet", False, (255, 255, 255))
    win.blit(textSurface, (430, 110))
    if level == 1:
        textSurface = myFont.render("Tip: Your strength may not be up to you here", False, (255, 255, 255))
        win.blit(textSurface, (340, 140))
    if level == 2:
        textSurface = myFont.render("Tip: Gravity is a little different here", False, (255, 255, 255))
        win.blit(textSurface, (380, 140))
    pygame.display.update()


def drawWinnerScreen():
    winnerBackground = pygame.image.load('WinnerBackground.png')
    win.blit(winnerBackground, (0, 0))
    if player1.wins == 2:
        textSurface = largeFont.render("Congratulations Ghost", False, (255, 255, 255))
        win.blit(textSurface, (300, 150))
        textSurface = largeFont.render("You are the ruler of this solar system", False, (255, 255, 255))
        win.blit(textSurface, (100, 210))
        win.blit(player1.characterIdleR, (600, 300))
    elif player2.wins == 2:
        textSurface = largeFont.render("Congratulations Alien", False, (255, 255, 255))
        win.blit(textSurface, (300, 150))
        textSurface = largeFont.render("You are the ruler of the solar system GEMBO", False, (255, 255, 255))
        win.blit(textSurface, (100, 210))
        win.blit(player2.characterIdleR, (600, 300))

    textSurface = myFont.render("Press N if you want to challenge each other again", False, (255, 255, 255))
    win.blit(textSurface, (300, 400))
    pygame.display.update()


# Finds the angle for shooting
def findAngle(position):
    sX = weapon.x
    sY = weapon.y
    try:
        angleF = math.atan((sY - position[1]) / (sX - position[0]))
    except:
        angleF = math.pi / 2
    if position[1] < sY and position[0] > sX:
        angleF = abs(angleF)
    elif position[1] < sY and position[0] < sX:
        angleF = math.pi - angleF
    elif position[1] > sY and position[0] < sX:
        angleF = math.pi + abs(angleF)
    elif position[1] > sY and position[0] > sX:
        angleF = (math.pi * 2) - angleF
    return angleF


# Draw endgame screen if someone lost
def EndLoop():
    global level
    EndGame = True
    while EndGame:
        clock.tick(fps)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if keys[pygame.K_n]:
                if level < 4 and player1.wins != 2 and player2.wins != 2:
                    level += 1
                    MainLoop()
                elif level >= 2:
                    MenuLoop()
        if level < 4 and player1.wins != 2 and player2.wins != 2:
            drawEndScreen()
        elif level >= 2:
            drawWinnerScreen()


# Starts the game with the Menu screen
if __name__ == '__main__':
    MenuLoop()
