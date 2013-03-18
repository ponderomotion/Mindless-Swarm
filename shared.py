import pygame
from pygame.locals import *
from vector import *

WINDOW_X = 800
WINDOW_Y = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (20, 20, 255)
YELLOW = (255,255,0)

NONE = 0
LEFT = 1
RIGHT = 2

FORWARDS = 1
BACKWARDS = 2

SCREEN = pygame.display.set_mode((WINDOW_X,WINDOW_Y),pygame.DOUBLEBUF)
clock = pygame.time.Clock()

class Bullet(object):
	def __init__(self, init_pos, init_vel, angle, speed=300):
		self.pos = Vec2d(init_pos.x, init_pos.y)
		self.vel = Vec2d(init_vel.x, init_vel.y)
		self.vel.x = (speed + abs(self.vel.x)) * sin(radians(angle))
		self.vel.y = -(speed + abs(self.vel.y)) * cos(radians(angle))