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

def main():
	pygame.init()
	topScore = 0
	current_score = 0
	kill_score = 0
	displayFont = pygame.font.SysFont("consola", 22)
	pygame.display.set_caption("Laika")
	state = 0
	clock = pygame.time.Clock()
	time_passed = clock.tick() / 1000.00
	wave = 0
	rotation = NONE
	movement = NONE
	player1 = Player()
	god_mode = False
	spawn_entities = True

	try:
		highscores = readhighscores()
		topScore = highscores.high_score
	except:
		print("No highscores detected, setting to 0")
		highscores = broids_data()
		highscores.high_score = 0.0
		highscores.high_scorer = ""

	music_channel = pygame.mixer.Channel(0)

	bg_music = load_sound('XXXXX.wav')
	#music_channel.set_volume(0.3)
	music_channel.play(bg_music, loops=-1)

	draw_collision_boxes=False

	bgOne = pygame.image.load('assets/spacebg.png').convert()
	bgTwo = pygame.image.load('assets/spacebg.png').convert()
	bgOne_x = 0
	bgTwo_x = bgOne.get_width()

	while (state==0):
		pressed_keys = pygame.key.get_pressed()
		time_passed += clock.tick() / 1000.00
		for event in pygame.event.get():
			if event.type == QUIT:
				state = 1
			if event.type == KEYDOWN:
				if event.key == K_d:
					rotation = RIGHT
				elif event.key == K_ESCAPE:
					state = pauseScreen(player1)
				elif event.key == K_a:
					rotation = LEFT
				elif event.key == K_w:
					movement = FORWARDS
				elif event.key == K_s:
					movement = BACKWARDS
				elif event.key == K_SPACE:
					player1.shoot()
				elif event.key == K_g:
					god_mode = not god_mode # toggle
				elif event.key == K_p:
					state = deathScreen(1.5)
				elif event.key == K_b:
					gravList.append(BlackHole(Vec2d(WINDOW_X,random()*WINDOW_Y),Vec2d(-20.0,0.0),1))
				elif event.key == K_l:
					spawn_entities = not spawn_entities
			if event.type == KEYUP:
				if (event.key == K_d or event.key == K_a):
					rotation = NONE
				if (event.key == K_w or event.key == K_s):
					movement = NONE

		# player controls, check if player is stunned or under any other effects
		if player1.stunned:
			player1.angle = player1.angle + 10
			player1.acc.x = 0.0
			player1.acc.y = 0.0
		else:
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

		# increase background scroll speed as score increases
		bgspeed = 1 + (current_score / 100000.0)

		# draw the background
		SCREEN.blit(bgOne,(bgOne_x,0))
		SCREEN.blit(bgTwo,(bgTwo_x,0))

		bgOne_x -= bgspeed
		bgTwo_x -= bgspeed

		# periodicity
		if bgOne_x <= -1 * bgOne.get_width():
			bgOne_x = bgTwo_x + bgTwo.get_width()
		if bgTwo_x <= -1 * bgTwo.get_width():
			bgTwo_x = bgOne_x + bgOne.get_width()

		current_score = int(time_passed*1000) + kill_score
		current_score_text = displayFont.render("SCORE: " + str(current_score), True, (255,200,255))
		if(current_score > topScore):
			if not god_mode: 
				topScore = current_score 
		top_score_text = displayFont.render("TOP SCORE: " + str(topScore), True, (255,255,200))
		if god_mode:
			god_mode_text = displayFont.render("GOD MODE ENABLED", True, (100,255,100))
			SCREEN.blit(god_mode_text, (10, 550))
		SCREEN.blit(current_score_text, (10, 30))
		SCREEN.blit(top_score_text, (10, 10))

		# update positions and maybe spawn enemies
		#dt = clock.tick() / 1000.00
		dt = 0.02

		if spawn_entities:
			spawnEnemies()
			spawnBlackholes()
		
		# check enemy bullet collisions with player here
		if not god_mode:
			playerorigin = player1.shipVertices[0].rotate(player1.angle, player1.pos)
			for bullet in enemyBullets:
				if (bullet.pos.x < playerorigin[0] + 6):
					if (bullet.pos.x > playerorigin[0] - 6):
						if(bullet.pos.y < playerorigin[1] + 6):
							if(bullet.pos.y > playerorigin[1] - 6):
								# player has been hit, decide what to do to them depending
								# on bullet type
								if(bullet.type == 3):
									player1.stun()
									enemyBullets.remove(bullet)
								else: # player takes a hit and maybe dies
									enemyBullets.remove(bullet)
									if (player1.take_hit()): #take_hit returns true if dead
										player1.dead = True
										
										


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
								kill_score += 5000
		

		if(draw_collision_boxes):
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

		# update all positions and draw
		for bullet in enemyBullets:
			bullet.update(dt)
			bullet.draw()
		for bullet in playerBullets:
			bullet.update(dt)
			bullet.draw()
		for enemy in enemyList:
			enemy.update(dt)
			enemy.display()
		for expl in explosionList:
			expl.update_and_draw()
		for obj in gravList:
			obj.update(dt)
			obj.attract(player1)
			obj.draw()

		player1.update(dt)
		player1.display()

		# remove things that are no longer in the game
		pruneBullets(enemyBullets)
		pruneBullets(playerBullets)
		pruneExplosions(explosionList)
		pruneGravs(gravList)

		# did player died?
		if(player1.dead and not god_mode):
			time_passed = 0
			kill_score = 0
			bgspeed = 1
			del enemyList[:]
			del enemyBullets[:]
			del gravList[:]
			if(current_score >= topScore):
				topScore = current_score
				highscores.high_score = topScore
				writescores(highscores)
				state = deathScreen(1.5, highscore=True)
			else:
				state = deathScreen(1, highscore=False)
			player1.reset()
			player1.dead = False

		pygame.display.flip()
      
main()
pygame.quit()