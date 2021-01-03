import pygame, sys, random, time
from pygame.locals import *

winWidth = 700
winHeight = 900
textColor = (28, 205, 0)

FPS = 60

baddieMinSize = 20
baddieMaxSize = 50
moreSpeedRate = 600
playerSpeed = 8


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    terminate()
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

font = pygame.font.SysFont(None, 40)
font1 = pygame.font.SysFont(None, 32)
gameOverSound = pygame.mixer.Sound('game_over.mp3')
pygame.mixer.music.load('backgroundMusic.mp3')

playerImage = pygame.image.load('ship.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('meteor.png')
backgroundImage = pygame.image.load('background.png')
fullHeartImage = pygame.image.load('heartFull1.png')
emptyHeartImage = pygame.image.load('heartEmpty1.png')
zaplatka = pygame.image.load('background1.png')

for i in range(4):
    for j in range(4):
        win.blit(backgroundImage, (256 * j, 256 * i))

drawText('Game', font, win, (winWidth / 2) - 50, (winHeight / 2) - 50)
drawText('Нажмите любую клавишу для начала игры', font, win, (winWidth / 2) - 290, (winHeight / 2) + 40)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    baddieMinSpeed = 1
    baddieMaxSpeed = 5
    addNewBaddieRate = 14
    baddies = []
    hearts = []
    emptyHearts = []
    heartChange = False
    score = 0
    moreSpeedCount = 0
    heartQuantity = 5
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
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]

        baddieAddCounter += 1
        moreSpeedCount += 1
        if baddieAddCounter == addNewBaddieRate:
            baddieAddCounter = 0
            baddieSize = random.randint(baddieMinSize, baddieMaxSize)
            newBaddie = {'rect': pygame.Rect(random.randint(0, winWidth - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                         'speed': random.randint(baddieMinSpeed, baddieMaxSpeed),
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize))}
            baddies.append(newBaddie)

        if moreSpeedRate == moreSpeedCount:
            baddieMinSpeed += 1
            baddieMaxSpeed += 1
            moreSpeedCount = 0
            baddieAddCounter = 0
            if addNewBaddieRate > 1:
                addNewBaddieRate -= 2

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * playerSpeed, 0)
        if moveRight and playerRect.right < winWidth:
            playerRect.move_ip(playerSpeed, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * playerSpeed)
        if moveDown and playerRect.bottom < winHeight:
            playerRect.move_ip(0, playerSpeed)

        for b in baddies:
            b['rect'].move_ip(0, b['speed'])

        for b in baddies[:]:
            if b['rect'].top > winHeight:
                baddies.remove(b)

        for i in range(4):
            for j in range(4):
                win.blit(backgroundImage, (256 * j, 256 * i))

        win.blit(playerImage, playerRect)

        for b in baddies:
            win.blit(b['surface'], b['rect'])

        if heartChange == True:
            for i in range(heartQuantity):
                newHeart = {'rect': (5 + 50 * i, 60)}
                hearts.append(newHeart)

            if topHeartQuantity > heartQuantity:
                for i in range(topHeartQuantity, heartQuantity, -1):
                    newEmptyHeart = {'rect': (5 + 50 * (i - 1), 60)}
                    emptyHearts.append(newEmptyHeart)

        for i in hearts:
                win.blit(fullHeartImage, i['rect'])
        for i in emptyHearts:
                win.blit(emptyHeartImage, i['rect'])

        heartChange = False





        drawText('Score: %s' % {score}, font1, win, 5, 0)
        drawText('Record %s' % {topScore}, font1, win, 5, 30)



        if playerHasHitBaddie(playerRect, baddies):
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
        pygame.display.update()
        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('Game Over', font, win, (winWidth / 2) - 75, (winHeight / 2) - 50)
    drawText('Нажмите любую клавишу для начала новой игры', font, win, (winWidth / 2) - 335, (winHeight / 2) + 40)
    pygame.display.update()
    waitForPlayerToPressKey()
    gameOverSound.stop()
