from utils import utils as ut
from utils import monte_carlo
from utils import calculos
from utils import series_historicas as sh
import numpy as np
class Valuation:

    def projetar(self,serie_historica):
        simulacao_ultimo_ano, simulacao_completa = monte_carlo.projetar_dados(n_simulacoes=self.n_simulacoes,
                                                       qtd_projecoes=self.qtd_projecoes,
                                                       serie_historica=serie_historica)


        return np.array(simulacao_ultimo_ano), simulacao_completa


    def projetar_growth(self):
        """
            Projeta o Growth

            :param peso_growth: int
            :param peso_pib: int
            :param peso_ipca: int
        """
        self.ipca_projetado = self.projetar_ipca()
        self.pib_projetado = self.projetar_pib()

        self.growth = calculos.calculo_growth(inflacao=self.ipca_projetado, pib=self.pib_projetado)

        return self.growth   

    def projetar_wacc(self):

        self.beta = calculos.calculo_beta(self.ativo)
        beta_projetado = np.array([self.beta] * self.n_simulacoes) 
        
        self.premio_risco_projetado = self.projetar_premio_risco()
        self.di_projetado = self.projetar_di()
        self.cds_projetado = self.projetar_cds()


        self.ke = calculos.calculo_ke(self.beta, self.premio_risco_projetado, self.di_projetado, self.cds_projetado)
        
        self.divida_bruta_projetado = np.array([self.divida_bruta] * self.n_simulacoes)
        self.valor_equity_projetado = np.array([self.valor_equity] * self.n_simulacoes)
        
        self.cje_projetado = self.projetar_cje()
        self.kd_projetado = calculos.calcular_kd(self.ipca_projetado, self.cje_projetado, self.n_simulacoes)

        self.wacc = calculos.calculo_wacc(ke=self.ke, valor_equity=self.valor_equity_projetado, kd=self.kd_projetado, divida_bruta=self.divida_bruta_projetado)

        return self.wacc


    


    def projetar_ipca(self):
        serie_historica = sh.pegar_serie_ipca()
        valores_projetados, simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(simulacoes=simulacao, qtd_projecoes=self.qtd_projecoes, titulo='Simulação do IPCA',n_simulacoes=self.n_simulacoes)
        return valores_projetados


    def projetar_pib(self):
        serie_historica = sh.pegar_serie_pib()
        valores_projetados, simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(simulacoes=simulacao, qtd_projecoes=self.qtd_projecoes, titulo='Simulação do PIB Brasileiro',n_simulacoes=self.n_simulacoes)
        return valores_projetados 


    def projetar_premio_risco(self):
        serie_historica = sh.pegar_serie_selic()
        valores_projetados, simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_projecoes, 
            titulo='Simulação do Premio de Risco',
            n_simulacoes=self.n_simulacoes
        )
        
        return valores_projetados

    def projetar_di(self):
        serie_historica = sh.pegar_serie_di()
        valores_projetados, simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_projecoes, 
            titulo='Simulação Depósitos Interbancários - DI',
            n_simulacoes=self.n_simulacoes
        )
        
        return valores_projetados

    def projetar_cds(self):
        serie_historica = sh.pegar_serie_cds()
        valores_projetados, simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_projecoes, 
            titulo='Simulação Credit Default Swap - CDS',
            n_simulacoes=self.n_simulacoes
        )
        
        return valores_projetados

    def projetar_cje(self):
        serie_historica = sh.pegar_serie_cje()
        valores_projetados, simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_projecoes, 
            titulo='Simulação da Cobertura de Juros da Empresa',
            n_simulacoes=self.n_simulacoes
        )
        
        return valores_projetados

    def projetar_fcff(self):
        """
            Projeta o FCL

        """
        growth = self.projetar_growth()

        np.savetxt('growth.txt',growth, delimiter=',' )

        serie_historica = sh.pegar_serie_fcl()
        valores_projetados, simulacao = monte_carlo.projetar_fcl(serie_fcf=serie_historica, growth_projetado=growth, n_simulacoes=self.n_simulacoes, qtd_projecoes=self.qtd_projecoes)

        ut.plotar_linhas(simulacoes=simulacao, qtd_projecoes=self.qtd_projecoes, titulo='Simulação do Fluxo de Caixa Livre - FCL', n_simulacoes=self.n_simulacoes)

        return valores_projetados
    

    def projetar_fcd(self):
        fcff = self.projetar_fcff()
        wacc = self.projetar_wacc()

        np.savetxt('fcff.txt',fcff, delimiter=',' )
        np.savetxt('wacc.txt',wacc, delimiter=',' )


        fcd = calculos.calculo_fcd(fcff_projetado=fcff, wacc_projetado=wacc, qtd_projecoes=self.qtd_projecoes, n_simulacoes=self.n_simulacoes)

        np_fcd = np.array(fcd)
        np.savetxt('fcd.txt',np_fcd, delimiter=',')

        ano = ut.get_ultimo_ano(self.qtd_projecoes)

        ut.plotar_hist(fcd, f'Simulação do FCD - Ano de {ano} ')

        return fcd

    def __init__(self, qtd_projecoes, n_simulacoes, ativo):
        self.qtd_projecoes = qtd_projecoes
        self.n_simulacoes = n_simulacoes
        self.ativo = ativo
        self.qtd_papeis, self.divida_bruta, self.valor_equity  = calculos.pegar_divida_equity()
