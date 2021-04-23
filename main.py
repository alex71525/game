import pygame, sys, random, time
from pygame.locals import *

winWidth = 700
winHeight = 900
textColor = (28, 205, 0)

FPS = 120

meteorMinSize = 20
meteorMaxSize = 50
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


def playerHasHitMeteor(playerRect, meteors):
    global heartQuantity, heartChange, hearts, emptyHearts
    for b in meteors[:]:
        if playerRect.colliderect(b['rect']):
            meteors.remove(b)
            collisionSound.play()
            heartQuantity -= 1
            heartChange = True
            hearts = []
            emptyHearts = []


def playerHasHitHeart(playerRect, extraLife):
    global heartQuantity, heartChange, hearts, emptyHearts
    for i in extraLife:
        if playerRect.colliderect(i['rect']):
            extraLife.remove(i)
            healSound.play()
            heartQuantity += 1
            hearts = []
            emptyHearts = []
            heartChange = True


def playerHasHitShield(playerRect, shields):
    global shieldCount, shieldUse, t, k
    for i in shields:
        if playerRect.colliderect(i['rect']):
            shieldSound.play()
            shields.remove(i)
            shieldCount = 0
            win.blit(shieldEffect, shieldRect)
            shieldUse = True
            t = 30
            k = 0


def meteorHasHitShield(playerRect, meteors):
    global shieldUse
    for b in meteors:
        if playerRect.colliderect(b['rect']):
            shieldBreak.play()
            meteors.remove(b)
            shieldUse = False


def playerHasHitBonus(playerRect, bullets):
    global bulletsQuantity
    for i in bullets:
        if playerRect.colliderect(i['rect']):
            gunReload.play()
            bullets.remove(i)
            bulletsQuantity += 10


def meteorHasHitBullet(meteors, bulletsEffect):
    for i in meteors:
        for j in bulletsEffect:
            if j['rect'].colliderect(i['rect']):
                bulletsEffect.remove(j)
                meteors.remove(i)

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()
mainClock = pygame.time.Clock()
win = pygame.display.set_mode((winWidth, winHeight), pygame.RESIZABLE)
pygame.display.set_caption('Game')
pygame.mouse.set_visible(True)
pygame.event.set_grab(True)

font = pygame.font.SysFont(None, 40)
font1 = pygame.font.SysFont(None, 32)
gameOverSound = pygame.mixer.Sound('game_over.wav')
collisionSound = pygame.mixer.Sound('collisionSound.wav')
healSound = pygame.mixer.Sound('healEffect.wav')
gunSound = pygame.mixer.Sound('gunSound.wav')
gunReload = pygame.mixer.Sound('gunReload.mp3')
shieldSound = pygame.mixer.Sound('shieldSound.mp3')
shieldBreak = pygame.mixer.Sound('shieldBreak.wav')
pygame.mixer.music.load('backgroundMusic.wav')
gameOverSound.set_volume(0.5)
healSound.set_volume(0.3)
collisionSound.set_volume(0.35)
gunSound.set_volume(0.25)
shieldBreak.set_volume(0.8)

playerImage = pygame.image.load('ship.png')
playerRect = playerImage.get_rect()
meteorImage = pygame.image.load('meteor.png')
backgroundImage = pygame.image.load('background.png')
fullHeartImage = pygame.image.load('heartFull.png')
emptyHeartImage = pygame.image.load('heartEmpty.png')
shield = pygame.image.load('shield.png')
shieldEffect = pygame.image.load('shieldEffect.png')
shieldRect = shieldEffect.get_rect()
zaplatka = pygame.image.load('background1.png')
bullet = pygame.image.load('bullet.png')
bulletRect = bullet.get_rect()
bonus = pygame.image.load('bonus.png')

win.blit(backgroundImage, (0, 0))

