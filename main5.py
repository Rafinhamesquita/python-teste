import pygame
import os

pygame.init()

# Tamanho da janela
WIDTH, HEIGHT = 1020, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Mover Imagem com Setas")

# Cor de fundo caso não tenha imagem
BG_COLOR = (193, 0, 40)

# Carregar imagem do personagem
image_file = "gato.png"
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()
    img_rect = img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))  # personagem começa no chão
else:
    print("Imagem do personagem não encontrada!")
    img = None
    img_rect = pygame.Rect(WIDTH // 2, HEIGHT - 60, 50, 50)

# Carregar imagem de fundo
background_file = "fundo.jpg"
if os.path.exists(background_file):
    background_orig = pygame.image.load(background_file).convert()
    background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
else:
    background_orig = None
    background = None
    print("Imagem de fundo não encontrada!")

# Velocidades e física
SPEED = 8
JUMP_STRENGTH = 30
GRAVITY = 1
velocity_y = 0
on_ground = True

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
    global velocity_y, on_ground
    if on_ground:
        velocity_y = -JUMP_STRENGTH
        on_ground = False

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_width, current_height = screen.get_size()
    if current_width != WIDTH or current_height != HEIGHT:
        WIDTH, HEIGHT = current_width, current_height
        if background_orig:
            background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
        # Ajustar chão se necessário:
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

    # Aplica gravidade vertical
    velocity_y += GRAVITY
    img_rect.y += velocity_y

    # Detectar chão
    if img_rect.bottom >= HEIGHT:
        img_rect.bottom = HEIGHT
        velocity_y = 0
        on_ground = True

    limit_movement()

    # Desenhar fundo
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # Desenhar personagem
    if img:
        screen.blit(img, img_rect.topleft)
    else:
        pygame.draw.rect(screen, (255, 0, 0), img_rect)

    pygame.display.flip()

pygame.quit()