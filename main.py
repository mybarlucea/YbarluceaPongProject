import pygame, sys, math, random
import pygame as pygame
import pygame.freetype
from pygame.locals import *

pygame.init()
global DISPLAYSURF
DISPLAYSURF = pygame.display.set_mode((750, 750), 0, 32)
WHITE = (255, 255, 255)
dev = False
screen = False
global dFont, gFont
dFont = pygame.freetype.Font('Arialn.ttf', 12)
sFont = pygame.freetype.Font('Arialn.ttf', 36)
gFont = pygame.freetype.Font('Arialn.ttf', 96)

def main():
    global rectl, rectw, dev
    global gamePad, gameBall, gamePad2, cpu1
    global p1Score, p2Score, p2Mode
    gamePad = vPaddle(100, 275, 200)
    gameBall = ball(10, 375, 375, -1, 0, 0.05)
    gamePad2 = vPaddle(650, 275, 200)
    cpu1 = cpu()
    cpuBool = False
    cpuBoolT = False
    cpuBoolN = 0
    p1Score = 0
    p2Score = 0
    p2Mode = False
    debInput = False
    lastdebL = ""
    lastdebTime = 0
    randN = 100
    mx, my = 0, 0
    while True:
        global screen
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if screen:
                if event.type == KEYUP:
                    if event.key == K_m and not debInput:
                        debInput = True
                        lastdebL = "m1"
                        lastdebTime = pygame.time.get_ticks()
                    elif debInput:
                        debInput, lastdebL = devEntry(event.key, lastdebL, lastdebTime)
                        lastdebTime = pygame.time.get_ticks()
                        if event.key == K_r and debInput:
                            dev = True
                    if event.key == K_SPACE:
                        gameBall.start()
            else:
                if event.type == MOUSEBUTTONUP:
                    mx, my = pygame.mouse.get_pos()
                    if 25 < mx < 725 and 150 < my < 400:
                        screen = True
                        p2Mode = False
                    if 25 < mx < 725 and 450 < my < 700:
                        screen = True
                        p2Mode = True
        if screen:
            if pressed[K_LEFT] and not pressed[K_RIGHT]:
                if not p2Mode:
                    if gamePad.isV():
                        if dev:
                            gamePad.shrink()
                    else:
                        gamePad.moveLeft()
                else:
                    if gamePad2.isV():
                        if dev:
                            gamePad2.shrink()
                    else:
                        gamePad2.moveLeft()
            if pressed[K_RIGHT] and not pressed[K_LEFT]:
                if not p2Mode:
                    if gamePad.isV():
                        if dev:
                            gamePad.grow()
                    else:
                        gamePad.moveRight()
                else:
                    if gamePad2.isV():
                        if dev:
                            gamePad2.grow()
                    else:
                        gamePad2.moveRight()
            if pressed[K_UP] and not pressed[K_DOWN]:
                if not p2Mode:
                    if gamePad.isV():
                        gamePad.moveLeft()
                    else:
                        if dev:
                            gamePad.grow()
                else:
                    if gamePad2.isV():
                        gamePad2.moveLeft()
                    else:
                        if dev:
                            gamePad2.grow()
            if pressed[K_DOWN] and not pressed[K_UP]:
                if not p2Mode:
                    if gamePad.isV():
                        gamePad.moveRight()
                    else:
                        if dev:
                            gamePad.shrink()
                else:
                    if gamePad2.isV():
                        gamePad2.moveRight()
                    else:
                        if dev:
                            gamePad2.shrink()
            if p2Mode:
                if pressed[K_w] and not pressed[K_s]:
                    if gamePad.isV():
                        gamePad.moveLeft()
                    else:
                        if dev:
                            gamePad.grow()
                if pressed[K_s] and not pressed[K_w]:
                    if gamePad.isV():
                        gamePad.moveRight()
                    else:
                        if dev:
                            gamePad.shrink()
                if pressed[K_a] and not pressed[K_d]:
                    if gamePad2.isV():
                        if dev:
                            gamePad.shrink()
                    else:
                        gamePad.moveLeft()
                if pressed[K_d] and not pressed[K_a]:
                    if gamePad.isV():
                        if dev:
                            gamePad.grow()
                    else:
                        gamePad.moveRight()
            else:
                if pygame.time.get_ticks() % randN == 0:
                    cpu1.guessSU()
                    yProb = 0
                    xProb = 0
                    if gameBall.y < gamePad2.recty:
                        yProb = gamePad2.recty - gameBall.y
                    elif gameBall.y > (gamePad2.recty + gamePad2.recth):
                        yProb = gameBall.y - (gamePad2.recty + gamePad2.recth)
                    else:
                        yProb = 0
                    xProb = abs(gamePad2.rectl - gameBall.x)
                    if xProb < 50:
                        xProb = 50
                    if xProb > 1000:
                        xProb = 1000
                    if yProb < 50:
                        yProb = 50
                    if yProb > 1000:
                        yProb = 1000
                    if yProb > xProb:
                        randN = random.randint(int(xProb), int(yProb))
                    else:
                        randN = random.randint(int(yProb), int(xProb))
                if pygame.time.get_ticks() % (int(cpu1.num / 200) + 1) == 0:
                    cpu1.move()
        gameDraw(gamePad, gamePad2, gameBall)
        gameBall.move()
        if pygame.time.get_ticks() % 17 == 0:
            pygame.display.update()

