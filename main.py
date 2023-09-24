from utils.valuation import Valuation

qtd_projecoes = 5
n_simulacoes = 1000

valuantion = Valuation(qtd_projecoes, n_simulacoes)

pesos_ipca = [0.1] * qtd_projecoes

ipca_projetado = valuantion.projetar_ipca(pesos=pesos_ipca)

print(ipca_projetado)





