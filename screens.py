# this file holds functions for different screens, e.g. death screen, high score entry etc..
from audio import *
import pygame
from pygame.locals import *
from shared import *
from random import random, randint

# All screens return which state to go to next
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
				return(QUIT_STATE)
			if event.type == KEYDOWN:
				if event.key == K_n:
					cont = True
				elif event.key == K_q:
					cont = True
					return(QUIT_STATE)

		pygame.display.update()
		pygame.time.wait(120)

	return(GAME_SCREEN)

def startScreen():

	titleFont = pygame.font.SysFont("andale mono",180)
	subFont = pygame.font.SysFont("consola", 20)
	titleText = "LAIKA"
	subtext = "A Game by Daniel Fletcher"
	subMessage = subFont.render(subtext,False,WHITE)
	opFont = pygame.font.SysFont("consola", 50)
	optext = []

	optext1 = "1: 1 Player Start"
	optext2 = "2: 2 Player Start"
	optext3 = "3: View Controls"
	optext4 = "4: Quit"

	roptext1 = opFont.render(optext1, False, WHITE)
	roptext2 = opFont.render(optext2, False, WHITE)
	roptext3 = opFont.render(optext3, False, WHITE)
	roptext4 = opFont.render(optext4, False, WHITE)

	global FULLSCREEN

	while(True):
		SCREEN.fill(BLACK)
		titleMessage = titleFont.render(titleText,False,(random()*255,random()*255,random()*255))
		
		SCREEN.blit(titleMessage, (WINDOW_X/2 - titleMessage.get_width()/2,WINDOW_Y/2 - 310))
		SCREEN.blit(subMessage, (WINDOW_X/2 - subMessage.get_width()/2 + 120,WINDOW_Y/2 - 130))

		SCREEN.blit(roptext1, (WINDOW_X/2 - roptext1.get_width()/2,WINDOW_Y/2))
		SCREEN.blit(roptext2, (WINDOW_X/2 - roptext1.get_width()/2,WINDOW_Y/2 + 40))
		SCREEN.blit(roptext3, (WINDOW_X/2 - roptext1.get_width()/2,WINDOW_Y/2 + 80))
		SCREEN.blit(roptext4, (WINDOW_X/2 - roptext1.get_width()/2,WINDOW_Y/2 + 120))

		for event in pygame.event.get():
			if event.type == QUIT:
				return(QUIT_STATE)
			if event.type == KEYDOWN:
				if event.key == K_1:
					return(GAME_SCREEN)
				elif event.key == K_2:
					return(QUIT_STATE)
				elif event.key == K_q:
					return(QUIT_STATE)
				elif event.key == K_f:
					#toggle fullscreen
					FULLSCREEN = not FULLSCREEN
					if(not FULLSCREEN):
						pygame.display.set_mode((WINDOW_X,WINDOW_Y),pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
					else:
						pygame.display.set_mode((WINDOW_X,WINDOW_Y),pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
		pygame.display.flip()

# returns 1 if user decides to quit
def pauseScreen(): 
 	cont = False
	bigFont = pygame.font.SysFont("andale mono", 80)
	contFont = pygame.font.SysFont("consola", 30)

	pause_message = bigFont.render("PAUSED", True, (200,255,255))
	cont_message = contFont.render("Press Space to continue or Q to (Q)uit",True, (255,255,200))

	SCREEN.blit(pause_message, (WINDOW_X/2 - pause_message.get_width()/2,WINDOW_Y/2 - 140))
	SCREEN.blit(cont_message, (WINDOW_X/2 - cont_message.get_width()/2,WINDOW_Y/2 + 30))

	pygame.display.update()

	while(True):
		#SCREEN.fill((random()*255,random()*255,random()*100))
		
		# see if space or q has been pressed
		for event in pygame.event.get():
			if event.type == QUIT:
				return(QUIT_STATE)
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					break
				elif event.key == K_q:
					return(QUIT_STATE)

	return(GAME_SCREEN)
