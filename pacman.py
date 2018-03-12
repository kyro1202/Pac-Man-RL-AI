import pygame
from pygame.locals import * 
from random import randint
from classes import *
from featureExtractor import *

if __name__ == "__main__" or __name__ == "pacman" :

    GAME = Maze()
    HERO = Pacman()
    VILLIAN = Blinky()
    VILLIAN2 = Inky()
    FEATURE = featureExtractor()
    pygame.init()
    GAME.scorefont = pygame.font.Font(None,30)
    done = False
    clock = pygame.time.Clock()
    bsl = 0
    isl = 0

    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == KEYDOWN:
                if event.key == K_q:
                    done = True
        HERO.pacmove(GAME)        
        GAME.screen.fill(GAME.BLACK)
        if bsl is 0:
            VILLIAN.blinkymove(GAME,HERO)
        if isl is 0:
            VILLIAN2.inkymove(GAME,HERO)
        bsl = abs(1-bsl)
        isl = abs(1-isl)     
        GAME.countfinal=0
        GAME.dispmaze()
        GAME.drawwall() 
        HERO.draw(GAME)
        VILLIAN.draw(GAME)
        VILLIAN2.draw(GAME) 
        if HERO.checkGhost(VILLIAN) or HERO.checkGhost(VILLIAN2):
            done = True
            print "Final Score = "+(str)(GAME.score)
        elif GAME.score == 106:
            GAME.reset()
            HERO.resetpacman()
            VILLIAN.resetblinky()
            VILLIAN2.resetinky()
            GAME.level += 1	
        GAME.scoredisp()
        GAME.leveldisp() 
        FEATURE.dispInky(HERO, VILLIAN2, GAME)
        FEATURE.dispBlinky(HERO, VILLIAN, GAME)
        clock.tick(10)
        pygame.display.flip()
    pygame.quit()
