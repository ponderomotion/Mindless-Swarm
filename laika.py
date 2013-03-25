import pygame
from pygame.locals import *
from sys import exit
from math import sin, cos, radians
from audio import *
from enemies import *
from vector import *
from shared import *
from random import random, randint
from screens import *
from player import *
from gravity_object import *


# main game class
class Laika(object):
	def __init__(self):
		# pygame window initialisation
		pygame.init()
		pygame.display.set_caption("Laika")

		# Score Keeping vars
		self.topScore = 0
		self.currentScore = 0
		self.killScore = 0
		self.ticksSurvived = 0
		self.newhighscore = False

		# timing and flow
		self.clock = pygame.time.Clock()
		self.time = self.clock.tick()/1000.0

		# states:
		# 0 : Title Screen
		# 1 : Options Screen
		# 2 : Main Game Screen
		# 3 : Pause Screen
		# 4 : Game Over Screen
		# 5 : Quit
		self.state = TITLE_SCREEN

		# fonts
		self.scoreFont = pygame.font.SysFont("consola", 22)

		# toggles and modes
		self.autoSpawn = True
		self.debug = True
		self.quit = False

		self.load_and_init_everything()
		self.initPlayers()


	def load_and_init_everything(self):
		# load any highscores
		try:
			self.highScores = readhighscores()
			self.topScore = self.highScores.high_score
		except:
			print("No highscores detected, setting to 0")
			self.highScores = broids_data()
			self.highScores.high_score = 0.0
			self.highScores.high_scorer = ""

		# init sound system
		pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=65536)
		self.music_channel = pygame.mixer.Channel(0)
		self.bg_music = load_sound('XXXXX.wav')
		#bg_music.play()
		#music_channel.set_volume(0.3)
		#music_channel.play(bg_music, loops=-1)

		# init graphics
		self.bgOne = load_image('spacebg.png')
		self.bgTwo = load_image('spacebg.png')
		self.fgOne = load_image('fgbg.png', alpha = True)
		self.fgTwo = load_image('fgbg.png', alpha = True)
		self.bgOne_x = 0
		self.bgTwo_x = self.bgOne.get_width()
		self.fgOne_x = 0
		self.fgTwo_x = self.fgOne.get_width()

	def initPlayers(self):
		# different depending on 1p or 2p game
		# just assume 1p for now
		self.player1 = Player()

	def mainLoop(self): # main loop
		while not (self.quit):
			
			if(self.state == TITLE_SCREEN):
				self.state = startScreen()

			if(self.state == GAME_SCREEN):
				self.getInput()
				self.spawnEntities()
				self.update_and_draw_background()
				self.update_and_draw_scores_and_status()
				self.update_and_draw_all_entities()
				self.collisions()

				# did player died? This code needs moving elsewhere
				if(self.player1.dead and not self.player1.godMode):
					del enemyList[:]
					del enemyBullets[:]
					del gravList[:]
					if(self.player1.currentScore >= self.topScore):
						self.topScore = self.player1.currentScore
						self.highScores.high_score = self.topScore
						self.highScores.high_scorer = "1up"
						writescores(self.highScores)
						self.newhighscore = True
					else:
						self.newhighscore = False
					self.state = GAMEOVER_SCREEN
					self.player1.reset()

			if(self.state==PAUSE_SCREEN):
				self.state = pauseScreen()
			
			if(self.state==GAMEOVER_SCREEN):
				self.state = deathScreen(1,highscore=self.newhighscore)

			if(self.state==QUIT_STATE):
				self.quit = True

	def getInput(self): # handle all input
		global FULLSCREEN
		pressed_keys = pygame.key.get_pressed()
		self.time += self.clock.tick() / 1000.00
		for event in pygame.event.get():
			if event.type == QUIT:
				state = self.quit = True
			if event.type == KEYDOWN:
				if event.key == K_d:
					self.player1.rotation = RIGHT
				elif event.key == K_ESCAPE:
					self.state = PAUSE_SCREEN
				elif event.key == K_a:
					self.player1.rotation = LEFT
				elif event.key == K_w:
					self.player1.movement = FORWARDS
				elif event.key == K_s:
					self.player1.movement = BACKWARDS
				elif event.key == K_SPACE:
					self.player1.shoot()
				elif event.key == K_g:
					self.player1.godMode = not self.player1.godMode
				elif event.key == K_p:
					self.state = GAMEOVER_SCREEN
				elif event.key == K_b:
					spawnBlackholes(forceSpawn=True)
				elif event.key == K_l:
					spawn_entities = not spawn_entities
				elif event.key == K_f:
					#toggle fullscreen
					FULLSCREEN = not FULLSCREEN
					if(not FULLSCREEN):
						pygame.display.set_mode((WINDOW_X,WINDOW_Y),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
					else:
						pygame.display.set_mode((WINDOW_X,WINDOW_Y),pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
			if event.type == KEYUP:
				if (event.key == K_d or event.key == K_a):
					self.player1.rotation = NONE
				if (event.key == K_w or event.key == K_s):
					self.player1.movement = NONE

	def update_and_draw_background(self):

		# increase background scroll speed as score increases
		bgspeed = 1 + (self.currentScore / 100000.0)
		fgspeed = 2.5 * bgspeed

		# draw the background
		SCREEN.blit(self.bgOne,(self.bgOne_x,0))
		SCREEN.blit(self.bgTwo,(self.bgTwo_x,0))

		# draw the forground
		SCREEN.blit(self.fgOne,(self.fgOne_x,0))
		SCREEN.blit(self.fgTwo,(self.fgTwo_x,0))

		# move along
		self.bgOne_x -= bgspeed
		self.bgTwo_x -= bgspeed
		self.fgOne_x -= fgspeed
		self.fgTwo_x -= fgspeed

		# periodicity
		if self.bgOne_x <= -1 * self.bgOne.get_width():
			self.bgOne_x = self.bgTwo_x + self.bgTwo.get_width()
		if self.bgTwo_x <= -1 * self.bgTwo.get_width():
			self.bgTwo_x = self.bgOne_x + self.bgOne.get_width()
		if self.fgOne_x <= -1 * self.fgOne.get_width():
			self.fgOne_x = self.fgTwo_x + self.fgTwo.get_width()
		if self.fgTwo_x <= -1 * self.fgTwo.get_width():
			self.fgTwo_x = self.fgOne_x + self.fgOne.get_width()

	def update_and_draw_scores_and_status(self):
		current_score_text = self.scoreFont.render("SCORE: " + str(self.player1.currentScore), True, (255,200,255))
		if(self.currentScore > self.topScore):
			if not god_mode: 
				self.topScore = self.player1.currentScore 
		top_score_text = self.scoreFont.render("TOP SCORE: " + str(self.topScore), True, (255,255,200))
		
		# status text
		if self.player1.godMode:
			god_mode_text = self.scoreFont.render("GOD MODE ENABLED", True, (100,255,100))
			SCREEN.blit(god_mode_text, (10, 550))
		SCREEN.blit(current_score_text, (10, 30))
		SCREEN.blit(top_score_text, (10, 10))

	def update_and_draw_all_entities(self):
		dt = clock.tick() / 800.00
		#dt = 0.02	
		# update all positions and draw
		for bullet in enemyBullets:
			bullet.update(dt)
			bullet.draw()
		for bullet in playerBullets:
			bullet.update(dt)
			bullet.draw()
		for enemy in enemyList:
			enemy.update(dt,self.player1)
			enemy.display()
		for expl in explosionList:
			expl.update_and_draw()
		for obj in gravList:
			obj.update(dt)
			obj.attract(self.player1)
			obj.draw()

		self.player1.update(dt)
		self.player1.display()

		# remove things that are no longer in the game
		pruneBullets(enemyBullets)
		pruneBullets(playerBullets)
		pruneExplosions(explosionList)
		pruneGravs(gravList)

		pygame.display.flip()

	def spawnEntities(self):
		spawnEnemies()
		spawnBlackholes()

	def collisions(self):
		# check enemy bullet collisions with player 1 here
		playerorigin = self.player1.shipVertices[0].rotate(self.player1.angle, self.player1.pos)
		if not self.player1.godMode:
			for bullet in enemyBullets:
				if (bullet.pos.x < playerorigin[0] + 6):
					if (bullet.pos.x > playerorigin[0] - 6):
						if(bullet.pos.y < playerorigin[1] + 6):
							if(bullet.pos.y > playerorigin[1] - 6):
								# player has been hit, decide what to do to them depending
								# on bullet type
								if(bullet.type == 3):
									self.player1.stun()
									enemyBullets.remove(bullet)
								else: # player takes a hit and maybe dies
									enemyBullets.remove(bullet)
									if (self.player1.take_hit()): #take_hit returns true if dead
										self.player1.dead = True

		# check player bullet collisions with enemies here
		for bullet in playerBullets:
			for enemy in enemyList:
				enemyorigin = Vec2d(enemy.pos.x, enemy.pos.y + 9)
				enemyorigin = enemyorigin.rotate(enemy.angle, enemy.pos)
				if (bullet.pos.x < enemyorigin[0] + 8):
					if (bullet.pos.x > enemyorigin[0] - 8):
						if (bullet.pos.y < enemyorigin[1] + 8):
							if (bullet.pos.y > enemyorigin[1] - 8):
								enemy.death_sound.play()
								explosionList.append(explosion(enemy.pos))
								enemyList.remove(enemy)
								try:
									#dont crash here because there's a possibilty that the
									#bullet is also pruned by screen edge
									playerBullets.remove(bullet)
								except:
									None
								self.player1.killScore += 5000
		
		# draw the collision boxes in debug mode
		if(self.debug):
			# draw the crap player collision box
			point_1 = (playerorigin[0]-7,playerorigin[1]-7)
			point_2 = (playerorigin[0]+7,playerorigin[1]-7)
			point_3 = (playerorigin[0]+7,playerorigin[1]+7)
			point_4 = (playerorigin[0]-7,playerorigin[1]+7)
			pygame.draw.polygon(SCREEN, BLUE, (point_1, point_2, point_3, point_4) ,1)

			# draw enemy collision boxes
			for enemy in enemyList:
				enemyorigin = Vec2d(enemy.pos.x, enemy.pos.y + 9)
				enemyorigin = enemyorigin.rotate(enemy.angle, enemy.pos)
				point_1 = (enemyorigin[0] + 7, enemyorigin[1] + 7)
				point_2 = (enemyorigin[0] + 7, enemyorigin[1] - 7)
				point_3 = (enemyorigin[0] - 7, enemyorigin[1] - 7)
				point_4 = (enemyorigin[0] - 7, enemyorigin[1] + 7)
				pygame.draw.polygon(SCREEN, BLUE, (point_1, point_2, point_3, point_4) ,1)


def main():
	game = Laika()
	game.mainLoop()

      
main()
pygame.mixer.quit()
pygame.quit()