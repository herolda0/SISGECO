class DashboardModel:
    def __init__(self, sistema):
        self.sistema = sistema

    def obter_indicadores(self):
        resumo = self.sistema.obter_resumo()
        return [
            {"titulo": "Faturamento total", "valor": f"R$ {resumo['faturamento']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "variacao": "Acumulado registrado", "cor": "#20B8A8"},
            {"titulo": "Vendas realizadas", "valor": str(resumo["total_vendas"]), "variacao": "Total de vendas", "cor": "#20B8A8"},
            {"titulo": "Clientes cadastrados", "valor": str(resumo["total_clientes"]), "variacao": "Total de clientes", "cor": "#20B8A8"},
            {"titulo": "Produtos cadastrados", "valor": str(resumo["total_produtos"]), "variacao": "Total de produtos", "cor": "#20B8A8"},
        ]

    def obter_vendas_mensais(self):
        return self.sistema.obter_vendas_mensais()

    def obter_produtos_mais_vendidos(self):
        return self.sistema.obter_produtos_mais_vendidos()

    def obter_vendas_recentes(self):
        return self.sistema.obter_vendas_recentes()