class hPaddle:
    def __init__(self, x, y, w):
        self.rectl = x
        self.recty = y
        self.rectw = w
        self.recth = 25

    def moveLeft(self):
        self.rectl -= 0.05

    def moveRight(self):
        self.rectl += 0.05

    def grow(self):
        self.rectw += 0.05
        self.rectl -= 0.025

    def shrink(self):
        self.rectw -= 0.05
        self.rectl += 0.025

    def isV(self):
        return False

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, WHITE, (self.rectl, self.recty, self.rectw, self.recth))

class vPaddle:
    def __init__(self, x, y, h):
        self.rectl = x
        self.recty = y
        self.rectw = 25
        self.recth = h

    def moveLeft(self):
        if self.recty > 0 - self.recth:
            self.recty -= gameBall.speed

    def moveRight(self):
        if self.recty < 750:
            self.recty += gameBall.speed

    def grow(self):
        self.recth += 0.05
        self.recty -= 0.025

    def shrink(self):
        g = self.recth * 0.005
        self.recth *= 0.99
        self.recty += g

    def isV(self):
        return True

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, WHITE, (self.rectl, self.recty, self.rectw, self.recth))

class ball:
    def __init__(self, r, x, y, dx, dy, s):
        self.rad = r
        self.x = x
        self.y = y
        self.dirX = dx
        self.dirY = dy
        self.speed = s
        self.dx = 0
        self.dy = 0
        self.moveS = False
        self.last = 0
        self.ldX = dx
        self.ldY = dy
        self.fs = False
        self.defS = s
        self.defH1 = 200
        self.defH2 = 200
        self.int = 0

    def start(self):
        if not self.moveS:
            self.moveS = True

    def move(self):
        if self.moveS:
            geth = math.pow(self.dirX, 2) + math.pow(self.dirY, 2)
            self.dirX /= math.sqrt(geth)
            self.dirY /= math.sqrt(geth)
            if self.dirY > 0.98 or self.dirY < -0.98:
                self.failSafe()
            self.dx = self.dirX * self.speed
            self.dy = self.dirY * self.speed
            self.x += self.dx
            self.y += self.dy
            self.bounceCheck()
            self.scoreCheck()

    def bounceCheck(self):
        global gamePad, gamePad2
        if gamePad.rectl - self.rad <= self.x <= gamePad.rectl + gamePad.rectw + self.rad and gamePad.recty - self.rad <= self.y <= gamePad.recty + gamePad.recth + self.rad:
            if gamePad.isV():
                if self.last != 1:
                    self.ldX = self.dirX
                    self.ldY = self.dirY
                    self.dirY += 1.5 * ((self.y - (gamePad.recty + (gamePad.recth / 2))) / (gamePad.recth))
                    self.dirX *= -1
                    self.speed += 0.0005 / self.speed
                    gamePad.shrink()
                    self.last = 1
                    self.fs = False
                else:
                    self.failSafe()
            else:
                if self.last != 1:
                    self.ldX = self.dirX
                    self.ldY = self.dirY
                    self.dirX += 1.5 * ((self.x - (gamePad.rectl + (gamePad.rectw / 2))) / (gamePad.rectw))
                    self.dirY *= -1
                    self.speed += 0.0001 / self.speed
                    gamePad.shrink()
                    self.last = 1
                    self.fs = False
                else:
                    self.failSafe()
        if gamePad2.rectl - self.rad <= self.x <= gamePad2.rectl + gamePad2.rectw + self.rad and gamePad2.recty - self.rad <= self.y <= gamePad2.recty + gamePad2.recth + self.rad:
            if gamePad2.isV():
                if self.last != 2:
                    self.ldX = self.dirX
                    self.ldY = self.dirY
                    self.dirY += 1.5 * ((self.y - (gamePad2.recty + (gamePad2.recth / 2))) / (gamePad2.recth))
                    self.dirX *= -1
                    self.speed += 0.0001 / self.speed
                    gamePad2.shrink()
                    self.last = 2
                    self.fs = False
                else:
                    self.failSafe()
            else:
                if self.last != 2:
                    self.ldX = self.dirX
                    self.ldY = self.dirY
                    self.dirX += 1.5 * ((self.x - (gamePad2.rectl + (gamePad2.rectw / 2))) / (gamePad2.rectw))
                    self.dirY *= -1
                    self.speed += 0.0001 / self.speed
                    gamePad2.shrink()
                    self.last = 2
                    self.fs = False
                else:
                    self.failSafe()
        if self.y - self.rad <= 0:
            self.dirY *= -1
        if self.y + self.rad >= 750:
            self.dirY *= -1

    def failSafe(self):
        if self.fs == False or pygame.time.get_ticks() - self.int < 100:
            self.dirX = self.ldX * -1
            self.dirY = self.ldY
            if self.last == 1:
                self.x = gamePad.rectl + gamePad.rectw + self.rad + 1
            elif self.last == 2:
                self.x = gamePad2.rectl - self.rad - 1
        else:
            if self.last == 1:
                self.dirX = 1
                self.x = gamePad.rectl + gamePad.rectw + self.rad + 1
            elif self.last == 2:
                self.dirX = -1
                self.x = gamePad2.rectl - self.rad - 1
            self.dirY = 0
        self.int = pygame.time.get_ticks()
        self.fs = True

    def scoreCheck(self):
        global p1Score, p2Score
        if self.x - self.rad <= 0:
            p2Score += 1
            self.respawn(2)
        if self.x + self.rad >= 750:
            p1Score += 1
            self.respawn(1)

    def respawn(self, n):
        global gamePad, gamePad2
        self.defS = (self.defS + self.speed + 0.05) / 3
        self.defH1 = (self.defH1 + gamePad.recth + 200) / 3
        self.defH2 = (self.defH2 + gamePad2.recth + 200) / 3
        self.x = 375
        self.y = 375
        if n == 1:
            self.dirX = -1
        else:
            self.dirX = 1
        self.dirY = 0
        self.moveS = False
        self.last = 0
        self.speed = self.defS
        self.fs = False
        gamePad = vPaddle(100, ((gamePad.recty + (gamePad.recth / 2)) - (self.defH1 / 2)), self.defH1)
        gamePad2 = vPaddle(650, ((gamePad2.recty + (gamePad2.recth / 2)) - (self.defH2 / 2)), self.defH2)

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, WHITE, (int(self.x), int(self.y)), self.rad)

