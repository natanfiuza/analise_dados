import pygame
import pandas as pd
import unicodedata
import matplotlib.pyplot as plt


def normalize_column_names(columns):
    def normalize(name):
        name = unicodedata.normalize('NFKD', name).encode(
            'ascii', 'ignore').decode('utf-8')
        name = name.replace(' ', '_').lower()
        return name
    return [normalize(col) for col in columns]


def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = normalize_column_names(df.columns)
    return df


def show_plot(plot_func):
    plot_func()
    plt.show()


def plot_population_distribution():
    df[['male_population', 'female_population']].sum().plot(
        kind='bar', color=['blue', 'pink'])
    plt.title("Distribuição da População por Gênero")
    plt.ylabel("População")


def plot_race_comparison():
    df[['white_alone', 'black_or_african_american_alone',
        'hispanic_or_latino']].sum().plot(kind='bar')
    plt.title("Distribuição por Raça")
    plt.ylabel("População")


def plot_hispanic_percentage():
    df['hispanic_percentage'] = (
        df['hispanic_or_latino'] / df['total_population']) * 100
    df.sort_values('hispanic_percentage', ascending=False).head(20).plot(
        x='county', y='hispanic_percentage', kind='bar', color='orange')
    plt.title("Percentual de Hispânicos/Latinos nos 20 principais condados")
    plt.ylabel("% da População")


def show_statistics():
    print(df.describe(include='all').T)


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Análises Demográficas")

    font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font(None, 40)

    button_color = (0, 0, 255)
    text_color = (255, 255, 255)
    buttons = [
        ("População por Gênero", plot_population_distribution),
        ("Comparação de Raças", plot_race_comparison),
        ("Percentual Hispânico", plot_hispanic_percentage),
        ("Estatísticas Descritivas", show_statistics)
    ]

    running = True
    while running:
        screen.fill((255, 255, 255))
        title = title_font.render(
            "Dados demográficos: população, raça, dados de gênero do condado", True, (0, 0, 0))
        screen.blit(title, (20, 20))

        y_offset = 80
        button_rects = []
        for text, _ in buttons:
            rect = pygame.Rect(150, y_offset, 300, 50)
            pygame.draw.rect(screen, button_color, rect, border_radius=10)
            label = font.render(text, True, text_color)
            screen.blit(label, (rect.x + 20, rect.y + 10))
            button_rects.append((rect, _))
            y_offset += 70

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, func in button_rects:
                    if rect.collidepoint(event.pos):
                        show_plot(func)

    pygame.quit()


if __name__ == "__main__":
    df = load_data("./assets/datasets/ahmedmohamed2003/county-level-demographic-population-race-gender/demographic_data.csv")  # Substitua pelo caminho do arquivo
    main()
