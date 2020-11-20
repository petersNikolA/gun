import pygame
from pygame.draw import *
from random import randint
import math

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TEAL = (0, 128, 128)
OLIVE = (128, 128, 0)
COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN, TEAL, OLIVE]


class Ball:
    def __init__(self, x=60, y=450):
        """ Конструктор класса ball

        Args:
        x, y - coordinates of center
        x - horizontal
        y - vertical
        r - radius
        vx - horizontal speed
        vy - vertical speed
        live - lifetime of ball
        get_time - detector of hitting
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.ay = 10
        self.color = COLORS[randint(0, 6)]
        self.id = circle(screen, self.color, (self.x, self.y), self.r)
        self.live = 30
        self.t = 0
        self.get_aim = False

    def set_speed(self, speed, alpha):
        """
        set new values of speed by direction (alpha)
        :param speed: speed of ball
        :param alpha: angle of direction
        :return: values of horizontal and vertical speed
        """
        self.vx = speed * math.cos(alpha)
        self.vy = speed * math.sin(alpha)

    def draw(self):
        """
        drawing balls in a new location
        """
        circle(screen, self.color, (int(self.x), int(self.y)), self.r)

    def move(self, dt):
        """moving of ball

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx * dt
        self.y -= self.vy * dt
        self.vy -= self.ay * dt
        if self.y - self.r <= 100 or self.y + self.r >= 500:
            self.vy *= -1
        if self.x - self.r <= 50 or self.x + self.r >= 700:
            self.vx *= -1
        self.t += dt
        if self.t >= 15:
            self.x = 0
            self.y = 0
            self.r = 0

    def hittest(self, xt, yt, rt):
        """
        checks hitting with target
        :param xt: x coordinate of target
        :param yt: y coordinate of target
        :param rt: z coordinate of target
        :return: True if hit
                False if missed
        """
        p = ((xt - self.x) ** 2 + (yt - self.y) ** 2) ** (1 / 2)
        if p <= float(self.r + rt):
            self.get_aim = True
        return self.get_aim

    def coord(self):
        """
        :return: coordinates of ball
        """
        return self.x, self.y, self.r

    def aftershot(self):
        """
        update shot flag
        :return: False
        """
        self.get_aim = False
        return self.get_aim


class Gun:
    def __init__(self, x=0, y=600, k=8):
        """

        :param x: horizontal coordinate of center
        :param y: vertical coordinate of center
        :param k: power coefficient

        Args:
        shotflag - flag of shot
        t, t0, t1 - time for timer
        """
        self.x = x
        self.y = y
        self.k = k
        self.shotflag = False
        self.t0 = 0
        self.t1 = 0
        self.t = 0

    def targeting(self, pos):
        """
        define the flight direction of ball
        :param pos: position of mouse
        :return: alpha - angle of direction
        """
        x, y = pos
        alpha = math.atan((self.y - y) / (x - self.x))
        return alpha

    def start(self):
        """
        beginning of shot
        starts timer for calculating power of shot
        """
        if not self.shotflag:
            self.shotflag = True
            self.t0 = pygame.time.get_ticks()

    def end(self):
        """
        ending of shot
        :return: first value of coefficient
        """
        self.shotflag = False
        self.k = 8

    def power_up(self):
        """
        determines power of shot based on time held down button
        :return: new value of coefficient
        """
        self.t1 = pygame.time.get_ticks()
        self.t = self.t1 - self.t0
        self.k *= self.t // 20
        if self.k > 100:
            self.k = 100
        return self.k


class Target:

    def __init__(self):
        """
        Initializing a new target

        Args:
            x, y - coordinates of center
            r - radius (size)
            vy - vertical speed
        """
        self.color = RED
        self.r = randint(15, 30)
        self.y = randint(200, 350)
        self.x = randint(200, 550)
        self.vy = randint(-30, 30)
        self.points = 0
        self.live = 1
        circle(screen, self.color, (self.x, self.y), self.r)

    def draw(self):
        """
        drawing of target
        """
        circle(screen, self.color, (int(self.x), int(self.y)), self.r)

    def move(self, dt):
        """
        moving of target
        :param dt: time (in order to make moving smooth)
        :return:
        """
        self.y += self.vy * dt
        if self.y - self.r <= 100 or self.y + self.r >= 400:
            self.vy *= -1
        if self.vy < -30:
            self.vy = -20
        if self.vy > 30:
            self.vy = 20

    def coord(self):
        """
        :return: coordinates of center
        """
        xt = self.x
        yt = self.y
        rt = self.r
        return xt, yt, rt


pygame.init()

text1 = pygame.font.Font(None, 30)
text3 = pygame.font.Font(None, 30)
alert = pygame.font.Font(None, 50)
FPS = 30
dt = 1 / FPS
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
finished = False
g1 = Gun()
t1 = Target()
t2 = Target()
bullet = 0
result = 0
balls = []
alpha = 0
while not finished:
    rect(screen, WHITE, (50, 100, 650, 400))
    rect(screen, RED, (50, 440, 20, 20))
    clock.tick(FPS)
    t1.draw()
    t2.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            g1.start()
        elif event.type == pygame.MOUSEBUTTONUP:
            alpha = g1.targeting(event.pos)
            g1.end()
            v = g1.power_up()
            ball = Ball()
            ball.set_speed(v, alpha)
            balls += [ball]
            bullet += 1
    aim1 = False
    aim2 = False
    for ball in balls:
        ball.move(dt)
        ball.draw()
        xt1, yt1, rt1 = t1.coord()
        xt2, yt2, rt2 = t2.coord()
        aim1 = ball.hittest(xt1, yt1, rt1)
        aim2 = ball.hittest(xt2, yt2, rt2)
        t1.move(dt)
        t2.move(dt)
        t1.draw()
        t2.draw()
        if aim1:
            result += 3
            t1.__init__()
            aim1 = ball.aftershot()
        elif aim2:
            result += 3
            t2.__init__()
            aim2 = ball.aftershot()
    text = "Выстрелы " + str(bullet)
    Text = "Результат " + str(result - bullet + 1)
    text2 = text1.render(text, True, WHITE, BLACK)
    text4 = text3.render(Text, True, WHITE, BLACK)
    screen.blit(text2, (50, 70))
    screen.blit(text4, (50, 500))
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
