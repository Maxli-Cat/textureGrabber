import tkinter as tk
from tkinter import filedialog
import pygame, pygame.locals
import cv2
import numpy as np

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

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

def shift(img, points):
    xs = [int(i[0]) for i in points]
    ys = [int(i[1]) for i in points]

    x_size = max(xs) - min(xs)
    y_size = max(ys) - min(ys)

    print(x_size, y_size)

    old_points = np.float32(points)
    new_points = np.float32([[0,0], [x_size, 0], [x_size, y_size], [0, y_size]])

    matrix = cv2.getPerspectiveTransform(old_points, new_points)
    result = cv2.warpPerspective(img, matrix, (x_size, y_size))

    cv2.imshow('image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    save_path = filedialog.asksaveasfilename(filetypes=[("jpegs","*.jpg")])
    if save_path != "":
        if ".jpg" not in save_path:
            save_path += ".jpg"
        cv2.imwrite(save_path, result)

def scale_points(points, old_size, new_size):
    x_scale = new_size[0] / old_size[0]
    y_scale = new_size[1] / old_size[1]

    new_points = [(i[0] * x_scale, i[1] * y_scale) for i in points]
    return new_points

if __name__ == '__main__':
    screen.fill(white)
    pygame.display.flip()

    file_path = filedialog.askopenfilename(filetypes=[("jpegs","*.jpg"), ("pngs","*.png"), ("All Files", "*.*")])
    if file_path != "":
        image = pygame.image.load(file_path)
        cvimage = cv2.imread(file_path)
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
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN] and len(points) == 4:
                    s_points = scale_points(points, SIZE, image.get_size())
                    shift(cvimage, s_points)
                elif keys[pygame.K_ESCAPE]:
                    points = []

        fit_image(image)
        draw_dots(points)
        if len(points) < 3:
            draw_lines(points + [pygame.mouse.get_pos()])
        elif len(points) == 3:
            draw_lines(points + [pygame.mouse.get_pos()], True)
        else:
            draw_lines(points, True)