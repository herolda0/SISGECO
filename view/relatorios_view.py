
import customtkinter as ctk
from view.sidebar import Sidebar


class RelatoriosView(ctk.CTkFrame):

    PAGE_NAME = "relatorios"
    MENU_LABEL = "Relatórios"
    MENU_ICON = "▥"
    MENU_ORDER = 6
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
            text="Relatórios",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#F0F3F8"
        ).pack(anchor="w")

        ctk.CTkLabel(
            conteudo,
            text="Acompanhe os resultados e indicadores comerciais.",
            font=ctk.CTkFont(size=13),
            text_color="#9AA6B5"
        ).pack(anchor="w", pady=(5, 25))

        indicadores = ctk.CTkFrame(
            conteudo,
            fg_color="transparent"
        )

        indicadores.pack(fill="x")

        dados = [
            ("Faturamento", "R$ 0,00"),
            ("Total de vendas", "0"),
            ("Ticket médio", "R$ 0,00")
        ]

        for titulo, valor in dados:

            card = ctk.CTkFrame(
                indicadores,
                fg_color="#1D2430",
                corner_radius=12
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 12),
                pady=5
            )

            ctk.CTkLabel(
                card,
                text=titulo,
                text_color="#9AA6B5",
                font=ctk.CTkFont(size=12)
            ).pack(
                anchor="w",
                padx=18,
                pady=(18, 5)
            )

            ctk.CTkLabel(
                card,
                text=valor,
                text_color="#F0F3F8",
                font=ctk.CTkFont(size=23, weight="bold")
            ).pack(
                anchor="w",
                padx=18,
                pady=(0, 18)
            )

        painel = ctk.CTkFrame(
            conteudo,
            fg_color="#1D2430",
            corner_radius=12
        )

        painel.pack(
            fill="both",
            expand=True,
            pady=(20, 0)
        )

        ctk.CTkLabel(
            painel,
            text="Relatórios comerciais",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#F0F3F8"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            painel,
            text="Os relatórios serão apresentados aqui quando houver dados registrados no sistema.",
            font=ctk.CTkFont(size=13),
            text_color="#9AA6B5",
            wraplength=650
        ).pack(
            anchor="w",
            padx=20,
            pady=15
        )
