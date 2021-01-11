import tkinter as tk
from tkinter import filedialog
import pygame, pygame.locals
from colors import *

#tkinter setup for file dialog
root = tk.Tk()
root.withdraw()

#pygame setup for main window
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 30)
small = pygame.font.SysFont("Courier New", 15)
FLAGS = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE
SIZE = WIDTH, HEIGHT = (900, 600)

screen = pygame.display.set_mode(SIZE, FLAGS)


if __name__ == '__main__':
    screen.fill(white)
    pygame.display.flip()

    file_path = filedialog.askopenfilename()

    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.locals.VIDEORESIZE:
                SIZE = WIDTH, HEIGHT = event.w, event.h
                screen.fill(white)
