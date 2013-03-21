from vector import *
import pygame
from pygame.locals import *
from shared import *
from audio import *


#define the players ship etc.
class Player(object):
	def __init__(self, name = "p1"):
		self.name = name
		self.pos = Vec2d(WINDOW_X/2,WINDOW_Y/2)
		self.vel = Vec2d(0.0,0.0)
		self.acc = Vec2d(0.0,0.0)
		self.forwardEngineOn = False
		self.reverseEngineOn = False
		self.scale = 2
		self.angle = 0
		self.maxSpeed = 700
		self.bulletSpeed = 300
		self.stunned = False

		# media
		self.fire_sound = load_sound('pew.wav')
		self.engine_sound = load_sound('engine_sophie.wav')

		# give engine sound its own channel
		self.engine_channel = pygame.mixer.Channel(1)
		self.engine_channel.set_volume(0.3)
		self.engine_channel.play(self.engine_sound, loops=-1)
		self.engine_channel.pause()

		# vertices of spaceship
		self.shipVertices = []
		self.exhaustVertices = []
		self.exhaustVertices1 = [] # reverse
		self.hitboxRect = []

		self.shipVertices.append(Vec2d(self.pos.x, self.pos.y))
		self.shipVertices.append(Vec2d(self.pos.x-(3*self.scale), self.pos.y+(5*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x, self.pos.y-(5*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x+(3*self.scale), self.pos.y+(5*self.scale)))

		self.hitboxRect.append(Vec2d(self.pos.x-(3*self.scale), self.pos.y+(5*self.scale)))
		self.hitboxRect.append(Vec2d(self.pos.x-(3*self.scale), self.pos.y-(5*self.scale)))
		self.hitboxRect.append(Vec2d(self.pos.x+(3*self.scale), self.pos.y-(5*self.scale)))
		self.hitboxRect.append(Vec2d(self.pos.x-(3*self.scale), self.pos.y-(5*self.scale)))
		
		self.exhaustVertices.append(Vec2d(self.pos.x, self.pos.y+(2*self.scale)))
		self.exhaustVertices.append(Vec2d(self.pos.x+(1.5*self.scale), self.pos.y+(3.5*self.scale)))
		self.exhaustVertices.append(Vec2d(self.pos.x, self.pos.y+(7*self.scale)))
		self.exhaustVertices.append(Vec2d(self.pos.x-(1.5*self.scale), self.pos.y+(3.5*self.scale)))

		self.exhaustVertices1.append(Vec2d(self.pos.x, self.pos.y+(2*self.scale)))
		self.exhaustVertices1.append(Vec2d(self.pos.x+(1.5*self.scale), self.pos.y+(3.5*self.scale)))
		self.exhaustVertices1.append(Vec2d(self.pos.x, self.pos.y+(5*self.scale)))
		self.exhaustVertices1.append(Vec2d(self.pos.x-(1.5*self.scale), self.pos.y+(3.5*self.scale)))

	def update(self,dt):
		# semi-implicit Euler integration
		# friction coefficient 0.99
		self.vel.x = (0.99 * self.vel.x) + self.acc.x * dt
		self.vel.y = (0.99 * self.vel.y) + self.acc.y * dt
		if self.vel.x > self.maxSpeed:
			self.vel.x = self.maxSpeed
		if self.vel.y > self.maxSpeed:
			self.vel.y = self.maxSpeed

		self.pos.x = self.pos.x + self.vel.x * dt
		self.pos.y = self.pos.y + self.vel.y * dt

		self.shipVertices[0] = Vec2d(self.pos.x, self.pos.y)
		self.shipVertices[1] = Vec2d(self.pos.x-(3*self.scale), self.pos.y+(5*self.scale))
		self.shipVertices[2] = Vec2d(self.pos.x, self.pos.y-(5*self.scale))
		self.shipVertices[3] = Vec2d(self.pos.x+(3*self.scale), self.pos.y+(5*self.scale))

		#bottomright->topright->topleft->bottomleft
		self.hitboxRect[0] = Vec2d(self.pos.x-(3*self.scale), self.pos.y+(5*self.scale))
		self.hitboxRect[1] = Vec2d(self.pos.x-(3*self.scale), self.pos.y-(5*self.scale))
		self.hitboxRect[2] = Vec2d(self.pos.x+(3*self.scale), self.pos.y-(5*self.scale))
		self.hitboxRect[3] = Vec2d(self.pos.x+(3*self.scale), self.pos.y+(5*self.scale))

		if(self.forwardEngineOn):
			self.exhaustVertices[0] = Vec2d(self.pos.x, self.pos.y+(2*self.scale))
			self.exhaustVertices[1] = Vec2d(self.pos.x+(1.5*self.scale), self.pos.y+(3.5*self.scale))
			self.exhaustVertices[2] = Vec2d(self.pos.x, self.pos.y+(7*self.scale))
			self.exhaustVertices[3] = Vec2d(self.pos.x-(1.5*self.scale), self.pos.y+(3.5*self.scale))
			self.exhaustVertices1[0] = Vec2d(self.pos.x, self.pos.y+(2*self.scale))
			self.exhaustVertices1[1] = Vec2d(self.pos.x+(1.5*self.scale), self.pos.y+(3.5*self.scale))
			self.exhaustVertices1[2] = Vec2d(self.pos.x, self.pos.y+(5*self.scale))
			self.exhaustVertices1[3] = Vec2d(self.pos.x-(1.5*self.scale), self.pos.y+(3.5*self.scale))

		if(self.reverseEngineOn):
			self.exhaustVertices1[0] = Vec2d(self.pos.x, self.pos.y+(2*self.scale))
			self.exhaustVertices1[1] = Vec2d(self.pos.x+(1.5*self.scale), self.pos.y+(3.5*self.scale))
			self.exhaustVertices1[2] = Vec2d(self.pos.x, self.pos.y+(5*self.scale))
			self.exhaustVertices1[3] = Vec2d(self.pos.x-(1.5*self.scale), self.pos.y+(3.5*self.scale))

		# periodic boundary
		if(self.pos.x > WINDOW_X):
			self.pos.x = 0
		if(self.pos.x < 0):
			self.pos.x = WINDOW_X
		if(self.pos.y > WINDOW_Y):
			self.pos.y = 0
		if(self.pos.y < 0):
			self.pos.y = WINDOW_Y

		# status updates
		self.status_update()

	def display(self):
		point_1 = self.shipVertices[0].rotate(self.angle, self.pos)
		point_2 = self.shipVertices[1].rotate(self.angle, self.pos)
		point_3 = self.shipVertices[2].rotate(self.angle, self.pos)
		point_4 = self.shipVertices[3].rotate(self.angle, self.pos)
		if self.stunned:
			pygame.draw.polygon(SCREEN, (100,100,255), (point_1, point_2, point_3, point_4) ,2)
		else:
			pygame.draw.polygon(SCREEN, WHITE, (point_1, point_2, point_3, point_4) ,1)
		if (self.forwardEngineOn):
			point_1 = self.exhaustVertices1[0].rotate(self.angle, self.pos)
			point_2 = self.exhaustVertices1[1].rotate(self.angle, self.pos)
			point_3 = self.exhaustVertices1[2].rotate(self.angle, self.pos)
			point_4 = self.exhaustVertices1[3].rotate(self.angle, self.pos)
			pygame.draw.polygon(SCREEN, YELLOW, (point_1, point_2, point_3, point_4) ,2)
			point_1 = self.exhaustVertices[0].rotate(self.angle, self.pos)
			point_2 = self.exhaustVertices[1].rotate(self.angle, self.pos)
			point_3 = self.exhaustVertices[2].rotate(self.angle, self.pos)
			point_4 = self.exhaustVertices[3].rotate(self.angle, self.pos)
			pygame.draw.polygon(SCREEN, RED, (point_1, point_2, point_3, point_4) ,1)
		if (self.reverseEngineOn):
			point_1 = self.exhaustVertices1[0].rotate(self.angle, self.pos)
			point_2 = self.exhaustVertices1[1].rotate(self.angle, self.pos)
			point_3 = self.exhaustVertices1[2].rotate(self.angle, self.pos)
			point_4 = self.exhaustVertices1[3].rotate(self.angle, self.pos)
			pygame.draw.polygon(SCREEN, BLUE, (point_1, point_2, point_3, point_4) ,1)

	def shoot(self):
		playerBullets.append(Bullet(self.pos, self.vel, self.angle,bullettype=1))
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

	def stun(self):
		self.stunned = True
		self.stuntimer = pygame.time.Clock()
		self.stuntime = 0.0

	def status_update(self):
		# check any player statuses and clear them if enough time has elapsed
		if(self.stunned):
			self.stuntime = self.stuntime + self.stuntimer.tick() / 1000.00
			if(self.stuntime > 1.5):
				self.stunned = False
