import pygame
import sys
import time

white = (255, 255, 255)

def imprimepontos(screen):
    for i in range(100, 200):
        screen.set_at((i, i), white)

pygame.init()  # inicialização
window = pygame.display.set_mode((500, 500))  # cria a janela de exibição
pygame.display.set_caption("Teste do Pygame")

imprimepontos(window) # aqui vc vai chamar a função para desenhar a reta ou circunferencia
pygame.display.update() # refresh da janela para exibir o que foi impresso com set_at

# loop para congelar a janela
# fica aguardando um evento, que no caso é o fechamento da janela no botao X
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # fechar a janela no x
            pygame.quit()
            sys.exit()