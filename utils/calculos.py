import datetime as dt
from datetime import timedelta
import yfinance as yf 
import statsmodels.api as sm 
import numpy as np 
import time
import json
import os 
import pandas as pd
import pyettj.ettj as ettj
import matplotlib.pyplot as plt

def __pegar_caminho_abs():
    return os.path.dirname(os.path.abspath(__file__))


def calculo_fcd(fcff_projetado, wacc_projetado):
    resultado = np.zeros_like(fcff_projetado)
    for ano in range(fcff_projetado.shape[1]):
        n = ano + 1
        resultado[:, ano] = fcff_projetado[:, ano] / ((1 + wacc_projetado[:, ano]) ** n)

    fcd_por_simulacao = np.sum(resultado, axis=1)

    return fcd_por_simulacao
    


def calculo_beta(ativo, bench="^BVSP",dias_passados = 3652.5):
    """
        Calcula o Beta de um ativo apartir de x anos passados

        :param ativo: string nome do Ativo
        :param bench: string
        :param dias_passados: int quantidade de dias que já passaram padrão 10 anos
        :return: int o Beta calculado
    """

    data_agora = dt.datetime.now()
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

    taxa_livre_risco = di - cds
    ke = taxa_livre_risco + (beta * premio_risco)
    return ke


# def calculo_fcd(wacc, fcl):



def pegar_divida_equity():
    """
        Valores retirados do site da 
        https://statusinvest.com.br/acoes/grnd3 para o ativo da Grendene.
        
        Data da última atualização: 28/09/2023
        
    """

    papeis = 902160000

    divida = 89361000 # Reais
    equity = 5927191200

    return papeis, divida, equity



def calcular_kd(inflacao, cje_projetado, n_simulacoes):
    kd = []
    for simulacao in range(n_simulacoes):
        r = inflacao[simulacao] + cje_projetado[simulacao]
        kd.append(r)

    return kd

def calculo_media_std_por_ano(growth):
    """
    Calcula a média e o desvio padrão por ano 

    Parameters
    ----------
    growth: np.array 
        Array contendo o growth simulado
    
    Returns
    -------
    resultado: np.array
        Array contendo a média e o desvio padrão para cada ano projetado no formato 
        [[media, desvio],...[media, desvio]]
    """
    medias = np.mean(growth, axis=0)
    desvios_padrao = np.std(growth, axis=0)
    resultado = np.vstack((medias, desvios_padrao))
    resultado = resultado.T
    return resultado


def calcular_di(qtd_anos_projetados):
    if(qtd_anos_projetados > 36):
        qtd_anos_projetados = 36
    elif (qtd_anos_projetados < 4):
        qtd_anos_projetados = 4


    dias_projetados = int(qtd_anos_projetados+1 * 365)
    anos = [x for x in range(365,dias_projetados, 365)]

    ano_atual_di = dt.date.today().year
    dados_ettj = ettj.get_ettj(data=ano_atual_di, curva="PRE")
    dias_corridos_di = dados_ettj['Dias Corridos'].unique()

    fig = ettj.plot_ettj(dados_ettj, 'DI x pré 360(1)', ano_atual_di)

    # Salvando o gráfico em um arquivo
    plt.savefig('DI.png')

    dias_corridos_anuais_di = [] # lista vazia para guardar os dias corridos de ano em ano
    for ano in anos: # para cada ano na lista
        indice = np.where(np.abs(dias_corridos_di - ano) == np.min(np.abs(dias_corridos_di - ano))) # encontra o índice do valor mais próximo de ano no array
        dias_corridos_anuais_di.append(dias_corridos_di[indice][0]) # adiciona o valor correspondente na lista
    
    coluna_ettj = "DI x pré 360(1)" # nome da coluna que você quer pegar
    resultado_di = dados_ettj.loc[dados_ettj['Dias Corridos'].isin(dias_corridos_anuais_di), coluna_ettj] # filtrando o DataFrame pelos dias corridos e pela coluna
    resultado_di /= 100

    return resultado_di.values
    


def calculo_pl_lpa_json():
    """
        Calculo do PL/LPA, indices historicos retirados do site da 
        https://statusinvest.com.br/acoes/grnd3 para o ativo da Grendene.

        Data da última atualização: 28/09/2023
    """

    pl = [
            {
                "year": 2023,
                "value": 10.4915
            },
            {
                "year": 2022,
                "value": 9.5771
            },
            {
                "year": 2021,
                "value": 12.9844
            },
            {
                "year": 2020,
                "value": 18.6574
            },
            {
                "year": 2019,
                "value": 22.3829
            },
            {
                "year": 2018,
                "value": 12.6342
            },
            {
                "year": 2017,
                "value": 12.9446
            },
            {
                "year": 2016,
                "value": 8.3321
            },
            {
                "year": 2015,
                "value": 9.1871
            },
            {
                "year": 2014,
                "value": 9.3852
            },
            {
                "year": 2013,
                "value": 12.5479
            },
            {
                "year": 2012,
                "value": 11.5591
            },
            {
                "year": 2011,
                "value": 7.571
            },
            {
                "year": 2010,
                "value": 1e-10
            },
            {
                "year": 2009,
                "value": 1e-10
            },
            {
                "year": 2008,
                "value": 1e-10
            }
        ]
    lpa = [
            {
                "year": 2023,
                "value": 0.6176
            },
            {
                "year": 2022,
                "value": 0.6296
            },
            {
                "year": 2021,
                "value": 0.6662
            },
            {
                "year": 2020,
                "value": 0.4492
            },
            {
                "year": 2019,
                "value": 0.5486
            },
            {
                "year": 2018,
                "value": 0.649
            },
            {
                "year": 2017,
                "value": 2.1978
            },
            {
                "year": 2016,
                "value": 2.1099
            },
            {
                "year": 2015,
                "value": 1.833
            },
            {
                "year": 2014,
                "value": 1.6302
            },
            {
                "year": 2013,
                "value": 1.4417
            },
            {
                "year": 2012,
                "value": 1.4266
            },
            {
                "year": 2011,
                "value": 1.0157
            },
            {
                "year": 2010,
                "value": 1e-10
            },
            {
                "year": 2009,
                "value": 1e-10
            },
            {
                "year": 2008,
                "value": 1e-10
            }
        ]

    df_pl = pd.DataFrame(pl)
    df_lpa = pd.DataFrame(lpa)
    series_pl = df_pl.set_index('year')['value']
    series_lpa = df_lpa.set_index('year')['value']

    s3 = series_pl / series_lpa

    return s3

