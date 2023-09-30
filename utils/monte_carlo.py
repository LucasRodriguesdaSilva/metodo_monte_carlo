import numpy as np
import random

def pegar_ultimo_ano(simulacoes, qtd_projecoes):
    """
    Seleciona somente os valores simulados do ultimo ano projetado.

    Parameters
    ----------
    simulacoes: array 
        Array contendo todas as simulações utilizando o Monte Carlo.
    qtd_projecoes: int 
        Quantidade de anos projetados.
    
    Returns
    -------
    ultimo_ano: array
        Array contendo o ultimo ano projetado.
    """
    ultimo_ano = []
    for simulacao in simulacoes:
        ultimo_ano.append(simulacao[qtd_projecoes - 1])

    return ultimo_ano


def projetar_dados(serie_historica, n_simulacoes, qtd_projecoes):
    """
    Projeta dados no futuro utilizando o Método de Monte Carlo.

    Parameters
    ----------
    serie_historica : Pandas.series
        Série Histórica dos dados.
    n_simulacoes: int
        Quantidade de simulações para o método.
    qtd_projecoes: int 
        Quantidade de anos projetados.

    Returns
    -------
    ultimo_ano: array
        n Simulações do ultimo ano projetado.
    resultados_simulados: array
        Simulação de todos os anos projetados.

    Examples
    --------
    >>> projetar({2016: 0.1, ..., 2023: 0.2})
    [array[0.4,...,0.21],...,array[0.2,...,0.05]]
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
    """
    Projeta dados para o Fluxo de caixa livre no futuro utilizando o Método de Monte Carlo.

    Parameters
    ----------
    serie_fcf : Pandas.series
        Série Histórica do fluxo de caixa livre.
    growth_projetado: array
        Growth do ultimo ano projetado. Utilizado para ser a taxa de crescimento do fluxo de caixa
    n_simulacoes: int
        Quantidade de simulações para o método.
    qtd_projecoes: int 
        Quantidade de anos projetados.

    Returns
    -------
    ultimo_ano: array
        n Simulações do ultimo ano projetado.
    resultados_simulados: array
        Simulação de todos os anos projetados.

    Examples
    --------
    >>> projetar({2016: 0.1, ..., 2023: 0.2})
    [array[0.4,...,0.21],...,array[0.2,...,0.05]]
    """

    media = np.mean(growth_projetado)
    desvio_padrao = np.std(growth_projetado)

    resultados_simulados = []
    valor_anterior = serie_fcf[-1]

    for _ in range(n_simulacoes):
        taxa_crescimento = np.random.normal(1 + media, desvio_padrao, size=qtd_projecoes)
        simulacao_atual = valor_anterior * np.cumprod(taxa_crescimento)
        resultados_simulados = np.vstack([resultados_simulados, simulacao_atual]) if _ > 0 else simulacao_atual

    
    ultimo_ano = pegar_ultimo_ano(simulacoes=resultados_simulados,qtd_projecoes=qtd_projecoes)

    return ultimo_ano, resultados_simulados


