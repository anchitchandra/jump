import pygame

pygame.init()

window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("jump")
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 100, 0)
IDKcolor = (200, 100, 100)
diesound = pygame.mixer.Sound('Game/hit.wav')
bulletsound = pygame.mixer.Sound('Game/b.wav')
hitsound = pygame.mixer.Sound('Game/h.wav')
ghitsound = pygame.mixer.Sound('Game/die.wav')


music = pygame.mixer.music.load('Game/music.mp3')
pygame.mixer.music.play(-1)

walkright = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'),
             pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'),
             pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png')]
walkleft = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'),
            pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'),
            pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png')]
bg = pygame.image.load('Game/bg.jpg')
char = pygame.image.load('Game/standing.png')
clock = pygame.time.Clock()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.v = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


class Player(object):
    def __init__(self, x, y, width, hight):
        self.x = x
        self.y = y
        self.width = width
        self.hight = hight
        self.iv = 5
        self.isjump = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkcount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y, 28, 60)

    def draw(self, window):
        if self.walkcount + 1 >= 27:
            self.walkcount = 0

        if not (self.standing):

            if self.left:
                window.blit(walkleft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1

            elif self.right:
                window.blit(walkright[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
        else:
            if self.right:
                window.blit(walkright[0], (self.x, self.y))
            else:
                window.blit(walkleft[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y, 28, 60)
        #pygame.draw.rect(window, red, self.hitbox, 2)
    def hit(self):
        self.isjump = False
        self.jumpcount = 10
        self.x = 60
        self.y = 410
        self.walkcount = 0

        textscreen("-5", red, 350, 250)
        pygame.display.update()
        i = 0
        while i < 60:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 61
                    pygame.quit()



class Enemy():
    walkright = [pygame.image.load('Game/R1E.png'), pygame.image.load('Game/R2E.png'),
                 pygame.image.load('Game/R3E.png'), pygame.image.load('Game/R4E.png'),
                 pygame.image.load('Game/R5E.png'), pygame.image.load('Game/R6E.png'),
                 pygame.image.load('Game/R7E.png'), pygame.image.load('Game/R8E.png'),
                 pygame.image.load('Game/R9E.png'), pygame.image.load('Game/R10E.png'),
                 pygame.image.load('Game/R11E.png')]
    walkleft = [pygame.image.load('Game/L1E.png'), pygame.image.load('Game/L2E.png'), pygame.image.load('Game/L3E.png'),
                pygame.image.load('Game/L4E.png'), pygame.image.load('Game/L5E.png'), pygame.image.load('Game/L6E.png'),
                pygame.image.load('Game/L7E.png'), pygame.image.load('Game/L8E.png'), pygame.image.load('Game/L9E.png'),
                pygame.image.load('Game/L10E.png'), pygame.image.load('Game/L11E.png')]

    def __init__(self, x, y, width, hight, end):
        self.x = x
        self.y = y
        self.hight = hight
        self.width = width
        self.end = end
        self.walkcount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 17, self.y, 32, 60)
        self.health = 10
        self.visible = True

    def draw(self, window):
        self.move()
        if self.visible:
            if self.walkcount + 1 >= 33:
                self.walkcount = 0

            if self.vel > 0:
                window.blit(self.walkright[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            else:
                window.blit(self.walkleft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            pygame.draw.rect(window, red, (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, green, (self.hitbox[0], self.hitbox[1] - 20, (50 - (5 * (10 - self.health))), 10))
            self.hitbox = (self.x + 17, self.y, 28, 60)
            #pygame.draw.rect(window, red, self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

            diesound.play()
        #print('HIT')


def textscreen(text, color, x, y):
    text_screen = font.render(text, True, color)
    window.blit(text_screen, [x, y])


def redraw():

    window.blit(bg, (0, 10))
    man.draw(window)
    goblin.draw(window)

    for bullet in bullets:
        bullet.draw(window)

    textscreen("POINTS: " + str(score), black, 0, 10)
    if goblin.visible == False:
        textscreen("YOU WON!!!!", IDKcolor, 250, 250)

    pygame.display.update()


#####################################mainloop###################################3
font = pygame.font.SysFont('comicsans', 30, True, True)
man = Player(300, 420, 64, 64)
goblin = Enemy(0, 425, 64, 64, 600)
run = True
shootloop = 0
bullets = []
score = 0
while run:
    clock.tick(27)
    if goblin.visible == True:

        if man.hitbox[0] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and  man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                score -= 5
                man.hit()
                ghitsound.play()
    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                score += 1
                goblin.hit()
                hitsound.play()

                bullets.pop(bullets.index(bullet))

        if bullet.x < 700 and bullet.x > 0:
            bullet.x += bullet.v
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootloop == 0:
        bulletsound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.hight // 2), 6, black, facing))

        shootloop = 1

    elif keys[pygame.K_RIGHT] and man.x < 700 - man.width - man.iv:
        man.x += man.iv
        man.right = True
        man.left = False
        man.standing = False
    elif keys[pygame.K_LEFT] and man.x > man.iv:
        man.x -= man.iv
        man.left = True
        man.right = False
        man.standing = False
    else:
        man.standing = True
        man.walkcount = 0

    if not (man.isjump):

        if keys[pygame.K_UP]:
            man.isjump = True
            man.right = False
            man.left = False
            man.walkcount = 0

    else:
        if man.jumpcount >= -10:
            neg = 1
            if man.jumpcount < 0:
                neg = -1
            man.y -= (man.jumpcount ** 2) * 0.5 * neg
            man.jumpcount -= 1
        else:
            man.isjump = False
            man.jumpcount = 10

    redraw()
pygame.quit()
