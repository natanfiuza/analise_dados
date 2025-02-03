import pandas as pd
import pygame
import matplotlib.pyplot as plt
import seaborn as sns
import io
import sys

# Função para limpar e padronizar os nomes das colunas
def clean_column_names(df):
    new_columns = []
    for col in df.columns:
        col = col.lower()
        col = col.replace(" ", "_")
        col = col.replace("á", "a")
        col = col.replace("é", "e")
        col = col.replace("í", "i")
        col = col.replace("ó", "o")
        col = col.replace("ú", "u")
        col = col.replace("ã", "a")
        col = col.replace("õ", "o")
        col = col.replace("ç", "c")
        col = col.replace("-", "_")
        col = col.replace(",", "")
        col = col.replace("(", "")
        col = col.replace(")", "")
        new_columns.append(col)
    df.columns = new_columns
    return df

# Carregar o arquivo CSV
try:
    df = pd.read_csv("./assets/datasets/ahmedmohamed2003/county-level-demographic-population-race-gender/demographic_data.csv", encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv("data.csv", encoding='latin1')
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        sys.exit()

df = clean_column_names(df)

# Inicializar o Pygame
pygame.init()

# Configurações da tela
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Análise Demográfica dos EUA")

# Cores
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)

# Fonte
font = pygame.font.Font(None, 36)

# Título
title_text = font.render("Análise Demográfica dos EUA", True, black)
title_rect = title_text.get_rect(center=(screen_width // 2, 50))

# Funções para gerar gráficos

def plot_population_by_state():
    plt.figure(figsize=(12, 6))
    population_by_state = df.groupby('state')['total_population'].sum().sort_values(ascending=False).head(10)
    sns.barplot(x=population_by_state.index, y=population_by_state.values, palette="viridis")
    plt.title('Top 10 Estados por População Total')
    plt.xlabel('Estado')
    plt.ylabel('População Total')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    #Converte o gráfico para uma superfície Pygame
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = pygame.image.load(buf)
    buf.close()
    return image

def plot_gender_distribution():
    plt.figure(figsize=(8, 6))
    gender_counts = [df['male_population'].sum(), df['female_population'].sum()]
    plt.pie(gender_counts, labels=['Masculino', 'Feminino'], autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
    plt.title('Distribuição de Gênero')
    plt.tight_layout()

    # Converte o gráfico para uma superfície Pygame
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = pygame.image.load(buf)
    buf.close()
    return image

def plot_race_distribution():
    plt.figure(figsize=(10, 6))
    race_columns = ['white_alone', 'black_or_african_american_alone', 'hispanic_or_latino']
    race_sums = df[race_columns].sum()
    sns.barplot(x=race_sums.index, y=race_sums.values, palette="Set2")
    plt.title('Distribuição de Raça')
    plt.xlabel('Raça')
    plt.ylabel('Número de Indivíduos')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Converte o gráfico para uma superfície Pygame
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = pygame.image.load(buf)
    buf.close()
    return image

def plot_top_counties_by_population():
    plt.figure(figsize=(12, 6))
    top_counties = df.sort_values('total_population', ascending=False).head(10)
    sns.barplot(x='county', y='total_population', hue='state', data=top_counties, dodge=False, palette="magma")
    plt.title('Top 10 Condados por População Total')
    plt.xlabel('Condado')
    plt.ylabel('População Total')
    plt.xticks(rotation=45)
    plt.legend([],[], frameon=False)
    plt.tight_layout()

    # Converte o gráfico para uma superfície Pygame
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = pygame.image.load(buf)
    buf.close()
    return image

def show_all_stats():
    desc_stats = df.describe(include='all').T
    desc_stats.reset_index(inplace=True)
    desc_stats.rename(columns={'index': 'statistic'}, inplace=True)

    stats_surface = pygame.Surface((screen_width, screen_height))
    stats_surface.fill(white)
    font = pygame.font.Font(None, 16)
    y_offset = 10
    font = pygame.font.Font(None, 16)
    for index, row in desc_stats.iterrows():
        stat_line = ""
        for col in desc_stats.columns:
            stat_line += f"{col}: {row[col]} | "
        
        text_surface = font.render(stat_line, True, black)
        stats_surface.blit(text_surface, (10, y_offset))
        y_offset += 15
    
    return stats_surface

# Botões
button_width = 300
button_height = 50
button_y_start = 150
button_spacing = 60

buttons = [
    {"text": "População por Estado", "action": plot_population_by_state},
    {"text": "Distribuição de Gênero", "action": plot_gender_distribution},
    {"text": "Distribuição de Raça", "action": plot_race_distribution},
    {"text": "Top Condados por População", "action": plot_top_counties_by_population},
    {"text": "Estatísticas Descritivas", "action": show_all_stats}
]

button_rects = []
for i, button in enumerate(buttons):
    button_y = button_y_start + i * button_spacing
    button_rect = pygame.Rect((screen_width - button_width) // 2, button_y, button_width, button_height)
    button_rects.append(button_rect)

# Função para desenhar os botões
def draw_buttons():
    for i, button_rect in enumerate(button_rects):
        pygame.draw.rect(screen, blue, button_rect, border_radius=15)
        text_surface = font.render(buttons[i]["text"], True, white)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

# Função para exibir gráficos
def display_chart(chart_func):
    chart_image = chart_func()
    
    
    chart_screen = pygame.display.set_mode((chart_image.get_width(), chart_image.get_height()))
    pygame.display.set_caption("Chart")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
    
        chart_screen.fill(white)
        chart_screen.blit(chart_image, (0, 0))
        pygame.display.flip()
    
    pygame.display.set_mode((screen_width, screen_height)) # Restore the main screen
    pygame.display.set_caption("Análise Demográfica dos EUA")

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button_rect in enumerate(button_rects):
                if button_rect.collidepoint(event.pos):
                    display_chart(buttons[i]["action"])

    screen.fill(white)
    screen.blit(title_text, title_rect)
    draw_buttons()
    pygame.display.flip()

pygame.quit()