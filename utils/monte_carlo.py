import numpy as np
import random

def pegar_ultimo_ano(simulacoes, qtd_projecoes):
    ultimo_ano = []
    for simulacao in simulacoes:
        ultimo_ano.append(simulacao[qtd_projecoes - 1])

    return ultimo_ano


def projetar_dados(serie_historica, n_simulacoes, qtd_projecoes):
    """
        Projeta a simulação para uma serie historica e retorna o valores
        simulados com uma distribuição normal e valores escolhidos aleatoriamente
        para o tamanho da projeção requisitada.

        :param peso: float
            Um valor inicial que com o tempo ira aumentar ou diminuir.
        :param serie_historica: array
            Array contendo a serie historica dos dados
        :param n_simulacoes: int
        :param qtd_projecoes: int
            Quantidade de projeções no futuro
        :param is_premio_risco: boolean
            Flag para calcular com base na selic
        :return: list
            Retorna uma lista, contendo os valores projetado e os valores simulados
    """

    media = np.mean(serie_historica)
    desvio_padrao = np.std(serie_historica)

    resultados_simulados = []
    valor_anterior = serie_historica[-1][-1] if isinstance(serie_historica[-1], list) else serie_historica[-1]

    for _ in range(n_simulacoes):
        valores_aleatorios = np.random.normal(1 + media, desvio_padrao, size=qtd_projecoes)
        simulacao_atual = valor_anterior * np.cumprod(valores_aleatorios)
        resultados_simulados = np.vstack([resultados_simulados, simulacao_atual]) if _ > 0 else simulacao_atual

    

    ultimo_ano = pegar_ultimo_ano(simulacoes=resultados_simulados,qtd_projecoes=qtd_projecoes)

    return ultimo_ano, resultados_simulados



def projetar_fcl(serie_fcf, growth_projetado, n_simulacoes, qtd_projecoes):

    media = np.mean(growth_projetado)
    desvio_padrao = np.std(growth_projetado)

    resultados_simulados = []
    # fcf_simulado = []
    valor_anterior = serie_fcf[-1]

    for _ in range(n_simulacoes):
        taxa_crescimento = np.random.normal(1 + media, desvio_padrao, size=qtd_projecoes)
        simulacao_atual = valor_anterior * np.cumprod(taxa_crescimento)
        resultados_simulados = np.vstack([resultados_simulados, simulacao_atual]) if _ > 0 else simulacao_atual

    
    ultimo_ano = pegar_ultimo_ano(simulacoes=resultados_simulados,qtd_projecoes=qtd_projecoes)

    return ultimo_ano, resultados_simulados