class cpu():
    def __init__(self):
        self.dir = True
        self.prob = 0
        self.num = 0
        self.pastDir = True

    def move(self):
        if gameBall.dirX < 0:
            if gameBall.y < gamePad2.recty:
                self.num = abs(gameBall.x - gamePad.rectl) - abs(gameBall.y - gamePad2.recty) + 550
            elif gameBall.y > gamePad2.recty + gamePad2.recth:
                self.num = abs(gameBall.x - gamePad.rectl) - abs((gamePad2.recth + gamePad2.recty) - gameBall.y) + 550
            else:
                self.num = abs(gameBall.x - gamePad.rectl) + 550
        else:
            if gameBall.y < gamePad2.recty:
                self.num = abs(gamePad2.rectl - gameBall.x) - abs(gameBall.y - gamePad2.recty)
            elif gameBall.y > gamePad2.recty + gamePad2.recth:
                self.num = abs(gamePad2.rectl - gameBall.x) - abs((gamePad2.recth + gamePad2.recty) - gameBall.y)
            else:
                self.num = abs(gamePad2.rectl - gameBall.x)
        if self.num < 0:
            self.num = 0
        self.y = random.randint(2, 5)
        if (gamePad2.recty - (gamePad2.recth / self.y)) < gameBall.x < (gamePad2.recty + gamePad2.recth + (gamePad2.recth / self.y)) and gameBall.x < 500:
            self.x = 1
            self.max = 0
        elif gamePad2.recty < gameBall.x < gamePad2.recty + gamePad2.recth:
            self.x = 1
            self.max = 0
        else:
            self.x = random.randint(0, 15)
            if gameBall.x < 500:
                self.max = 14
            else:
                self.max = 16
        if self.x > self.max:
            if self.dir == self.pastDir:
                if self.dir:
                    gamePad2.moveLeft()
                else:
                    gamePad2.moveRight()
        else:
            if self.dir:
                gamePad2.moveLeft()
            else:
                gamePad2.moveRight()

    def guessSU(self):
        if gameBall.y < gamePad2.recty:
            self.pastDir = self.dir
            self.x = random.randint(0, 31)
            if self.x == 0 and gameBall.x < 500:
                self.guess(2)
            else:
                self.dir = True
        elif gameBall.y > gamePad2.recty + gamePad2.recth:
            self.pastDir = self.dir
            self.x = random.randint(0, 31)
            if self.x == 0 and gameBall.x < 500:
                self.guess(2)
            else:
                self.dir = False
        else:
            self.x = random.randint(2, 5)
            if gameBall.y < gamePad2.recty + (gamePad2.recth / self.x):
                self.x = random.randint(0, 7)
                if self.x == 0:
                    self.pastDir = self.dir
                    self.dir = True
                else:
                    self.guess(15)
            elif gameBall.y > gamePad2.recty + gamePad.recth - (gamePad2.recth / self.x):
                self.x = random.randint(0, 7)
                if self.x == 0:
                    self.pastDir = self.dir
                    self.dir = False
                else:
                    self.guess(15)
            else:
                self.guess(8)

    def guess(self, n):
        self.prob = random.randint(0, n)
        if self.prob == 0:
            self.pastDir = self.dir
            self.dir = True
        elif self.prob == 1:
            self.pastDir = self.dir
            self.dir = False
        elif self.prob == 3 or self.prob == 4:
            if gameBall.x <= 375:
                if gameBall.y < gamePad.recty + (gamePad.recth / 2):
                    self.pastDir = self.dir
                    self.dir = True
                else:
                    self.pastDir = self.dir
                    self.dir = False
            else:
                if gameBall.y < gamePad.recty + (gamePad.recth / 2):
                    self.pastDir = self.dir
                    self.dir = False
                else:
                    self.pastDir = self.dir
                    self.dir = True
        elif self.prob >= 5:
            if gameBall.y < gamePad2.recty + (gamePad2.recth / 2):
                self.pastDir = self.dir
                self.dir = False
            else:
                self.pastDir = self.dir
                self.dir = True

