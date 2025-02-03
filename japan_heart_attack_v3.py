import pygame
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import re
import numpy as np

# Função para converter nomes de colunas em snake_case sem acentos
def normalize_column_name(column_name):
    column_name = column_name.strip()
    column_name = unicodedata.normalize('NFKD', column_name).encode('ASCII', 'ignore').decode('utf-8')
    column_name = re.sub(r'[^a-zA-Z0-9_]', '_', column_name)
    column_name = re.sub(r'_{2,}', '_', column_name)
    return column_name.lower()

# Carregar e tratar o CSV
def load_and_preprocess_csv(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    df.columns = [normalize_column_name(col) for col in df.columns]
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

# Função para exibir estatísticas descritivas como cards
def show_statistics(df):
    desc_stats = df.describe(include='all').T  # Gera estatísticas descritivas
    
    # Lista de estatísticas a serem exibidas
    stats_labels = [
        "Contagem", "Valores Únicos", "Valor Mais Frequente", "Frequência do Mais Frequente",
        "Média", "Mínimo", "25º Percentil", "50º Percentil (Mediana)",
        "75º Percentil", "Máximo"
    ]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.axis('off')

    num_columns = 3  # Número de colunas por linha
    num_rows = int(np.ceil(len(desc_stats) / num_columns))  # Define a quantidade de linhas necessárias
    
    # Criar os cards
    for idx, (col_name, stats) in enumerate(desc_stats.iterrows()):
        row = idx // num_columns
        col = idx % num_columns
        x_pos = col * 0.33 + 0.01
        y_pos = 0.9 - row * 0.3
        
        # Criando retângulo do card
        ax.add_patch(plt.Rectangle((x_pos, y_pos), 0.3, 0.25, fill=True, color="lightgray", alpha=0.8, edgecolor="black"))

        # Exibindo título do campo no topo do card
        plt.text(x_pos + 0.15, y_pos + 0.22, col_name.replace("_", " ").title(), 
                 fontsize=12, ha="center", fontweight="bold")

        # Exibir estatísticas dentro do card
        for i, (label, key) in enumerate(zip(stats_labels, stats.index)):
            value = stats[key] if not pd.isnull(stats[key]) else "N/A"
            plt.text(x_pos + 0.15, y_pos + 0.18 - (i * 0.02), f"{label}: {value}", 
                     fontsize=9, ha="center")
    
    plt.title("Estatísticas Descritivas", fontsize=14, fontweight='bold', pad=20)
    plt.show()

def show_statistics_v2(df):
    desc_stats = df.describe(include='all').T  # Gera estatísticas descritivas

    # Definir os nomes das estatísticas que queremos exibir
    stats_labels = [
        "Contagem", "Valores Únicos", "Valor Mais Frequente", "Frequência do Mais Frequente",
        "Média", "Mínimo", "25º Percentil", "50º Percentil (Mediana)",
        "75º Percentil", "Máximo"
    ]

    # Criar um DataFrame preenchendo valores ausentes com "N/A"
    stats_data = desc_stats.reindex(columns=[
        "count", "unique", "top", "freq", "mean", "min", "25%", "50%", "75%", "max"
    ]).fillna("N/A")

    # Criar tabela formatada para exibição
    fig, ax = plt.subplots(figsize=(12, len(stats_data) * 0.5 + 2))
    ax.axis('tight')
    ax.axis('off')

    # Criar lista de dados para a tabela
    table_data = []
    column_headers = ["Campo"] + stats_labels  # Definir os títulos corretamente

    for col_name, stats in stats_data.iterrows():
        row = [col_name.replace("_", " ").title()]  # Nome do campo
        row.extend(stats.tolist())  # Adiciona as estatísticas da linha
        table_data.append(row)

    # Criar tabela no matplotlib
    table = ax.table(cellText=table_data, colLabels=column_headers, cellLoc='center', loc='center')

    # Ajustes visuais
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width([i for i in range(len(column_headers))])

    # Destacar a primeira coluna (nomes dos campos)
    for i in range(len(table_data)):
        table[(i + 1, 0)].set_text_props(fontweight='bold')

    # Exibir a tabela
    plt.title("Estatísticas Descritivas", fontsize=14, fontweight='bold', pad=20)
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
    "Frequência Cardíaca e Tabagismo",
    "Estatísticas Descritivas"  # Novo botão
]

# Posição inicial dos botões
button_x = WIDTH // 2 - 150
button_y = 150
button_width = 300
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
                    if insight == "Estatísticas Descritivas":
                        show_statistics(df)
                    else:
                        show_graph(insight, df)

pygame.quit()