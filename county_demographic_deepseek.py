import pandas as pd
import pygame
import sys
import matplotlib.pyplot as plt
from unidecode import unidecode

# Função para normalizar os nomes das colunas


def normalize_column_name(column_name):
    # Remove acentos e caracteres especiais
    normalized = unidecode(column_name)
    # Converte para snake_case
    normalized = normalized.lower().replace(" ", "_").replace("-", "_")
    return normalized

# Carregar o arquivo CSV


def load_csv(file_path):
    df = pd.read_csv(file_path)
    # Normalizar os nomes das colunas
    df.columns = [normalize_column_name(col) for col in df.columns]
    return df

# Função para exibir estatísticas descritivas


def show_descriptive_stats(df):
    desc_stats = df.describe(include='all').T
    print(desc_stats)
    return desc_stats

# Função para plotar gráficos


def plot_gender_distribution(df):
    df[['male_population', 'female_population']].sum().plot(
        kind='bar', color=['blue', 'pink'])
    plt.title('Distribuição de Gênero')
    plt.ylabel('População')
    plt.show()


def plot_racial_distribution(df):
    df[['white_alone', 'black_or_african_american_alone', 'hispanic_or_latino']
       ].sum().plot(kind='bar', color=['gray', 'black', 'orange'])
    plt.title('Distribuição Racial')
    plt.ylabel('População')
    plt.show()


# Inicializar o Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ataque cardíaco no Japão: jovens versus adultos")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Fonte
font = pygame.font.Font(None, 36)

# Função para criar botões


def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

# Função principal


def main():
    # Substitua pelo caminho do seu arquivo CSV
    df = load_csv("./assets/datasets/ahmedmohamed2003/county-level-demographic-population-race-gender/demographic_data.csv")

    buttons = [
        {"text": "Distribuição de Gênero",
            "action": lambda: plot_gender_distribution(df)},
        {"text": "Distribuição Racial",
            "action": lambda: plot_racial_distribution(df)},
        {"text": "Estatísticas Descritivas",
            "action": lambda: show_descriptive_stats(df)},
    ]

    running = True
    while running:
        screen.fill(WHITE)
        # Título
        title_surface = font.render(
            "Dados demográficos: população, raça, dados de gênero do condado", True, BLACK)
        title_rect = title_surface.get_rect(center=(screen_width / 2, 50))
        screen.blit(title_surface, title_rect)

        # Desenhar botões
        button_y = 150
        for button in buttons:
            draw_button(button["text"], 300, button_y, 200, 50, BLUE)
            button_y += 70

        # Verificar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_y = 150
                for button in buttons:
                    button_rect = pygame.Rect(300, button_y, 200, 50)
                    if button_rect.collidepoint(mouse_pos):
                        button["action"]()
                        # Abrir nova tela
                        screen.fill(WHITE)
                        pygame.display.flip()
                        waiting = True
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    waiting = False
                    button_y += 70

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
