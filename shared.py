import pygame
from pygame.locals import *
from vector import *
import cPickle as pickle
from random import random

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

TITLE_SCREEN = 0
OPTION_SCREEN = 1
GAME_SCREEN = 2
PAUSE_SCREEN = 3
GAMEOVER_SCREEN = 4
CREDITS_SCREEN = 5
QUIT_STATE = 6

FULLSCREEN = False

SCREEN = pygame.display.set_mode((WINDOW_X,WINDOW_Y),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
clock = pygame.time.Clock()

enemyBullets = []
playerBullets = []
explosionList = []

class Bullet(object):
	def __init__(self, init_pos, init_vel, angle, bullettype=1):
		# BULLET TYPES:
		# 1: Player's white bullets
		# 2: Standard red lethal
		# 3: Blue stun bullet
		self.speed = 300
		self.type = bullettype
		# for animated bullets
		self.fliptag = 0

		# all bullets that dont have the default speed
		if bullettype == 2:
			self.speed = 100
		if bullettype == 3:
			self.speed = 50
		self.pos = Vec2d(init_pos.x, init_pos.y)
		self.vel = Vec2d(init_vel.x, init_vel.y)
		self.physacc = Vec2d(0, 0)
		self.vel.x = (self.speed + abs(self.vel.x)) * sin(radians(angle))
		self.vel.y = -(self.speed + abs(self.vel.y)) * cos(radians(angle))
	def update(self, dt):
		self.vel.x = self.vel.x + self.physacc.x * dt
		self.vel.x = self.vel.x + self.physacc.y * dt

		self.pos.x = self.pos.x + self.vel.x * dt
		self.pos.y = self.pos.y + self.vel.y * dt

		self.physacc = Vec2d(0, 0)
	def draw(self):
		if (self.type == 1):
			pygame.draw.circle(SCREEN, WHITE, (int(self.pos.x), int(self.pos.y)), 2)
		if (self.type == 2):
			pygame.draw.circle(SCREEN, RED, (int(self.pos.x), int(self.pos.y)), 2)
		if (self.type == 3):
			self.fliptag += 1
			if(self.fliptag <= 7):
				pygame.draw.circle(SCREEN, BLUE, (int(self.pos.x), int(self.pos.y)), 3)
			elif (self.fliptag > 7):
				pygame.draw.circle(SCREEN, WHITE, (int(self.pos.x), int(self.pos.y)), 2)
			if(self.fliptag == 10):
				self.fliptag = 0
			pygame.draw.circle(SCREEN, BLUE, (int(self.pos.x), int(self.pos.y)), 1)

def pruneBullets(bulletlist):
	# update all of this players bullet positions
	for bullet in bulletlist:
		#delete bullets that have gone out of bounds
		if (bullet.pos.x > WINDOW_X):
			bulletlist.remove(bullet)
			continue
		if (bullet.pos.x < 0):
			bulletlist.remove(bullet)
			continue
		if (bullet.pos.y > WINDOW_Y):
			bulletlist.remove(bullet)
			continue
		if (bullet.pos.y < 0):
			bulletlist.remove(bullet)
			continue

def pruneExplosions(explosions):
	for expl in explosions:
		if expl.age > 0.5:
			explosions.remove(expl)


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

# draw an explosion where a ship has been destroyed
class explosion(object):
	def __init__(self,position,etype=1):
		self.pos = Vec2d(position.x, position.y)

		# made up of 2 stars that alternate in colour
		self.star1verts = []
		self.star2verts = []

		self.timer = pygame.time.Clock()
		self.age = 0.0

		self.fliptag = 0

		self.debrisverts = []
		self.debrisvels = []

		self.star1verts.append((self.pos.x-4, self.pos.y-4))
		self.star1verts.append((self.pos.x, self.pos.y-12)) # north point
		self.star1verts.append((self.pos.x+4, self.pos.y-4))
		self.star1verts.append((self.pos.x+12, self.pos.y)) # east point
		self.star1verts.append((self.pos.x+4, self.pos.y+4))
		self.star1verts.append((self.pos.x, self.pos.y+12)) # south point
		self.star1verts.append((self.pos.x-4, self.pos.y+4))
		self.star1verts.append((self.pos.x-12, self.pos.y)) # west point

		self.star2verts.append((self.pos.x, self.pos.y-4))
		self.star2verts.append((self.pos.x+10, self.pos.y-10)) # north east point
		self.star2verts.append((self.pos.x+4, self.pos.y))
		self.star2verts.append((self.pos.x+10, self.pos.y+10)) # south east point
		self.star2verts.append((self.pos.x, self.pos.y+4))
		self.star2verts.append((self.pos.x-10, self.pos.y+10)) # south west point
		self.star2verts.append((self.pos.x-4, self.pos.y))
		self.star2verts.append((self.pos.x-10, self.pos.y-10)) # north west point

		self.debrisverts.append((self.pos.x+4,self.pos.y+4))
		self.debrisverts.append((self.pos.x-4,self.pos.y+4))
		self.debrisverts.append((self.pos.x-4,self.pos.y-4))
		self.debrisverts.append((self.pos.x+4,self.pos.y-4))

		# debris velocites
		self.debrisvels.append((1,1))
		self.debrisvels.append((-1,1))
		self.debrisvels.append((-1,-1))
		self.debrisvels.append((1,-1))

	def update_and_draw(self):
		self.age = self.age + self.timer.tick() / 1000.00

		# update debris positions
		tmp = []
		for i in range(0,4):
			tmp.append((self.debrisverts[i][0] + self.debrisvels[i][0] * 2.0,self.debrisverts[i][1] + self.debrisvels[i][1] * 2.0))

		self.debrisverts = tmp

		for debvert in self.debrisverts:
			pygame.draw.circle(SCREEN, (random()*255,random()*255,random()*100), (int(debvert[0]),int(debvert[1])), 1)

		self.fliptag += 1
		if(self.fliptag <= 7):
			pygame.draw.polygon(SCREEN, (255,random()*255,random()*100), self.star1verts , 0)
			pygame.draw.polygon(SCREEN, (255,255,random()*100), self.star2verts , 0)
		elif (self.fliptag > 7):
			pygame.draw.polygon(SCREEN, (255,255,random()*100), self.star1verts , 0)
			pygame.draw.polygon(SCREEN, (255,random()*100,random()*100), self.star2verts , 0)
		if(self.fliptag == 10):
			self.fliptag = 0