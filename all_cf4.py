import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# --- Função 1: Ler e processar o XML ---
def parse_xml(file_path):
    """
    Função para ler um arquivo XML e extrair os dados de interesse.
    Retorna uma lista com os dados das galáxias.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Definir o namespace do XML
    namespace = {'vot': 'http://www.ivoa.net/xml/VOTable/v1.2'}

    # Inicializar uma lista para armazenar os dados das galáxias
    data = []
    
    # Iterar sobre cada linha da tabela (TR) e extrair os dados das colunas (TD)
    for row in root.findall('.//vot:TR', namespaces=namespace):
        row_data = [td.text for td in row.findall('vot:TD', namespaces=namespace)]
        data.append(row_data)

    return data

# --- Função 2: Converter os dados em um DataFrame ---
def create_dataframe(data, columns):
    """
    Função para criar um DataFrame a partir dos dados extraídos do XML.
    Converte as colunas relevantes número.
    """
    # Criar o DataFrame com os dados e colunas especificadas
    df = pd.DataFrame(data, columns=columns)

    # Converter as colunas de interesse para numérico
    df['DM'] = pd.to_numeric(df['DM'], errors='coerce')
    df['DMsnIa'] = pd.to_numeric(df['DMsnIa'], errors='coerce')
    df['DMtf'] = pd.to_numeric(df['DMtf'], errors='coerce')
    df['eDM'] = pd.to_numeric(df['eDM'], errors='coerce')
    df['SGX'] = pd.to_numeric(df['SGX'], errors='coerce')
    df['SGY'] = pd.to_numeric(df['SGY'], errors='coerce')
    df['SGZ'] = pd.to_numeric(df['SGZ'], errors='coerce')
    df['Vcmb'] = pd.to_numeric(df['Vcmb'], errors='coerce')
    
    return df

# --- Função 3: Plotar Mapa 3D das Galáxias ---
def plot_galaxies_3d(df):
    print("- func. plot_galaxies_3d: Mapeando objetos em coordenadas supergalácticas")
    """
    Função para plotar as galáxias em 3D usando as coordenadas SGX, SGY, SGZ.
    """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plotar as galáxias com as coordenadas SGX, SGY, SGZ e colorir pelo módulo de distância (DM)
    scatter = ax.scatter(df['SGX'], df['SGY'], df['SGZ'], c=df['DM'], cmap='plasma', s=5, alpha=0.7)

    # Adicionar barra de cores, título e rótulos dos eixos
    fig.colorbar(scatter, ax=ax, label='Distância Módulo (DM) [Mpc]')
    ax.set_title('Coordenadas Supergalácticas Individuais das Galáxias no Universo Observável', fontsize=14)
    ax.set_xlabel('SGX [Mpc]')
    ax.set_ylabel('SGY [Mpc]')
    ax.set_zlabel('SGZ [Mpc]')

    # Exibir gráfico
    plt.show()

# --- Função 4: Plotar Mapa 3D com Galáxias Coloridas por Erros ---
def plot_galaxies_by_error(df):
    print("- func. plot_galaxies_by_error: saturando galáxias com base nos erros")

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Definir um gradiente de cor para representar o erro:
    scatter = ax.scatter(df['SGX'], df['SGY'], df['SGZ'], c=df['eDM'], cmap='Oranges', s=5, alpha=0.7)

    # Adicionar barra de cor para indicar a magnitude do erro
    fig.colorbar(scatter, ax=ax, label='Erro no Módulo de Distância (eDM) [mag]')
    
    # Título e rótulos dos eixos
    ax.set_title('Diferença da Margem de Erro do Módulo de Distância Entre Múltiplos Métodos de Medição', fontsize=14)
    ax.set_xlabel('SGX [Mpc]')
    ax.set_ylabel('SGY [Mpc]')
    ax.set_zlabel('SGZ [Mpc]')

    # Exibir o gráfico
    plt.show()

# --- Função 5: Plotar Gráfico Vetorial do Movimento das Galáxias ---
def plot_vector_field(df):
    print("- func. plot_vector_field: Mapeando o movimento das galáxias")
    """
    Função para plotar um gráfico vetorial do movimento das galáxias.
    """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Criar vetores de movimento baseados na velocidade radial (Vcmb)
    ax.quiver(df['SGX'], df['SGY'], df['SGZ'], 
              df['Vcmb'] * np.cos(df['SGZ']), df['Vcmb'] * np.sin(df['SGZ']), np.zeros(len(df['SGZ'])), 
              length=0.1, normalize=True, color='b', alpha=0.5)

    ax.set_title('Campo Vetorial do Movimento das Galáxias', fontsize=14)
    ax.set_xlabel('SGX [Mpc]')
    ax.set_ylabel('SGY [Mpc]')
    ax.set_zlabel('SGZ [Mpc]')


    plt.show()





# --- Função 5: Plotar Gráfico Vetorial do Movimento das Galáxias com Galáxias Plotadas e Transparência ---
def plot_vector_field_with_galaxies(df, point_alpha=0.5):
    print("- func. plot_vector_field_with_galaxies: Mapeando o movimento das galáxias com plot")
    """
    Função para plotar um gráfico vetorial do movimento das galáxias junto as galáxias
    """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Criar vetores de movimento baseados na velocidade radial (Vcmb)
    ax.quiver(df['SGX'], df['SGY'], df['SGZ'], 
              df['Vcmb'] * np.cos(df['SGZ']), df['Vcmb'] * np.sin(df['SGZ']), np.zeros(len(df['SGZ'])), 
              length=0.1, normalize=True, color='b', alpha=0.5)

    # Plotar as galáxias como pontos
    ax.scatter(df['SGX'], df['SGY'], df['SGZ'], c='yellow', s=10, alpha=point_alpha, label='Galáxias')


    ax.set_title('Campo Vetorial do Movimento das Galáxias com Galáxias Plotadas', fontsize=14)
    ax.set_xlabel('SGX [Mpc]')
    ax.set_ylabel('SGY [Mpc]')
    ax.set_zlabel('SGZ [Mpc]')
    ax.legend()

    # Exibir o gráfico
    plt.show()


def plot_magnitude_histogram(df):
    """
    Função para plotar um histograma da magnitude (DM) das galáxias.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(df['DM'], bins=30, color='Blue', alpha=0.7, edgecolor='black')
    plt.title('Distribuição da Magnitude (DM)')
    plt.xlabel('Magnitude (DM)')
    plt.ylabel('Frequência')
    plt.grid()
    plt.show()


