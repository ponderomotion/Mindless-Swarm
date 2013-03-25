from vector import *
import pygame
from pygame.locals import *
import pygame.gfxdraw
from shared import *
from audio import *

#define the players ship etc.
class Player(object):
	def __init__(self, name = "p1", initpos=Vec2d(WINDOW_X/2,WINDOW_Y/2)):
		self.name = name
		self.pos = Vec2d(initpos.x,initpos.y)
		self.vel = Vec2d(0.0,0.0)
		self.acc = Vec2d(0.0,0.0)
		self.physacc = Vec2d(0.0,0.0)
		self.forwardEngineOn = False
		self.reverseEngineOn = False
		self.scale = 2
		self.angle = 0
		self.maxSpeed = 700
		self.bulletSpeed = 300
		self.stunned = False
		self.dead = False
		self.godMode = False

		self.shieldstrength = 2
		self.currentScore = 0
		self.killScore = 0
		self.ticksSurvived = 0
		self.dead = False

		self.rotation = NONE
		self.movement = NONE

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

		# player controls, check if player is stunned or under any other effects
		if self.stunned:
			self.angle = self.angle + 10
			self.acc.x = 0.0
			self.acc.y = 0.0
		else:
			if self.rotation == RIGHT:
				self.angle = self.angle + 10
			elif self.rotation == LEFT:
				self.angle = self.angle - 10
			if self.movement == FORWARDS:
				self.acc.x = 300 * sin(radians(self.angle))
				self.acc.y = -300 * cos(radians(self.angle))
				self.forwardEngine_activate()
			if self.movement == BACKWARDS:
				self.acc.x = -300 * sin(radians(self.angle))
				self.acc.y = 300 * cos(radians(self.angle))
				self.reverseEngine_activate()
			if self.movement == NONE:
				self.acc.x = 0.0
				self.acc.y = 0.0
				self.forwardEngine_deactivate()
				self.reverseEngine_deactivate()

		# semi-implicit Euler integration
		# friction coefficient 0.99
		self.vel.x = (0.99 * self.vel.x) + (self.acc.x+self.physacc.x) * dt
		self.vel.y = (0.99 * self.vel.y) + (self.acc.y+self.physacc.y) * dt
		
		#reset
		self.physacc = Vec2d(0.0,0.0)

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

		# status updates
		self.status_update()

		self.ticksSurvived += 1
		self.currentScore = self.ticksSurvived * 10 + self.killScore

	def display(self):
		point_1 = self.shipVertices[0].rotate(self.angle, self.pos)
		point_2 = self.shipVertices[1].rotate(self.angle, self.pos)
		point_3 = self.shipVertices[2].rotate(self.angle, self.pos)
		point_4 = self.shipVertices[3].rotate(self.angle, self.pos)
		if self.stunned:
			pygame.draw.polygon(SCREEN, (100,100,255), (point_1, point_2, point_3, point_4) ,2)
		else:
			#pygame.draw.polygon(SCREEN, WHITE, (point_1, point_2, point_3, point_4) ,1)
			#pygame.draw.aalines(SCREEN, WHITE, True, (point_1, point_2, point_3, point_4) ,False)
			pygame.gfxdraw.aapolygon(SCREEN, (point_1, point_2, point_3, point_4), WHITE)
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
		if (self.shieldstrength > 0):
			if(self.shieldstrength == 2):
				#pygame.draw.circle(SCREEN, (100,100,255), (int(self.pos.x), int(self.pos.y)), 12,1)
				pygame.gfxdraw.aacircle(SCREEN, int(self.pos.x), int(self.pos.y), 12, (100,100,255))
			if(self.shieldstrength == 1):
				pygame.gfxdraw.aacircle(SCREEN, int(self.pos.x), int(self.pos.y), 11, (100,20,20))

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
	def take_hit(self):
		self.shieldstrength = self.shieldstrength - 1
		if self.shieldstrength < 0:
			return True
		else:
			return False
	def stun(self):
		self.stunned = True
		self.stuntimer = pygame.time.Clock()
		self.stuntime = 0.0
	def reset(self):
		self.shieldstrength = 2
		self.currentScore = 0
		self.killScore = 0
		self.ticksSurvived = 0
		self.dead = False

	def status_update(self):
		# check any player statuses and clear them if enough time has elapsed
		if(self.stunned):
			self.stuntime = self.stuntime + self.stuntimer.tick() / 1000.00
			if(self.stuntime > 1.5):
				self.stunned = False





