import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from analysisNum import ranked_ROIC, port_acc_vet1, port_acc_vet2, port_acc_vet3, port_acc_vet4, ref_acc_vet, port_chg_vet1, port_chg_vet2, port_chg_vet3, port_chg_vet4, ref_chg_vet
from dataManagement import data_inicial, data_final, step_eval

#Evolução das quotas de um portfólio e de uma referência (IBX) com base 1

# Crie o DataFrame final_df com os índices do intervalo de interesse de ranked_ROIC
final_df = pd.DataFrame(index=ranked_ROIC.iloc[data_inicial:data_final+1].index)

# Ajuste os comprimentos das séries temporais para coincidirem com o comprimento do índice de final_df
final_df['Fator Vol'] = port_acc_vet1[:len(final_df)]
final_df['Fator Qual'] = port_acc_vet2[:len(final_df)]
final_df['Fatores Vol & Qual'] = port_acc_vet3[:len(final_df)]
final_df['Port Otim'] = port_acc_vet4[:len(final_df)]
final_df['IBX'] = ref_acc_vet[:len(final_df)]
final_df.iloc[0:].plot(figsize=(18,6), grid=True);
plt.show()

#Volatilidade dos últimos 12 meses de um portfólio e de uma referência (IBX)
final_vol_df = pd.DataFrame()
final_vol_df['Fator Vol'] = pd.Series(port_chg_vet1).rolling(int(12/step_eval)).std()*(int(12/step_eval)**(1/2))
final_vol_df['Fator Qual'] = pd.Series(port_chg_vet2).rolling(int(12/step_eval)).std()*(int(12/step_eval)**(1/2))
final_vol_df['Fatores Vol & Qual'] = pd.Series(port_chg_vet3).rolling(int(12/step_eval)).std()*(int(12/step_eval)**(1/2))
final_vol_df['Port Otim'] = pd.Series(port_chg_vet4).rolling(int(12/step_eval)).std()*(int(12/step_eval)**(1/2))
final_vol_df['IBX']   = pd.Series(ref_chg_vet).rolling(int(12/step_eval)).std()*(int(12/step_eval)**(1/2))
final_vol_df.plot(figsize=(18,6), grid=True);
plt.show()

#Retorno anual de um portfólio e de uma referência (IBX)
final_df12 = pd.DataFrame(columns=['Data', 'Fator Vol', 'Fator Qual', 'Fatores Vol & Qual', 'Port RP', 'IBX'])
for ind in range(0, len(final_df.index)-12, 12):
  final_temp = final_df.iloc[ind+12]/final_df.iloc[ind]-1
  final_df12 =pd.concat([final_df12, pd.DataFrame([final_temp])], ignore_index=True)
  final_df12.iat[len(final_df12)-1, 0] = final_df.index[ind]

final_df12.set_index(keys = 'Data', inplace = True)

final_df12.plot.bar(figsize=(18,6), grid=True);
plt.show()