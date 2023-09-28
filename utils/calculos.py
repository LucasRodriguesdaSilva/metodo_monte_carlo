from datetime import timedelta
from datetime import datetime
import yfinance as yf 
import statsmodels.api as sm 
import numpy as np 
import time
import json
import os 
import pandas as pd

def __pegar_caminho_abs():
    return os.path.dirname(os.path.abspath(__file__))


def calculo_beta(ativo, bench="^BVSP",dias_passados = 3652.5):
    """
        Calcula o Beta de um ativo apartir de x anos passados

        :param ativo: string nome do Ativo
        :param bench: string
        :param dias_passados: int quantidade de dias que já passaram padrão 10 anos
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


def calculo_wacc(ke, valor_equity, kd, divida_bruta):
    wacc = ((ke * valor_equity) + (kd * divida_bruta)) / (valor_equity + divida_bruta)
    return wacc


def calculo_ke(beta, premio_risco, di, cds):
    di = np.array(di)
    cds = np.array(cds)

    taxa_livre_risco = di - cds
    ke = taxa_livre_risco + (beta * premio_risco)
    return ke

def pegar_divida_equity():
    """
        Esses dados foram obtidos por meio do código disponibilizado no github https://github.com/lfreneda/statusinvest com licensa MIT
        
    """
    arq = os.path.join(__pegar_caminho_abs(),'dados','info.json')

    with open(arq, 'r') as f:
        dados = json.load(f)

    ativos = dados['Ativos']
    divida = dados['Divida bruta']
    equity = dados['Valor de mercado']

    return ativos, divida, equity



def calcular_kd(inflacao, cje_projetado):
    kd = []
    for ano in range(len(inflacao)):
        r = inflacao[ano] + cje_projetado[ano]
        kd.append(r)

    return kd

def calculo_pl_lpa_json():
    """
        Calculo do PL/LPA, indices historicos retirados do site da 
        https://statusinvest.com.br/acoes/grnd3 para o ativo da Grendene.

        Esses dados foram obtidos por meio do código disponibilizado no github https://github.com/lfreneda/statusinvest com licensa MIT
    """



    arq = os.path.join(__pegar_caminho_abs(),'dados','dados_historicos.json')

    with open(arq, 'r') as f:
        dados = json.load(f)

    pl = dados['P/L']['series']
    lpa = dados['LPA']['series']

    df1 = pd.DataFrame(pl)
    df2 = pd.DataFrame(lpa)
    df1['value'] = df1['value'].fillna(1e-10)
    df2['value'] = df2['value'].fillna(1e-10)
    series1 = df1.set_index('year')['value']
    series2 = df2.set_index('year')['value']

    s3 = series1 / series2

    return s3

