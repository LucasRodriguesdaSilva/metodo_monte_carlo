from utils import utils as ut
from utils import monte_carlo
from utils import series_historicas as sh

class Valuation:

    def projetar_ipca(self, pesos):
        serie_historica = sh.pegar_serie_ipca()
        valores_projetados, simulacao = monte_carlo.projetar_dados(pesos=pesos, n_simulacoes=self.n_simulacoes,
                                                       qtd_projecoes=self.qtd_projecoes,
                                                       serie_historica=serie_historica)

        ut.plotar_linhas(simulacoes=simulacao, qtd_projecoes=self.qtd_projecoes, titulo='Var. do IPCA')
        return valores_projetados


    def projetar_pib(self, pesos):
        serie_historica = sh.pegar_serie_pib()
        valores_projetados, simulacao = monte_carlo.projetar_dados(pesos=pesos, n_simulacoes=self.n_simulacoes,
                                                       qtd_projecoes=self.qtd_projecoes,
                                                       serie_historica=serie_historica)

        ut.plotar_linhas(simulacoes=simulacao, qtd_projecoes=self.qtd_projecoes, titulo='Var. do PIB')
        return valores_projetados


    def __init__(self, qtd_projecoes, n_simulacoes):
        self.qtd_projecoes = qtd_projecoes
        self.n_simulacoes = n_simulacoes
