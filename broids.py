import pygame
from pygame.locals import *
from sys import exit
from math import sin, cos, radians
from audio import *

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

SCREEN = pygame.display.set_mode((WINDOW_X,WINDOW_Y),0,32)
clock = pygame.time.Clock()



class Vec2d():
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def to_tuple(self):
		return self.x, self.y
	def rotate(self, degrees, origin):
		theta = radians(degrees)
		newx = origin.x + ((self.x - origin.x) * cos(theta) - (self.y - origin.y) * sin(theta))
		newy = origin.y + ((self.x - origin.x) * sin(theta) + (self.y - origin.y) * cos(theta))
		return newx,newy

class Bullet(object):
	def __init__(self, init_pos, init_vel, angle):
		self.pos = Vec2d(init_pos.x, init_pos.y)
		self.vel = Vec2d(init_vel.x, init_vel.y)
		self.vel.x = (300 + abs(self.vel.x)) * sin(radians(angle))
		self.vel.y = -(300 + abs(self.vel.y)) * cos(radians(angle))

class Player(object):
	def __init__(self, name = "p1"):
		self.name = name
		self.pos = Vec2d(WINDOW_X/2,WINDOW_Y/2)
		self.vel = Vec2d(0.0,0.0)
		self.acc = Vec2d(0.0,0.0)
		self.bullets = []
		self.forwardEngineOn = False
		self.reverseEngineOn = False
		self.scale = 2
		self.angle = 0
		self.maxSpeed = 500

		# media
		self.fire_sound = load_sound('player_fire.wav')
		self.engine_sound = load_sound('engine_on.wav')

		# give engine sound its own channel
		self.engine_channel = pygame.mixer.Channel(1)
		self.engine_channel.set_volume(0.3)
		self.engine_channel.play(self.engine_sound, loops=-1)
		self.engine_channel.pause()

		# vertices of spaceship
		self.shipVertices = []
		self.exhaustVertices = []
		self.exhaustVertices1 = [] # reverse

		self.shipVertices.append(Vec2d(self.pos.x, self.pos.y))
		self.shipVertices.append(Vec2d(self.pos.x-(3*self.scale), self.pos.y+(5*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x, self.pos.y-(5*self.scale)))
		self.shipVertices.append(Vec2d(self.pos.x+(3*self.scale), self.pos.y+(5*self.scale)))
		
		self.exhaustVertices.append(Vec2d(self.pos.x, self.pos.y+(2*self.scale)))
		self.exhaustVertices.append(Vec2d(self.pos.x+(1.5*self.scale), self.pos.y+(3.5*self.scale)))
		self.exhaustVertices.append(Vec2d(self.pos.x, self.pos.y+(7*self.scale)))
		self.exhaustVertices.append(Vec2d(self.pos.x-(1.5*self.scale), self.pos.y+(3.5*self.scale)))

		self.exhaustVertices1.append(Vec2d(self.pos.x, self.pos.y+(2*self.scale)))
		self.exhaustVertices1.append(Vec2d(self.pos.x+(1.5*self.scale), self.pos.y+(3.5*self.scale)))
		self.exhaustVertices1.append(Vec2d(self.pos.x, self.pos.y+(5*self.scale)))
		self.exhaustVertices1.append(Vec2d(self.pos.x-(1.5*self.scale), self.pos.y+(3.5*self.scale)))

	def update(self):
		# semi-implicit Euler integration
		dt = clock.tick() / 1000.00
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
		point_1 = self.shipVertices[0].rotate(self.angle, self.pos)
		point_2 = self.shipVertices[1].rotate(self.angle, self.pos)
		point_3 = self.shipVertices[2].rotate(self.angle, self.pos)
		point_4 = self.shipVertices[3].rotate(self.angle, self.pos)
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
		
		for bullet in self.bullets:
			pygame.draw.circle(SCREEN, WHITE, (int(bullet.pos.x), int(bullet.pos.y)), 2)

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

def main():
	pygame.init()
	player1 = Player()
	displayFont = pygame.font.SysFont("consola", 16)
	pygame.display.set_caption("AstroRoidRage")
	state = 0
	clock = pygame.time.Clock()
	time_passed = clock.tick() / 1000.00
	wave = 0
	rotation = NONE
	movement = NONE
	#bg_music = load_sound('XXXXX.ogg')
	# start music
	#bg_music.play()
	while (state==0):
		SCREEN.fill(BLACK)
		pressed_keys = pygame.key.get_pressed()
		time_passed += clock.tick() / 1000.00
		for event in pygame.event.get():
			if event.type == QUIT:
				state = 1
			if event.type == KEYDOWN:
				if event.key == K_d:
					rotation = RIGHT
				elif event.key == K_a:
					rotation = LEFT
				elif event.key == K_w:
					movement = FORWARDS
				elif event.key == K_s:
					movement = BACKWARDS
				elif event.key == K_SPACE:
					player1.shoot()
			if event.type == KEYUP:
				if (event.key == K_d or event.key == K_a):
					rotation = NONE
				if (event.key == K_w or event.key == K_s):
					movement = NONE
		if rotation == RIGHT:
			player1.angle = player1.angle + 10
		elif rotation == LEFT:
			player1.angle = player1.angle - 10
		if movement == FORWARDS:
			player1.acc.x = 300 * sin(radians(player1.angle))
			player1.acc.y = -300 * cos(radians(player1.angle))
			player1.forwardEngine_activate()
		if movement == BACKWARDS:
			player1.acc.x = -300 * sin(radians(player1.angle))
			player1.acc.y = 300 * cos(radians(player1.angle))
			player1.reverseEngine_activate()
		if movement == NONE:
			player1.acc.x = 0.0
			player1.acc.y = 0.0
			player1.forwardEngine_deactivate()
			player1.reverseEngine_deactivate()

		clock_time = displayFont.render("TIME: " + str(time_passed), True, (255,0,255)) 
		SCREEN.blit(clock_time, (400, 500))
		player1.update()
		player1.display()
		pygame.display.update()
      
main()
pygame.quit()