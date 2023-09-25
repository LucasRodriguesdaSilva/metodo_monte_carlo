import numpy as np


def escolha_aleatoria(qtd_projecoes, valores_simulados):
    projecoes_anuais = []
    for ano in range(qtd_projecoes):
        simulacao_ano = valores_simulados[ano]
        valor_escolhido = np.random.choice(simulacao_ano)
        projecoes_anuais.append(valor_escolhido)

    return projecoes_anuais


def projetar_dados(pesos, serie_historica, n_simulacoes, qtd_projecoes):
    """
        Projeta a simulação para uma serie historica e retorna o valores
        simulados com uma distribuição normal e valores escolhidos aleatoriamente
        para o tamanho da projeção requisitada.

        :param pesos: array
            Array contendo os pesos para cada ano projetado
        :param serie_historica: array
            Array contendo a serie historica dos dados
        :param n_simulacoes: int
        :param qtd_projecoes: int
            Quantidade de projeções no futuro
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
            distribuicao_normal_ponderada = np.random.normal(media, desvio_padrao) * pesos[ano_projetado]
            valor_atual = valor_atual * (1 + distribuicao_normal_ponderada)
            simulacao_atual.append(valor_atual)

        resultados_simulados.append(np.array(simulacao_atual))

    valores_projetados = escolha_aleatoria(qtd_projecoes=qtd_projecoes,valores_simulados=resultados_simulados)

    return valores_projetados, resultados_simulados


