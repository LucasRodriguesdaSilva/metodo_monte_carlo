import matplotlib.pyplot as plt
import os
import datetime
import numpy as np


def __pegar_caminho_abs():
    return os.path.dirname(os.path.abspath(__file__))

def __gerar_caminho_output(nome_arquivo, extensao='png'):
    arq = f'{nome_arquivo}.{extensao}'
    dir_name = __pegar_caminho_abs()
    output = os.path.join(dir_name, 'output', arq)
    return output

def get_ultimo_ano(qtd_projecoes):
    anos = __gerar_lista_anos(qtd_projecoes)
    return anos[-1]

def __gerar_lista_anos(qtd_projecoes):

    ano_atual = datetime.datetime.now().year

    ano_atual += 1
    anos_futuros = [ano_atual + i for i in range(qtd_projecoes)]
    return anos_futuros



def plotar_linhas(simulacoes,qtd_projecoes, titulo, n_simulacoes):
    plt.figure(figsize=(20, 8))
    for ano in range(n_simulacoes):
        plt.plot(simulacoes[ano])

    plt.xlabel('Valores Simulados')
    plt.ylabel(titulo)
    plt.title(titulo)
    # plt.legend()
    plt.grid(True)
    saida = __gerar_caminho_output(f'simulacao - {n_simulacoes} - {qtd_projecoes} - {titulo}')
    anos_futuros = __gerar_lista_anos(qtd_projecoes=qtd_projecoes)
    plt.xticks(range(qtd_projecoes), anos_futuros)
    plt.savefig(saida)
    plt.close()



def plotar_serie_historia(serie, titulo):
    plt.figure(figsize=(20, 8))
    # Plota o gráfico de linha com os dados
    plt.plot(serie)
    plt.title(titulo)
    plt.xlabel("Anos")
    plt.ylabel("Taxa (%)")
    plt.grid(True)
    saida = __gerar_caminho_output(f'serie - {titulo}')
    plt.savefig(saida)
    plt.close()


def plotar_hist_valuation(simulacoes,qtd_papeis, titulo):
    """
    Gera, salva e exibe um histograma dos valores simulados.

    :param simulacoes: Array numpy com os valores simulados.
    :param qtd_projecoes: Int correspondente a quantidade de anos projetados.
    :param titulo: string referente ao titulo do cálculo.
    :param bins: int Número de intervalos no histograma.
    :param salvar: boolean Salvar ou não a gráfico.
    :return: null
    """
    plt.figure(figsize=(14, 8))

    plt.hist(simulacoes, edgecolor='black', bins=20)
   

    # anos = __gerar_lista_anos(qtd_projecoes)
    plt.xlabel('Valuations')
    plt.ylabel('Frequência')
    plt.title(titulo)

    saida = __gerar_caminho_output(f'histograma_{titulo}')
    plt.savefig(saida)
    # plt.show()

    preco_atual = round(np.mean(simulacoes),2)
    # fcd_sum = np.sum(simulacoes)
    # preco_atual = (fcd_sum * (10**6) # Em milhoes) / qtd_papeis
    # print(preco_atual)

    plt.axvline(preco_atual,color='r', linestyle='dashed',linewidth=2)

    saida = __gerar_caminho_output(f'histograma_com_preco_atual')
    plt.savefig(saida)
    plt.close()

    plt.figure(figsize=(14, 8))
    x_values = (simulacoes - preco_atual) / preco_atual

    plt.hist(x_values, edgecolor='black', bins=40)
   

    # anos = __gerar_lista_anos(qtd_projecoes)
    plt.xlabel('Valuations')
    plt.ylabel('Frequência')
    plt.title(titulo)
    plt.axvline(0, color='r', linestyle='dashed', linewidth=2)

    saida = __gerar_caminho_output(f'histograma_em_x')

    plt.savefig(saida)
    plt.close()

