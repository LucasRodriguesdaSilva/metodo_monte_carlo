from utils import utils as ut
from utils import monte_carlo
from utils import calculos
from utils import series_historicas as sh

class Valuation:

    def projetar(self,pesos, serie_historica, is_premio_risco = False):
        valores_projetados, simulacao = monte_carlo.projetar_dados(pesos=pesos, n_simulacoes=self.n_simulacoes,
                                                       qtd_projecoes=self.qtd_projecoes,
                                                       serie_historica=serie_historica, is_premio_risco=is_premio_risco)
        return valores_projetados, simulacao


    def projetar_ipca(self, pesos):
        serie_historica = sh.pegar_serie_ipca()
        valores_projetados, simulacao = self.projetar(pesos=pesos, serie_historica=serie_historica)

        ut.plotar_linhas(simulacoes=simulacao, qtd_projecoes=self.qtd_projecoes, titulo='Var. do IPCA')
        return valores_projetados


    def projetar_pib(self, pesos):
        serie_historica = sh.pegar_serie_pib()
        valores_projetados, simulacao = self.projetar(pesos=pesos, serie_historica=serie_historica)

        ut.plotar_linhas(simulacoes=simulacao, qtd_projecoes=self.qtd_projecoes, titulo='Var. do PIB Brasileiro')
        return valores_projetados

    def projetar_growth(self, peso_growth=0.0025, peso_pib = 0.1, peso_ipca = 0.1):
        """
            Projeta o Growth
            :param peso_growth: int
            :param peso_pib: int | list
                Se for uma lista, deve ser do tamanho da quantidade de projeções futuras
            :param peso_ipca: int | list
                Se for uma lista, deve ser do tamanho da quantidade de projeções futuras
        """
        try:
            ut.is_lista(peso_growth)
        except TypeError as e:
            print(e)


        if not isinstance(peso_pib, list):
            peso_pib = [peso_pib] * self.qtd_projecoes

        if not isinstance(peso_ipca, list):
            peso_ipca = [peso_ipca] * self.qtd_projecoes


        ipca_projetado = self.projetar_ipca(pesos=peso_ipca)
        pib_projetado = self.projetar_pib(pesos=peso_pib)

        ultimo_ipca = ipca_projetado[-1]
        ultimo_pib = pib_projetado[-1]

        growth = calculos.calculo_growth(inflacao=ultimo_ipca, pib=ultimo_pib)

        array_growth = ut.distribuir_valor(valor=growth, peso=0.0025, tam_array=10)

        return array_growth    


    def projetar_premio_risco(self, pesos):
        serie_historica = sh.pegar_serie_selic()
        valores_projetados, simulacao = self.projetar(pesos=pesos, serie_historica=serie_historica, is_premio_risco=True)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_projecoes, 
            titulo='Var. do Premio de Risco'
        )
        
        return valores_projetados

    def projetar_cds(self,pesos):
        serie_historica = sh.pegar_serie_cds()
        valores_projetados, simulacao = self.projetar(pesos=pesos, serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_projecoes, 
            titulo='Var. do Premio de Risco'
        )
        
        return valores_projetados

    


    def __init__(self, qtd_projecoes, n_simulacoes):
        self.qtd_projecoes = qtd_projecoes
        self.n_simulacoes = n_simulacoes
