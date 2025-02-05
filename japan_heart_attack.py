import pygame
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import re

# Função para converter nomes de colunas em snake_case sem acentos
def normalize_column_name(column_name):
    column_name = column_name.strip()  # Remove espaços extras
    column_name = unicodedata.normalize('NFKD', column_name).encode('ASCII', 'ignore').decode('utf-8')  # Remove acentos
    column_name = re.sub(r'[^a-zA-Z0-9_]', '_', column_name)  # Substitui caracteres especiais por _
    column_name = re.sub(r'_{2,}', '_', column_name)  # Remove múltiplos _
    return column_name.lower()  # Converte para minúsculas

# Carregar e tratar o CSV
def load_and_preprocess_csv(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')  # Lê o CSV
    df.columns = [normalize_column_name(col) for col in df.columns]  # Aplica normalização aos nomes das colunas
    return df

# Função para exibir um gráfico
def show_graph(insight_type, df):
    plt.figure(figsize=(8, 6))
    
    if insight_type == "Pressão Arterial por Idade":
        df.groupby("age")[["systolic_bp", "diastolic_bp"]].mean().plot()
        plt.title("Média da Pressão Arterial por Idade")
        plt.ylabel("Pressão Arterial (mmHg)")
        plt.xlabel("Idade")

    elif insight_type == "Distribuição do Colesterol":
        df["cholesterol_level"].hist(bins=20, alpha=0.7, color="blue", edgecolor="black")
        plt.title("Distribuição dos Níveis de Colesterol")
        plt.xlabel("Colesterol")
        plt.ylabel("Frequência")

    elif insight_type == "IMC por Atividade Física":
        df.groupby("physical_activity")["bmi"].mean().plot(kind="bar", color="green", edgecolor="black")
        plt.title("IMC Médio por Nível de Atividade Física")
        plt.xlabel("Atividade Física")
        plt.ylabel("IMC")

    elif insight_type == "Frequência Cardíaca e Tabagismo":
        df.groupby("smoking_history")["heart_rate"].mean().plot(kind="bar", color="red", edgecolor="black")
        plt.title("Frequência Cardíaca Média por Histórico de Tabagismo")
        plt.xlabel("Tabagismo")
        plt.ylabel("Frequência Cardíaca (bpm)")

    plt.grid()
    plt.show()

# Configuração inicial do Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Análise de Ataques Cardíacos")

# Cores e fontes
WHITE = (255, 255, 255)
BLUE = (50, 100, 200)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 32)

# Lista de insights
insights = [
    "Pressão Arterial por Idade",
    "Distribuição do Colesterol",
    "IMC por Atividade Física",
    "Frequência Cardíaca e Tabagismo"
]

# Posição inicial dos botões
button_x = WIDTH // 2 - 150
button_y = 150
button_width = 380
button_height = 50
button_spacing = 20

# Estrutura dos botões
buttons = []
for index, insight in enumerate(insights):
    rect = pygame.Rect(button_x, button_y + index * (button_height + button_spacing), button_width, button_height)
    buttons.append((rect, insight))

# Carrega os dados
csv_file = "./assets/datasets/ashaychoudhary/heart-attack-in-japan-youth-vs-adult/japan_heart_attack_dataset.csv"  # Nome do arquivo CSV
df = load_and_preprocess_csv(csv_file)
desc_stats = df.describe(include='all').T
print(desc_stats)
# Loop principal do Pygame
running = True
while running:
    screen.fill(WHITE)

    # Renderiza o título
    title_text = FONT.render("Ataque cardíaco no Japão: jovens versus adultos", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Renderiza os botões
    for rect, insight in buttons:
        pygame.draw.rect(screen, BLUE, rect, border_radius=10)
        text_surface = FONT.render(insight, True, WHITE)
        screen.blit(text_surface, (rect.x + (button_width - text_surface.get_width()) // 2, rect.y + 10))

    pygame.display.flip()

    # Lida com eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for rect, insight in buttons:
                if rect.collidepoint(mouse_pos):
                    show_graph(insight, df)

pygame.quit()