import pygame
from pygame.locals import *
import random

WINDOW_SIZE = (500, 500)  # Tamanho da tela
PIXEL_SIZE = 15  # Tamanho da célula da cobrinha
SNAKE_COLOR = (0, 255, 0)  # Cor da cobrinha (verde)

# Função para inicializar o Pygame e checar a inicialização
pygame.init()
print("Pygame iniciado!")

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Snake Game')

# Função para gerar posição aleatória dentro da grade (dentro do fundo preto)
def random_on_grid():
    # Gera um valor aleatório dentro da área que não é ocupada pela borda
    x = random.randint(1, (WINDOW_SIZE[0] // PIXEL_SIZE) - 2) * PIXEL_SIZE
    y = random.randint(1, (WINDOW_SIZE[1] // PIXEL_SIZE) - 2) * PIXEL_SIZE
    return (x, y)

# Função para verificar colisão entre a cabeça da cobrinha e a maçã
def collision(snake_head, apple_pos):
    return (snake_head[0] < apple_pos[0] + PIXEL_SIZE and
            snake_head[0] + PIXEL_SIZE > apple_pos[0] and
            snake_head[1] < apple_pos[1] + PIXEL_SIZE and
            snake_head[1] + PIXEL_SIZE > apple_pos[1])

# Função para verificar colisão com a parede
def wall_collision(snake_head):
    head_x, head_y = snake_head
    return head_x < 0 or head_x >= WINDOW_SIZE[0] or head_y < 0 or head_y >= WINDOW_SIZE[1]

# Função para verificar colisão com o corpo da cobra (auto-colisão)
def self_collision(snake_head):
    return snake_head in snake_pos[1:]  # Verifica se a cabeça da cobra colide com qualquer segmento do corpo

# Inicialização da cobrinha
snake_pos = [(250, 250), (240, 250), (230, 250)]  # Cobrinha com 3 segmentos (posição centralizada)
snake_direction = K_LEFT
last_direction = K_LEFT  # Para impedir movimentos contrários

# Função para desenhar a cobrinha com segmentos retangulares
def draw_snake():
    for segment in snake_pos:
        pygame.draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], PIXEL_SIZE, PIXEL_SIZE))  # Retângulo para a cobrinha

# Função para desenhar a maçã com formato redondo
def draw_apple():
    apple_center = (apple_pos[0] + PIXEL_SIZE // 2, apple_pos[1] + PIXEL_SIZE // 2)
    pygame.draw.circle(screen, (255, 0, 0), apple_center, PIXEL_SIZE // 2)  # Círculo para maçã vermelha

# Função para desenhar a parede com a cor verde da cobrinha
def draw_wall():
    pygame.draw.rect(screen, SNAKE_COLOR, (0, 0, WINDOW_SIZE[0], PIXEL_SIZE))  # Parede superior
    pygame.draw.rect(screen, SNAKE_COLOR, (0, 0, PIXEL_SIZE, WINDOW_SIZE[1]))  # Parede esquerda
    pygame.draw.rect(screen, SNAKE_COLOR, (0, WINDOW_SIZE[1] - PIXEL_SIZE, WINDOW_SIZE[0], PIXEL_SIZE))  # Parede inferior
    pygame.draw.rect(screen, SNAKE_COLOR, (WINDOW_SIZE[0] - PIXEL_SIZE, 0, PIXEL_SIZE, WINDOW_SIZE[1]))  # Parede direita

# Inicialização da maçã
apple_pos = random_on_grid()  # Gera a posição inicial da maçã
apple_color = (255, 0, 0)  # Cor vermelha da maçã

# Inicialização da pontuação
score = 0
font = pygame.font.SysFont('Comic Sans MS', 20)

# Função para reiniciar o jogo
def restart_game():
    global snake_pos, apple_pos, snake_direction, score, apple_color, last_direction
    snake_pos = [(250, 250), (240, 250), (230, 250)]  # Posição inicial da cobrinha no centro da tela
    snake_direction = K_LEFT
    last_direction = K_LEFT
    apple_pos = random_on_grid()  # Gerar nova posição para a maçã
    apple_color = (255, 0, 0)  # A maçã será vermelha
    score = 0
    print("Jogo reiniciado!")

# Função para desenhar o fundo (preto)
def draw_background():
    screen.fill((0, 0, 0))  # Preenche o fundo com a cor preta

# Loop principal do jogo
while True:
    pygame.time.Clock().tick(13)  # tempo/velocidade de movimento da cobrinha
    
    # Desenha o fundo (preto)
    draw_background()

    # Desenha as paredes (agora verdes)
    draw_wall()

    for event in pygame.event.get():
        if event.type == QUIT:  # Evento para fechar a janela
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:  # Direção da cobrinha
            # Impedir que a cobrinha se mova para a direção oposta
            if event.key == K_UP and last_direction != K_DOWN:
                snake_direction = K_UP
            elif event.key == K_DOWN and last_direction != K_UP:
                snake_direction = K_DOWN
            elif event.key == K_LEFT and last_direction != K_RIGHT:
                snake_direction = K_LEFT
            elif event.key == K_RIGHT and last_direction != K_LEFT:
                snake_direction = K_RIGHT

    # Exibindo a maçã
    draw_apple()

    # Verificando colisão com a maçã
    if collision(snake_pos[0], apple_pos):
        snake_pos.append(snake_pos[-1])  # Adiciona um novo segmento à cobra
        apple_pos = random_on_grid()  # Coloca a maçã em uma nova posição
        score += 1  # Aumenta a pontuação

    # Atualizando a cobrinha
    draw_snake()

    # Atualizando a posição do corpo da cobrinha (sem buracos)
    for i in range(len(snake_pos) - 1, 0, -1):
        snake_pos[i] = snake_pos[i - 1]  # Cada segmento vai para o lugar do anterior

    # Movendo a cabeça da cobrinha
    head_x, head_y = snake_pos[0]

    # Verificando a direção e movendo a cabeça da cobrinha
    if snake_direction == K_UP:
        snake_pos[0] = (head_x, head_y - PIXEL_SIZE)
    elif snake_direction == K_DOWN:
        snake_pos[0] = (head_x, head_y + PIXEL_SIZE)
    elif snake_direction == K_LEFT:
        snake_pos[0] = (head_x - PIXEL_SIZE, head_y)
    elif snake_direction == K_RIGHT:
        snake_pos[0] = (head_x + PIXEL_SIZE, head_y)

    # Verificando colisão com a parede
    if wall_collision(snake_pos[0]) or self_collision(snake_pos[0]):
        restart_game()  # Reinicia o jogo se a cobrinha colidir com a parede ou com ela mesma

    # Atualizando a última direção
    last_direction = snake_direction

    # Exibindo a pontuação na tela
    score_text = font.render(f'Pontuação: {score}', True, (255, 255, 255))  # Texto branco
    screen.blit(score_text, (10, 10))

    pygame.display.update()
