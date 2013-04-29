import pygame
from stopandgo import world

clock = pygame.time.Clock()
FRAMES_PER_SECOND = 60

def step():
    for thing in world:
        thing.switch()
    for thing in world:
        thing.display()
    clock.tick(FRAMES_PER_SECOND)

