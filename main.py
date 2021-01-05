import pygame, sys, random, time
from pygame.locals import *

winWidth = 700
winHeight = 900
textColor = (28, 205, 0)

FPS = 120

baddieMinSize = 20
baddieMaxSize = 50
moreSpeedRate = 1200
playerSpeed = 4


def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_p:
                    return


def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def removeBaddie(playerRect, baddies):
    for b in baddies[:]:
        if playerRect.colliderect(b['rect']):
            baddies.remove(b)


def playerHasHitHeart(playerRect, extraLife):
    for i in extraLife:
        if playerRect.colliderect(i['rect']):
            return True
    return False


def removeHeart(playerRect, extraLife):
    for i in extraLife:
        if playerRect.colliderect(i['rect']):
            extraLife.remove(i)


def playerHasHitShield(playerRect, shields):
    for i in shields:
        if playerRect.colliderect(i['rect']):
            return True
    return False


def removeShield(playerRect, shields):
    for i in shields:
        if playerRect.colliderect(i['rect']):
            shields.remove(i)

def meteorHasHitShield(shieldRect, baddies):
    for b in baddies:
        if shieldRect.colliderect(b['rect']):
            return True
    return False


def removeMeteorCollideShield(shieldRect, baddies):
    for b in baddies[:]:
        if shieldRect.colliderect(b['rect']):
            baddies.remove(b)



def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()
mainClock = pygame.time.Clock()
win = pygame.display.set_mode((winWidth, winHeight), pygame.RESIZABLE)
pygame.display.set_caption('Game')
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

font = pygame.font.SysFont(None, 40)
font1 = pygame.font.SysFont(None, 32)
gameOverSound = pygame.mixer.Sound('game_over.wav')
collisionSound = pygame.mixer.Sound('collisionSound.wav')
healSound = pygame.mixer.Sound('healEffect.wav')
pygame.mixer.music.load('backgroundMusic.wav')
gameOverSound.set_volume(0.5)
healSound.set_volume(0.3)
collisionSound.set_volume(0.35)

