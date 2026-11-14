
from view.dashboard_view import DashboardView
from view.vendas_view import VendasView


class Navigation:

    def __init__(self, container):
        self.container = container
        self.tela_atual = None
        self.vendas = []

    def mostrar_tela(self, nome):

        if self.tela_atual is not None:
            self.tela_atual.destroy()

        if nome == "dashboard":
            self.tela_atual = DashboardView(
                self.container,
                self
            )

        elif nome == "vendas":
            self.tela_atual = VendasView(
                self.container,
                self
            )

        else:
            return

        self.tela_atual.pack(
            fill="both",
            expand=True
        )
