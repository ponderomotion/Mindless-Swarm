import pygame
from pygame.locals import *
from sys import exit
from math import sin, cos, radians, copysign
from audio import *
from vector import *
from shared import *
import random

enemyList = []

class Enemy(object):
	def __init__(self, name = "enemy", init_pos=Vec2d(WINDOW_X/2,WINDOW_Y/2), init_vel=Vec2d(0,0)):
		self.name = name
		self.pos = Vec2d(init_pos.x,init_pos.x)
		self.vel = Vec2d(init_vel.x,init_vel.y)
		self.acc = Vec2d(0.0,0.0)
		self.bullets = []
		self.forwardEngineOn = False
		self.reverseEngineOn = False
		self.scale = 2
		self.angle = 0
		self.maxSpeed = 50

		# media
		self.fire_sound = load_sound('enemy_fire.wav')
		self.fire_sound.set_volume(0.1)
		self.engine_sound = load_sound('engine_on.wav')

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

		self.shipVertices.append(Vec2d(self.pos.x, self.pos.y))
		self.shipVertices.append(Vec2d(self.pos.x+(1*self.scale), self.pos.y+(6*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x+(3*self.scale), self.pos.y+(2*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x, self.pos.y+(10*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x-(3*self.scale), self.pos.y+(2*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x-(1*self.scale), self.pos.y+(6*self.scale)))
		
	def update(self, dt):
		# semi-implicit Euler integration
		
		# friction coefficient 0.99

		# AI : just do a random walk
		self.angle = self.angle + 10*(random.random()-0.5)

		rand1 = random.random()
		if(rand1 < 0.8): #80% chance of activating thrusters
			self.acc.x = 300 * sin(radians(self.angle))
			self.acc.y = -300 * cos(radians(self.angle))
		rand1 = random.random()
		if(rand1 < 0.01): #1% chance of shooting
			self.shoot()

		self.vel.x = self.vel.x + self.acc.x * dt
		self.vel.y = self.vel.y + self.acc.y * dt

		if abs(self.vel.x) > self.maxSpeed:
			self.vel.x = copysign(self.maxSpeed, self.vel.x)
		if abs(self.vel.y) > self.maxSpeed:
			self.vel.y = copysign(self.maxSpeed, self.vel.y)

		self.pos.x = self.pos.x + self.vel.x * dt
		self.pos.y = self.pos.y + self.vel.y * dt

		#print self.pos.x, self.vel.x, self.acc.x

		self.shipVertices[0] = Vec2d(self.pos.x, self.pos.y)
		self.shipVertices[1] = Vec2d(self.pos.x+(1*self.scale), self.pos.y+(6*self.scale))
		self.shipVertices[2] = Vec2d(self.pos.x+(3*self.scale), self.pos.y+(2*self.scale))
		self.shipVertices[3] = Vec2d(self.pos.x, self.pos.y+(10*self.scale))
		self.shipVertices[4] = Vec2d(self.pos.x-(3*self.scale), self.pos.y+(2*self.scale))
		self.shipVertices[5] = Vec2d(self.pos.x-(1*self.scale), self.pos.y+(6*self.scale))

		# periodic boundary
		if(self.pos.x > WINDOW_X):
			self.pos.x = 0
		if(self.pos.x < 0):
			self.pos.x = WINDOW_X
		if(self.pos.y > WINDOW_Y):
			self.pos.y = 0
		if(self.pos.y < 0):
			self.pos.y = WINDOW_Y

		# update all of this players bullet positions
		for bullet in self.bullets:
			#delete bullets that have gone out of bounds
			if (bullet.pos.x > WINDOW_X):
				self.bullets.remove(bullet)
				continue
			if (bullet.pos.x < 0):
				self.bullets.remove(bullet)
				continue
			if (bullet.pos.y > WINDOW_Y):
				self.bullets.remove(bullet)
				continue
			if (bullet.pos.y < 0):
				self.bullets.remove(bullet)
				continue

			bullet.pos.x = bullet.pos.x + bullet.vel.x * dt
			bullet.pos.y = bullet.pos.y + bullet.vel.y * dt

	def display(self):
		# todo: make these rotations more efficient using something like this:
		# http://gis.stackexchange.com/questions/23587/how-do-i-rotate-the-polygon-about-an-anchor-point-using-python-script
		point_1 = self.shipVertices[0].rotate(self.angle, self.pos)
		point_2 = self.shipVertices[1].rotate(self.angle, self.pos)
		point_3 = self.shipVertices[2].rotate(self.angle, self.pos)
		point_4 = self.shipVertices[3].rotate(self.angle, self.pos)
		point_5 = self.shipVertices[4].rotate(self.angle, self.pos)
		point_6 = self.shipVertices[5].rotate(self.angle, self.pos)

		pygame.draw.polygon(SCREEN, GREEN, (point_1, point_2, point_3, point_4, point_5, point_6) ,1)
		
		for bullet in self.bullets:
			pygame.draw.circle(SCREEN, RED, (int(bullet.pos.x), int(bullet.pos.y)), 2)

	def shoot(self):
		self.bullets.append(Bullet(self.pos, self.vel, self.angle))
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