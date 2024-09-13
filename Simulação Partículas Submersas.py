import pygame
import numpy as np
import random

# Inicializar o Pygame
pygame.init()

# Definir cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
AZUL_MAR = (0, 105, 148)  # Cor do mar
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)

# Configuração da tela
screen_width, screen_height = 800, 600
altura_mar = 300
screen = pygame.display.set_mode((screen_width, screen_height))



# Declarando a tela

pygame.display.set_caption("Simulação de Partículas Submersas")

# Configurar parâmetros da simulação
m = 1.0  # Massa (kg)
g = 9.81  # Gravidade (m/s^2)
c = 0.1  # Constante de resistência
x0 = screen_height // 2  # Posição inicial (pixels)
v0 = 0.0  # Velocidade inicial (m/s)
dt = 0.01  # Passo de tempo (s)
t_final = 10  # Tempo final da simulação (s)

# Função para simular movimento com diferentes valores de k
def simulate_motion(k):
    t = np.arange(0, t_final, dt)
    x = np.zeros_like(t)
    v = np.zeros_like(t)
    x[0] = x0
    v[0] = v0

    for i in range(1, len(t)):
        a = g - (c/m) * v[i-1]**k  # Aceleração com resistência v^k
        v[i] = v[i-1] + a * dt  # Atualiza velocidade
        x[i] = x[i-1] + v[i] * dt  # Atualiza posição
    
    return t, x

# Simular as três situações
t1, x1 = simulate_motion(1)  # Resistência linear
t2, x2 = simulate_motion(2)  # Resistência quadrática
t3, x3 = simulate_motion(3)  # Resistência cúbica

# Função para desenhar as posições

def draw_positions(x1_pos, x2_pos, x3_pos):

# declarando o fundo de tela

    screen.fill(WHITE)
    pygame.draw.rect(screen, AZUL_MAR, (0, altura_mar, screen_width, screen_height - altura_mar))
    pygame.draw.circle(screen, AMARELO, (screen_width // 3, int(x1_pos)), 15)
    pygame.draw.circle(screen, RED, (screen_width // 2, int(x2_pos)), 15)
    pygame.draw.circle(screen, GREEN, (2 * screen_width // 3, int(x3_pos)), 15)
    
# Declarando o azul escuro do do céu

    screen.fill((0, 0, 30))  # Fundo escuro para representar o céu noturno
    pygame.draw.rect(screen, AZUL_MAR, (0, altura_mar, screen_width, screen_height - altura_mar))

# Declarando  a Lua | Lua no canto superior direito
    pygame.draw.circle(screen, CINZA, (screen_width - 100, 100), 50)

# Declarando as estrelas
    def generate_stars(num_stars):
        stars = []
        for _ in range(num_stars):
            x = random.randint(0, screen_width)
            y = random.randint(0, altura_mar)  # As estrelas ficam na área do céu, acima do mar
            stars.append((x, y))
        return stars
    stars = generate_stars(1)
    
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 2)  # Estrelas pequenas
    
    pygame.draw.rect(screen, AZUL_MAR, (0, altura_mar, screen_width, screen_height - altura_mar))
    pygame.draw.circle(screen, AMARELO, (screen_width // 3, int(x1_pos)), 15)
    pygame.draw.circle(screen, RED, (screen_width // 2, int(x2_pos)), 15)
    pygame.draw.circle(screen, GREEN, (2 * screen_width // 3, int(x3_pos)), 15)
    
    # Declarando o eixo Y
    
    x_position = 100  # A posição X onde a linha será desenhada
    tick_interval_pixels = 20  # Cada 20 pixels representam 1 metro
    num_ticks = (screen_height - altura_mar) // tick_interval_pixels  # Número total de ticks abaixo do nível do mar
    
    pygame.draw.line(screen, WHITE, (x_position, altura_mar), (x_position, screen_height), 2)
    font = pygame.font.Font(None, 25)  # Fonte para os números
    label_zero = font.render("0 m", True, WHITE)
    screen.blit(label_zero, (x_position + 10, altura_mar - 10))  # Valor "0" um pouco à direita da linha
    
    for i in range(1, num_ticks + 1):  # Começar em 1 para não desenhar o valor "0" novamente
        pos_y_down = altura_mar + i * tick_interval_pixels  # Posições abaixo do nível do mar
        
        if pos_y_down <= screen_height:  # Certificar-se de que não desenha fora da tela
            # Desenhar as pequenas linhas horizontais para as marcações abaixo
            pygame.draw.line(screen, WHITE, (x_position - 10, pos_y_down), (x_position + 10, pos_y_down), 2)
            
            # Exibir os valores numéricos abaixo do nível do mar
            label_down = font.render(f"-{i} m", True, WHITE)  # Posições abaixo do mar (em metros)
            screen.blit(label_down, (x_position + 20, pos_y_down - 10))  # Mostrar os números ao lado das linhas de marcação

    
    # Fonte para a legenda
    font = pygame.font.Font(None, 30)
    
    # Texto da legenda
    legenda_1 = font.render("Amarelo  - Resistência linear", True, AMARELO)
    legenda_2 = font.render("Vermelho - Resistência quadrática", True, RED)
    legenda_3 = font.render("Verde    - Resistência cúbica", True, GREEN)
    
    # Desenhar a legenda na tela
    screen.blit(legenda_1, (10, 10))   # Posição (10, 10)
    screen.blit(legenda_2, (10, 40))   # Posição (10, 40)
    screen.blit(legenda_3, (10, 70))   # Posição (10, 70))
    
    pygame.display.flip()

# Loop principal
running = True
clock = pygame.time.Clock()
frame = 0
delay = 25

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.time.delay(delay)
    # Desenhar os corpos em suas posições atuais
    if frame < len(t1):
        draw_positions(x1[frame], x2[frame], x3[frame])
        frame += 1

    # Limitar a taxa de quadros
    clock.tick(200)

pygame.quit()
