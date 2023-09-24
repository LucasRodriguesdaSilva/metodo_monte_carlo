from bcb import sgs
from time import  sleep

def pegar_serie_ipca():
    try:
        serie_ipca = sgs.get(433)
    except:
        sleep(1)
        serie_ipca = sgs.get(433)

    serie_ipca = serie_ipca.values.tolist()

    serie_ipca = [[valor / 100 for valor in lista] for lista in serie_ipca]

    return serie_ipca