class DashboardModel:

    def obter_indicadores(self):
        return [
            {
                "titulo": "Faturamento total",
                "valor": "R$ 28.450,00",
                "variacao": "+12,8%",
                "cor": "#159B8E"
            },
            {
                "titulo": "Vendas realizadas",
                "valor": "184",
                "variacao": "+8,4%",
                "cor": "#159B8E"
            },
            {
                "titulo": "Clientes cadastrados",
                "valor": "96",
                "variacao": "+5,2%",
                "cor": "#159B8E"
            },
            {
                "titulo": "Produtos cadastrados",
                "valor": "248",
                "variacao": "Estoque ativo",
                "cor": "#159B8E"
            },
        ]

    def obter_vendas_mensais(self):
        return [
            ("Jan", 8),
            ("Fev", 11),
            ("Mar", 9),
            ("Abr", 14),
            ("Mai", 12),
            ("Jun", 17),
            ("Jul", 15),
            ("Ago", 21),
        ]

    def obter_produtos_mais_vendidos(self):
        return [
            ("Notebook", 82),
            ("Mouse", 68),
            ("Teclado", 54),
            ("Monitor", 43),
            ("Headset", 31),
        ]

    def obter_vendas_recentes(self):
        return [
            ("#000184", "Mariana Costa", "Notebook",
             "R$ 3.200,00", "Concluída"),

            ("#000183", "Pedro Henrique", "Mouse",
             "R$ 120,00", "Concluída"),

            ("#000182", "Ana Souza", "Monitor",
             "R$ 890,00", "Pendente"),

            ("#000181", "Lucas Oliveira", "Teclado",
             "R$ 250,00", "Concluída"),
        ]