import pygame
import pandas as pd
import unicodedata
import re
import matplotlib.pyplot as plt


def normalize_column_names(columns):
    def normalize(col):
        col = unicodedata.normalize('NFKD', col).encode(
            'ASCII', 'ignore').decode('utf-8')
        col = re.sub(r'[^a-zA-Z0-9_]', '_', col)
        col = col.lower()
        return col
    return [normalize(col) for col in columns]


def load_csv(file_path):
    df = pd.read_csv(file_path)
    df.columns = normalize_column_names(df.columns)
    return df


def show_graphic(data, title, xlabel, ylabel):
    plt.figure(figsize=(8, 6))
    data.plot(kind='bar')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def generate_markdown_stats(df):
    desc_stats = df.describe(include='all').T
    with open('ship_performance_stats.md', 'w', encoding='utf-8') as f:
        f.write("## Estatísticas Descritivas\n\n")
        # Usa .to_string() em vez de .to_markdown()
        f.write(desc_stats.to_string())



def main():
    df = load_csv('./assets/datasets/jeleeladekunlefijabi/ship-performance-clustering-dataset/Ship_Performance_Dataset.csv')
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Ship Performance Insights")
    font = pygame.font.Font(None, 36)

    title = font.render(
        "Conjunto de dados de agrupamento de desempenho de navios", True, (0, 0, 0))
    title_rect = title.get_rect(center=(400, 50))

    buttons = [
        ("Velocidade Média", lambda: show_graphic(
            df['speed_over_ground_knots'], "Velocidade Média", "Navios", "Nós")),
        ("Distância Percorrida", lambda: show_graphic(df.nlargest(10, 'distance_traveled_nm')[
         'distance_traveled_nm'], "Top 10 Distância Percorrida", "Navios", "Milhas Náuticas")),
        ("Eficiência Energética", lambda: show_graphic(
            df['efficiency_nm_per_kwh'], "Eficiência Energética", "Navios", "Nm/kWh")),
        ("Gerar Estatísticas", lambda: generate_markdown_stats(df))
    ]

    button_surfaces = []
    button_rects = []
    for idx, (text, _) in enumerate(buttons):
        surface = pygame.Surface((300, 50), pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 0, 255, 255),
                         (0, 0, 300, 50), border_radius=10)
        text_surf = font.render(text, True, (255, 255, 255))
        surface.blit(text_surf, (50, 10))
        rect = surface.get_rect(center=(400, 150 + idx * 70))
        button_surfaces.append(surface)
        button_rects.append(rect)

    running = True
    while running:
        screen.fill((255, 255, 255))
        screen.blit(title, title_rect)

        for surface, rect in zip(button_surfaces, button_rects):
            screen.blit(surface, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, (_, action) in zip(button_rects, buttons):
                    if rect.collidepoint(event.pos):
                        action()

    pygame.quit()


if __name__ == "__main__":
    main()
