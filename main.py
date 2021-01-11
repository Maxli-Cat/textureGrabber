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

def fit_image(image):
    sized_image = pygame.transform.smoothscale(image, SIZE)
    screen.blit(sized_image, (0,0))

def draw_dots(points):
    if len(points) == 0: return
    for i in points:
        pygame.draw.circle(screen, blue, i, 3)

def draw_lines(points, closed=False):
    #print(f"{points=}")
    if len(points) < 2: return
    pygame.draw.lines(screen, blue, closed, points)

def shift(image, points):
    pass

def scale_points(points, old_size, new_size):
    pass


if __name__ == '__main__':
    screen.fill(white)
    pygame.display.flip()

    file_path = filedialog.askopenfilename(filetypes=[("jpegs","*.jpg"), ("pngs","*.png"), ("All Files", "*.*")])
    if file_path != "":
        image = pygame.image.load(file_path)
        fit_image(image)
    else:
        pygame.quit()
        exit()

    points = []

    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.locals.VIDEORESIZE:
                SIZE = WIDTH, HEIGHT = event.w, event.h
                points = []
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(points) >= 4:
                    points = []
                pos = pygame.mouse.get_pos()
                points.append(pos)

        fit_image(image)
        draw_dots(points)
        if len(points) < 4:
            draw_lines(points + [pygame.mouse.get_pos()])
        else:
            draw_lines(points, True)