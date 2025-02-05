import pandas as pd
import pygame
import matplotlib.pyplot as plt
import seaborn as sns
import unidecode
import re
import webbrowser

# Função para converter nomes de colunas para snake_case


def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    s3 = unidecode.unidecode(s2)
    s4 = re.sub(r'\s+', '_', s3)
    s5 = re.sub(r'[^a-z0-9_]', '', s4)
    return s5

# Função para carregar o arquivo CSV e tratar os nomes das colunas


def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df.columns = [to_snake_case(col) for col in df.columns]
        print(df.columns)
        return df
    except UnicodeDecodeError:
        print("Erro ao decodificar o arquivo CSV. Verifique a codificação do arquivo.")
        return None
    except Exception as e:
        print(f"Erro inesperado ao carregar o arquivo CSV: {e}")
        return None


# Função para gerar estatísticas descritivas e salvar em HTML
def generate_stats_html(df, filename="ship_performance_stats.html"):
    desc_stats = df.describe(include='all').T
    html_string = "<html><head><title>Estatísticas Descritivas</title><style>"
    html_string += "body { font-family: sans-serif; }"
    html_string += ".card { box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); transition: 0.3s; border-radius: 5px; padding: 10px; margin: 10px; }"
    html_string += ".card:hover { box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2); }"
    html_string += "</style></head><body><h1>Estatísticas Descritivas</h1>"

    for index, row in desc_stats.iterrows():
        html_string += "<div class='card'>"
        html_string += f"<h2>{index}</h2>"
        for col, value in row.items():
            html_string += f"<p><b>{col}:</b> {value}</p>"
        html_string += "</div>"

    html_string += "</body></html>"

    with open(filename, 'w') as f:
        f.write(html_string)

    return filename

# Funções para criar gráficos


def plot_speed_vs_efficiency(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='speed__over__ground_knots',
                    y='efficiency_nm_per_k_wh', hue='ship__type')
    plt.title('Velocidade vs. Eficiência (por Tipo de Navio)')
    plt.xlabel('Velocidade (nós)')
    plt.ylabel('Eficiência (nm/kWh)')
    plt.tight_layout()
    plt.show()


def plot_maintenance_vs_cost(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='maintenance__status', y='operational__cost_usd')
    plt.title('Status de Manutenção vs. Custo Operacional')
    plt.xlabel('Status de Manutenção')
    plt.ylabel('Custo Operacional (USD)')
    plt.tight_layout()
    plt.show()


def plot_engine_power_vs_distance(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='engine__power_k_w',
                    y='distance__traveled_nm', hue='route__type')
    plt.title('Potência do Motor vs. Distância Percorrida (por Tipo de Rota)')
    plt.xlabel('Potência do Motor (kW)')
    plt.ylabel('Distância Percorrida (nm)')
    plt.tight_layout()
    plt.show()


def plot_cargo_weight_vs_revenue(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='cargo__weight_tons',
                    y='revenue_per__voyage_usd', hue='weather__condition')
    plt.title('Peso da Carga vs. Receita por Viagem (por Condição Climática)')
    plt.xlabel('Peso da Carga (toneladas)')
    plt.ylabel('Receita por Viagem (USD)')
    plt.tight_layout()
    plt.show()


# Funções Pygame
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def create_button(surface, text, rect, color, action, data=None):
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)

    draw_rounded_rect(surface, color, rect, 15)
    surface.blit(text_surf, text_rect)

    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            return action, data
    return None, None


def main():
    # Inicialização do Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Análise de Desempenho de Navios")
    clock = pygame.time.Clock()

    # Carregar dados
    df = load_data("./assets/datasets/jeleeladekunlefijabi/ship-performance-clustering-dataset/Ship_Performance_Dataset.csv")

    if df is None:
        print("Falha ao carregar os dados. Encerrando o programa.")
        pygame.quit()
        return

    # Definir cores
    blue = (0, 105, 148)

    # Título
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render(
        "Conjunto de dados de agrupamento de desempenho de navios", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))

    # Botões
    button_height = 50
    button_spacing = 60
    button_y_start = 150
    buttons = [
        {"text": "Velocidade vs. Eficiência", "action": plot_speed_vs_efficiency},
        {"text": "Manutenção vs. Custo", "action": plot_maintenance_vs_cost},
        {"text": "Potência do Motor vs. Distância",
            "action": plot_engine_power_vs_distance},
        {"text": "Peso da Carga vs. Receita",
            "action": plot_cargo_weight_vs_revenue},
        {"text": "Estatísticas Descritivas", "action": generate_stats_html},
    ]
    button_rects = []
    for i, button in enumerate(buttons):
        button_rect = pygame.Rect(
            200, button_y_start + i * button_spacing, 400, button_height)
        button_rects.append(button_rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((240, 240, 240))

        # Desenhar título
        screen.blit(title_text, title_rect)

        # Desenhar botões
        for i, button_rect in enumerate(button_rects):
            action_result, data_result = create_button(
                screen, buttons[i]["text"], button_rect, blue, buttons[i]["action"], df)
            if action_result:
                if action_result == generate_stats_html:
                    stats_html_filename = action_result(data_result)
                    webbrowser.open_new_tab(f'file://{stats_html_filename}')
                else:
                    action_result(data_result)
                    new_screen = pygame.display.set_mode((800, 600))
                    waiting_for_close = True
                    while waiting_for_close:
                        for inner_event in pygame.event.get():
                            if inner_event.type == pygame.MOUSEBUTTONDOWN or inner_event.type == pygame.QUIT:
                                waiting_for_close = False
                                pygame.display.set_mode((800, 600))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
