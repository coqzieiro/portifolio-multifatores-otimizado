import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np
import pandas as pd
import riskfolio as rp
import statsmodels
import portfolio_functions

#Composição do índice IBX
comp_indice=pd.read_excel('dados-economatica/Dados-Comp-IBRX.xlsx', engine='openpyxl')
comp_indice.set_index(keys = 'Data', inplace = True)

#Preços de fechamento dos ativos
fechamento=pd.read_excel('dados-economatica/Dados-Fechamento.xlsx', engine='openpyxl')
fechamento.set_index(keys = 'Data', inplace = True)

#Indices de referência (Ibov, IBX, SELIC...)
referencias=pd.read_excel('dados-economatica/Dados-Base.xlsx', engine='openpyxl')
referencias.set_index(keys = 'Data', inplace = True)

# Cálculo de rentabilidade / volatilidade / drawdown da SELIC
ref_acc_vet, ref_chg_vet, ref_ddown_vet, ret_aa_ref, vol_aa_ref = EvalRef(referencias, 2)
print("Ref SELIC:\nRet. Acc.:",round(ref_acc_vet[-1]*100-100, 2) ,"% Ret. Anual.:",round(ret_aa_ref*100,2), "% Vol.:", round(vol_aa_ref*100,2), "% Ret/Vol:", round(ret_aa_ref/vol_aa_ref, 2), "DDown:", round(np.min(ref_ddown_vet)*100,2), "%")

# Cálculo de rentabilidade / volatilidade / drawdown do IBX
ref_acc_vet, ref_chg_vet, ref_ddown_vet, ret_aa_ref, vol_aa_ref = EvalRef(referencias, 1)
print("Ref IBX:\nRet. Acc.:",round(ref_acc_vet[-1]*100-100, 2) ,"% Ret. Anual.:",round(ret_aa_ref*100,2), "% Vol.:", round(vol_aa_ref*100,2), "% Ret/Vol:", round(ret_aa_ref/vol_aa_ref, 2), "DDown:", round(np.min(ref_ddown_vet)*100,2), "%")

# Cálculo de rentabilidade / volatilidade / drawdown do Ibovespa
ref_acc_vet, ref_chg_vet, ref_ddown_vet, ret_aa_ref, vol_aa_ref = EvalRef(referencias, 0)
print("Ref Ibov:\nRet. Acc.:",round(ref_acc_vet[-1]*100-100, 2) ,"% Ret. Anual.:",round(ret_aa_ref*100,2), "% Vol.:", round(vol_aa_ref*100,2), "% Ret/Vol:", round(ret_aa_ref/vol_aa_ref, 2), "DDown:", round(np.min(ref_ddown_vet)*100,2), "%")

# Avaliação de um portfólio 1
ranked1 = SelPort1(ranked_Vol, 0, 30)
port_acc_vet1, port_chg_vet1, port_ddown_vet1, ret_aa1, vol_aa1 = EvalPort(ranked1, fechamento)
print("Port Fator Vol:\nRet. Acc.:",round(port_acc_vet1[-1]*100-100, 2) ,"% Ret. Anual.:",round(ret_aa1*100,2), "% Vol.:", round(vol_aa1*100,2), "% Ret/Vol:", round(ret_aa1/vol_aa1, 2), "DDown:", round(np.min(port_ddown_vet1)*100,2), "%")

# Avaliação de um portfólio 2
ranked2 = SelPort1(ranked_ROIC, 0, 30)
port_acc_vet2, port_chg_vet2, port_ddown_vet2, ret_aa2, vol_aa2 = EvalPort(ranked2, fechamento)
print("Port Fator ROIC:\nRet. Acc.:",round(port_acc_vet2[-1]*100-100, 2) ,"% Ret. Anual.:",round(ret_aa2*100,2), "% Vol.:", round(vol_aa2*100,2), "% Ret/Vol:", round(ret_aa2/vol_aa2, 2), "DDown:", round(np.min(port_ddown_vet2)*100,2), "%")

ranked2

# Avaliação de um portfólio 3
ranked3 = SelPort2Par(ranked_Vol, 30, ranked_ROIC, 30)
port_acc_vet3, port_chg_vet3, port_ddown_vet3, ret_aa3, vol_aa3 = EvalPort(ranked3, fechamento)
print("\nPort Fator Vol & ROIC:\nRet. Acc.:",round(port_acc_vet3[-1]*100-100, 2) ,"% Ret. Anual.:",round(ret_aa3*100,2), "% Vol.:", round(vol_aa3*100,2), "% Ret/Vol:", round(ret_aa3/vol_aa3, 2), "DDown:", round(np.min(port_ddown_vet3)*100,2), "%")
beta, alpha = np.polyfit(ref_chg_vet, port_chg_vet3, 1)
print("Port Alpha:",round(alpha*(12/step_eval)*100,2),"%, Beta:", round(beta,2))

# Portifólio usando o critério Standard Risk Parity
port_riskfolio = calc_riskfolio_opt(ranked3, 'RP')
port_acc_vet4, port_chg_vet4, port_ddown_vet4, ret_aa4, vol_aa4 = EvalPort(port_riskfolio, fechamento)
print("\nPort RP:\nRet. Acc.:",round(port_acc_vet4[-1]*100-100, 2) ,"% Ret. Anual.:",round(ret_aa4*100,2), "% Vol.:", round(vol_aa4*100,2), "% Ret/Vol:", round(ret_aa4/vol_aa4, 2), "DDown:", round(np.min(port_ddown_vet4)*100,2), "%")
beta, alpha = np.polyfit(ref_chg_vet, port_chg_vet4, 1)
print("Port Alpha:",round(alpha*(12/step_eval)*100,2),"%, Beta:", round(beta,2))

# Portifólio usando o critério Minimun Variance
port_riskfolio = calc_riskfolio_opt(ranked3, 'GMV')
port_acc_vet5, port_chg_vet5, port_ddown_vet5, ret_aa5, vol_aa5 = EvalPort(port_riskfolio, fechamento)
print("\nPort GMV:\nRet. Acc.:",round(port_acc_vet5[-1]*100-100, 2) ,"% Ret. Anual.:",round(ret_aa5*100,2), "% Vol.:", round(vol_aa5*100,2), "% Ret/Vol:", round(ret_aa5/vol_aa5, 2), "DDown:", round(np.min(port_ddown_vet5)*100,2), "%")
beta, alpha = np.polyfit(ref_chg_vet, port_chg_vet5, 1)
print("Port Alpha:",round(alpha*(12/step_eval)*100,2),"%, Beta:", round(beta,2))

# Portifólio usando o critério Maximun Decorrelation
port_riskfolio = calc_riskfolio_opt(ranked3, 'MDP')
port_acc_vet6, port_chg_vet6, port_ddown_vet6, ret_aa6, vol_aa6 = EvalPort(port_riskfolio, fechamento)
print("\nPort MDP:\nRet. Acc.:",round(port_acc_vet6[-1]*100-100, 2) ,"% Ret. Anual.:",round(ret_aa6*100,2), "% Vol.:", round(vol_aa6*100,2), "% Ret/Vol:", round(ret_aa6/vol_aa6, 2), "DDown:", round(np.min(port_ddown_vet6)*100,2), "%")
beta, alpha = np.polyfit(ref_chg_vet, port_chg_vet6, 1)
print("Port Alpha:",round(alpha*(12/step_eval)*100,2),"%, Beta:", round(beta,2))