def plot_scatter_with_magnitude(df):
    """
    Função para plotar um gráfico de dispersão colorido pela magnitude (DM).
    """
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df['SGX'], df['SGY'], c=df['DM'], cmap='Blues', alpha=0.6, edgecolor='black')
    plt.colorbar(scatter, label='Magnitude (DM)')
    plt.title('Gráfico de Dispersão Colorido por Magnitude')
    plt.xlabel('SGX [Mpc]')
    plt.ylabel('SGY [Mpc]')
    plt.grid()
    plt.show()











# --- Função Principal: Carregar dados e executar as funções ---
def main():
    # Definir o caminho do arquivo XML
    file_path = './data/allCf4.xml' 
    print(f"Carregando a base de dados ... !! ... Aguarde\n\tCaminho: {file_path}")

    # Definir as colunas do DataFrame
    columns = [
        "PGC_ID", "1PGC", "T17", "Vcmb", "DM", "eDM", "DMsnIa", "eDMsn1", "DMtf", "eDMtf", "DMfp", "eDMfp",
        "DMsbf", "eDMsbf", "DMsnII", "eDMsn2", "DMtrgb", "eDMt", "DMcep", "eDMcep", "DMmas", "eDMmas", 
        "RA", "DE", "glon", "glat", "sgl", "sgb", "SGX", "SGY", "SGZ"
    ]

    # Ler os dados do arquivo XML
    data = parse_xml(file_path)
    # Criar um DataFrame com os dados
    df = create_dataframe(data, columns)

    # --- Menu de Opções ---
    while True:
        print("\nÍNDICE")
        print("aa - Mapear objetos em coordenadas supergalácticas")
        print("ab - Colorir galáxias com base nos erros")
        print("ac - Gráfico Vetorial do Movimento das Galáxias sem Plot")
        print("ad - Gráfico Vetorial do Movimento das Galáxias com Plot")
        print("ae - Histograma da magnitude (DM) das galáxias")
        print("af - Gráfico de dispersão pela magnitude (DM)")
        print("q - Sair")
        
        choice = input("Digite sua escolha: ").strip().lower()

        if choice == 'aa':
            plot_galaxies_3d(df)
        elif choice == 'ab':
            plot_galaxies_by_error(df)
        elif choice == 'ac':
            plot_vector_field(df)
        elif choice == 'ad':
            plot_vector_field_with_galaxies(df)
        elif choice == 'ae':
            plot_magnitude_histogram(df)
        elif choice == 'af':
            plot_scatter_with_magnitude(df)
        elif choice == 'q':
            print("Obrigado por seu interesse pela ciência")
            break
        else:
            print("\tOpção inválida.")





if __name__ == "__main__":
    main()
