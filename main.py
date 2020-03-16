import pygame, sys
import numpy as np
from scipy.spatial import Delaunay
import random


# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def init():
    pygame.init()
    scr_size = pygame.display.list_modes(depth=0, flags=pygame.FULLSCREEN, display=0)[0]
    return pygame.display.set_mode(scr_size), scr_size


def terminate():
    pygame.quit()
    sys.exit()


def draw_noise(display, scr_size):

    noise = np.random.uniform(low=0, high=255, size=(320, 240))
    surface = pygame.surfarray.make_surface(noise)
    frame = pygame.transform.scale(surface, scr_size)
    display.blit(frame, frame.get_rect())
    pygame.display.update()


def draw_delaunay(display, scr_size):

    points = np.array([[random.randrange(0, 900), random.randrange(0, 800)] for _ in range(100)], dtype=int)
    tri = Delaunay(points)

    for vertex in tri.simplices:
        pygame.draw.polygon(display, GREEN, [points[p] for p in vertex], width=1)

    pygame.display.update()

    return tri


def build_graph(tri):

    incidency_table = {}

    for s in tri.simplices:
        for i in range(0, 3):
            neighbors = s.take(range(i+1, i+3), mode='wrap')
            incidency_table.setdefault(s[i], []).extend(neighbors)

    for i in incidency_table:
        incidency_table[i] = list(set(incidency_table[i]))


def run():

    display, scr_size = init()

    running = True

    tri = draw_delaunay(display, scr_size)

    build_graph(tri)

    while running:
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    terminate()

            if event.type == pygame.QUIT:
                terminate()




if __name__ == '__main__':
    run()
