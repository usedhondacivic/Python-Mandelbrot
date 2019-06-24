import pygame
from pygame.locals import *
import math
import random

pygame.init()

display_width = 400
display_height = 400
aspect_ratio = display_height / display_width

surface = pygame.display.set_mode((display_width, display_height))

escape_radius = 2
max_iterations = 50
window_min = -2.5
window_max = 1.5
y_offset = (window_max + window_min) / 2.

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def map_range(var, iMin, iMax, fMin, fMax):
    iRange = iMax - iMin
    fRange = fMax - fMin
    coefficient = fRange / iRange

    return (var - iMin) * coefficient + fMin

def event_handler():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            render()

def mandelbrot(a, b):
    n = 0
    z = 0
    c = complex(a, b)

    while n < max_iterations:
        z = z*z + c
        if abs(z) > escape_radius:
            break
        n += 1

    return n

def render():
    pixel_array = pygame.PixelArray(surface)
    for x in range(0, len(pixel_array)):
        for y in range(0, len(pixel_array[x])):
            a = map_range(x, 0, len(pixel_array), window_min, window_max)
            b = map_range(y, 0, len(pixel_array[x]), (window_min - y_offset) * aspect_ratio, (window_max - y_offset) * aspect_ratio)

            n = mandelbrot(a, b)

            if n == max_iterations:
                pixel_array[x, y] = pygame.Color(0)
            else:
                hue = int(map_range(n, 0, max_iterations, 0, 360))
                pixel_array[x, y] = hsv2rgb(hue, 1, 1)

    pixel_array.close()

render()

while True:
    event_handler()
    pygame.display.update()