def devEntry(currL, lastDebL, lastdebTime):
    lel = ""
    ldl = ""
    if currL == K_n:
        lel = "m1"
        ldl = "n"
    elif currL == K_m:
        lel = "n"
        ldl = "m2"
    elif currL == K_4:
        lel = "m2"
        ldl = "4"
    elif currL == K_e:
        lel = "4"
        ldl = "e"
    elif currL == K_v:
        lel = "e"
        ldl = "v"
    elif currL == K_r:
        lel = "v"
    if lastDebL == lel and (pygame.time.get_ticks() - lastdebTime) < 1000:
        return True, ldl
    else:
        return False, ldl

def gameDraw(gamePad, gamePad2, gameBall):
    DISPLAYSURF.fill((0, 0, 0))
    if screen:
        if not gameBall.moveS:
            sFont.render_to(DISPLAYSURF, (300, 600), "Press space", WHITE)
        if dev:
            dFont.render_to(DISPLAYSURF, (0, 0), "gamePad.recth: " + str(int(gamePad.recth)), WHITE)
            dFont.render_to(DISPLAYSURF, (0, 12), "gameBall.dirX: " + str(round(gameBall.dirX, 2)), WHITE)
            dFont.render_to(DISPLAYSURF, (0, 24), "gameBall.dirY: " + str(round(gameBall.dirY, 2)), WHITE)
            dFont.render_to(DISPLAYSURF, (0, 36), "gameBall.speed: " + str(round(gameBall.speed, 4)), WHITE)
            dFont.render_to(DISPLAYSURF, (0, 48), "cpu1.prob: " + str(cpu1.prob), WHITE)
            dFont.render_to(DISPLAYSURF, (0, 60), "cpu1.dir: " + str(cpu1.dir), WHITE)
            dFont.render_to(DISPLAYSURF, (0, 72), "cpu1.num: " + str(int(cpu1.num)), WHITE)
            dFont.render_to(DISPLAYSURF, (0, 84), "gameBall.last: " + str(gameBall.last), WHITE)
            dFont.render_to(DISPLAYSURF, (0, 96), "gameBall.fs: " + str(gameBall.fs), WHITE)
        gFont.render_to(DISPLAYSURF, (300, 10), str(p1Score) + " - " + str(p2Score), WHITE)
        gamePad.draw()
        gamePad2.draw()
        gameBall.draw()
    else:
        gFont.render_to(DISPLAYSURF, (250, 25), "PONG", WHITE)
        pygame.draw.rect(DISPLAYSURF, WHITE, (25, 150, 700, 250))
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (50, 175, 650, 200))
        pygame.draw.rect(DISPLAYSURF, WHITE, (25, 450, 700, 250))
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (50, 475, 650, 200))
        gFont.render_to(DISPLAYSURF, (190, 240), "1 PLAYER", WHITE)
        gFont.render_to(DISPLAYSURF, (160, 540), "2 PLAYERS", WHITE)

if __name__ == '__main__':
    main()