# Laika
# Daniel Fletcher 2013
# License: 
#    Creative Commons Attribution-NonCommercial 2.5
#    See LICENSE for details

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
		death_text = "YOUR SHIP EXPLODED AND YOU BURNED ALIVE!"
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
	optext2 = "2: 2 Player Start(Coming Soon)"
	optext3 = "3: View Controls(Coming Soon)"
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
    def __init__(self, quality = MEDIUM_QUALITY):
        # init graphics

        self.quality = quality
        self.layer1a = load_image('bglayer1.png')
        self.layer1b = load_image('bglayer1.png')
        self.layer1a_x = 0
        self.layer1b_x = self.layer1a.get_width()

        if quality == HIGH_QUALITY:
        	self.layer2a = load_image('bglayer2.png', alpha = True)
        	self.layer2b = load_image('bglayer2.png', alpha = True)
        	self.layer2a_x = 0
        	self.layer2b_x = self.layer2a.get_width()
        if quality == HIGH_QUALITY or quality == MEDIUM_QUALITY:
        	self.layer3a = load_image('bglayer3.png', alpha = True)
        	self.layer3b = load_image('bglayer3.png', alpha = True)
        	self.layer3a_x = 0
        	self.layer3b_x = self.layer3a.get_width()

    def set_quality(quality):
    	self.quality = quality
        self.layer1a = load_image('bglayer1.png')
        self.layer1b = load_image('bglayer1.png')
        self.layer1a_x = 0
        self.layer1b_x = self.layer1a.get_width()
        self.layer2a = None
        self.layer2b = None
        self.layer3a = None
        self.layer3b = None

        if quality == HIGH_QUALITY:
        	self.layer2a = load_image('bglayer2.png', alpha = True)
        	self.layer2b = load_image('bglayer2.png', alpha = True)
        	self.layer2a_x = 0
        	self.layer2b_x = self.layer2a.get_width()
        if quality == HIGH_QUALITY or quality == MEDIUM_QUALITY:
        	self.layer3a = load_image('bglayer3.png', alpha = True)
        	self.layer3b = load_image('bglayer3.png', alpha = True)
        	self.layer3a_x = 0
        	self.layer3b_x = self.layer3a.get_width()

        
    def update_and_draw(self):
        # increase background scroll speed as score increases
        #bgspeed = 1 + (self.currentScore / 100000.0)
        
        # background layer 1 drawn for all quality levels
        l1speed = 0.3
        # draw the bottom layer
        SCREEN.blit(self.layer1a,(self.layer1a_x,0))
        SCREEN.blit(self.layer1b,(self.layer1b_x,0))
        # move along
        self.layer1a_x -= l1speed
        self.layer1b_x -= l1speed
        # periodicity
        if self.layer1a_x <= -1 * self.layer1a.get_width():
            self.layer1a_x = self.layer1a_x + self.layer1a.get_width()
        if self.layer1b_x <= -1 * self.layer1b.get_width():
            self.layer1b_x = self.layer1b_x + self.layer1b.get_width()

        if self.quality == HIGH_QUALITY:
        	l2speed = 1.0
        	# middle layer
        	SCREEN.blit(self.layer2a,(self.layer2a_x,0))
        	SCREEN.blit(self.layer2b,(self.layer2b_x,0))
        	self.layer2a_x -= l2speed
        	self.layer2b_x -= l2speed
        	if self.layer2a_x <= -1 * self.layer2a.get_width():
        		self.layer2a_x = self.layer2a_x + self.layer2a.get_width()
        	if self.layer2b_x <= -1 * self.layer2b.get_width():
        		self.layer2b_x = self.layer2b_x + self.layer2b.get_width()
        
        if self.quality == HIGH_QUALITY or self.quality == MEDIUM_QUALITY:
        	l3speed = 2.5
        	# top layer
        	SCREEN.blit(self.layer3a,(self.layer3a_x,0))
        	SCREEN.blit(self.layer3b,(self.layer3b_x,0))        
        	self.layer3a_x -= l3speed
        	self.layer3b_x -= l3speed

        
        	if self.layer3a_x <= -1 * self.layer3a.get_width():
        		self.layer3a_x = self.layer3a_x + self.layer3a.get_width()
        	if self.layer3b_x <= -1 * self.layer3b.get_width():
        		self.layer3b_x = self.layer3b_x + self.layer3b.get_width()

