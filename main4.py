import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mover Imagem com Setas e Pular com Espaço")

BG_COLOR = (30, 30, 40)

image_file = "gato.png"
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()
    img_rect = img.get_rect(midbottom=(WIDTH // 2, HEIGHT))  # Começa no chão
else:
    print("Imagem não encontrada!")
    img = None
    img_rect = pygame.Rect(WIDTH // 2, HEIGHT - 50, 50, 50)

SPEED = 6  # velocidade horizontal mais natural
JUMP_STRENGTH = 15
GRAVITY = 0.8

is_jumping = False
y_velocity = 0

clock = pygame.time.Clock()
FPS = 60

def limit_movement():
    global img_rect
    if img_rect.left < 0:
        img_rect.left = 0
    if img_rect.right > WIDTH:
        img_rect.right = WIDTH

running = True
while running:
    clock.tick(FPS)  # controla a velocidade do jogo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Movimento horizontal só
    if keys[pygame.K_LEFT]:
        img_rect.x -= SPEED
    if keys[pygame.K_RIGHT]:
        img_rect.x += SPEED

    # Pulo
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        y_velocity = -JUMP_STRENGTH

    if is_jumping:
        img_rect.y += y_velocity
        y_velocity += GRAVITY

        if img_rect.bottom >= HEIGHT:
            img_rect.bottom = HEIGHT
            is_jumping = False
            y_velocity = 0

    limit_movement()

    screen.fill(BG_COLOR)

    if img:
        screen.blit(img, img_rect.topleft)
    else:
        pygame.draw.rect(screen, (255, 0, 0), img_rect)

    pygame.display.flip()

pygame.quit()