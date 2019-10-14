from Player import *
from Weapon import *

# Setup code
pygame.init()
pygame.display.set_caption("GEMBO")
win = pygame.display.set_mode((1200, 600), pygame.DOUBLEBUF)
background = pygame.image.load('Background.jpg')
menuBackground = pygame.image.load('MenuBackground.jpg')
myFont = pygame.font.SysFont('Comic Sans MS', 30)
haveFunFont = pygame.font.SysFont('Comic Sans MS', 50)
tiles = pygame.image.load('Tiles.png')
clock = pygame.time.Clock()
timer = pygame.time
fps = 27
platforms = pygame.sprite.Group()
for plat in PLATFORM_LIST_LEFT:
    p = Platform(*plat)
    platforms.add(p)
for plat in PLATFORM_LIST_RIGHT:
    p = Platform(*plat)
    platforms.add(p)


# Menu loop
def MenuLoop():
    menuTrue = True
    showInstructions = False
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
    global player, player1, players, player2, weapon, true, playerTime, isPlayerOne, shoot, hasShotOnce, shootTime,\
        power, angle, assignRole, isRightWall, isLeftWall, hitMyHead, startingPointForProjectileX, \
        startingPointForProjectileY, timeForPlayer
    # Setting the players starting health, character and position
    LevelOneSetup()
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
                EndLoop()
            else:
                player2.health = 0
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
            if keys[pygame.K_SPACE] and not player.isJump:
                if not shoot and not hasShotOnce:
                    startingPointForProjectileX = weapon.x
                    startingPointForProjectileY = weapon.y
                    pos = pygame.mouse.get_pos()
                    shoot = True
                    hasShotOnce = True
                    if math.sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2) / 4 > 100:
                        power = 100
                    else:
                        power = math.sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2) / 4
                    angle = findAngle(pos)
            # JUMPING
            if not player.isJump and timer.get_ticks() / 1000 - start_time < timeForPlayer:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    player.jump()
                    player.isJump = True
                    player.right = False
                    player.left = False
                    player.walkCount = 0
        elif shoot:
            projectileCollide = pygame.sprite.spritecollide(weapon, platforms, False)
            playerCollide = pygame.sprite.spritecollide(weapon, players, False)
            # Check if the projectile has hit the enemy player and damage him
            if playerCollide:
                timeForPlayer = 5.4
                shoot = False
                start_time = timer.get_ticks() / 1000
                if isPlayerOne:
                    player2.health -= 20
                    player2.healthbarWidth -= player.healthCut
                    if 40 < player2.health < 70:
                        player2.healthbarColor = (255, 255, 0)
                    if player2.health <= 40:
                        player2.healthbarColor = (255, 0, 0)
                    if player2.health <= 0:
                        while player2.deathCount <= 5:
                            redrawGameWindow()
                            if player2.side:
                                print(player2.right)
                                player2.drawDeath(win, character2Death)
                            else:
                                player2.drawDeath(win, character2LDeath)
                        EndLoop()
                        true = False
                else:
                    player1.health -= 20
                    player1.healthbarWidth -= player.healthCut
                    if 40 < player1.health < 70:
                        player1.healthbarColor = (255, 255, 0)
                    if player1.health <= 40:
                        player1.healthbarColor = (255, 0, 0)
                    if player1.health <= 0:
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
            players.remove(player1)
            players.remove(player2)
            if isPlayerOne:
                player = player1
                players.add(player2)
            else:
                player = player2
                players.add(player1)
            assignRole = False
            start_time = timer.get_ticks() / 1000
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
    textForGamePlay = haveFunFont.render("Have Fun Playing!", False, (255, 255, 255))
    win.blit(textForGamePlay, (500, 520))
    pygame.display.update()


def redrawGameWindow():
    global fps
    win.blit(background, (0, 0))
    win.blit(tiles, (0, 54))
    if player1.health > 0:
        player1.draw(win)
    if player2.health > 0:
        player2.draw(win)
    weapon.draw(win)
    player.collide(platforms, hitMyHead)
    textSurface = myFont.render(str(playerTime), False, (255, 255, 255))
    win.blit(textSurface, (1150, 30))
    if isPlayerOne:
        textSurface = myFont.render("Ghost", False, (255, 255, 255))
        win.blit(textSurface, (530, 10))
    else:
        textSurface = myFont.render("Alien", False, (255, 255, 255))
        win.blit(textSurface, (530, 10))
    pygame.display.update()


def LevelOneSetup():
    global player, player1, players, player2, weapon
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
    # remove the players from the sprite in case they are both added so no self collision is done
    players = pygame.sprite.Group()
    # at the beginning of the game add the second player for collision with the ball because player one starts first
    players.add(player2)
    weapon = Weapon(player.pos.x + 20, player.pos.y + 30, 9)


def drawEndScreen():
    win.blit(background, (0, 0))
    win.blit(tiles, (0, 54))
    if player1.health > 0:
        player1.draw(win)
        textSurface = myFont.render("Congratulations Ghost", False, (255, 255, 255))
        win.blit(textSurface, (450, 300))
    if player2.health > 0:
        player2.draw(win)
        textSurface = myFont.render("Congratulations Alien", False, (255, 255, 255))
        win.blit(textSurface, (450, 300))
    textSurface = myFont.render("Press N for a new game", False, (255, 255, 255))
    win.blit(textSurface, (430, 350))
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
    EndGame = True
    while EndGame:
        clock.tick(fps)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if keys[pygame.K_n]:
                MenuLoop()
        drawEndScreen()

# Starts the game with the Menu screen
if __name__ == '__main__':
    MenuLoop()
