import pygame
import os

# Inicializando o Pygame
pygame.init()

# Tamanho inicial da janela
WIDTH, HEIGHT = 720, 360
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Mover Imagem com Setas + Explosão")

# Cor de fundo padrão
BG_COLOR = (193, 0, 40)

# Constantes de movimento e física
SPEED = 3
JUMP_STRENGTH = 18
GRAVITY = 0.3

# ------------------------------
# Classe Explosão
# ------------------------------
class Explosion:
    def __init__(self, pos):
        self.pos = pos
        self.radius = 10
        self.max_radius = 80
        self.active = True

    def update(self):
        if self.active:
            self.radius += 5
            if self.radius >= self.max_radius:
                self.active = False

    def draw(self, surface):
        if self.active:
            alpha = max(255 - (self.radius * 3), 0)
            color = (255, 200, 0, alpha)
            temp_surface = pygame.Surface((self.max_radius*2, self.max_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, color, (self.max_radius, self.max_radius), self.radius)
            surface.blit(temp_surface, (self.pos[0] - self.max_radius, self.pos[1] - self.max_radius))


# ------------------------------
# Classe Player
# ------------------------------
class Player:
    def __init__(self, image_path, start_pos):
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.rect = self.image.get_rect(center=start_pos)
        else:
            print("Imagem do jogador não encontrada!")
            self.image = None
            self.rect = pygame.Rect(start_pos[0], start_pos[1], 50, 50)
        self.is_jumping = False
        self.velocity_y = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += SPEED
        if keys[pygame.K_UP]:   # ✅ voltou o movimento para cima
            self.rect.y -= SPEED
        if keys[pygame.K_DOWN]: # ✅ voltou o movimento para baixo
            self.rect.y += SPEED

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True

    def update_jump(self):
        if self.is_jumping:
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.is_jumping = False
                self.velocity_y = 0

    def limit_movement(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)


# ------------------------------
# Classe Target
# ------------------------------
class Target:
    def __init__(self, image_path, start_pos):
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.rect = self.image.get_rect(center=start_pos)
        else:
            print("Imagem do alvo não encontrada!")
            self.image = None
            self.rect = pygame.Rect(start_pos[0], start_pos[1], 50, 50)
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False

    def update_physics(self):
        if self.is_jumping:
            self.velocity_y += GRAVITY
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y

            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.is_jumping = False
                self.velocity_x = 0
                self.velocity_y = 0
            else:
                self.velocity_x *= 0.95
                if abs(self.velocity_x) < 0.1:
                    self.velocity_x = 0

    def limit_movement(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(surface, (0, 255, 0), self.rect)

    def kick(self, player_rect):
        dist_x = self.rect.centerx - player_rect.centerx
        dist_y = self.rect.centery - player_rect.centery
        distancia = (dist_x ** 2 + dist_y ** 2) ** 0.5

        if distancia < 150:
            self.velocity_x = 20 if dist_x > 0 else -20
            self.velocity_y = -15
            self.is_jumping = True
            return True  # ✅ Retorna que foi chutado
        return False


# ------------------------------
# Fundo opcional
# ------------------------------
background_file = "fundo.png"
if os.path.exists(background_file):
    background_orig = pygame.image.load(background_file).convert()
    background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
else:
    background_orig = None
    background = None
    print("Imagem de fundo não encontrada!")

player = Player("gato.png", (WIDTH // 2, HEIGHT // 2))
target = Target("rato.png", (WIDTH // 2 + 200, HEIGHT // 2))

explosions = []  # lista de explosões ativas

last_width, last_height = WIDTH, HEIGHT

# ------------------------------
# Loop principal
# ------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if player.rect.colliderect(target.rect) and target.kick(player.rect):
                    explosions.append(Explosion(target.rect.center))  # 💥 cria explosão
            if event.key == pygame.K_SPACE:
                player.jump()

    # Detectar resize da janela
    current_width, current_height = screen.get_size()
    if current_width != last_width or current_height != last_height:
        WIDTH, HEIGHT = current_width, current_height
        if background_orig:
            background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
        last_width, last_height = current_width, current_height

    # Atualizações
    keys = pygame.key.get_pressed()
    player.move(keys)
    player.limit_movement()
    target.limit_movement()
    player.update_jump()
    target.update_physics()

    # Desenhar fundo
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # Desenhar player, target e explosões
    player.draw(screen)
    target.draw(screen)

    for explosion in explosions[:]:
        explosion.update()
        explosion.draw(screen)
        if not explosion.active:
            explosions.remove(explosion)

    pygame.display.flip()

pygame.quit()