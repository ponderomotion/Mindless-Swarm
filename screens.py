# this file holds functions for different screens, e.g. death screen, high score entry etc..
from audio import *
import pygame
from pygame.locals import *
from shared import *
from random import random, randint

def deathScreen(time=5,highscore=False):
	dsclock = pygame.time.Clock()
	timePassed = dsclock.tick() / 1000.00
	rand1 = randint(1,5)
	rand1 = int(rand1 + 0.5)
	if (rand1 == 1):
		sheitsound = load_sound('sheit.wav')
	if (rand1 == 2):
		sheitsound = load_sound('rasp.wav')
	if (rand1 == 3):
		sheitsound = load_sound('cough.wav')
	if (rand1 == 4):
		sheitsound = load_sound('wahwah.wav')
	if (rand1 == 5):
		sheitsound = load_sound('hellno.wav')
 
 	cont = False
	sheitsound.play()
	while (timePassed<time):
		SCREEN.fill((random()*255,random()*255,random()*255))
		timePassed = timePassed + dsclock.tick() / 1000.00
		displayFont = pygame.font.SysFont("consola", 32)
		if(highscore):
			death_message = displayFont.render("You died but....NEW HIGH SCORE!", True, (0,0,0))
		else:
			death_message = displayFont.render("YOU DIED IN AGONY!", True, (0,0,0))
		SCREEN.blit(death_message, (WINDOW_X/2 - death_message.get_width()/2,WINDOW_Y/2))
		pygame.display.update()