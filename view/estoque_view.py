
import customtkinter as ctk
from view.sidebar import Sidebar


class EstoqueView(ctk.CTkFrame):

    PAGE_NAME = "estoque"
    MENU_LABEL = "Estoque"
    MENU_ICON = "▤"
    MENU_ORDER = 5
    SHOW_IN_MENU = True

    def __init__(self, master, navigation):
        super().__init__(master, fg_color="#141820")

        self.navigation = navigation

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_sidebar()
        self.criar_conteudo()

    def criar_sidebar(self):
        self.sidebar = Sidebar(
            self,
            self.navigation,
            self.PAGE_NAME
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

    def criar_conteudo(self):

        conteudo = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        conteudo.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=35,
            pady=30
        )

        ctk.CTkLabel(
            conteudo,
            text="Estoque",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#F0F3F8"
        ).pack(anchor="w")

        ctk.CTkLabel(
            conteudo,
            text="Acompanhe a quantidade de produtos disponíveis.",
            font=ctk.CTkFont(size=13),
            text_color="#9AA6B5"
        ).pack(anchor="w", pady=(5, 25))

        tabela = ctk.CTkFrame(
            conteudo,
            fg_color="#1D2430",
            corner_radius=12
        )

        tabela.pack(fill="both", expand=True)

        cabecalho = ctk.CTkFrame(
            tabela,
            fg_color="#252E3B",
            corner_radius=8
        )

        cabecalho.pack(
            fill="x",
            padx=15,
            pady=15
        )

        colunas = [
            "Produto",
            "Categoria",
            "Quantidade",
            "Situação"
        ]

        for coluna in colunas:
            ctk.CTkLabel(
                cabecalho,
                text=coluna,
                text_color="#F0F3F8",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(
                side="left",
                expand=True,
                padx=10,
                pady=12
            )

        ctk.CTkLabel(
            tabela,
            text="Nenhum produto disponível no estoque.",
            text_color="#9AA6B5",
            font=ctk.CTkFont(size=13)
        ).pack(pady=40)
