import customtkinter as ctk
from view.sidebar import Sidebar

BG, WHITE, DARK = "#141820", "#1D2430", "#F0F3F8"
MUTED, TEAL = "#9AA6B5", "#20B8A8"


class RelatoriosView(ctk.CTkFrame):
    PAGE_NAME, MENU_LABEL, MENU_ICON, MENU_ORDER, SHOW_IN_MENU = "relatorios", "Relatórios", "▥", 6, True

    def __init__(self, master, navigation):
        super().__init__(master, fg_color=BG)
        self.navigation = navigation
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        Sidebar(self, navigation, self.PAGE_NAME).grid(row=0, column=0, sticky="ns")
        self.criar_conteudo()

    def criar_conteudo(self):
        conteudo = ctk.CTkFrame(self, fg_color="transparent")
        conteudo.grid(row=0, column=1, sticky="nsew", padx=35, pady=30)
        conteudo.grid_columnconfigure((0, 1, 2), weight=1)
        ctk.CTkLabel(conteudo, text="Relatórios", font=ctk.CTkFont(size=28, weight="bold"), text_color=DARK).grid(row=0, column=0, columnspan=3, sticky="w")
        ctk.CTkLabel(conteudo, text="Indicadores calculados a partir das vendas registradas.", font=ctk.CTkFont(size=13), text_color=MUTED).grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 25))
        resumo = self.navigation.sistema.obter_resumo()
        dados = (("Faturamento", f"R$ {resumo['faturamento']:.2f}"), ("Total de vendas", str(resumo["total_vendas"])), ("Ticket médio", f"R$ {resumo['ticket_medio']:.2f}"))
        for col, (titulo, valor) in enumerate(dados):
            card = ctk.CTkFrame(conteudo, fg_color=WHITE, corner_radius=12)
            card.grid(row=2, column=col, sticky="ew", padx=(0 if col == 0 else 8, 8 if col < 2 else 0), pady=5)
            ctk.CTkLabel(card, text=titulo, text_color=MUTED, font=ctk.CTkFont(size=12)).pack(anchor="w", padx=18, pady=(18, 5))
            ctk.CTkLabel(card, text=valor, text_color=DARK, font=ctk.CTkFont(size=23, weight="bold")).pack(anchor="w", padx=18, pady=(0, 18))
        painel = ctk.CTkFrame(conteudo, fg_color=WHITE, corner_radius=12)
        painel.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(20, 0))
        ctk.CTkLabel(painel, text="Produtos mais vendidos", font=ctk.CTkFont(size=17, weight="bold"), text_color=DARK).pack(anchor="w", padx=20, pady=(20, 10))
        ranking = self.navigation.sistema.obter_produtos_mais_vendidos()
        if ranking:
            for nome, quantidade in ranking:
                ctk.CTkLabel(painel, text=f"{nome}  •  {quantidade} unidade(s)", font=ctk.CTkFont(size=13), text_color=MUTED).pack(anchor="w", padx=22, pady=6)
        else:
            ctk.CTkLabel(painel, text="Ainda não existem vendas suficientes para gerar este relatório.", font=ctk.CTkFont(size=13), text_color=MUTED).pack(anchor="w", padx=22, pady=(5, 25))
