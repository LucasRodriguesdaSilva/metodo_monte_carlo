from datetime import timedelta
from datetime import datetime
import yfinance as yf 
import statsmodels.api as sm 
import numpy as np 



def calculoBeta(ativo, bench="^BVSP",dias_passados = 3652.5):
    """
        Calcula o Beta de um ativo apartir de x anos passados

        :param dias_passados: int quantidade de dias que já passaram
        :return: int o Beta calculado
    """

    data_agora = datetime.now()
    x_anos_atras = data_agora - timedelta(days= dias_passados)
    dados_cotacoes = yf.download(tickers=[ativo, bench],start=x_anos_atras, end=data_agora)['Adj Close']
    retornos_diarios = dados_cotacoes.pct_change().dropna()
    x = retornos_diarios[bench]
    y = retornos_diarios[ativo]
    x = sm.add_constant(x)
    calculo_beta = sm.OLS(y, x).fit() # Regressão linear
    # beta = np.full(11,calculo_beta.params[1])

    return calculo_beta.params[1]

def calculo_growth(inflacao, pib):
    """
        Calcular o Growth utilizando a inflação e o pib
        
        :param inflacao: int
        :param pib: int
        :return: int
    """
    return ((1 + inflacao) * (1 + pib)) - 1



