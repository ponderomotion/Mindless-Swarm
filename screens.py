# this file holds functions for different screens, e.g. death screen, high score entry etc..
from audio import *
import pygame
from pygame.locals import *
from shared import *
from random import random, randint

# returns 1 if user decides to quit
def deathScreen(time=5,highscore=False):
	dsclock = pygame.time.Clock()
	timePassed = dsclock.tick() / 1000.00
	rand1 = randint(1,5)
	rand1 = int(rand1 + 0.5)
	if (rand1 == 1):
		sheitsound = load_sound('sheit.wav')
		death_text = "YOU DIED IN AGONY!"
	if (rand1 == 2):
		sheitsound = load_sound('rasp.wav')
		death_text = "YOUR EFFORTS WERE IN VAIN!"
	if (rand1 == 3):
		sheitsound = load_sound('cough.wav')
		death_text = "YOUR SHIP EXPLODED!"
	if (rand1 == 4):
		sheitsound = load_sound('wahwah.wav')
		death_text = "YOU DIDN'T SURVIVE!"
	if (rand1 == 5):
		sheitsound = load_sound('hellno.wav')
		death_text = "YOU COULDN'T BEAT THE HIGH SCORE!"
 
 	cont = False
	sheitsound.play()
	displayFont = pygame.font.SysFont("consola", 32)
	bigFont = pygame.font.SysFont("andale mono", 80)
	contFont = pygame.font.SysFont("consola", 30)

	gameover_message = bigFont.render("GAME OVER", True, (0,0,0))
	cont_message = contFont.render("Press N for a (N)ew game or Q to (Q)uit",True, (0,0,0))
	if(highscore):
		death_message = displayFont.render("You died but....NEW HIGH SCORE!", True, (0,0,0))
	else:
		death_message = displayFont.render(death_text, True, (0,0,0))

	cont = False
	while (cont==False):
		SCREEN.fill((random()*255,random()*255,random()*100))
		timePassed = timePassed + dsclock.tick() / 1000.00
		SCREEN.blit(gameover_message, (WINDOW_X/2 - gameover_message.get_width()/2,WINDOW_Y/2 - 140))
		SCREEN.blit(death_message, (WINDOW_X/2 - death_message.get_width()/2,WINDOW_Y/2 + 30))
		SCREEN.blit(cont_message, (WINDOW_X/2 - cont_message.get_width()/2,WINDOW_Y/2 + 100))

		# see if space or q has been pressed
		for event in pygame.event.get():
			if event.type == QUIT:
				cont = True
				return(1)
			if event.type == KEYDOWN:
				if event.key == K_n:
					cont = True
				elif event.key == K_q:
					cont = True
					return(1)

		pygame.display.update()
		pygame.time.wait(120)

	return(0)

def startScreen():
	SCREEN.fill(BLACK)
	

# returns 1 if user decides to quit
def pauseScreen(player1): 
 	cont = False
	bigFont = pygame.font.SysFont("andale mono", 80)
	contFont = pygame.font.SysFont("consola", 30)

	pause_message = bigFont.render("PAUSED", True, (200,255,255))
	cont_message = contFont.render("Press Space to continue or Q to (Q)uit",True, (255,255,200))

	SCREEN.blit(pause_message, (WINDOW_X/2 - pause_message.get_width()/2,WINDOW_Y/2 - 140))
	SCREEN.blit(cont_message, (WINDOW_X/2 - cont_message.get_width()/2,WINDOW_Y/2 + 30))

	pygame.display.update()

	while (cont==False):
		#SCREEN.fill((random()*255,random()*255,random()*100))
		
		# see if space or q has been pressed
		for event in pygame.event.get():
			if event.type == QUIT:
				cont = True
				return(1)
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					cont = True
				elif event.key == K_q:
					cont = True
					return(1)

	return(0)
