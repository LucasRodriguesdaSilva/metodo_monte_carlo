from bcb import sgs
from time import  sleep
import ipeadatapy
import numpy as np

def __get_code_pib():
    return 'PAN4_PIBPMG4'

def __get_code_ipca():
    return 'PRECOS12_IPCAG12'

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



def pegar_serie_ipca():
    code = __get_code_ipca()
    serie_ipca = ipeadatapy.timeseries(code)[f'VALUE ((% a.m.))']
    serie_ipca = serie_ipca.values
    serie_ipca = serie_ipca / 100
    
    return serie_ipca


def pegar_serie_pib():
    code = __get_code_pib()
    pib_var_trim = ipeadatapy.timeseries(code)[f'VALUE ((% a.a.))']
    pib_var_trim = pib_var_trim.values
    pib_var_trim = pib_var_trim / 100

    return pib_var_trim




pegar_serie_pib()