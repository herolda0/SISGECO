
class DashboardModel:

    def obter_indicadores(self):
        return [
            {
                "titulo": "Faturamento total",
                "valor": "R$ 0,00",
                "variacao": "Sem dados",
                "cor": "#20B8A8"
            },
            {
                "titulo": "Vendas realizadas",
                "valor": "0",
                "variacao": "Sem dados",
                "cor": "#20B8A8"
            },
            {
                "titulo": "Clientes cadastrados",
                "valor": "0",
                "variacao": "Sem dados",
                "cor": "#20B8A8"
            },
            {
                "titulo": "Produtos cadastrados",
                "valor": "0",
                "variacao": "Sem dados",
                "cor": "#20B8A8"
            }
        ]

    def obter_vendas_mensais(self):
        return []

    def obter_produtos_mais_vendidos(self):
        return []

    def obter_vendas_recentes(self):
        return []