playerImage = pygame.image.load('ship.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('meteor.png')
backgroundImage = pygame.image.load('background.png')
fullHeartImage = pygame.image.load('heartFull.png')
emptyHeartImage = pygame.image.load('heartEmpty.png')
shield = pygame.image.load('shield.png')
shieldEffect = pygame.image.load('shieldEffect.png')
shieldRect = shieldEffect.get_rect()
zaplatka = pygame.image.load('background1.png')

win.blit(backgroundImage, (0, 0))

drawText('Game', font, win, (winWidth / 2) - 50, (winHeight / 2) - 50)
drawText('Нажмите любую клавишу для начала игры', font, win, (winWidth / 2) - 290, (winHeight / 2) + 20)
pygame.display.flip()
waitForPlayerToPressKey()

topScore = 0
while True:
    baddieMinSpeed = 1
    baddieMaxSpeed = 5
    addNewBaddieRate = 14
    baddies = []
    hearts = []
    shields = []
    emptyHearts = []
    heartChange = False
    shieldUse = False
    shieldCount = 0
    extraLife = []
    score = 0
    moreSpeedCount = 0
    heartQuantity = 3
    topHeartQuantity = heartQuantity
    playerRect.topleft = (winWidth / 2, winHeight - 85)
    moveLeft = moveRight = moveUp = moveDown = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    for i in range(heartQuantity):
        newHeart = {'rect': (5 + 50 * i, 60)}
        hearts.append(newHeart)

    while True:
        score += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_p:
                    pause()
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                if event.pos[0] < winWidth - 64:
                    playerRect.left = event.pos[0]
                    shieldRect.left = event.pos[0] - 13
                if event.pos[1] > 50:
                    playerRect.bottom = event.pos[1]
                    shieldRect.bottom = event.pos[1] + 19

        baddieAddCounter += 0.5
        moreSpeedCount += 0.5
        if baddieAddCounter == addNewBaddieRate:
            baddieAddCounter = 0
            baddieSize = random.randint(baddieMinSize, baddieMaxSize)
            newBaddie = {'rect': pygame.Rect(random.randint(0, winWidth - baddieSize), 0 - baddieSize, baddieSize,
                                             baddieSize),
                         'speed': random.randint(baddieMinSpeed, baddieMaxSpeed),
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize))}
            baddies.append(newBaddie)

        randomNumber = random.randint(0, 3500)
        if randomNumber == 7 and score > 1000:
            extraHeart = {'rect': pygame.Rect(random.randint(0, winWidth - 40), -34, 40, 34),
                          'speed': random.randint(2, 5)}
            extraLife.append(extraHeart)

        randomNumber1 = random.randint(0, 3500)
        if randomNumber1 == 7 and score > 1000:
            newShield = {'rect': pygame.Rect(random.randint(0, winWidth - 40), -34, 40, 34),
                         'speed': random.randint(2, 5)}
            shields.append(newShield)

        if score % 2 == 0:
            for b in baddies:
                b['rect'].move_ip(0, b['speed'])
            for i in extraLife:
                i['rect'].move_ip(0, i['speed'])
            for i in shields:
                i['rect'].move_ip(0, i['speed'])

        for b in baddies[:]:
            if b['rect'].top > winHeight:
                baddies.remove(b)
        for i in shields[:]:
            if i['rect'].top > winHeight:
                shields.remove(i)
        for i in extraLife[:]:
            if i['rect'].top > winHeight:
                extraLife.remove(i)

        if moreSpeedRate == moreSpeedCount:
            baddieMinSpeed += 1
            baddieMaxSpeed += 1
            moreSpeedCount = 0
            baddieAddCounter = 0
            if addNewBaddieRate > 4:
                addNewBaddieRate -= 1

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * playerSpeed, 0)
            shieldRect.move_ip(-1 * playerSpeed, 0)
        if moveRight and playerRect.right < winWidth:
            playerRect.move_ip(playerSpeed, 0)
            shieldRect.move_ip(playerSpeed, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * playerSpeed)
            shieldRect.move_ip(0, -1 * playerSpeed)
        if moveDown and playerRect.bottom < winHeight:
            playerRect.move_ip(0, playerSpeed)
            shieldRect.move_ip(0, playerSpeed)

        win.blit(backgroundImage, (0, 0))
        win.blit(playerImage, playerRect)

        for b in baddies:
            win.blit(b['surface'], b['rect'])
        for i in extraLife:
            win.blit(fullHeartImage, i['rect'])
        for i in shields:
            win.blit(shield, i['rect'])

        for i in hearts:
            win.blit(fullHeartImage, i['rect'])
        for i in emptyHearts:
            win.blit(emptyHeartImage, i['rect'])

        if playerHasHitShield(playerRect, shields):
            shieldCount = 0
            removeShield(playerRect, shields)
            win.blit(shieldEffect, shieldRect)
            shieldUse = True
            t = 30
            k = 0

        if shieldUse:
            if shieldCount < 1200:
                if meteorHasHitShield(shieldRect, baddies):
                    removeMeteorCollideShield(shieldRect, baddies)
                if shieldCount > 840:
                    if k < t:
                        win.blit(shieldEffect, shieldRect)
                        k += 1
                    elif k < 2 * t:
                        k += 1
                    elif k == 2 * t:
                        t = 30
                        k = 0
                else:
                    win.blit(shieldEffect, shieldRect)
                shieldCount += 1
            else:
                shieldCount = 0
                shieldUse = False
                t = 60
                k = 0

        if playerHasHitHeart(playerRect, extraLife):
            healSound.play()
            removeHeart(playerRect, extraLife)
            heartQuantity += 1
            if heartQuantity > topHeartQuantity:
                topHeartQuantity += 1
            hearts = []
            emptyHearts = []
            heartChange = True

        if playerHasHitBaddie(playerRect, baddies):
            collisionSound.play()
            removeBaddie(playerRect, baddies)
            heartQuantity -= 1
            heartChange = True
            if heartQuantity == 0:
                win.blit(zaplatka, (5, 60))
                win.blit(emptyHeartImage, (5, 60))
                if score > topScore:
                    topScore = score
                break
            hearts = []
            emptyHearts = []

        if heartChange:
            for i in range(heartQuantity):
                newHeart = {'rect': (5 + 50 * i, 60)}
                hearts.append(newHeart)

            if topHeartQuantity > heartQuantity:
                for i in range(topHeartQuantity, heartQuantity, -1):
                    newEmptyHeart = {'rect': (5 + 50 * (i - 1), 60)}
                    emptyHearts.append(newEmptyHeart)

        heartChange = False

        drawText('Score: %s' % {score}, font1, win, 5, 0)
        drawText('Record %s' % {topScore}, font1, win, 5, 30)

        pygame.display.flip()
        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('Score: %s' % {score}, font1, win, 5, 0)
    drawText('Record %s' % {topScore}, font1, win, 5, 30)
    drawText('Game Over', font, win, (winWidth / 2) - 75, (winHeight / 2) - 50)
    drawText('Нажмите любую клавишу для начала новой игры', font, win, (winWidth / 2) - 335, (winHeight / 2) + 20)
    pygame.display.flip()
    waitForPlayerToPressKey()
    gameOverSound.stop()
