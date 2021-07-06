import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((400,300))

while True:
    #comment
    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == pygame.K_DOWN:
                print('Down was pressed')

            if event.key == pygame.K_UP:
                print('Up was pressed')

            if event.key == pygame.K_RIGHT:
                print('Right was pressed')

            if event.key == pygame.K_LEFT:
                print('Left was pressed')