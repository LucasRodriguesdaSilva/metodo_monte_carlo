from bcb import sgs
from time import  sleep
import ipeadatapy
import numpy as np
from utils import utils as ut
from utils import calculos
import pandas as pd

def __get_code_pib():
    return 'PAN4_PIBPMG4'

def __get_code_ipca():
    return 'PRECOS12_IPCAG12'

def __get_code_di():
    return 'BMF12_SWAPDI36012' # Taxa referencial - swaps - DI x pré-fixada - 360 dias - média do período

def __Get_code_cds():
    return 'JPM366_EMBI366'

def porcentagem(serie):
    serie = [[valor / 100 for valor in lista] for lista in serie]
    return serie

def sgs_get(codigo):
    continua = True
    while continua:
        try: 
            serie = sgs.get(codigo)
            continua = False
        except:
            sleep(1)

    return serie


def pegar_serie_selic():

    selic = sgs_get(11) # SELIC

    ut.plotar_serie_historia(serie=selic,titulo='SELIC')

    selic = selic.values.tolist()
    selic = porcentagem(serie=selic)

    return selic



def pegar_serie_ipca():
    code = __get_code_ipca()
    serie_ipca = ipeadatapy.timeseries(code)[f'VALUE ((% a.m.))']

    ut.plotar_serie_historia(serie=serie_ipca,titulo='IPCA')

    serie_ipca = serie_ipca.values
    serie_ipca = serie_ipca / 100
    
    return serie_ipca


def pegar_serie_pib():
    code = __get_code_pib()
    pib_var_trim = ipeadatapy.timeseries(code)[f'VALUE ((% a.a.))']

    ut.plotar_serie_historia(serie=pib_var_trim,titulo='PIB Brasileiro')

    pib_var_trim = pib_var_trim.values
    pib_var_trim = pib_var_trim / 100

    return pib_var_trim


def pegar_serie_di():
    code = __get_code_di()
    serie_di = ipeadatapy.timeseries(code)[f'VALUE ((% a.a.))']

    ut.plotar_serie_historia(serie=serie_di,titulo='DI x pré-fixada')

    serie_di = serie_di.values
    serie_di = serie_di / 100

    return serie_di


def pegar_serie_cds():
    code = __Get_code_cds()
    serie_cds = ipeadatapy.timeseries(code)['VALUE (-)']
    serie_cds = serie_cds.pct_change().dropna().resample('Y').mean().to_frame()

    ut.plotar_serie_historia(serie=serie_cds,titulo='Var. CDS Anual')
    serie_cds = serie_cds.values
    
    novo_array = []
    for cds in serie_cds:
        novo_array.append(cds[0])


    return novo_array

# Alterar depois 
# Calculo do PL / LPA retirado do site da statuinvesti 
def pegar_serie_cje():
    """
        Calculo do PL / LPA 
    """
    cje = calculos.calculo_pl_lpa_json()

    ut.plotar_serie_historia(serie=cje,titulo='var. da Cobertura de Juros da Empresa')

    cje = cje.values
    cje = cje / 100

    return cje


def pegar_serie_fcl():
    """
        indices historicos retirados do site da 
        https://statusinvest.com.br/acoes/grnd3 para o ativo da Grendene.

        Data da última atualização: 28/09/2023
    """
    serie = [
        {
            'year': 2022,
            'value': 407.69
        },
        {
            'year': 2021,
            'value': 690.17
        },
        {
            'year': 2020,
            'value': 319.29
        },
        {
            'year': 2019,
            'value': 368.17
        },
        {
            'year': 2018,
            'value': 335.97
        },
        {
            'year': 2017,
            'value': 400.26
        },
        {
            'year': 2016,
            'value': 391.73
        },
        {
            'year': 2015,
            'value': 244.13
        },
        {
            'year': 2014,
            'value': 176.94
        },
        {
            'year': 2013,
            'value': 392.90
        },
        {
            'year': 2012,
            'value': 214.99
        },
        {
            'year': 2011,
            'value': 283.08
        },
        {
            'year': 2010,
            'value': 83.42
        },
        {
            'year': 2009,
            'value': 210.81
        },
        {
            'year': 2008,
            'value': 172.94
        },
        
    ]

    df_pl = pd.DataFrame(serie)
    serie_fcl = df_pl.set_index('year')['value']

    serie_fcl = serie_fcl.values

    return serie_fcl
