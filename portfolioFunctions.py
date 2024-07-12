import numpy as np
import pandas as pd
import riskfolio as rp

data_inicial = 13
data_final = 217
colunas = 291
step_port = 1
step_eval = 1

#Funções de apoio

#Preços de fechamento dos ativos
fechamento=pd.read_excel('dados-economatica/Dados-Fechamento.xlsx', engine='openpyxl')
fechamento.set_index(keys = 'Data', inplace = True)

#Seleção das ações que compõe um portfólio.
#Parâmetros: (fator, ranking_inicio, ranking_fim)
#Retorno: portfólio
def SelPort1(port_ranked_1, param_1a, param_1b):

    port_ranked_final = port_ranked_1.copy()
    port_ranked_final.loc[:, :] = 0

    for lin in range(data_inicial, data_final, step_port):
        for col in range(0, colunas):
            if ((port_ranked_1.iat[lin-1, col]  >= param_1a) and (port_ranked_1.iat[lin-1, col]  <= param_1b)):
                port_ranked_final.iat[lin-1, col] = 1

    return port_ranked_final
#--------------------------
#Seleção das ações que compõe um portfólio com 2 fatores.
#Parâmetros: (fator1, limite1, fator2, limite2)
#Retorno: portfólio

def SelPort2Par(ranked_1, param_1, ranked_2, param_2):
  port_ranked_final = ranked_1.copy()
  port_ranked_final.loc[:, :] = 0

  for lin in range(data_inicial, data_final, step_port):
    for col in range(0, colunas):
      if ((ranked_1.iat[lin-1, col]  >= 1) and (ranked_1.iat[lin-1, col]  <= param_1) and
          (ranked_2.iat[lin-1, col]  >= 1) and (ranked_2.iat[lin-1, col]  <= param_2)):
        port_ranked_final.iat[lin-1, col] = 1

  return port_ranked_final
#--------------------------

#Avaliação de um portfólio.
#Parâmetros: (portfólio, histórico de preços dos ativos)
#Retorno: vetor com retorno acumulado, vetor com retornos periódicos, vetor com drawdown, retorno anualizado, volatilidade anualizada
def EvalPort(port, fechamento):
    port_acc_vet = []
    port_chg_vet = []
    port_ddown_vet = []

    port_acc = 1.0
    port_acc_vet.append(1.0)
    cost_trans = 0.0006
    #cost_trans = 0.0005 + (0.004*step_eval/12)

    for lin in range(data_inicial, data_final, step_eval):
        cont = 0.0
        rent = 0.0
        for col in range(0, colunas):
            if (port.iat[lin-1, col] > 0 and fechamento.iat[lin-1, col]>0 and fechamento.iat[lin-1+step_eval, col]>0):
                rent = rent + (fechamento.iat[lin-1+step_eval,col]/fechamento.iat[lin-1,col]-1)*(port.iat[lin-1, col])
                cont = cont + port.iat[lin-1, col]
        if (cont == 0):
          return [1,1], [1,1], [0,0], 0, 0.000001
        port_acc = port_acc * (1.0 + rent/cont - cost_trans)
        port_chg_vet.append(rent/cont - cost_trans)
        port_acc_vet.append(port_acc)
        port_ddown_vet.append(port_acc/(np.max(port_acc_vet))-1)

    ret_aa = pow(port_acc, 12/(data_final-data_inicial))-1
    vol_aa = np.std(port_chg_vet)*((12/step_eval)**(1/2))
    return port_acc_vet, port_chg_vet, port_ddown_vet, ret_aa, vol_aa

#--------------------------

#Avaliação de um índice de referência.
#Parâmetros: (dataframe de referências, indice da referência desejada [0 - Ibovespa, 1 - IBX])
##Retorno: vetor com retorno acumulado, vetor com retornos periódicos, vetor com drawdown, retorno anualizado, volatilidade anualizada
def EvalRef(ref, ind):
    ref_acc_vet = []
    ref_chg_vet = []
    ref_ddown_vet = []

    ref_acc = 1.0
    ref_acc_vet.append(1.0)

    for lin in range(data_inicial, data_final, step_eval):
        rent = ref.iat[lin-1+step_eval,ind]/ref.iat[lin-1,ind]
        ref_acc = ref_acc * rent
        ref_chg_vet.append(rent-1)
        ref_acc_vet.append(ref_acc)
        ref_ddown_vet.append(ref_acc/(np.max(ref_acc_vet))-1)

    ret_aa = pow(ref_acc, 12/(data_final-data_inicial))-1
    vol_aa = np.std(ref_chg_vet)*((12/step_eval)**(1/2))
    return ref_acc_vet, ref_chg_vet, ref_ddown_vet, ret_aa, vol_aa

def calc_riskfolio_opt(ranked, otim_opt):
    hist_size = 24
    port = ranked.copy()

    if otim_opt not in ['RP', 'GMV', 'MDP']:
        print("\nInvalid Option.")
        return None

    print(f"\nCalculating {otim_opt} Portfolio...")

    successful_periods = 0
    failed_periods = []

    for lin in range(data_inicial + hist_size, data_final, 1):
        print("\r", lin, "/", data_final - 1, end=' ')
        port_comp = pd.DataFrame()
        for col in range(0, colunas):
            if port.iat[lin - 1, col] > 0:
                port_comp[port.columns[col]] = fechamento[port.columns[col]].iloc[lin - 1 - hist_size:lin - 1]

        port_comp.fillna(method='backfill', axis=0, inplace=True)
        port_comp_chg = port_comp.pct_change().dropna()

        if port_comp_chg.empty:
            print(f"No data to process for period {lin}.")
            continue

        rp_port = rp.Portfolio(returns=port_comp_chg)
        rp_port.assets_stats(method_cov='hist')

        if otim_opt == 'RP':
            w = rp_port.rp_optimization(rm='MV', rf=0, b=None)
        elif otim_opt == 'GMV':
            w = rp_port.optimization(model='Classic', rm='MV', obj='MinRisk')
        elif otim_opt == 'MDP':
            w = rp_port.optimization(model='Classic', rm='MV', obj='MaxDecorrelation')

        if w is not None:
            port_len = len(port_comp_chg.columns)
            for at in range(port_len):
                port.at[port.index[lin - 1], port_comp.columns[at]] = w['weights'].iat[at]
            successful_periods += 1
        else:
            failed_periods.append(lin)
            
    print("\nFinished calculating portfolio. Successful periods:", successful_periods)
    if failed_periods:
        print("Failed periods:", len(failed_periods), "at indices", failed_periods)

    port_final = port.copy()
    return port_final
