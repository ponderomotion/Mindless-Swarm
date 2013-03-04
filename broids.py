import pygame
from pygame.locals import *
from sys import exit
from math import sin, cos, radians
from audio import *
from enemies import *
from vector import *
from shared import *
from random import random


def deathScreen(time=5):
	dsclock = pygame.time.Clock()
	timePassed = dsclock.tick() / 1000.00
	while (timePassed<time):
		SCREEN.fill((random()*255,random()*255,random()*255))
		timePassed = timePassed + dsclock.tick() / 1000.00
		displayFont = pygame.font.SysFont("consola", 32)
		death_message = displayFont.render("YOU DIED", True, (0,0,0))
		SCREEN.blit(death_message, (WINDOW_X/2,WINDOW_Y/2))
		pygame.display.update()



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
	topScore = 0.0
	player1 = Player()
	new_enemy = Enemy()
	enemyList.append(new_enemy)
	displayFont = pygame.font.SysFont("consola", 16)
	pygame.display.set_caption("How Long Can You Survive the Mindless Swarm?")
	state = 0
	clock = pygame.time.Clock()
	time_passed = clock.tick() / 1000.00
	wave = 0
	rotation = NONE
	movement = NONE
	bg_music = load_sound('XXXXX.ogg')
	# start music
	bg_music.play()
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
				#elif event.key == K_p:
					#deathScreen(2.5)
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

		current_score = displayFont.render("SCORE: " + str(int(time_passed*1000)), True, (255,120,255)) 
		top_score = displayFont.render("TOP SCORE: " + str(topScore), True, (255,255,0))
		SCREEN.blit(current_score, (10, 30))
		SCREEN.blit(top_score, (10, 10))

		# update positions and maybe spawn enemies
		#dt = clock.tick() / 1000.00
		dt = 0.02

		# 0.1% chance of spawning an enemy
		rand1 = random()
		if(rand1<0.02):
			new_enemy = Enemy(init_angle = (random()*360))
			enemyList.append(new_enemy)
		
		player1.update(dt)
		for enemy in enemyList:
			enemy.update(dt)
		
		# check enemy bullet collisions here
		playerorigin = player1.shipVertices[0].rotate(player1.angle, player1.pos)
		for enemy in enemyList:
			for bullet in enemy.bullets:
				if (bullet.pos.x < playerorigin[0] + 6):
					if (bullet.pos.x > playerorigin[0] - 6):
						if(bullet.pos.y < playerorigin[1] + 6):
							if(bullet.pos.y > playerorigin[1] - 6):
								if(time_passed > topScore):
									topScore = int(time_passed) * 1000
								time_passed = 0
								del enemyList[:]
								deathScreen(1)
		
		# draw the crap collision box
		point_1 = (playerorigin[0]-7,playerorigin[1]-7)
		point_2 = (playerorigin[0]+7,playerorigin[1]-7)
		point_3 = (playerorigin[0]+7,playerorigin[1]+7)
		point_4 = (playerorigin[0]-7,playerorigin[1]+7)
		pygame.draw.polygon(SCREEN, BLUE, (point_1, point_2, point_3, point_4) ,1)



		for enemy in enemyList:
			enemy.display()
		player1.display()

		pygame.display.update()
      
main()
pygame.quit()