class Button:

    def __init__(self, coords, name, f):
        self.coords = coords
        self.name = name
        self.f = f
        self.width = 300
        self.height = 80
        self.button = pygame.Rect(coords, (self.width, self.height))

    def draw_button(self, screen):
        pygame.draw.rect(screen, pygame.Color("Green"), self.button, 3)
        font = pygame.font.Font(None, 60)
        text = font.render(self.name, 1, pygame.Color("Green"))
        text_x = self.coords[0] + self.width // 2 - text.get_width() // 2
        text_y = self.coords[1] + self.height // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))

    def check_button(self, pos):
        x, y = pos
        if self.coords[0] <= x <= self.width + self.coords[0] and self.coords[1] <= y <= self.height + self.coords[1]:
            return True
        else:
            return False

def do_something():
    pass

def main_menu():
    pygame.mouse.set_visible(True)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    menu_name(screen)
    start_button = Button((200, 300), "Старт", do_something)
    start_button.draw_button(screen)
    info_button = Button((200, 400), "Правила", rules_menu)
    info_button.draw_button(screen)
    guys_button = Button((200, 500), "Создатели", creators_menu)
    guys_button.draw_button(screen)
    exit_button = Button((200, 600), "Выход", exit)
    exit_button.draw_button(screen)
    buttons = [start_button, info_button, guys_button, exit_button]
    running = True

    while running:
        # внутри игрового цикла ещё один цикл
        # приёма и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.check_button(event.pos):
                        b.f()
                        return
        # ...
        # отрисовка и изменение свойств объектов
        # ...
        pygame.display.flip()


def creators_menu():
    window = pygame.display.set_mode(size)
    window.fill((0, 0, 0))
    menu_name(window)
    exit_button = Button((200, 700), "Назад", main_menu)
    exit_button.draw_button(window)
    font = pygame.font.Font(None, 65)
    text2 = font.render("Создатели", 1, pygame.Color("Green"))
    text_x2 = width // 2 - text2.get_width() // 2
    text_y2 = 200 - text2.get_height() // 2
    # text_w = text.get_width()
    # text_h = text.get_height()
    window.blit(text2, (text_x2, text_y2))
    running = True

    MYEVENTTYPE = 30
    pygame.time.set_timer(MYEVENTTYPE, 10)
    x = width - 327
    x1 = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.check_button(event.pos):
                    main_menu()
                    return

            if event.type == MYEVENTTYPE:
                pygame.draw.rect(window, (0, 0, 0), (0, 380,
                                                     width, 150))
                creators_info(window, x, x1)
                x1 += 2
                x -= 2
                if x <= -327:
                    x = width
                if x1 >  width:
                    x1 = -327

        pygame.display.flip()


# Имена создателей игры. Приклеивание текста на холст
def creators_info(screen, x, x1):
    font = pygame.font.Font(None, 65)
    text1 = font.render("Александр Кох", 1, pygame.Color("Green"))
    text = font.render("Иван Петренко", 1, pygame.Color("Green"))
    text_y = 480 - text.get_height() // 2
    text_y1 = 400 - text1.get_height() // 2
    screen.blit(text, (x, text_y))
    screen.blit(text1, (x1, text_y1))


def rules_menu():
    window = pygame.display.set_mode(size)
    window.fill((0, 0, 0))
    menu_name(window)
    exit_button = Button((200, 700), "Назад", main_menu)
    exit_button.draw_button(window)
    running = True
    rules_info(window)

    while running:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.check_button(event.pos):
                    main_menu()
                    return
        pygame.display.flip()


def rules_info(screen):
    font = pygame.font.Font(None, 30)
    text = [
        "Правила", "",
        "Вы в открытом космосе.",
        "Управление кораблем возьмите на себя,",
        "с помощью мыши или стрелок на клавиатуре.",
        "Остерегайтесь астероидов, летящих навстречу.",
        "Нажимая ЛКМ или пробел на клавиатуре,",
        "стреляйте по астероидам и разрушайте их.",
        "Обратите внимание,",
        "запасы патронов не бесконечны,",
        "собирайте всё, что видите.",
        "Говорят, что на просторах космоса",
        "можно найти ремнабор или щит",
        "действующий 10 секунд.",
        "Удачи сержант."]
    text_coord = 170
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width // 2 - string_rendered.get_width() // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def menu_name(screen):
    font = pygame.font.Font(None, 80)
    text = font.render("IKS Space", 1, pygame.Color("Green"))
    text_x = width // 2 - text.get_width() // 2
    text_y = 100 - text.get_height() // 2
    # text_w = text.get_width()
    # text_h = text.get_height()
    screen.blit(text, (text_x, text_y))


