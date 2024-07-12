import pandas as pd

# Constantes básicas para o script
data_inicial = 13                   # Índice inicial para a análise dos dados: 01/2005
data_final = data_inicial + 204     # Índice final para a análise dos dados: 12/2021
colunas = 291                       # Número de colunas nos dados carregados
step_port = 1                       # Intervalo de passos para operações de portfólio
step_eval = 1                       # Intervalo de passos para operações de avaliação

def load_data(file_name, index_col='Data'):
    """
    Carrega dados de um arquivo Excel especificado e define uma coluna como índice.

    Args:
    file_name (str): O caminho para o arquivo a ser carregado.
    index_col (str): O nome da coluna a ser usada como índice do DataFrame.

    Returns:
    pd.DataFrame: Um DataFrame com a coluna especificada definida como índice.
    """
    data = pd.read_excel(file_name, engine='openpyxl')  # Utiliza o motor openpyxl para ler arquivos Excel
    data.set_index(keys=index_col, inplace=True)        # Define a coluna especificada como índice
    return data

# Carregamento de dados de composição dos índices e preços
comp_indice = load_data('dados-economatica/Dados-Comp-IBRX.xlsx')      # Composição do índice IBRX
fechamento = load_data('dados-economatica/Dados-Fechamento.xlsx')      # Dados de fechamento dos ativos
referencias = load_data('dados-economatica/Dados-Base.xlsx')           # Dados de referências como Ibovespa, IBX, SELIC, etc.
fator_ROIC = load_data('dados-economatica/Dados-ROIC-A2.xlsx')         # Dados do fator ROIC (Return on Invested Capital)
fator_Mom = load_data('dados-economatica/Dados-Momentum-12.xlsx')      # Dados do fator de Momentum (12 meses)
fator_Val_Merc = load_data('dados-economatica/Dados-Val-Merc.xlsx')    # Dados do fator de valor de mercado das empresas
fator_PVP = load_data('dados-economatica/Dados-PVP.xlsx')              # Dados do fator preço sobre valor patrimonial (PVP)
fator_Vol = load_data('dados-economatica/Dados-Vol-12.xlsx')           # Dados do fator de volatilidade (12 meses)