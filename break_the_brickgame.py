import sys
import math
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect, KEYUP
import time


 
class Brick:
    """object representing a brick"""
    def __init__(self, col, rect, speed=0):
        self.col = col
        self.rect = rect
        self.speed = speed
        self.dir = random.randint(-45, 45) + 270
 
    def move(self):
        """ moving ball """
        self.rect.centerx += math.cos(math.radians(self.dir)) * self.speed
        self.rect.centery -= math.sin(math.radians(self.dir)) * self.speed
    def draw(self):
        """ object representing """
        if self.speed == 0:
            pygame.draw.rect(SURFACE, self.col, self.rect)
        else:
            pygame.draw.ellipse(SURFACE, self.col, self.rect)
 
#eventtime
def eventTime():
    global BALLS
 
    # adding 1 extra balls once it hits 1000
    for i in range(1):
        BALLS.append(Brick((200, 242, 0), Rect(300, 400, 20, 20), 10))
    
    # set ball speed as 15
    for BALL in BALLS:
        BALL.speed = 10
 
def tick():
    """ process """
    global BALLS, BRICKS, score, iseventTime, startTime, endTime
 
    # put the input section
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                PADDLE.rect.centerx -= 10
            elif event.key == K_RIGHT:
                PADDLE.rect.centerx += 10
    for BALL in BALLS:
        if BALL.rect.centery < 1000:
            BALL.move()
 
        # when it confront the ball
        prevlen = len(BRICKS)
        BRICKS = [x for x in BRICKS
                if not x.rect.colliderect(BALL.rect)]
        if len(BRICKS) != prevlen:
            BALL.dir *= -1
            score += 100 # get score + 100
 
        # if score is 1000, and not evertime -> make it to eventtime
        if score == 1000 and iseventTime == False:
            iseventTime = True
            eventTime()
        # count 10 sec, and then after 10 sec eventtime is over
        elif iseventTime == True:    
            if startTime == 0.0:
                startTime = time.time()
            elif startTime != 0.0:
                endTime = time.time()
                if endTime - startTime >= 10: # 10초
                    iseventTime = False
 
        # when it hit paddle
        if PADDLE.rect.colliderect(BALL.rect):
            BALL.dir = 90 + (PADDLE.rect.centerx - BALL.rect.centerx) \
                / PADDLE.rect.width * 80
 
        # when it hi the wall
        if BALL.rect.centerx < 0 or BALL.rect.centerx > 600:
            BALL.dir = 180 - BALL.dir
        if BALL.rect.centery < 0:
            BALL.dir = -BALL.dir
            BALL.speed = 15

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((600, 800))
FPSCLOCK = pygame.time.Clock()
BRICKS = []
PADDLE = Brick((242, 242, 0), Rect(300, 700, 100, 30))
BALLS = [Brick((242, 242, 0), Rect(300, 400, 20, 20), 10)]
 
isNeedToRestart = False
iseventTime = False
score = 0
startTime = 0.0
endTime = 0.0
# Reset
def init():
    global SURFACE, FPSCLOCK, BRICKS, PADDLE, BALLS, isNeedToRestart, iseventTime, score, startTime, endTime
 
    pygame.init()
    pygame.key.set_repeat(5, 5)
    SURFACE = pygame.display.set_mode((600, 800))
    FPSCLOCK = pygame.time.Clock()
    BRICKS = []
    PADDLE = Brick((242, 242, 0), Rect(300, 700, 100, 30))
    BALLS = [Brick((242, 242, 0), Rect(300, 400, 20, 20), 10)]
    isNeedToRestart = False
    iseventTime = False
    score = 0
    startTime = 0.0
    endTime = 0.0
 
def main():
    global isNeedToRestart, score, iseventTime, startTime, endTime
 
    """main fuction """
    myfont = pygame.font.SysFont(None, 80)
    smallfont = pygame.font.SysFont(None, 36)
    scorefont = pygame.font.SysFont(None, 25)
    mess_clear = myfont.render("Cleared!", True, (255, 255, 0))
    mess_over = myfont.render("Game Over!", True, (255, 255, 0))
    mess_replay = smallfont.render("replay (press r)", True, (255, 0, 0))
    fps = 30
    colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0),
              (0, 255, 0), (128, 0, 128), (0, 0, 255)]

    # adding bricks
    for ypos, color in enumerate(colors, start=0):
        for xpos in range(0, 5):
            BRICKS.append(Brick(color, Rect(xpos * 100 + 60, ypos * 50 + 40, 80, 30)))
    while True:
        tick()
    # draw ball
        SURFACE.fill((0, 0, 0))
        for BALL in BALLS:
            BALL.draw()
        PADDLE.draw()
 
        # draw bricks
        for brick in BRICKS:
            brick.draw()        
 
        # if you get rid of every bricks(win)
        if len(BRICKS) == 0:
            SURFACE.blit(mess_clear, (200, 400))
        
        # if balls goes under paddle, remove that ball
        for BALL in BALLS:
            if BALL.rect.centery > 800 and len(BRICKS) > 0:
                BALLS.remove(BALL)
 
        # end of event time
        if iseventTime == False and startTime != 0.0 and endTime != 0.0:
             # get rid of extra event balls, and leave one ball.
            for BALL in BALLS:
                BALLS.remove(BALL)
                if(len(BALLS) == 1):
                    break
            startTime = 0.0
            endTime = 0.0
            # speed 10
            for BALL in BALLS:
                BALL.speed = 10
 
        # there is no more ball to play(end)
        if len(BALLS) <= 0:
            SURFACE.blit(mess_over, (150, 400))
            SURFACE.blit(mess_replay, (230, 460))
            isNeedToRestart = True
 
        # scoreboard
        mess_score = scorefont.render("score : " + str(score), True, (255, 255, 255))
        SURFACE.blit(mess_score, (10, 10))
 
        pygame.display.update()
        FPSCLOCK.tick(fps)
 
        # Press r to restart the game
        while isNeedToRestart:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == pygame.K_r:
                    isNeedToRestart = False
                    break
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    break
 
            if isNeedToRestart == False:
                init()
                main()
                break
            
 
if __name__ == '__main__':
    main()