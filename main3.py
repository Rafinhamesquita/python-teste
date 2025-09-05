import pygame
import os

# Inicializando o Pygame
pygame.init()

# Definindo o tamanho da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mover Imagem com Setas")

# Definindo a cor de fundo
BG_COLOR = (193, 0, 40)  # cor de fundo (um tom escuro)

# Carregar a imagem
image_file = "gato.png"  # coloque o nome da sua imagem aqui
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()  # Carregar a imagem
    img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centraliza a imagem
else:
    print("Imagem não encontrada!")

# Velocidade de movimento
SPEED = 1  # pixels por movimento

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pega as teclas pressionadas
    keys = pygame.key.get_pressed()

    #paramos por aqui, ainda tem coisaaaa

    # Movimentação da imagem
    if keys[pygame.K_LEFT]:
        img_rect.x -= SPEED  # Move para a esquerda
    if keys[pygame.K_RIGHT]:
        img_rect.x += SPEED  # Move para a direita
    if keys[pygame.K_UP]:
        img_rect.y -= SPEED  # Move para cima
    if keys[pygame.K_DOWN]:
        img_rect.y += SPEED  # Move para baixo

    # Preencher o fundo
    screen.fill(BG_COLOR)

    # Desenhar a imagem na tela
    screen.blit(img, img_rect.topleft)

    # Atualizar a tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()
