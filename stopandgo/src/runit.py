import pygame, sys
from pygame import mouse
from stopandgo import importLevel, graphics, scheduler, level1

importLevel(level1)

def isQuit(event):
    if event.type == pygame.QUIT:
        return True
    elif event.type == pygame.KEYDOWN:
        if event.mod == 1024 and event.unicode == u'q':
            return True
    return False

black = 0, 0, 0
while True:
    for event in pygame.event.get():
        if isQuit(event):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.mod == 0 and event.unicode == u' ':
                scheduler.pauseOrResume()

    graphics.screen.fill(black)
    scheduler.step()
    pygame.display.flip()
