# Laika
# Daniel Fletcher 2013
# License: 
#    Creative Commons Attribution-NonCommercial 2.5
#    See LICENSE for details

# this object will fly through the game and attract everything to it
from vector import *
from shared import *
from enemies import *
import pygame
from pygame.locals import *
from math import sqrt
from random import random

gravList = []

def spawnBlackholes(forceSpawn=False):
	if(random()<0.0005 or forceSpawn):
		xvel = 50*random()
		gravList.append(BlackHole(Vec2d(WINDOW_X,random()*WINDOW_Y),Vec2d(-xvel,0.0),1))

def pruneGravs(objlist):
	for obj in objlist:
		if (obj.pos.x > WINDOW_X):
			objlist.remove(obj)
			continue
		if (obj.pos.x < 0):
			objlist.remove(obj)
			continue
		if (obj.pos.y > WINDOW_Y):
			objlist.remove(obj)
			continue
		if (obj.pos.y < 0):
			objlist.remove(obj)
			continue

class BlackHole(object):
	def __init__(self, init_pos, init_vel, angle, mass=1.0):
		self.pos = Vec2d(init_pos.x,init_pos.y)
		self.vel = Vec2d(init_vel.x,init_vel.y)
		self.angle = angle
		self.mass = 5000.0
		self.radius = 15
		self.G = 1.0

	def update(self,dt):
		self.pos.x = self.pos.x + self.vel.x * dt
		self.pos.y = self.pos.y + self.vel.y * dt

	def draw(self):
		pygame.draw.circle(SCREEN, (70,40,40), (int(self.pos.x), int(self.pos.y)), self.radius)
		pygame.draw.circle(SCREEN, (70,60,50), (int(self.pos.x), int(self.pos.y)), self.radius-3)
	
	def attract(self, player1, player2=None):
		# attract all enemies and players
		for enemy in enemyList:
			enemy.physacc += self.calc_acc(enemy.pos)
			if(magnitude(self.pos,enemy.pos)<self.radius):
				enemyList.remove(enemy)
				enemy.death_sound.play()
				explosionList.append(explosion(enemy.pos))

		# collisions
		for bullet in enemyBullets:
			bullet.physacc += self.calc_acc(bullet.pos)
			if(magnitude(self.pos,bullet.pos)<self.radius):
				enemyBullets.remove(bullet)

		for bullet in playerBullets:
			bullet.physacc += self.calc_acc(bullet.pos)
			if(magnitude(self.pos,bullet.pos)<self.radius):
				playerBullets.remove(bullet)

		for star in l2List:
			star.physacc += self.calc_acc(star.pos)
			if(magnitude(self.pos,star.pos)<self.radius):
				l2List.remove(star)

		player1.physacc += self.calc_acc(player1.pos)
		if(magnitude(self.pos,player1.pos)<self.radius):
			player1.dead = True

			

	def calc_acc(self,bpos):
		#given its position, calculates acceleration on it
		r = magnitude(self.pos,bpos)
		if(r<400): # cut off radius
			rhatx = bpos.x - self.pos.x
			rhaty = bpos.y - self.pos.y
			accx = -(rhatx * self.G * self.mass) / (r**2)
			accy = -(rhaty * self.G * self.mass) / (r**2)
		else:
			accx = 0.0
			accy = 0.0

		return Vec2d(accx, accy)




# magnitude between 2 vec2d's
def magnitude(v1,v2):
	return sqrt((v2.x-v1.x)**2 + (v2.y-v1.y)**2) 




