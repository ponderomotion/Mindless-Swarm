import pygame
from pygame.locals import *
from sys import exit
from math import sin, cos, radians, copysign, atan2, degrees
from audio import *
from vector import *
from shared import *
import random

enemyList = []

class Enemy(object):
	def __init__(self, name = "enemy", init_pos=Vec2d(WINDOW_X/2,WINDOW_Y/2), init_vel=Vec2d(0,0),init_angle=0, enemytype=1):
		self.name = name
		self.pos = Vec2d(init_pos.x,init_pos.x)
		self.vel = Vec2d(init_vel.x,init_vel.y)
		self.acc = Vec2d(0.0,0.0)
		self.physacc = Vec2d(0.0,0.0)
		self.forwardEngineOn = False
		self.reverseEngineOn = False
		self.scale = 2
		self.angle = init_angle
		self.maxspeed = 80
		self.bulletSpeed = 200

		# ENEMY TYPES #
		# 1 - Standard green with lethal red bullets
		# 2 - Purple with Blue stun bullets
		self.type = enemytype
		if self.type == 1:
			self.maxspeed = 200
		if self.type == 2:
			self.maxspeed = 300
		if self.type == 3:
			self.maxspeed = 120

		# media
		self.fire_sound = load_sound('wub.wav')
		self.fire_sound.set_volume(0.3)
		self.engine_sound = load_sound('engine_on.wav')
		self.death_sound = load_sound('explosion.wav')
		self.death_sound.set_volume(0.2)

		# give engine sound its own channel
		# self.engine_channel = pygame.mixer.Channel(EngineChannel)
		# EngineChannel = EngineChannel + 1
		# self.engine_channel.set_volume(0.3)
		# self.engine_channel.play(self.engine_sound, loops=-1)
		# self.engine_channel.pause()

		# vertices of spaceship
		self.shipVertices = []
		self.exhaustVertices = []
		self.exhaustVertices1 = [] # reverse
		self.hitboxRect = []

		self.shipVertices.append(Vec2d(self.pos.x, self.pos.y))
		self.shipVertices.append(Vec2d(self.pos.x+(1*self.scale), self.pos.y+(6*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x+(3*self.scale), self.pos.y+(2*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x, self.pos.y+(10*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x-(3*self.scale), self.pos.y+(2*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x-(1*self.scale), self.pos.y+(6*self.scale)))

		self.hitboxRect.append(Vec2d(self.pos.x-(3*self.scale), self.pos.y+(5*self.scale)))
		self.hitboxRect.append(Vec2d(self.pos.x-(3*self.scale), self.pos.y-(5*self.scale)))
		self.hitboxRect.append(Vec2d(self.pos.x+(3*self.scale), self.pos.y-(5*self.scale)))
		self.hitboxRect.append(Vec2d(self.pos.x-(3*self.scale), self.pos.y-(5*self.scale)))
		
	def update(self, dt, player1):
		# semi-implicit Euler integration
		
		# dumbest enemies
		# if (self.type == 1) or (self.type == 2):
		# 	# AI : just do a random walk		
		# 	self.angle = self.angle + 10*(random.random()-0.5)
		# 	rand1 = random.random()
		# 	if(rand1 < 0.8): #80% chance of activating thrusters
		# 		self.acc.x = 20 * sin(radians(self.angle))
		# 		self.acc.y = -20 * cos(radians(self.angle))
		# 	rand1 = random.random()
		# 	if(rand1 < 0.005): #.5% chance of shooting
		# 		self.shoot()

		# # slightly smarter
		# if (self.type == 3):
			# always face the player
		self.angle = self.aim_at(player1.pos)

		# 90% chance of thrusters firing to make them less predictable
		self.acc.x = random.random() * 100 * sin(radians(self.angle))
		self.acc.y = -random.random() * 100 * cos(radians(self.angle))

		# .9% chance of shooting
		if(random.random()<0.009):
			self.shoot()

		# update equations of motion
		self.vel.x = self.vel.x + (self.acc.x + self.physacc.x) * dt
		self.vel.y = self.vel.y + (self.acc.y + self.physacc.y) * dt

		self.physacc.x = 0
		self.physacc.y = 0

		if abs(self.vel.x) > self.maxspeed:
			self.vel.x = copysign(self.maxspeed, self.vel.x)
		if abs(self.vel.y) > self.maxspeed:
			self.vel.y = copysign(self.maxspeed, self.vel.y)

		self.pos.x = self.pos.x + self.vel.x * dt
		self.pos.y = self.pos.y + self.vel.y * dt

		#print self.pos.x, self.vel.x, self.acc.x

		if(self.type == 1 or self.type == 2):
			self.shipVertices[0] = Vec2d(self.pos.x, self.pos.y)
			self.shipVertices[1] = Vec2d(self.pos.x+(0.5*self.scale), self.pos.y+(6*self.scale))
			self.shipVertices[2] = Vec2d(self.pos.x+(3*self.scale), self.pos.y+(2*self.scale))
			self.shipVertices[3] = Vec2d(self.pos.x, self.pos.y+(10*self.scale))
			self.shipVertices[4] = Vec2d(self.pos.x-(3*self.scale), self.pos.y+(2*self.scale))
			self.shipVertices[5] = Vec2d(self.pos.x-(0.5*self.scale), self.pos.y+(6*self.scale))

		if(self.type==3):
			self.shipVertices[0] = Vec2d(self.pos.x, self.pos.y)
			self.shipVertices[1] = Vec2d(self.pos.x-(3*self.scale), self.pos.y+(5*self.scale))
			self.shipVertices[2] = Vec2d(self.pos.x, self.pos.y-(5*self.scale))
			self.shipVertices[3] = Vec2d(self.pos.x+(3*self.scale), self.pos.y+(5*self.scale))

		self.hitboxRect[0] = Vec2d(self.pos.x-(3*self.scale), self.pos.y+(5*self.scale))
		self.hitboxRect[1] = Vec2d(self.pos.x-(3*self.scale), self.pos.y-(5*self.scale))
		self.hitboxRect[2] = Vec2d(self.pos.x+(3*self.scale), self.pos.y-(5*self.scale))
		self.hitboxRect[3] = Vec2d(self.pos.x+(3*self.scale), self.pos.y+(5*self.scale))

		# periodic boundary
		# if(self.pos.x > WINDOW_X):
		# 	self.pos.x = 0
		# if(self.pos.x < 0):
		# 	self.pos.x = WINDOW_X
		# if(self.pos.y > WINDOW_Y):
		# 	self.pos.y = 0
		# if(self.pos.y < 0):
		# 	self.pos.y = WINDOW_Y

		# hard boundaries
		if(self.pos.x > WINDOW_X):
			self.pos.x = WINDOW_X
			self.vel.x = -0.7*self.vel.x
		if(self.pos.x < 0):
			self.pos.x = 0
			self.vel.x = -0.7*self.vel.x
		if(self.pos.y > WINDOW_Y):
			self.pos.y = WINDOW_Y
			self.vel.y = -0.7*self.vel.y
		if(self.pos.y < 0):
			self.pos.y = 0
			self.vel.y = -0.7*self.vel.y

	def display(self):
		# todo: make these rotations more efficient using something like this:
		# http://gis.stackexchange.com/questions/23587/how-do-i-rotate-the-polygon-about-an-anchor-point-using-python-script
		
		# type 1 and 2 have the same model
		if(self.type==1 or self.type==2):
			point_1 = self.shipVertices[0].rotate(self.angle, self.pos)
			point_2 = self.shipVertices[1].rotate(self.angle, self.pos)
			point_3 = self.shipVertices[2].rotate(self.angle, self.pos)
			point_4 = self.shipVertices[3].rotate(self.angle, self.pos)
			point_5 = self.shipVertices[4].rotate(self.angle, self.pos)
			point_6 = self.shipVertices[5].rotate(self.angle, self.pos)
		#type 3 has the same model as the player
		if(self.type==3):
			point_1 = self.shipVertices[0].rotate(self.angle, self.pos)
			point_2 = self.shipVertices[1].rotate(self.angle, self.pos)
			point_3 = self.shipVertices[2].rotate(self.angle, self.pos)
			point_4 = self.shipVertices[3].rotate(self.angle, self.pos)

		if(self.type==1):
			pygame.draw.polygon(SCREEN, GREEN, (point_1, point_2, point_3, point_4, point_5, point_6) ,1)
			#pygame.gfxdraw.aapolygon(SCREEN, (point_1, point_2, point_3, point_4, point_5, point_6), GREEN)
		elif(self.type==2):
			pygame.draw.polygon(SCREEN, (255,0,255), (point_1, point_2, point_3, point_4, point_5, point_6) ,1)
			#pygame.gfxdraw.aapolygon(SCREEN, (point_1, point_2, point_3, point_4, point_5, point_6), (255,0,255))
		elif(self.type==3):
			pygame.draw.polygon(SCREEN, (255,200,100), (point_1, point_2, point_3, point_4) ,1)


	def shoot(self):
		if(self.type==1):
			bullettype = 2
		if(self.type==2):
			bullettype = 3
		if(self.type==3):
			bullettype = 2
		enemyBullets.append(Bullet(self.pos, self.vel, self.angle, bullettype=bullettype))
		self.fire_sound.play()

	def forwardEngine_activate(self):
		self.forwardEngineOn = True
		self.engine_channel.unpause()
	def forwardEngine_deactivate(self):
		self.forwardEngineOn = False
		self.engine_channel.pause()
	def reverseEngine_activate(self):
		self.reverseEngineOn = True
		self.engine_channel.unpause()
	def reverseEngine_deactivate(self):
		self.reverseEngineOn = False
		self.engine_channel.pause()
	def aim_at(self,targetpos):
		angle = degrees(atan2(self.pos.x - targetpos.x, self.pos.y - targetpos.y))
		return ((360 - angle) % 360)

def spawnEnemies():
	#spawn enemies randomly
	# 0.1% chance of spawning an enemy
	spawnchance = 0.01

	if(random.random()<spawnchance):

		rand4 = random.randint(1,4)
		randy = random.random()*WINDOW_Y
		randx = random.random()*WINDOW_X

		# choose which wall to spawn on
		if(rand4==1): #WEST
			initxpos = 2
			initypos = randy
		if(rand4==2): #EAST
			initxpos = WINDOW_X-2
			initypos = randy
		if(rand4==3): #NORTH
			initxpos = randx
			initypos = 2
		if(rand4==4): #SOUTH
			initxpos = randx
			initypos = WINDOW_Y-2

		etype = random.randint(1,2)
		#etype = random.randint(1,3)

		new_enemy = Enemy(init_angle = (random.random()*360),init_pos=Vec2d(initxpos,initypos), enemytype=etype)
		enemyList.append(new_enemy)

