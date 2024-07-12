import pandas as pd

data_inicial = 13
data_final = 217
colunas = 291
step_port = 1
step_eval = 1

def load_data(file_name, index_col='Data'):
    data = pd.read_excel(file_name, engine='openpyxl')
    data.set_index(keys=index_col, inplace=True)
    return data

# Dados de composição dos índices e preços
comp_indice = load_data('dados-economatica/Dados-Comp-IBRX.xlsx')
fator_ROIC = load_data('dados-economatica/Dados-ROIC-A2.xlsx')
fator_Mom = load_data('dados-economatica/Dados-Momentum-12.xlsx')
fator_Val_Merc = load_data('dados-economatica/Dados-Val-Merc.xlsx')
fator_PVP = load_data('dados-economatica/Dados-PVP.xlsx')
fator_Vol = load_data('dados-economatica/Dados-Vol-12.xlsx')

print("Periodo de avaliacao - de:", comp_indice.index[data_inicial], "(", data_inicial, ")",  "ate:", comp_indice.index[data_final-1], "(", data_final-1, ")")
print("Rebalanceamento a cada", step_eval,"/", step_port, "meses")
