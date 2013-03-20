import pygame
from pygame.locals import *
from vector import *
import pickle

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
	def __init__(self, init_pos, init_vel, angle, bullettype=1):
		# BULLET TYPES:
		# 1: Player's white bullets
		# 2: Standard red lethal
		# 3: Blue stun bullet
		self.speed = 300
		self.type = bullettype
		

		# all bullets that dont have the default speed
		if bullettype == 2:
			self.speed = 100
		if bullettype == 3:
			self.speed = 50
		self.pos = Vec2d(init_pos.x, init_pos.y)
		self.vel = Vec2d(init_vel.x, init_vel.y)
		self.vel.x = (self.speed + abs(self.vel.x)) * sin(radians(angle))
		self.vel.y = -(self.speed + abs(self.vel.y)) * cos(radians(angle))
	def update(self, dt):
		self.pos.x = self.pos.x + self.vel.x * dt
		self.pos.y = self.pos.y + self.vel.y * dt
	def draw(self):
		if (self.type == 1):
			pygame.draw.circle(SCREEN, WHITE, (int(self.pos.x), int(self.pos.y)), 2)
		if (self.type == 2):
			pygame.draw.circle(SCREEN, RED, (int(self.pos.x), int(self.pos.y)), 2)
		if (self.type == 3):
			pygame.draw.circle(SCREEN, BLUE, (int(self.pos.x), int(self.pos.y)), 3)

# object to hold data between games i.e. high scores, settings etc.
class broids_data(object):
	def __init__(self):
		self.high_score = 0.0
		self.high_scorer = None #placeholder for name

# load highscores
def writescores(highscores):
	with open('dat.pk', 'wb') as output:
		pickle.dump(highscores,output,pickle.HIGHEST_PROTOCOL)
		print "output written"

def readhighscores():
	highscores = None
	with open('dat.pk', 'rb') as input:
		highscores = pickle.load(input)
	return highscores

