from utils import utils as ut
from utils import monte_carlo
from utils import calculos
from utils import series_historicas as sh
import numpy as np
class Valuation:

    def projetar(self,serie_historica):
        """
        Chama a função do Monte Carlo para gerar Simulações no futuro.
        
        Parameters
        ----------
        serie_historica : Pandas.series
            Série Histórica dos dados.

        Returns
        -------
        simulacao_ultimo_ano: np.array
            n Simulações do ultimo ano projetado.
        simulacao_completa: np.array | list
            Simulação de todos os anos projetados.


        Examples
        --------
        >>> projetar({2016: 0.1, ..., 2023: 0.2})
        [simulacao 1:[2016:0.4,...,2023:0.21],...,simulacao n:[2016:0.2,...,2023:0.05]]
        """
        
        simulacao_completa = monte_carlo.projetar_dados(n_simulacoes=self.n_simulacoes,
                                                       qtd_projecoes=self.qtd_anos_projetados,
                                                       serie_historica=serie_historica)


        return simulacao_completa


    def projetar_growth(self):
        """
        Projeta o Growth no futuro (ultimo ano das projeções), utilizando o IPCA e o PIB no futuro.

        Returns
        -------
        self.growth: np.array
            Array contendo o growth no ultimo ano das projeções.

        """

        self.ipca_projetado = self.projetar_ipca()
        self.pib_projetado = self.projetar_pib()

        self.growth = calculos.calculo_growth(inflacao=self.ipca_projetado, pib=self.pib_projetado)
        ut.plotar_linhas(simulacoes=self.growth, qtd_projecoes=self.qtd_anos_projetados,titulo='Simulação do GROWTH', n_simulacoes=self.n_simulacoes)

        return self.growth   

    def projetar_wacc(self):
        """
        Projeta o WACC no futuro (ultimo ano das projeções) utilizando algumas variaveis importantes

        Returns
        -------
        self.wacc: np.array 
            Array contendo o WACC no ultimo ano das projeções.

        """
        self.ipca_projetado = self.projetar_ipca()

        self.beta = calculos.calculo_beta(self.ativo)
        beta_projetado = np.tile(self.beta, (self.n_simulacoes, self.qtd_anos_projetados)) 
        
        self.premio_risco_projetado = self.projetar_premio_risco()
        self.cds_projetado = self.projetar_cds()
        self.di_projetado = self.projetar_di()

        self.ke = calculos.calculo_ke(self.beta, self.premio_risco_projetado, self.di_projetado, self.cds_projetado)
        
        self.divida_bruta_projetado = np.tile(self.divida_bruta, (self.n_simulacoes, self.qtd_anos_projetados))
        self.valor_equity_projetado = np.tile(self.valor_equity, (self.n_simulacoes, self.qtd_anos_projetados))
        
        self.cje_projetado = self.projetar_cje()
        self.kd_projetado = calculos.calcular_kd(self.ipca_projetado, self.cje_projetado, self.n_simulacoes)

        self.wacc = calculos.calculo_wacc(
            ke=self.ke, 
            valor_equity=self.valor_equity_projetado, 
            kd=self.kd_projetado, 
            divida_bruta=self.divida_bruta_projetado
        )

        ut.plotar_linhas(simulacoes=self.wacc, qtd_projecoes=self.qtd_anos_projetados,titulo='Simulação do WACC', n_simulacoes=self.n_simulacoes)

        return self.wacc


    


    def projetar_ipca(self):
        """
        Projeta o IPCA utilizando a sua serie historica.

        Returns
        -------
        valores_projetados: np.array
            Valores no ultimo ano das projeções.
        """

        serie_historica = sh.pegar_serie_ipca()
        simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_anos_projetados, 
            titulo='Simulação do IPCA',
            n_simulacoes=self.n_simulacoes
        )

        return simulacao


    def projetar_pib(self):
        """
        Projeta o PIB Brasileiro utilizando a sua serie historica.

        Returns
        -------
        valores_projetados: np.array
            Valores no ultimo ano das projeções.
        """

        serie_historica = sh.pegar_serie_pib()
        simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_anos_projetados, 
            titulo='Simulação do PIB Brasileiro',
            n_simulacoes=self.n_simulacoes
        )

        return simulacao 


    def projetar_premio_risco(self):
        """
        Projeta o Premio de Risco utilizando a sua serie historica.

        Returns
        -------
        valores_projetados: np.array
            Valores no ultimo ano das projeções.
        """
        serie_historica = sh.pegar_serie_selic()
        simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_anos_projetados, 
            titulo='Simulação do Premio de Risco',
            n_simulacoes=self.n_simulacoes
        )
        
        return simulacao

    def projetar_di(self):
        """
        Projeta o DI utilizando a sua serie historica.

        Returns
        -------
        valores_projetados: np.array
            Valores no ultimo ano das projeções.
        """
        # serie_historica = sh.pegar_serie_di()
        # di_ettj = self.projetar(serie_historica=serie_historica)
        di_ettj = calculos.calcular_di(self.qtd_anos_projetados)

        di = np.round(di_ettj, 3)

        # ut.plotar_serie_historia(di_ettj, 'Depósitos Interbancários - DI ')

        # ut.plotar_linhas(
        #     simulacoes=di_ettj, 
        #     qtd_projecoes=self.qtd_anos_projetados, 
        #     titulo='Simulação Depósitos Interbancários - DI',
        #     n_simulacoes=self.n_simulacoes
        # )
        
        return di_ettj

    def projetar_cds(self):
        """
        Projeta o CDS utilizando a sua serie historica.

        Returns
        -------
        valores_projetados: np.array
            Valores no ultimo ano das projeções.
        """
        serie_historica = sh.pegar_serie_cds()
        simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_anos_projetados, 
            titulo='Simulação Credit Default Swap - CDS',
            n_simulacoes=self.n_simulacoes
        )
        
        return simulacao

    def projetar_cje(self):
        """
        Projeta o Cobertura de Juros da Empresa utilizando a sua serie historica.

        Returns
        -------
        valores_projetados: np.array
            Valores no ultimo ano das projeções.
        """
        serie_historica = sh.pegar_serie_cje()
        simulacao = self.projetar(serie_historica=serie_historica)

        ut.plotar_linhas(
            simulacoes=simulacao, 
            qtd_projecoes=self.qtd_anos_projetados, 
            titulo='Simulação da Cobertura de Juros da Empresa',
            n_simulacoes=self.n_simulacoes
        )
        
        return simulacao

    def projetar_fcff(self):
        """
        Projeta o Fluxo de Caixa Livre utilizando a sua serie historica mais o GROWTH projetado.

        Returns
        -------
        valores_projetados: np.array
            Valores no ultimo ano das projeções.
        """
        growth = self.projetar_growth() # Projeta o Growth no futuro

        # Para cada simulação do GROWTH é pego o sua média e desvio padrão
        media_desvio_growth = calculos.calculo_media_std_por_ano(growth)

        serie_historica = sh.pegar_serie_fcl() # Serie Historia do Fluxo de Caixa Livre

        simulacao = monte_carlo.projetar_fcl(serie_fcf=serie_historica, dados_growth=media_desvio_growth, n_simulacoes=self.n_simulacoes, qtd_projecoes=self.qtd_anos_projetados)

        ut.plotar_linhas(simulacoes=simulacao, qtd_projecoes=self.qtd_anos_projetados, titulo='Simulação do Fluxo de Caixa Livre - FCL', n_simulacoes=self.n_simulacoes)

        return simulacao
    

    def projetar_fcd(self):
        """
        Projeta o Fluxo de Caixa Descontado no ultimo ano das projeções utilizando o cálculo:
            FCD = Fluxo de Caixa / (1 + WACC)^n
            Onde n é o ano projetado, indo de 1 até self.qtd_anos_projetados 

        Returns
        -------
        FCD: np.array
            Valores no ultimo ano das projeções.
        """
        fcff = self.projetar_fcff() # Projeta o Fluxo de caixa livre no futuro
        wacc = self.projetar_wacc() # Projeta o WACC no futuro

        fcd = calculos.calculo_fcd(fcff_projetado=fcff, wacc_projetado=wacc) # Calcula o FCD

        ut.plotar_hist_valuation(fcd,self.qtd_papeis, f'Simulação do FCD')

        return fcd

    def __init__(self, anos_projetados, n_simulacoes, ativo):
        """
        Inicia a classe com as configurações principais

        Parameters
        ----------
        anos_projetados: int 
            Quantidade de anos futuros 
        n_simulacoes: int 
            Quantidade de Simulações para cada ano projetado
        ativo:
            Nome do ativo da empresa para busca de alguns dados e cálculo do BETA
        """
        self.qtd_anos_projetados = anos_projetados
        self.n_simulacoes = n_simulacoes
        self.ativo = ativo
        self.qtd_papeis, self.divida_bruta, self.valor_equity  = calculos.pegar_divida_equity()
