import matplotlib.pyplot as plt
import os

import numpy as np


def __pegar_caminho_abs():
    return os.path.dirname(os.path.abspath(__file__))

def __gerar_caminho_output(nome_arquivo, extensao='png'):
    arq = f'{nome_arquivo}.{extensao}'
    dir_name = __pegar_caminho_abs()
    output = os.path.join(dir_name, 'output', arq)
    return output


def __gerar_lista_anos(qtd_projecoes):
    return np.arange(0, qtd_projecoes, step=1)



def plotar_linhas(simulacoes,qtd_projecoes, titulo):

    for ano in range(qtd_projecoes):
        plt.plot(simulacoes[ano], label=f'ano: {ano + 1}')

    plt.xlabel('Valores Simulados')
    plt.ylabel(titulo)
    plt.title(f'Distribuição dos Valores Simulados - {titulo}')
    plt.legend()
    plt.grid(True)
    saida = __gerar_caminho_output(f'histograma_{titulo}')
    plt.xticks(__gerar_lista_anos(qtd_projecoes=qtd_projecoes))
    plt.savefig(saida)
    plt.close()

"""
def plotar_hist(simulacoes, qtd_projecoes, titulo:

    Gera, salva e exibe um histograma dos valores simulados.

    :param simulacoes: Array numpy com os valores simulados.
    :param qtd_projecoes: Int correspondente a quantidade de anos projetados.
    :param titulo: string referente ao titulo do cálculo.
    :param bins: int Número de intervalos no histograma.
    :param salvar: boolean Salvar ou não a gráfico.
    :return: null



    for i, array in enumerate(simulacoes): 
        plt.figure(i)
        plt.hist(array, bins='auto')

    # anos = __gerar_lista_anos(qtd_projecoes)
    plt.xlabel('Valores Simulados')
    plt.ylabel('Frequência')
    plt.title(f'Distribuição dos Valores Simulados - {titulo}')

    saida = __gerar_caminho_output(f'histograma_{titulo}')
    plt.savefig(saida)
    plt.close()
"""

