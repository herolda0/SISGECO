
import customtkinter as ctk


BG = "#141820"
WHITE = "#1D2430"
DARK = "#F0F3F8"
MUTED = "#9AA6B5"
BORDER = "#303A49"
TEAL = "#20B8A8"


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, navigation, pagina_atual):

        super().__init__(
            master,
            width=225,
            fg_color="#191F29",
            corner_radius=0
        )

        self.navigation = navigation
        self.pagina_atual = pagina_atual

        self.grid_propagate(False)

        self.criar_conteudo()

    def criar_conteudo(self):

        logo = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        logo.pack(
            fill="x",
            padx=22,
            pady=(25, 35)
        )

        ctk.CTkLabel(
            logo,
            text="SISGECO",
            text_color=DARK,
            font=ctk.CTkFont(
                family="Georgia",
                size=25,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo,
            text="GESTÃO COMERCIAL",
            text_color=MUTED,
            font=ctk.CTkFont(size=9, weight="bold")
        ).pack(anchor="w")

        for pagina in self.navigation.obter_menu():

            ativa = (
                pagina["nome"] == self.pagina_atual
            )

            self.criar_item(
                pagina["nome"],
                pagina["titulo"],
                pagina["icone"],
                ativa
            )

        ctk.CTkFrame(
            self,
            fg_color="transparent"
        ).pack(
            expand=True,
            fill="both"
        )

        ctk.CTkLabel(
            self,
            text="Sistema acadêmico • v1.0",
            text_color="#707D8E",
            font=ctk.CTkFont(size=10)
        ).pack(
            anchor="w",
            padx=20,
            pady=20
        )

    def criar_item(self, nome, titulo, icone, ativa):

        cor = "#167F76" if ativa else "transparent"

        texto_cor = (
            "#FFFFFF" if ativa else "#B7C1CF"
        )

        botao = ctk.CTkButton(
            self,
            text=f"  {icone}     {titulo}",
            anchor="w",
            height=44,
            corner_radius=9,
            fg_color=cor,
            hover_color="#263B43" if not ativa else "#126D66",
            text_color=texto_cor,
            font=ctk.CTkFont(
                size=13,
                weight="bold" if ativa else "normal"
            ),
            command=lambda: self.navigation.mostrar_tela(nome)
        )

        botao.pack(
            fill="x",
            padx=12,
            pady=4
        )
