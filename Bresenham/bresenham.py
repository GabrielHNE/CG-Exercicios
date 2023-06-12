import pygame
import sys
import time

# PYGAMES FUNCTIONS

WHITE = (255, 255, 255)
WINDOW = None

def plot_pixel(x, y):
    WINDOW.set_at((x, y), WHITE)


# BRESENHAM

def bresenham_retas(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    x = x1
    y = y1
    points = []
    while True:
        points.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points

def bresenham_circunferencia(xc, yc, r):
    x = 0
    y = r
    p = 1 - r
    
    plot_circle_points(xc, yc, x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        plot_circle_points(xc, yc, x, y)
    
def plot_circle_points(xc, yc, x, y):
    plot_pixel(xc + x, yc + y)
    plot_pixel(xc - x, yc + y)
    plot_pixel(xc + x, yc - y)
    plot_pixel(xc - x, yc - y)
    plot_pixel(xc + y, yc + x)
    plot_pixel(xc - y, yc + x)
    plot_pixel(xc + y, yc - x)
    plot_pixel(xc - y, yc - x)

def plot_points(points):
    for p in points:
        plot_pixel(p[0], p[1])


if __name__ == "__main__":
    pygame.init()  # inicialização
    WINDOW = pygame.display.set_mode((500, 500))  # cria a janela de exibição
    pygame.display.set_caption("Bresenhan para traçado de circunferências")

    #desenha as linhas de bresenham
    bresenham_circunferencia(250, 250, 100)
    
    points = bresenham_retas(250, 250, 480, 480)
    plot_points(points)


    pygame.display.update() # refresh da janela para exibir o que foi impresso com set_at

    # loop para congelar a janela
    # fica aguardando um evento, que no caso é o fechamento da janela no botao X
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # fechar a janela no x
                pygame.quit()
                sys.exit()