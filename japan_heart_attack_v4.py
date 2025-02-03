import pygame
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import re

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

# Função para exibir estatísticas descritivas como uma tabela
def show_statistics(df):
    desc_stats = df.describe(include='all').T  # Gera estatísticas descritivas
    
    # Lista de estatísticas a serem exibidas
    stats_labels = [
        "Contagem", "Valores Únicos", "Valor Mais Frequente", "Frequência do Mais Frequente",
        "Média", "Mínimo", "25º Percentil", "50º Percentil (Mediana)",
        "75º Percentil", "Máximo"
    ]
    
    # Criar figura e eixo para exibição
    fig, ax = plt.subplots(figsize=(12, len(desc_stats) * 0.5 + 2))
    ax.axis('tight')
    ax.axis('off')

    # Criar os dados da tabela
    table_data = []
    column_headers = ["Campo"] + stats_labels

    for col_name, stats in desc_stats.iterrows():
        row = [col_name.replace("_", " ").title()]  # Nome do campo
        for key in stats.index:
            value = stats[key] if not pd.isnull(stats[key]) else "N/A"
            row.append(value)
        table_data.append(row)

    # Criando a tabela
    table = ax.table(cellText=table_data, colLabels=column_headers, cellLoc='center', loc='center')

    # Ajustando estilos
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
    "Estatísticas Descritivas"
]

# Posição dos botões
button_x = WIDTH // 2 - 150
button_y = 150
button_width = 300
button_height = 50

# Estrutura dos botões
buttons = []
for index, insight in enumerate(insights):
    rect = pygame.Rect(button_x, button_y + index * (button_height + 20), button_width, button_height)
    buttons.append((rect, insight))

# Carrega os dados
csv_file = "./assets/datasets/ashaychoudhary/heart-attack-in-japan-youth-vs-adult/japan_heart_attack_dataset.csv"
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

pygame.quit()
