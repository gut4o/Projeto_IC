import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error

class Analise_Fluxos:

    def __init__(self, df_1, df_2, delimiter_1=',', delimiter_2=';', decimal_1='.', decimal_2='.'): # inicializando os df
        self.df1 = pd.read_csv(df_1, delimiter=delimiter_1, decimal=decimal_1)
        #self.df1['EXP_N'] = self.df1['EXP_NS'] - self.df1['EXP_NEN'] ----- para fazer a aproximação do fluxo N UNICAMP
        #self.df1['Xingu_Total'] = self.df1['XESTR_MW'] + self.df1['XTRIO_MW'] ----- para obter Xingu Total UNICAMP
        self.df2 = pd.read_csv(df_2, delimiter=delimiter_2, decimal=decimal_2)
        #self.dfaux = pd.read_csv(df_aux, delimiter=delimiter_aux, decimal=decimal_aux) ----- para fazer a aproximação do fluxo NEN NORUS
        #self.dfaux['EXP_NEN'] = - self.df2['MW'] + self.dfaux['MW']
        self._sincronizar_dados()

    def _sincronizar_dados(self): # deixando os df com a mesma quantidade de linhas
        min_linhas = min(len(self.df1), len(self.df2))
        self.df1 = self.df1.head(min_linhas)
        self.df2 = self.df2.head(min_linhas)

    def correl(self, col_1, col_2): # calculando o índice de correlação
        correlacao = self.df1[col_1].corr(self.df2[col_2])
        print('A correlação entre os fluxos de potências Ativas é:', correlacao)
        return correlacao

    def scatter_plot(self, col_1, col_2):
        sns.regplot(x=self.df1[col_1], y=self.df2[col_2], scatter=True, ci=None, line_kws={'color':'red'}, scatter_kws={'s': 20}, marker='x')
        plt.xlabel('UNICAMP')
        plt.ylabel('NORUS')
        plt.title('Dispersão Xingu T.Rio (MW)')
        plt.show()

    def erro(self, col_1, col_2):
        rmse = mean_squared_error(self.df1[col_1], self.df2[col_2], squared=False)
        print("O RMSE é:", rmse)
        return rmse
    
    def time_series(self, col_1, col_2):
        fig = plt.figure(figsize=(20, 8))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twiny()

        # Add some extra space for the second axis at the bottom
        fig.subplots_adjust(bottom=0.2)

        ax1.plot(self.df1[col_1], label='UNICAMP', c='r') # UNICAMP
        ax1.plot(self.df2[col_2], label='NORUS', c='g') # NORUS
        ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax1.set_yticks(np.arange(0, 4500, 500))
        ax1.set_xticks(np.arange(0, 1500, 50))
        ax1.set_xlim(0, 1345)
        ax1.set_ylabel("P (MW)", fontsize=12, weight='bold')
        ax1.set_xlabel("# PO", fontsize=12, weight='bold')
        ax1.legend()

        def tick_function(X):
            return [f"{z}" for z in X]

        # AX 2
        ax2.xaxis.set_ticks_position("bottom")
        ax2.xaxis.set_label_position("bottom")
        ax2.spines["bottom"].set_position(("axes", -0.1))
        ax2.set_frame_on(True)
        ax2.patch.set_visible(False)
        new_tick_locations = np.arange(1, 29) 
        ax2.set_xticks(new_tick_locations)
        ax2.set_xticklabels(tick_function(new_tick_locations))
        ax2.set_xlim(1, 29)
        ax2.set_xlabel("Dia", fontsize=12, weight='bold')

        plt.tight_layout()
        plt.show()

# Explicitando os dfs a serem utilizados:

df_1 = 'unicamp_DC.csv'
df_2 = 'fluxo_intercambio_Fxgtr.csv'

# Criando uma instância da classe:

analise = Analise_Fluxos(df_1, df_2)

# Ações a serem executadas:

analise.correl('XTRIO_MW', 'MW')
analise.scatter_plot('XTRIO_MW', 'MW')
analise.erro('XTRIO_MW', 'MW')
analise.time_series('XTRIO_MW', 'MW')