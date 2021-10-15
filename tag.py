import pygame
import random

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

#window's dimensions
width = 500  
height = 480

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("TAG")
clock = pygame.time.Clock()

#background and initial objects
bg = pygame.image.load('images/bg.jpg')
startPos = pygame.image.load('images/standing.png')

#texts
white = (255, 255, 255)
font = pygame.font.SysFont("comicsans", 48)
starttext = font.render("Press 'space' to start!", True, white, (0,0,0))
endtext = font.render("TAGGED!", True, (0,0,0))
endsubtext = font.render("Press 'space' to replay!", True, white, (0,0,0))

jumpsound = pygame.mixer.Sound ('sounds/jump.wav')
deadsound = pygame.mixer.Sound ('sounds/dead.wav')

#start screen
run = False
start = True
while start:
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        run = True
        start = False
    else:
        win.blit(startPos, (14, 400))
        win.blit(starttext,(80, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
    pygame.display.update()

class player():
    def __init__(self, x):
        self.x = x
        self.y = 400
        self.dimension = 64
        self.vel = 5

        self.bounce = 8
        self.jumps = self.bounce
        self.isJump = False

        self.left = False
        self.right = False
        self.walks = 0

        self.walkLeft = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'),
            pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'),
            pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'),
            pygame.image.load('images/L9.png'), ]
        self.walkRight = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'),
             pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'),
             pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'),
             pygame.image.load('images/R9.png'), ]
        self.still = pygame.image.load('images/standing.png')

    def counter(self):
        if self.walks >= 27:
            self.walks = 0

        if self.left:
            win.blit(self.walkLeft[self.walks // 3], (self.x, self.y))
            self.walks += 1
        elif self.right:
            win.blit(self.walkRight[self.walks // 3], (self.x, self.y))
            self.walks += 1
        else:
            win.blit(self.still, (self.x, self.y))
            self.walks = 0
        pygame.display.update()

class bot():
    def __init__(self, x, vel):
        self.bx = x
        self.by = 400
        self.bdimension = 64
        self.bvel = vel
        
        self.bleft = False
        self.bright = True
        self.bwalks = 0
        self.pause = False
        
        self.bLeft = [pygame.image.load('images/L1E.png'), pygame.image.load('images/L2E.png'),
             pygame.image.load('images/L3E.png'),
             pygame.image.load('images/L4E.png'), pygame.image.load('images/L5E.png'),
             pygame.image.load('images/L6E.png'),
             pygame.image.load('images/L7E.png'), pygame.image.load('images/L8E.png'),
             pygame.image.load('images/L9E.png'), ]
        self.bRight = [pygame.image.load('images/R1E.png'), pygame.image.load('images/R2E.png'),
              pygame.image.load('images/R3E.png'),
              pygame.image.load('images/R4E.png'), pygame.image.load('images/R5E.png'),
              pygame.image.load('images/R6E.png'),
              pygame.image.load('images/R7E.png'), pygame.image.load('images/R8E.png'),
              pygame.image.load('images/R9E.png'), ]
    def play(self):
        if self.bwalks >= 27:
            self.bwalks = 0

        if self.bleft:
            win.blit(self.bLeft[self.bwalks // 3], (self.bx, self.by))
            if self.pause == False:
                self.bx -= self.bvel
                self.bwalks += 1
                if self.bx <= 0:
                    self.bleft = False
                    self.bright = True
        elif self.bright:
            win.blit(self.bRight[self.bwalks // 3], (self.bx, self.by))
            if self.pause == False:
                self.bx += self.bvel
                self.bwalks += 1
                if self.bx >= (width - self.bvel - self.bdimension):
                    self.bright = False
                    self.bleft = True
        pygame.display.update()

p = player(14) #our player       
#run
def playerRun(game, run):
    runtime = 0
    botcheck = False
    botx = 540 #initial bot position
    botNum = 1 #initial number of bots
    dodge = 0
    botposcheck = False
    botxcheck = 0
    velocity = [2,3,4,5]
    G = []
    for i in range (botNum):
        g = bot(botx, random.choice(velocity))
        G.append(g) #initial bots
    while run:
        while botcheck:
            g = bot(botx, random.choice(velocity))
            G.append(g)
            botcheck = False
        clock.tick(27)
        runtime += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and game.x > game.vel:
            game.x -= game.vel
            game.left = True
            game.right = False

        elif keys[pygame.K_RIGHT] and game.x < (width - game.vel - game.dimension):
            game.x += game.vel
            game.left = False
            game.right = True

        else:
            game.left = False
            game.right = False
            game.walks = 0

        if not game.isJump:
            if keys[pygame.K_SPACE]:
                pygame.mixer.Sound.play(jumpsound)
                pygame.mixer.music.stop()
                game.isJump = True
                game.left = False
                game.right = False
                game.walks = 0
        else:
            if game.jumps >= -game.bounce:
                if game.jumps <= 0:
                    sign = 1
                else:
                    sign = -1
                game.y += ((game.jumps ** 2) // 2) * sign
                game.jumps -= 1
            else:
                game.isJump = False
                game.jumps = game.bounce
        
        for i in range(botNum):
            if game.x+(game.dimension//2) in range(G[i].bx, G[i].bx+G[i].bdimension-20):
                if game.y == G[i].by:
                    pygame.mixer.Sound.play(deadsound)
                    pygame.mixer.music.stop()
                    while game.y >= 0:
                        game.y -= game.vel
                        win.blit(bg, (0, 0))
                        game.counter()
                        for i in range(botNum):
                            G[i].pause = True
                            G[i].play()
                    run = False
                for j in range(game.x, game.x+game.dimension):
                    for k in range(G[i].bx, G[i].bx+G[i].bdimension):
                        if j == G[i].bx+G[i].bdimension:
                            dodge += 1
        
        win.blit(bg, (0, 0))
        scoretext = font.render(str(dodge//128), 1, (255, 255, 255))
        respawntext = font.render("New respawn in T minus " +str(10-(runtime//27)), 1, (0, 0, 0))
        win.blit(scoretext,(240, 20))
        if runtime >= 189:
            win.blit(respawntext,(50, 200))
        game.counter()
        for i in range(botNum):
            G[i].play()
        if runtime == 270:
            botNum += 1
            botcheck = True
            runtime = 0

playerRun(p, run)

#rerun
def rerun(game, check):
    game.x = 14
    game.y = 400
    playerRun(game, check)

#end screen
end = True
while end:
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        rerun(p, run)
    else:
        win.blit(bg, (0, 0))
        win.blit(endtext,(80, 185)) 
        win.blit(endsubtext,(80, 215))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
    pygame.display.update()

pygame.quit()
