'''
    display scan 
'''

import pygame
import threading
from math import pi, cos, sin
from time import sleep

RESOLUTION = 0.05

BLUE = (0, 0, 255)
WHILTE = (255, 255, 255)

SCREENSIZE = (400, 400)

R_BIGPOINT = 5
R_SMALLPOINTT = 2

class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)

        thread = threading.Thread(name='display', target=self.run)
        thread.setDaemon(True)
        thread.start()

    def draw(self, scan):
        n = len(scan)
        if n!= 360:
            print("got incorrect scan data length")
            raise RuntimeError
        
        self.screen.fill(WHILTE)
        center = (int(SCREENSIZE[0]/2), int(SCREENSIZE[1]/2))
        pygame.draw.circle(self.screen, BLUE, center, R_BIGPOINT, 3)
        for i in range(n):
            d = scan[i] # m
            th = i / 180.0 * pi
            x = d * cos(th)
            y = d * sin(th)

            posx = int(SCREENSIZE[0]/2.0 + (x / RESOLUTION))
            posy = int(SCREENSIZE[1]/2.0 - (y / RESOLUTION))
            pygame.draw.circle(self.screen, BLUE, (posx, posy), R_SMALLPOINTT, 1)
        pygame.display.flip()

    def run(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
        pygame.quit()