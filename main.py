from utils.valuation import Valuation
import numpy as np
# dividir pelo numero de ações

def main():

    anos_projetados = 11 # Quantidade de anos projetados no futuro
    n_simulacoes = 1000 # iterações no monte carlo
    ativo = 'GRND3.SA' # Ativo da empresa para pegar alguns dados.

    # Classe que faz os cálculos nescessários para o Fluxo de Caixa descontado
    VALUATION = Valuation(anos_projetados, n_simulacoes,ativo)
    FCD = VALUATION.projetar_fcd()


    # print(FCD)

    print('concluído !')

main()


