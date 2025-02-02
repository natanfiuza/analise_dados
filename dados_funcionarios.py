import pandas as pd
import pygame
import matplotlib.pyplot as plt
import re
import locale
import chardet
from unidecode import unidecode
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Configurar localidade para pt_BR para formatação monetária
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# --- Funções de Pré-processamento ---

def clean_column_name(name):
    """
    Limpa um nome de coluna, convertendo para snake_case, removendo acentos,
    espaços e caracteres especiais.
    """
    name = unidecode(name)  # Remove acentos
    name = name.lower()
    name = re.sub(r'[^a-z0-9_]', '_', name)  # Substitui caracteres não alfanuméricos por '_'
    name = re.sub(r'[_]+', '_', name)  # Substitui múltiplas ocorrências de '_' por uma única
    name = name.strip('_')  # Remove '_' do início e do fim
    return name

def load_and_clean_csv(file_path):
    """
    Carrega um arquivo CSV, limpa os nomes das colunas e retorna um DataFrame.
    Detecta automaticamente a codificação do arquivo usando chardet.
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())

    encoding = result['encoding']
    df = pd.read_csv(file_path, encoding=encoding)
    df.columns = [clean_column_name(col) for col in df.columns]
    
    #Removendo caracteres especiais dos dados
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: unidecode(x) if isinstance(x, str) else x)

    return df

# --- Funções de Análise ---

def total_anual_salarios(df):
    """
    Calcula o total anual de salários.
    """
    total = df['custo_total_anual'].sum()
    return {"name": "total_anual_salarios","data":total,"texto": 'Total anual dos sálarios:'}

def top_10_setores_por_salario_anual(df):
    """
    Retorna os top 10 setores por salário anual.
    """
    return {"name": "top_10_setores_por_salario_anual","data":df.groupby('departamento')['custo_total_anual'].sum().nlargest(10),"texto": ''}

def top_10_funcoes_por_salario_anual(df):
    """
    Retorna os top 10 funções por salário anual.
    """
    return {"name": "top_10_funcoes_por_salario_anual","data":df.groupby('cargo')['custo_total_anual'].sum().nlargest(10),"texto": ''}

def top_10_setores_por_salario_mensal(df):
    """
    Retorna os top 10 setores por salário mensal (aproximado).
    """
    df_temp = df.copy()
    df_temp['salario_mensal_aprox'] = df_temp['salario']
    return {"name": "top_10_setores_por_salario_mensal","data":df_temp.groupby('departamento')['salario_mensal_aprox'].sum().nlargest(10),"texto": ''}

def top_10_funcoes_por_salario_mensal(df):
    """
    Retorna os top 10 funções por salário mensal (aproximado).
    """
    df_temp = df.copy()
    df_temp['salario_mensal_aprox'] = df_temp['salario']
    return {"name": "top_10_funcoes_por_salario_mensal","data": df_temp.groupby('cargo')['salario_mensal_aprox'].sum().nlargest(10),"texto": ''}

def evolucao_temporal_salarios(df):
    """
    Retorna a evolução temporal dos salários (considerando data de admissão).
    """
    df['data_de_admissao'] = pd.to_datetime(df['data_de_admissao'], dayfirst=True, errors='coerce')
    df = df.sort_values('data_de_admissao')
    df['custo_acumulado'] = df['custo_total_anual'].cumsum()

    return {"name": "evolucao_temporal_salarios","data":df[['data_de_admissao', 'custo_acumulado']],"texto": ''}

def distribuicao_graus_academicos(df):
    """
    Retorna a distribuição de graus acadêmicos.
    """
    return {"name": "distribuicao_graus_academicos","data":df['grau_academico'].value_counts(),"texto": ''}

def custo_total_anual_por_setor(df):
    """
    Retorna o custo total anual por setor.
    """
    return {"name": "custo_total_anual_por_setor","data": df.groupby('departamento')['custo_total_anual'].sum(),"texto": ''}

def custo_total_anual_por_funcao(df):
    """
    Retorna o custo total anual por função.
    """
    return {"name": "custo_total_anual_por_funcao","data":df.groupby('cargo')['custo_total_anual'].sum().nlargest(10),"texto": ''}

# --- Funções de Visualização com Pygame ---

def formatar_valor(valor):
    return locale.currency(valor, grouping=True)

def show_value_screen(screen, value, font):
    """
    Exibe uma tela com um valor formatado.
    """
    screen.fill((255, 255, 255))
    text_surface = font.render(value, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text_surface, text_rect)

    font = pygame.font.Font(None, 24)
    back_text = font.render("<- Voltar", True, (0, 0, 128))
    back_rect = back_text.get_rect(topleft=(10, 10))

    screen.blit(back_text, back_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):  # Verifica se clicou no botão "Voltar"
                    waiting = False     
                

def show_plot_screen(screen, data, title, xlabel, ylabel):
    """
    Exibe uma tela com um gráfico gerado pelo matplotlib.
    """

    fig, ax = plt.subplots(figsize=(8, 6))

    if isinstance(data, pd.Series):
        if data.dtype == 'float64' or data.dtype == 'int64':
          data.plot(kind='bar', ax=ax)
          ax.set_xticklabels(data.index, rotation=45, ha='right')
          # Formatando os valores do eixo y para moeda
          ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: locale.currency(x, grouping=True)))

        else:
          data.plot(kind='bar', ax=ax)
          ax.set_xticklabels(data.index, rotation=45, ha='right')

    elif isinstance(data, pd.DataFrame):
        if 'data_de_admissao' in data.columns:
            ax.plot(data['data_de_admissao'], data['custo_acumulado'])
            ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d/%m/%Y'))
            fig.autofmt_xdate()
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: locale.currency(x, grouping=True)))


    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.tight_layout()

    # Converte a figura do matplotlib para uma superfície do pygame
    canvas = FigureCanvasAgg(fig) # Importe o backend FigureCanvasAgg
    canvas.draw()
    width, height = canvas.get_width_height()
    
    image_str = canvas.buffer_rgba()
    plt.close(fig)
    
    image = pygame.image.frombuffer(image_str, (width, height), "RGBA")

    screen.fill((255, 255, 255))
    screen.blit(image, (0, 0))
 
    font = pygame.font.Font(None, 24)
    back_text = font.render("<- Voltar", True, (0, 0, 128))
    back_rect = back_text.get_rect(topleft=(10, 10))

    screen.blit(back_text, back_rect)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):  # Verifica se clicou no botão "Voltar"
                    waiting = False                
                #else:
                #    waiting = False
# --- Classe Button ---

class Button:
    def __init__(self, text, x, y, width, height, action, df, screen, font, title, xlabel, ylabel):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 0, 255)  # Azul
        self.action = action
        self.df = df
        self.screen = screen
        self.font = font
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.hover_color = (50, 50, 255) #Azul um pouco mais claro
        self.is_hovered = False

    def draw(self, screen):
      """
      Desenha o botão na tela
      """
      if self.is_hovered:
          color = self.hover_color
      else:
          color = self.color

      pygame.draw.rect(screen, color, self.rect, border_radius=10)
      text_surface = self.font.render(self.text, True, (255, 255, 255))
      text_rect = text_surface.get_rect(center=self.rect.center)
      screen.blit(text_surface, text_rect)

    def handle_event(self, event):
      """
      Trata eventos do mouse
      """
      if event.type == pygame.MOUSEMOTION:
          self.is_hovered = self.rect.collidepoint(event.pos)
      elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1 and self.is_hovered:
              self.on_click()

    def on_click(self):
        """
        Chama a função de ação do botão
        """
        import numpy as np
        result = self.action(self.df)      
        
        if isinstance(result['data'], (int, float,np.int64, np.float64)):
            print('Show value screen')
            show_value_screen(self.screen, f"{result['texto']} {formatar_valor(result['data'])}", self.font)
        else:
            print('Show plot screen')
            show_plot_screen(self.screen, result['data'], self.title, self.xlabel, self.ylabel)


# --- Função Principal ---

def main():
    pygame.init()

    # Configurações da tela
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Análise de Dados de RH")

    # Carrega os dados
    df = load_and_clean_csv("./assets/datasets/funcionarios_ficticios/dados.csv")  # Substitua "dados.csv" pelo caminho do seu arquivo

    # Fonte para os botões
    font = pygame.font.Font(None, 24)

    # Criação dos botões
    button_width = 300
    button_height = 40
    gap = 10
    start_y = 50
    buttons = [
        Button("Total Anual de Salários", (screen_width - button_width) // 2, start_y, button_width, button_height, total_anual_salarios, df, screen, font, "", "", ""),
        Button("Top 10 Setores por Salário Anual", (screen_width - button_width) // 2, start_y + (button_height + gap), button_width, button_height, top_10_setores_por_salario_anual, df, screen, font, "Top 10 Setores por Salário Anual", "Setor", "Custo Anual"),
        Button("Top 10 Funções por Salário Anual", (screen_width - button_width) // 2, start_y + 2 * (button_height + gap), button_width, button_height, top_10_funcoes_por_salario_anual, df, screen, font, "Top 10 Funções por Salário Anual", "Função", "Custo Anual"),
        Button("Top 10 Setores por Salário Mensal", (screen_width - button_width) // 2, start_y + 3 * (button_height + gap), button_width, button_height, top_10_setores_por_salario_mensal, df, screen, font, "Top 10 Setores por Salário Mensal", "Setor", "Salário Mensal Aprox."),
        Button("Top 10 Funções por Salário Mensal", (screen_width - button_width) // 2, start_y + 4 * (button_height + gap), button_width, button_height, top_10_funcoes_por_salario_mensal, df, screen, font, "Top 10 Funções por Salário Mensal", "Função", "Salário Mensal Aprox."),
        Button("Evolução Temporal dos Salários", (screen_width - button_width) // 2, start_y + 5 * (button_height + gap), button_width, button_height, evolucao_temporal_salarios, df, screen, font, "Evolução Temporal dos Salários", "Data de Admissão", "Custo Acumulado"),
        Button("Distribuição de Graus Acadêmicos", (screen_width - button_width) // 2, start_y + 6 * (button_height + gap), button_width, button_height, distribuicao_graus_academicos, df, screen, font, "Distribuição de Graus Acadêmicos", "Grau Acadêmico", "Quantidade"),
        Button("Custo Total Anual por Setor", (screen_width - button_width) // 2, start_y + 7 * (button_height + gap), button_width, button_height, custo_total_anual_por_setor, df, screen, font, "Custo Total Anual por Setor", "Setor", "Custo Anual"),
        Button("Custo Total Anual por Função", (screen_width - button_width) // 2, start_y + 8 * (button_height + gap), button_width, button_height, custo_total_anual_por_funcao, df, screen, font, "Custo Total Anual por Função", "Função", "Custo Anual"),
    ]

    # Loop principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.handle_event(event)

        screen.fill((255, 255, 255))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()