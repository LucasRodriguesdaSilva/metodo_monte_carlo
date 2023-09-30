from utils.valuation import Valuation


def main():

    qtd_projecoes = 10
    n_simulacoes = 1000
    ativo = 'GRND3.SA'

    VALUATION = Valuation(qtd_projecoes, n_simulacoes,ativo)
    FCD = VALUATION.projetar_fcd()

    print('concluído !')

main()


