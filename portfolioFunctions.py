import numpy as np
import pandas as pd
import riskfolio as rp
from dataManagement import fechamento
from dataManagement import data_inicial, data_final, step_eval, step_port, colunas

def SelPort1(port_ranked_1, param_1a, param_1b):
    """
    Seleciona ações para um portfólio com base em um único critério de ranking.

    Args:
    port_ranked_1 (DataFrame): DataFrame contendo rankings de ações.
    param_1a (int): Limite inferior do ranking para inclusão no portfólio.
    param_1b (int): Limite superior do ranking para inclusão no portfólio.

    Returns:
    DataFrame: Um DataFrame indicando quais ações foram selecionadas (1) ou não (0).
    """
    port_ranked_final = port_ranked_1.copy()
    port_ranked_final.loc[:, :] = 0

    for lin in range(data_inicial, data_final, step_port):
        for col in range(0, colunas):
            if param_1a <= port_ranked_1.iat[lin-1, col] <= param_1b:
                port_ranked_final.iat[lin-1, col] = 1

    return port_ranked_final

def SelPort2Par(ranked_1, param_1, ranked_2, param_2):
    """
    Seleciona ações para um portfólio com base em dois critérios de ranking.

    Args:
    ranked_1 (DataFrame): DataFrame com o primeiro ranking de ações.
    param_1 (int): Limite de seleção para o primeiro fator.
    ranked_2 (DataFrame): DataFrame com o segundo ranking de ações.
    param_2 (int): Limite de seleção para o segundo fator.

    Returns:
    DataFrame: DataFrame indicando a seleção de ações com base nos dois fatores.
    """
    port_ranked_final = ranked_1.copy()
    port_ranked_final.loc[:, :] = 0

    for lin in range(data_inicial, data_final, step_port):
        for col in range(0, colunas):
            if 1 <= ranked_1.iat[lin-1, col] <= param_1 and 1 <= ranked_2.iat[lin-1, col] <= param_2:
                port_ranked_final.iat[lin-1, col] = 1

    return port_ranked_final

def EvalPort(port, fechamento):
    """
    Avalia um portfólio dado, calculando retorno acumulado, retorno periódico, drawdown,
    retorno anualizado e volatilidade anualizada.

    Args:
    port (DataFrame): DataFrame do portfólio a ser avaliado.
    fechamento (DataFrame): DataFrame com os preços de fechamento das ações.

    Returns:
    tuple: Contém listas de retorno acumulado, retorno periódico, drawdown, e valores de
           retorno anualizado e volatilidade anualizada.
    """
    port_acc_vet = [1.0]  # Inicia com o capital inicial normalizado para 1
    port_chg_vet = []
    port_ddown_vet = []

    for lin in range(data_inicial, data_final, step_eval):
        total_return = sum((fechamento.iat[lin-1+step_eval, col] / fechamento.iat[lin-1, col] - 1) * port.iat[lin-1, col]
                           for col in range(colunas) if port.iat[lin-1, col] > 0 and fechamento.iat[lin-1, col] > 0)
        num_assets = port.iloc[lin-1].sum()
        net_return = total_return / num_assets - 0.0006 if num_assets > 0 else 0
        port_acc_vet.append(port_acc_vet[-1] * (1 + net_return))
        port_chg_vet.append(net_return)
        port_ddown_vet.append(min(port_acc_vet[-1] / max(port_acc_vet) - 1, 0))

    ret_aa = (port_acc_vet[-1] ** (12 / (data_final - data_inicial)) - 1)
    vol_aa = np.std(port_chg_vet) * (12 / step_eval) ** 0.5
    return port_acc_vet, port_chg_vet, port_ddown_vet, ret_aa, vol_aa

def EvalRef(ref, ind):
    """
    Avalia um índice de referência, calculando retorno acumulado, retornos periódicos, drawdown,
    retorno anualizado e volatilidade anualizada.

    Args:
    ref (DataFrame): DataFrame com os dados do índice.
    ind (int): Coluna do DataFrame que será avaliada.

    Returns:
    tuple: Contém listas de retorno acumulado, retornos periódicos, drawdown, e valores de
           retorno anualizado e volatilidade anualizada.
    """
    ref_acc_vet = [1.0]
    ref_chg_vet = []
    ref_ddown_vet = []

    for lin in range(data_inicial, data_final, step_eval):
        rent = ref.iat[lin-1+step_eval, ind] / ref.iat[lin-1, ind]
        ref_acc_vet.append(ref_acc_vet[-1] * rent)
        ref_chg_vet.append(rent - 1)
        ref_ddown_vet.append(ref_acc_vet[-1] / max(ref_acc_vet) - 1)

    ret_aa = ref_acc_vet[-1] ** (12 / (data_final - data_inicial)) - 1
    vol_aa = np.std(ref_chg_vet) * (12 / step_eval) ** 0.5
    return ref_acc_vet, ref_chg_vet, ref_ddown_vet, ret_aa, vol_aa

def calc_riskfolio_opt(ranked, otim_opt):
    """
    Calcula a otimização de portfólio com base em um critério de otimização específico.

    Args:
    ranked (DataFrame): DataFrame com o ranking das ações.
    otim_opt (str): Tipo de otimização a ser realizada ('RP', 'GMV' ou 'MDP').

    Returns:
    DataFrame: DataFrame do portfólio otimizado, ou None se a opção for inválida.
    """
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
            
    print(" Finished calculating portfolio. Successful periods:", successful_periods)
    if failed_periods:
        print("Failed periods:", len(failed_periods), "at indices", failed_periods)

    port_final = port.copy()
    return port_final