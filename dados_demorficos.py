import pygame
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
import re

def normalize_column_name(name):
    name = name.strip().lower()
    name = ''.join(
        c for c in unicodedata.normalize('NFKD', name) if not unicodedata.combining(c)
    )
    name = re.sub(r'[^a-z0-9_]', '_', name)
    return name

def load_csv(file_path):
    df = pd.read_csv(file_path)
    df.columns = [normalize_column_name(col) for col in df.columns]
    return df

def plot_graph(insight, df):
    plt.figure(figsize=(8, 5))
    if insight == "Distribuição de Idades":
        df['age'].hist(bins=20, color='blue', edgecolor='black')
        plt.xlabel("Idade")
        plt.ylabel("Frequência")
        plt.title("Distribuição de Idades")
    elif insight == "Educação vs Salário":
        df_grouped = df.groupby('education')['salary'].value_counts().unstack().fillna(0)
        df_grouped.plot(kind='bar', stacked=True, figsize=(10, 5))
        plt.xlabel("Nível de Educação")
        plt.ylabel("Quantidade")
        plt.title("Distribuição de Salário por Nível de Educação")
    elif insight == "Horas Trabalhadas por Semana":
        df['hours_per_week'].hist(bins=20, color='green', edgecolor='black')
        plt.xlabel("Horas por Semana")
        plt.ylabel("Frequência")
        plt.title("Distribuição de Horas Trabalhadas")
    elif insight == "Distribuição por Ocupação":
        df['occupation'].value_counts().plot(kind='bar', color='purple')
        plt.xlabel("Ocupação")
        plt.ylabel("Quantidade")
        plt.title("Distribuição por Ocupação")
    plt.show()

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Insights de Ciência de Dados")
    
    df = load_csv("./assets/datasets/guilhermelima92/dados-demorficos/adult.data.csv")  # Substitua pelo caminho do seu arquivo CSV
    
    font = pygame.font.Font(None, 36)
    button_color = (0, 0, 255)
    button_width = 400
    button_height = 50
    button_x = 100
    spacing = 20
    
    insights = [
        "Distribuição de Idades",
        "Educação vs Salário",
        "Horas Trabalhadas por Semana",
        "Distribuição por Ocupação"
    ]
    
    buttons = []
    for i, text in enumerate(insights):
        rect = pygame.Rect(button_x, 50 + i * (button_height + spacing), button_width, button_height)
        buttons.append((rect, text))
    
    running = True
    while running:
        screen.fill((255, 255, 255))
        for rect, text in buttons:
            pygame.draw.rect(screen, button_color, rect, border_radius=10)
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (rect.x + 10, rect.y + 10))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, text in buttons:
                    if rect.collidepoint(event.pos):
                        plot_graph(text, df)
    
    pygame.quit()

if __name__ == "__main__":
    main()
