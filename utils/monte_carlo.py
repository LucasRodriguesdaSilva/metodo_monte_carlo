import numpy as np
import random

def ultimo_ano_projetado(qtd_projecoes, valores_simulados):
    return valores_simulados[-1]

def projetar_dados(serie_historica, n_simulacoes, qtd_projecoes, is_premio_risco = False):
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

    for _ in range(n_simulacoes):
        simulacao_atual = []

        if isinstance(serie_historica[-1], list):
            valor_atual = serie_historica[-1][-1]
        else:
            valor_atual = serie_historica[-1]       
        for ano_projetado in range(qtd_projecoes):
            distribuicao_normal = np.random.normal(media, desvio_padrao)
            valor_atual = valor_atual * (1 + distribuicao_normal)

            simulacao_atual.append(valor_atual)

        resultados_simulados.append(np.array(simulacao_atual))

    valores_projetados = ultimo_ano_projetado(qtd_projecoes=qtd_projecoes,valores_simulados=resultados_simulados)

    return valores_projetados, resultados_simulados




