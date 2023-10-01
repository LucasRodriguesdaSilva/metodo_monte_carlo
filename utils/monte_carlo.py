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
    [simulacao 1:[2016:0.4,...,2023:0.21],...,simulacao n:[2016:0.2,...,2023:0.05]]
    """

    media = np.mean(serie_historica)
    desvio_padrao = np.std(serie_historica)

    resultados_simulados = []
    valor_anterior = serie_historica[-1][-1] if isinstance(serie_historica[-1], list) else serie_historica[-1]

    for _ in range(n_simulacoes):
        valores_aleatorios = np.random.normal(1 + media, desvio_padrao, size=qtd_projecoes)
        simulacao_atual = valor_anterior * np.cumprod(valores_aleatorios)
        resultados_simulados = np.vstack([resultados_simulados, simulacao_atual]) if _ > 0 else simulacao_atual

    

    # ultimo_ano = pegar_ultimo_ano(simulacoes=resultados_simulados,qtd_projecoes=qtd_projecoes)

    return resultados_simulados



def projetar_fcl(serie_fcf, dados_growth, n_simulacoes, qtd_projecoes):
    """
    Projeta dados para o Fluxo de caixa livre no futuro utilizando o Método de Monte Carlo.

    Parameters
    ----------
    serie_fcf : Pandas.series
        Série Histórica do fluxo de caixa livre.
    dados_growth: array
        Dados do Growth contendo a média e o desvio padrão para cada ano projetado
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

    resultados_simulados = []
    valor_anterior = serie_fcf[-1]

    for _ in range(n_simulacoes):
        simulacao_atual = []
        for ano in range(qtd_projecoes):
            media, desvio_padrao = dados_growth[ano]
            taxa_crescimento_ano = np.random.normal(media, desvio_padrao)
            resultado  = valor_anterior * (1 + taxa_crescimento_ano)
            simulacao_atual.append(resultado)

        resultados_simulados.append(simulacao_atual) 



        # taxa_crescimento = np.random.normal(1 + media, desvio_padrao, size=qtd_projecoes)
        # simulacao_atual = valor_anterior * np.cumprod(taxa_crescimento)
        # resultados_simulados = np.vstack([resultados_simulados, simulacao_atual]) if _ > 0 else simulacao_atual

    

    return np.array(resultados_simulados)


