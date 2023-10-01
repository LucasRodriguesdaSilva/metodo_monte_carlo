from utils.valuation import Valuation

# [ ] Salvar dados em um arquivo .txt?

def main():

    qtd_projecoes = 4
    n_simulacoes = 10
    ativo = 'GRND3.SA'

    VALUATION = Valuation(qtd_projecoes, n_simulacoes,ativo)
    FCD = VALUATION.projetar_fcd()

    print('concluído !')

main()


