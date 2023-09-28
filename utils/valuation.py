from utils import utils as ut
from utils import monte_carlo
from utils import calculos
from utils import series_historicas as sh
import numpy as np
class Valuation:

    def projetar(self,peso, serie_historica, is_premio_risco = False):
        valores_projetados, simulacao = monte_carlo.projetar_dados(peso=peso, n_simulacoes=self.n_simulacoes,
                                                       qtd_projecoes=self.qtd_projecoes,
                                                       serie_historica=serie_historica, is_premio_risco=is_premio_risco)
        return np.array(valores_projetados), simulacao


    def projetar_growth(self, peso_growth=0.0025, peso_pib = 0.1, peso_ipca = 0.1):
        """
            Projeta o Growth

            :param peso_growth: int
            :param peso_pib: int
            :param peso_ipca: int
        """

        self.ipca_projetado = self.projetar_ipca(peso=peso_ipca)
        self.pib_projetado = self.projetar_pib(peso=peso_pib)

        ultimo_ipca = self.ipca_projetado[-1]
        ultimo_pib = self.pib_projetado[-1]

        self.growth = calculos.calculo_growth(inflacao=ultimo_ipca, pib=ultimo_pib)

        self.array_growth = ut.distribuir_valor(valor=self.growth, peso=0.0025, tam_array=10)

        return self.array_growth   

    def projetar_wacc(self, peso_premio_risco=0.1, peso_di=0.1, peso_cds=0.1):
        self.beta = calculos.calculo_beta(self.ativo)
        beta_projetado = np.array([self.beta]) * self.qtd_projecoes
        self.premio_risco_projetado = self.projetar_premio_risco(peso_premio_risco)
        self.di_projetado = self.projetar_di(peso_di)
        self.cds_projetado = self.projetar_cds(peso_cds)

        self.ke = calculos.calculo_ke(self.beta, self.premio_risco_projetado, self.di_projetado, self.cds_projetado)
        divida_bruta_projetado = np.array([self.divida_bruta]) * self.qtd_projecoes
        valor_equity_projetado = np.array([self.valor_equity]) * self.qtd_projecoes

        self.cje_projetado = self.projetar_cje(0.1)
        self.kd_projetado = calculos.calcular_kd(self.ipca_projetado, self.cje_projetado)

        self.wacc = calculos.calculo_wacc(ke=self.ke, valor_equity=valor_equity_projetado, kd=self.kd_projetado, divida_bruta=divida_bruta_projetado)

        self.array_wacc = ut.distribuir_valor(valor=self.wacc[-1], peso=0.005, tam_array=10)

        return self.array_wacc






    def projetar_ipca(self, peso):
        serie_historica = sh.pegar_serie_ipca()
        valores_projetados, simulacao = self.projetar(peso=peso, serie_historica=serie_historica)

        ut.plotar_linhas(simulacoes=simulacao, qtd_projecoes=self.qtd_projecoes, titulo='Var. do IPCA')
        return valores_projetados


    def projetar_pib(self, peso):
        serie_historica = sh.pegar_serie_pib()
        valores_projetados, simulacao = self.projetar(peso=peso, serie_historica=serie_historica)

        ut.plotar_linhas(simulacoes=simulacao, qtd_projecoes=self.qtd_projecoes, titulo='Var. do PIB Brasileiro')
        return valores_projetados 


    def projetar_premio_risco(self, peso):
        serie_historica = sh.pegar_serie_selic()
        valores_projetados, simulacao = self.projetar(peso=peso, serie_historica=serie_historica, is_premio_risco=True)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_projecoes, 
            titulo='Var. do Premio de Risco'
        )
        
        return valores_projetados

    def projetar_di(self,peso):
        serie_historica = sh.pegar_serie_di()
        valores_projetados, simulacao = self.projetar(peso=peso, serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_projecoes, 
            titulo='Var. Depósitos Interbancários - DI'
        )
        
        return valores_projetados

    def projetar_cds(self,peso):
        serie_historica = sh.pegar_serie_cds()
        valores_projetados, simulacao = self.projetar(peso=peso, serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_projecoes, 
            titulo='Var. Credit Default Swap - CDS'
        )
        
        return valores_projetados

    def projetar_cje(self,peso):
        serie_historica = sh.pegar_serie_cje()
        valores_projetados, simulacao = self.projetar(peso=peso, serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_projecoes, 
            titulo='Var. da Cobertura de Juros da Empresa'
        )
        
        return valores_projetados


    


    def __init__(self, qtd_projecoes, n_simulacoes, ativo):
        self.qtd_projecoes = qtd_projecoes
        self.n_simulacoes = n_simulacoes
        self.ativo = ativo
        self.qtd_ativos, self.divida_bruta, self.valor_equity  = calculos.pegar_divida_equity()
        print(f'divida Bruta da Empresa: {self.divida_bruta}')
