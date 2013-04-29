import pygame
from stopandgo import world

clock = pygame.time.Clock()
FRAMES_PER_SECOND = 60
paused = False

def pauseOrResume():
    global paused
    paused = not paused

def step():
    if not paused:
        for thing in world:
            thing.switch()
    for thing in world:
        thing.display()
    clock.tick(FRAMES_PER_SECOND)

