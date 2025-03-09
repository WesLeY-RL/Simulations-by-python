import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

# Parâmetros da elipse
a = 3  # Semieixo maior
b = 2  # Semieixo menor
alpha = 0  # Limite inferior
beta = 2 * np.pi  # Limite superior

# Derivadas paramétricas
def dx_dt(t):
    return -a * np.sin(t)

def dy_dt(t):
    return b * np.cos(t)

# Função para o integrando
def integrand(t):
    return np.sqrt(dx_dt(t)**2 + dy_dt(t)**2)

# Pontos para a simulação
t_values = np.linspace(alpha, beta, 500)
x_values = a * np.cos(t_values)
y_values = b * np.sin(t_values)

# Comprimento do arco para cada valor de t (cálculo incremental)
s_values = [0]
for i in range(1, len(t_values)):
    ds, _ = quad(integrand, t_values[i-1], t_values[i])
    s_values.append(s_values[-1] + ds)

# Distância relativa ao centro
distance_to_center = np.sqrt(x_values**2 + y_values**2)

# Criar uma tabela com t (ângulo), s (comprimento de arco) e distância relativa
data = pd.DataFrame({
    'Ângulo (t)': t_values,
    'Comprimento Métrico (s)': s_values,
    'Distância ao Centro (d)': distance_to_center
})
print(data.head())  # Visualizar os primeiros valores da tabela

# Simulação da partícula percorrendo a elipse
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_aspect('equal')
ax.set_xlim(-a - 1, a + 1)
ax.set_ylim(-b - 1, b + 1)

# Desenhar a elipse
ax.plot(x_values, y_values, label="Elipse", color='blue')

# Adicionar eixos na elipse
ax.axhline(0, color='black', linewidth=0.8, linestyle="--")
ax.axvline(0, color='black', linewidth=0.8, linestyle="--")

# Texto com as dimensões da elipse
ax.text(a + 0.2, 0, f'a = {a}', fontsize=10, color='blue')
ax.text(0, b + 0.2, f'b = {b}', fontsize=10, color='blue')

# Partícula (ponto)
particle, = ax.plot([], [], 'ro', label="Partícula")

# Texto animado para exibir t (ângulo), s (comprimento do arco) e distância relativa
info_text = ax.text(0, -b - 0.5, '', fontsize=10, color='darkred', ha='center')

def init():
    particle.set_data([], [])
    info_text.set_text('')
    return particle, info_text

def update(frame):
    # Atualizar posição da partícula
    particle.set_data(x_values[frame], y_values[frame])
    # Atualizar texto com os valores de ângulo, comprimento do arco e distância relativa
    info_text.set_text(
        f"Ângulo (t): {t_values[frame]:.2f} rad\n"
        f"Comprimento (s): {s_values[frame]:.2f} m\n"
        f"Distância ao Centro (d): {distance_to_center[frame]:.2f} m"
    )
    return particle, info_text

ani = FuncAnimation(fig, update, frames=len(t_values), init_func=init, interval=20, blit=True)

# Adicionar legenda e título
ax.legend(loc='upper right')
ax.set_title("Simulação: Partícula Percorrendo a Elipse")

# Mostrar animação
plt.show()

# Exportar tabela para CSV, caso necessário
data.to_csv("variacao_angular_metrica_distancia.csv", index=False)
