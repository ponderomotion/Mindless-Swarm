# this file holds functions for different screens, e.g. death screen, high score entry etc..
import pygame
from pygame.locals import *
from shared import *
from audio import *
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

def startScreen(bg):

	titleFont = pygame.font.SysFont("andale mono",180)
	titleFont.set_underline(True)
	subFont = pygame.font.SysFont("consola", 22)
	titleText = "LAIKA"
	subtext = "A Game by Daniel Fletcher"
	subMessage = subFont.render(subtext,False,WHITE)
	opFont = pygame.font.SysFont("consola", 50)
	optext = []

	optext1 = "1: 1 Player Start"
	optext2 = "2: 2 Player Start"
	optext3 = "3: View Controls"
	optext4 = "4: Credits"
	optext5 = "5: Quit"

	roptext1 = opFont.render(optext1, False, (200,255,255))
	roptext2 = opFont.render(optext2, False, (200,255,255))
	roptext3 = opFont.render(optext3, False, (200,255,255))
	roptext4 = opFont.render(optext4, False, (200,255,255))
	roptext5 = opFont.render(optext5, False, (200,255,255))

	global FULLSCREEN

	while(True):
		bg.update_and_draw()

		titleMessage = titleFont.render(titleText,False,(random()*255,random()*255,random()*255))
		
		SCREEN.blit(titleMessage, (WINDOW_X/2 - titleMessage.get_width()/2,WINDOW_Y/2 - 300))
		SCREEN.blit(subMessage, (WINDOW_X/2 - subMessage.get_width()/2 + 150,WINDOW_Y/2 - 100))

		SCREEN.blit(roptext1, (WINDOW_X/2 - roptext1.get_width()/2,WINDOW_Y/2))
		SCREEN.blit(roptext2, (WINDOW_X/2 - roptext1.get_width()/2,WINDOW_Y/2 + 50))
		SCREEN.blit(roptext3, (WINDOW_X/2 - roptext1.get_width()/2,WINDOW_Y/2 + 100))
		SCREEN.blit(roptext4, (WINDOW_X/2 - roptext1.get_width()/2,WINDOW_Y/2 + 150))
		SCREEN.blit(roptext5, (WINDOW_X/2 - roptext1.get_width()/2,WINDOW_Y/2 + 200))

		for event in pygame.event.get():
			if event.type == QUIT:
				return(QUIT_STATE)
			if event.type == KEYDOWN:
				if event.key == K_1:
					return(GAME_SCREEN)
				elif event.key == K_2:
					return(GAME_SCREEN)
				elif event.key == K_3:
					None
				elif event.key == K_4:
					return(CREDITS_SCREEN)
				elif event.key == K_5:
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

def creditsScreen(bg):

	nFont = pygame.font.SysFont("consola", 35)
	uFont = pygame.font.SysFont("consola", 25)

	ntext1 = "Programming and Design"
	ntext2 = "Music"
	ntext3 = "Sound Effects"
	dantext = "Daniel Fletcher"
	ashtext = "Ashley Wilkinson"
	soptext = "Sophie Rees"

	ntext1 = nFont.render(ntext1, False, (200,255,255))
	ntext2 = nFont.render(ntext2, False, (200,255,255))
	ntext3 = nFont.render(ntext3, False, (200,255,255))

	utext1 = uFont.render(dantext, False, (255,255,200))
	utext2 = uFont.render(ashtext, False, (255,255,200))
	utext3 = uFont.render(soptext, False, (255,255,200))

	global FULLSCREEN

	while(True):
		bg.update_and_draw()
		
		# Programming and Design
		SCREEN.blit(ntext1, (WINDOW_X/2 - ntext1.get_width()/2,WINDOW_Y/2 - 150))
		# Daniel Fletcher
		SCREEN.blit(utext1, (WINDOW_X/2 - utext1.get_width()/2,WINDOW_Y/2 - 100))
		# Music
		SCREEN.blit(ntext2, (WINDOW_X/2 - ntext2.get_width()/2,WINDOW_Y/2 - 50))
		# Ashley Wilkinson
		SCREEN.blit(utext2, (WINDOW_X/2 - utext2.get_width()/2,WINDOW_Y/2))
		# Sound Effects
		SCREEN.blit(ntext3, (WINDOW_X/2 - ntext3.get_width()/2,WINDOW_Y/2 + 50))
		# Sophie Rees
		SCREEN.blit(utext1, (WINDOW_X/2 - utext1.get_width()/2,WINDOW_Y/2 + 100))
		SCREEN.blit(utext3, (WINDOW_X/2 - utext3.get_width()/2,WINDOW_Y/2 + 120))

		for event in pygame.event.get():
			if event.type == QUIT:
				return(QUIT_STATE)
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return(TITLE_SCREEN)
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
		
		# see if space or q has been pressed
		for event in pygame.event.get():
			if event.type == QUIT:
				return(QUIT_STATE)
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					return(GAME_SCREEN)
				elif event.key == K_q:
					return(TITLE_SCREEN)


# hold and advance backdrop
class Background(object):
    def __init__(self):
        # init graphics
        self.bgOne = load_image('spacebg.png')
        self.bgTwo = load_image('spacebg.png')
        self.fgOne = load_image('fgbg.png', alpha = True)
        self.fgTwo = load_image('fgbg.png', alpha = True)
        self.bgOne_x = 0
        self.bgTwo_x = self.bgOne.get_width()
        self.fgOne_x = 0
        self.fgTwo_x = self.fgOne.get_width()
        
    def update_and_draw(self):
        # increase background scroll speed as score increases
        #bgspeed = 1 + (self.currentScore / 100000.0)
        bgspeed = 1
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
