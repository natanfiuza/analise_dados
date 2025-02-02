import os
import kagglehub
import shutil
import argparse

def copiar_arquivos(caminho_origem, caminho_destino):
    """
    Copia todos os arquivos de um diretório para outro.

    Args:
        caminho_origem: O caminho do diretório de origem.
        caminho_destino: O caminho do diretório de destino.
    """

    try:
        # Verifica se os caminhos existem
        if not os.path.exists(caminho_origem):
            raise FileNotFoundError(f"Diretório de origem '{caminho_origem}' não encontrado.")
        if not os.path.exists(caminho_destino):
            raise FileNotFoundError(f"Diretório de destino '{caminho_destino}' não encontrado.")

        # Itera sobre os arquivos e subdiretórios no diretório de origem
        for item in os.listdir(caminho_origem):
            caminho_completo_origem = os.path.join(caminho_origem, item)
            caminho_completo_destino = os.path.join(caminho_destino, item)

            # Se for um arquivo, copia
            if os.path.isfile(caminho_completo_origem):
                shutil.copy2(caminho_completo_origem, caminho_completo_destino)  # Use copy2 para preservar metadados

            # Se for um subdiretório, chama a função recursivamente
            elif os.path.isdir(caminho_completo_origem):
                # Cria o subdiretório correspondente no destino (se não existir)
                os.makedirs(caminho_completo_destino, exist_ok=True)
                copiar_arquivos(caminho_completo_origem, caminho_completo_destino)

    except Exception as e:
        print(f"Erro ao copiar arquivos: {e}")

def concatenar_path(caminho1, caminho2):
  """
  Concatena dois caminhos de arquivos, garantindo que haja apenas uma barra entre eles.

  Args:
    caminho1: O primeiro caminho.
    caminho2: O segundo caminho.

  Returns:
    Uma string contendo a concatenação dos dois caminhos.
  """

  return os.path.join(caminho1, caminho2)
def main():
    parser = argparse.ArgumentParser(description="Script para download de dados de um dataset do Kaggle.")

    # Adiciona argumentos
    parser.add_argument("-dataset", dest="dataset", help="Nome do dataset no Kaggle Hub (ex: guilhermelima92/dados-demorficos)")
    parser.add_argument("-target_path", dest="target_path", help="Caminho para salvar os dados (ex: ./assets/datasets)")

    # Faz o parsing dos argumentos
    args = parser.parse_args()

    # Verifica se algum argumento foi fornecido
    if args.dataset or args.target_path:
        print(f"Importando dados do dataset Kaggle: {args.dataset}")

        # Faz o download da última versão do dataset para o diretório especificado
        path = kagglehub.dataset_download(args.dataset)
        if not args.target_path:
            args.target_path = "./assets/datasets/"

        if args.target_path:
            # Define o diretório de destino
            target_dir = concatenar_path(caminho1=args.target_path,caminho2=args.dataset)
            # Cria o diretório, se ele ainda não existir
            os.makedirs(target_dir, exist_ok=True)
            copiar_arquivos(caminho_origem=path,caminho_destino=target_dir)
            print("Path to dataset files:", target_dir)
        else: 
            print("Path to dataset files:", path)

        
    else:
        print("Nenhum parâmetro foi informado. Utiliza -h")

if __name__ == "__main__":
    main()