size = width, height = 700, 900


# drawText('Game', font, win, (winWidth / 2) - 50, (winHeight / 2) - 50)
# drawText('Нажмите любую клавишу для начала игры', font, win, (winWidth / 2) - 290, (winHeight / 2) + 20)
# pygame.display.flip()
# waitForPlayerToPressKey()

topScore = 0
while True:
    main_menu()
    meteorMinSpeed = 1
    meteorMaxSpeed = 5
    bulletSpeed = -20
    addNewMeteorRate = 14
    meteors = []
    hearts = []
    shields = []
    emptyHearts = []
    bullets = []
    bulletsEffect = []
    heartChange = False
    shieldUse = False
    shoot = False
    shieldCount = 0
    extraLife = []
    score = 0
    moreSpeedCount = 0
    heartQuantity = 3
    bulletsQuantity = 10
    topHeartQuantity = heartQuantity
    playerRect.topleft = (winWidth / 2, winHeight - 85)
    moveLeft = moveRight = moveUp = moveDown = False
    meteorAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    for i in range(heartQuantity):
        newHeart = {'rect': (5 + 50 * i, 60)}
        hearts.append(newHeart)
    pygame.mouse.set_visible(False)
    esc_key = 0
    while True:
        score += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_key = 1
                    break
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
                if event.key == K_SPACE:
                    shoot = True
            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    shoot = True

            if event.type == MOUSEMOTION:
                if event.pos[0] < winWidth - 64:
                    playerRect.left = event.pos[0]
                    shieldRect.left = event.pos[0] - 13
                if event.pos[1] > 50:
                    playerRect.bottom = event.pos[1]
                    shieldRect.bottom = event.pos[1] + 19

        if esc_key:
            break
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

        meteorAddCounter += 0.5
        if meteorAddCounter == addNewMeteorRate:
            meteorAddCounter = 0
            meteorSize = random.randint(meteorMinSize, meteorMaxSize)
            newMeteor = {'rect': pygame.Rect(random.randint(0, winWidth - meteorSize), 0 - meteorSize, meteorSize,
                                             meteorSize),
                         'speed': random.randint(meteorMinSpeed, meteorMaxSpeed),
                         'surface': pygame.transform.scale(meteorImage, (meteorSize, meteorSize))}
            meteors.append(newMeteor)

        moreSpeedCount += 0.5
        if moreSpeedRate == moreSpeedCount:
            meteorMinSpeed += 1
            meteorMaxSpeed += 1
            moreSpeedCount = 0
            meteorAddCounter = 0
            if addNewMeteorRate > 4:
                addNewMeteorRate -= 1

        randomNumber = random.randint(0, 3500)
        if randomNumber == 7 and score > 1000:
            extraHeart = {'rect': pygame.Rect(random.randint(0, winWidth - 40), -34, 40, 34),
                          'speed': random.randint(2, 5)}
            extraLife.append(extraHeart)

        randomNumber1 = random.randint(0, 3500)
        if randomNumber1 == 7 and score > 1000:
            newShield = {'rect': pygame.Rect(random.randint(0, winWidth - 32), -32, 32, 32),
                         'speed': random.randint(2, 5)}
            shields.append(newShield)

        randomNumber2 = random.randint(0, 2500)
        if randomNumber2 == 7:
            newBonus = {'rect': pygame.Rect(random.randint(0, winWidth - 22), -29, 22, 29),
                        'speed': random.randint(2, 5)}
            bullets.append(newBonus)

        if score % 2 == 0:
            for b in meteors:
                b['rect'].move_ip(0, b['speed'])
            for i in extraLife:
                i['rect'].move_ip(0, i['speed'])
            for i in shields:
                i['rect'].move_ip(0, i['speed'])
            for i in bullets:
                i['rect'].move_ip(0, i['speed'])
            for i in bulletsEffect:
                i['rect'].move_ip(0, bulletSpeed)

        for b in meteors[:]:
            if b['rect'].top > winHeight:
                meteors.remove(b)
        for i in shields[:]:
            if i['rect'].top > winHeight:
                shields.remove(i)
        for i in extraLife[:]:
            if i['rect'].top > winHeight:
                extraLife.remove(i)
        for i in bullets[:]:
            if i['rect'].bottom < 0:
                bullets.remove(i)

        win.blit(backgroundImage, (0, 0))
        win.blit(playerImage, playerRect)

        for b in meteors:
            win.blit(b['surface'], b['rect'])
        for i in extraLife:
            win.blit(fullHeartImage, i['rect'])
        for i in shields:
            win.blit(shield, i['rect'])
        for i in bullets:
            win.blit(bonus, i['rect'])
        for i in bulletsEffect:
            win.blit(bullet, i['rect'])
        for i in hearts:
            win.blit(fullHeartImage, i['rect'])
        for i in emptyHearts:
            win.blit(emptyHeartImage, i['rect'])

        playerHasHitShield(playerRect, shields)

        if shieldUse:
            if shieldCount < 1200:
                if shieldCount < 20:
                    for b in meteors:
                        if playerRect.colliderect(b['rect']):
                            meteors.remove(b)
                else:
                    meteorHasHitShield(playerRect, meteors)
                if shieldCount > 840:
                    if k < t:
                        win.blit(shieldEffect, shieldRect)
                        meteorHasHitShield(playerRect, meteors)
                        k += 1
                    elif k < 2 * t:
                        k += 1
                        meteorHasHitShield(playerRect, meteors)
                    elif k == 2 * t:
                        meteorHasHitShield(playerRect, meteors)
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

        playerHasHitBonus(playerRect, bullets)
        if shoot and bulletsQuantity > 0:
            gunSound.play()
            bulletsQuantity -= 1
            newBullet = {'rect': pygame.Rect(playerRect.centerx - 5, playerRect.centery, 11, 16)}
            bulletsEffect.append(newBullet)

        meteorHasHitBullet(meteors, bulletsEffect)

        playerHasHitHeart(playerRect, extraLife)
        if heartQuantity > topHeartQuantity:
            topHeartQuantity += 1

        playerHasHitMeteor(playerRect, meteors)
        if heartQuantity == 0:
            win.blit(zaplatka, (5, 60))
            win.blit(emptyHeartImage, (5, 60))
            if score > topScore:
                topScore = score
            break

        if heartChange:
            for i in range(heartQuantity):
                newHeart = {'rect': (5 + 50 * i, 60)}
                hearts.append(newHeart)

            if topHeartQuantity > heartQuantity:
                for i in range(topHeartQuantity, heartQuantity, -1):
                    newEmptyHeart = {'rect': (5 + 50 * (i - 1), 60)}
                    emptyHearts.append(newEmptyHeart)

        heartChange = False
        shoot = False

        drawText('Score: %s' % {score}, font1, win, 5, 0)
        drawText('Record %s' % {topScore}, font1, win, 5, 30)
        drawText('Bullets: %s' % bulletsQuantity, font1, win, 5, 100)

        pygame.display.flip()
        mainClock.tick(FPS)

    if esc_key:
        continue
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('Score: %s' % {score}, font1, win, 5, 0)
    drawText('Record %s' % {topScore}, font1, win, 5, 30)
    drawText('Game Over', font, win, (winWidth / 2) - 75, (winHeight / 2) - 50)
    drawText('Нажмите любую клавишу для начала новой игры', font, win, (winWidth / 2) - 335, (winHeight / 2) + 20)
    pygame.display.flip()
    waitForPlayerToPressKey()
    gameOverSound.stop()

