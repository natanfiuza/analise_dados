import pygame
import pandas as pd
import matplotlib.pyplot as plt
import re
import unicodedata

# Configurações do Pygame
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Análise de Dados Hospitalares")
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 30)

# Função para limpar os nomes das colunas
def clean_column_name(name):
    """
    Converte o nome da coluna para snake_case, remove acentos,
    espaços e caracteres especiais.
    """
    s = unicodedata.normalize('NFD', name)
    s = s.encode('ascii', 'ignore').decode('utf-8')
    s = s.lower()
    s = re.sub(r'[^a-zA-Z0-9\s]', '', s)
    s = re.sub(r'\s+', '_', s)
    return s

# Função para carregar o arquivo CSV e limpar os nomes das colunas
def load_csv(filepath):
    """
    Carrega o arquivo CSV, limpa os nomes das colunas e trata erros de encoding.
    """
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filepath, encoding='latin-1')
        except UnicodeDecodeError:
            df = pd.read_csv(filepath, encoding='cp1252')
            
    df.columns = [clean_column_name(col) for col in df.columns]
    return df

# Carregar os dados
try:
    df = load_csv("./assets/datasets/cms/hospital-general-information/HospInfo.csv") # Substitua "hospital_data.csv" pelo nome do seu arquivo
except FileNotFoundError:
    print("Erro: Arquivo hospital_data.csv não encontrado. Certifique-se de que o arquivo está no mesmo diretório do script ou forneça o caminho completo.")
    pygame.quit()
    exit()

# Insights sugeridos
insights = [
    "Top 10 Hospitais por Avaliação",
    "Comparação de Mortalidade por Estado",
    "Serviços de Emergência por Tipo de Propriedade",
    "Avaliação por Tipo de Hospital",
    "Readmissão vs. Experiência do Paciente",
]

# Funções para gerar os gráficos
def plot_top_10_hospitals(df):
    df_sorted = df.sort_values('hospital_overall_rating', ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    plt.bar(df_sorted['hospital_name'], df_sorted['hospital_overall_rating'])
    plt.title('Top 10 Hospitais por Avaliação')
    plt.xlabel('Hospital')
    plt.ylabel('Avaliação')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_mortality_by_state(df):
    df_filtered = df[df['mortality_national_comparison'] != 'Not Available']
    plt.figure(figsize=(12, 6))
    plt.bar(df_filtered['state'].value_counts().index, df_filtered['state'].value_counts().values, color=(0,0,255))
    plt.title('Comparação de Mortalidade por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Número de Hospitais')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_emergency_services_by_ownership(df):
    df_filtered = df[df['emergency_services'] == 'Yes']
    ownership_counts = df_filtered['hospital_ownership'].value_counts()
    plt.figure(figsize=(10, 6))
    plt.pie(ownership_counts, labels=ownership_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Serviços de Emergência por Tipo de Propriedade')
    plt.tight_layout()
    plt.show()

def plot_rating_by_hospital_type(df):
    df_filtered = df[df['hospital_overall_rating'] != 'Not Available']
    df_filtered['hospital_overall_rating'] = pd.to_numeric(df_filtered['hospital_overall_rating'], errors='coerce')
    plt.figure(figsize=(12, 6))
    df_filtered.boxplot(column='hospital_overall_rating', by='hospital_type', grid=False, rot=45)
    plt.title('Avaliação por Tipo de Hospital')
    plt.xlabel('Tipo de Hospital')
    plt.ylabel('Avaliação')
    plt.suptitle('')
    plt.tight_layout()
    plt.show()

def plot_readmission_vs_patient_experience(df):
    readmission_map = {
        'Same as the National average': 0,
        'Below the National average': -1,
        'Above the National average': 1,
        'Not Available': None,
    }
    patient_exp_map = {
        'Same as the National average': 0,
        'Below the National average': -1,
        'Above the National average': 1,
        'Not Available': None,
    }
    df['readmission_score'] = df['readmission_national_comparison'].map(readmission_map)
    df['patient_exp_score'] = df['patient_experience_national_comparison'].map(patient_exp_map)

    df_filtered = df.dropna(subset=['readmission_score', 'patient_exp_score'])

    plt.figure(figsize=(8, 6))
    plt.scatter(df_filtered['readmission_score'], df_filtered['patient_exp_score'], color=BLUE)
    plt.title('Readmissão vs. Experiência do Paciente')
    plt.xlabel('Readmissão (Comparado à Média Nacional)')
    plt.ylabel('Experiência do Paciente (Comparado à Média Nacional)')
    plt.xticks([-1, 0, 1], ['Abaixo', 'Igual', 'Acima'])
    plt.yticks([-1, 0, 1], ['Abaixo', 'Igual', 'Acima'])
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
# Dicionário de insights e suas funções de plotagem
insight_functions = {
    "Top 10 Hospitais por Avaliação": plot_top_10_hospitals,
    "Comparação de Mortalidade por Estado": plot_mortality_by_state,
    "Serviços de Emergência por Tipo de Propriedade": plot_emergency_services_by_ownership,
    "Avaliação por Tipo de Hospital": plot_rating_by_hospital_type,
    "Readmissão vs. Experiência do Paciente": plot_readmission_vs_patient_experience,
}

# Classe para os botões
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        # Desenha o botão com bordas arredondadas
        pygame.draw.rect(surface, BLUE, self.rect, border_radius=10)
        text_surface = FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

# Função para exibir a tela de gráfico
def show_graph_screen(plot_function):
    graph_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gráfico")
    
    plot_function(df)  # Chama a função de plotagem

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False  # Fecha a tela ao clicar em qualquer lugar

        graph_screen.fill(WHITE)
        pygame.display.flip()

    plt.close()  # Fecha a janela do gráfico do Matplotlib

# Criando os botões
buttons = []
button_width = 450
button_height = 40
button_y_start = 50
button_spacing = 10

for i, insight in enumerate(insights):
    button_y = button_y_start + i * (button_height + button_spacing)
    button = Button(insight, (SCREEN_WIDTH - button_width) // 2, button_y, button_width, button_height, action=lambda insight=insight: show_graph_screen(insight_functions[insight]))
    buttons.append(button)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)

    screen.fill(WHITE)
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()

pygame.quit()