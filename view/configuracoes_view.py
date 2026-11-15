
import customtkinter as ctk
from view.sidebar import Sidebar


class ConfiguracoesView(ctk.CTkFrame):

    PAGE_NAME = "configuracoes"
    MENU_LABEL = "Configurações"
    MENU_ICON = "⚙"
    MENU_ORDER = 7
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
            text="Configurações",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#F0F3F8"
        ).pack(anchor="w")

        ctk.CTkLabel(
            conteudo,
            text="Informações e preferências do sistema.",
            font=ctk.CTkFont(size=13),
            text_color="#9AA6B5"
        ).pack(anchor="w", pady=(5, 25))

        geral = ctk.CTkFrame(
            conteudo,
            fg_color="#1D2430",
            corner_radius=12
        )

        geral.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            geral,
            text="Preferências gerais",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#F0F3F8"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            geral,
            text="As preferências do sistema poderão ser configuradas nesta área.",
            font=ctk.CTkFont(size=13),
            text_color="#9AA6B5",
            wraplength=650
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        sobre = ctk.CTkFrame(
            conteudo,
            fg_color="#1D2430",
            corner_radius=12
        )

        sobre.pack(fill="x")

        ctk.CTkLabel(
            sobre,
            text="Sobre o sistema",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#F0F3F8"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            sobre,
            text="SISGECO\nSistema de Gestão Comercial\nVersão 1.0",
            font=ctk.CTkFont(size=13),
            text_color="#9AA6B5",
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )
