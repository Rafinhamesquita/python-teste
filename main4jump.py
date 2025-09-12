import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Mover Imagem com Setas")

BG_COLOR = (193, 0, 40)

# Carregar imagem
image_file = "gato.png"
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()
    img_rect = img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))  # Começa no chão
else:
    print("Imagem não encontrada!")
    img = None
    img_rect = pygame.Rect(WIDTH // 2, HEIGHT - 60, 50, 50)

SPEED = 5
JUMP_STRENGTH = 15
GRAVITY = 0.7
velocity_y = 0
jumping = False

clock = pygame.time.Clock()
FPS = 60

def limit_movement():
    global img_rect, WIDTH, HEIGHT
    if img_rect.left < 0:
        img_rect.left = 0
    if img_rect.right > WIDTH:
        img_rect.right = WIDTH
    if img_rect.bottom > HEIGHT:
        img_rect.bottom = HEIGHT
    if img_rect.top < 0:
        img_rect.top = 0

def jump():
    global velocity_y, jumping
    if not jumping:
        velocity_y = -JUMP_STRENGTH
        jumping = True

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_width, current_height = screen.get_size()
    if current_width != WIDTH or current_height != HEIGHT:
        WIDTH, HEIGHT = current_width, current_height
        # Apenas garante que o personagem fique dentro da tela
        if img_rect.bottom > HEIGHT:
            img_rect.bottom = HEIGHT

    keys = pygame.key.get_pressed()

    # Movimento horizontal
    if keys[pygame.K_LEFT]:
        img_rect.x -= SPEED
    if keys[pygame.K_RIGHT]:
        img_rect.x += SPEED

    # Pulo
    if keys[pygame.K_SPACE]:
        jump()

    # Aplica gravidade
    velocity_y += GRAVITY
    img_rect.y += velocity_y

    # Detecta chão
    if img_rect.bottom >= HEIGHT:
        img_rect.bottom = HEIGHT
        velocity_y = 0
        jumping = False

    limit_movement()

    screen.fill(BG_COLOR)

    if img:
        screen.blit(img, img_rect.topleft)
    else:
        pygame.draw.rect(screen, (255, 0, 0), img_rect)

    pygame.display.flip()

pygame.quit()