import pygame

size = width, height = 800, 600
bg = 0, 0, 0

pygame.init()

screen = pygame.display.set_mode(size)
assert isinstance(screen, pygame.Surface)

ball = pygame.image.load("../resources/ball.gif")
assert isinstance(ball, pygame.Surface)
