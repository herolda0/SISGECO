
import customtkinter as ctk
from tkinter import Canvas
from models.dashboard_model import DashboardModel


BG = "#F5F7FA"
WHITE = "#FFFFFF"
DARK = "#172B4D"
MUTED = "#7B8798"
TEAL = "#159B8E"
BORDER = "#E8EDF2"


class DashboardView(ctk.CTkFrame):

    def __init__(self, master, navigation=None):
        super().__init__(
            master,
            fg_color=BG,
            corner_radius=0
        )

        self.navigation = navigation
        self.model = DashboardModel()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._criar_sidebar()
        self._criar_conteudo()

    # MENU LATERAL
    def _criar_sidebar(self):

        sidebar = ctk.CTkFrame(
            self,
            width=225,
            fg_color=WHITE,
            corner_radius=0
        )

        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        logo = ctk.CTkFrame(
            sidebar,
            fg_color="transparent"
        )

        logo.pack(fill="x", padx=22, pady=(25, 35))

        ctk.CTkLabel(
            logo,
            text="SISGECO",
            text_color="#142B3A",
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

        menu = [
            ("⌂", "Visão geral", True),
            ("▣", "Vendas", False),
            ("♙", "Clientes", False),
            ("▦", "Produtos", False),
            ("▤", "Estoque", False),
            ("▥", "Relatórios", False),
            ("⚙", "Configurações", False),
        ]

        for icon, label, active in menu:
            self._menu_item(
                sidebar,
                icon,
                label,
                active
            )

        ctk.CTkFrame(
            sidebar,
            fg_color="transparent"
        ).pack(expand=True, fill="both")

        ctk.CTkLabel(
            sidebar,
            text="Sistema acadêmico • v1.0",
            text_color="#A0A9B5",
            font=ctk.CTkFont(size=10)
        ).pack(anchor="w", padx=20, pady=20)

    def _menu_item(self, parent, icon, label, active=False):

        color = TEAL if active else WHITE
        text_color = WHITE if active else "#425166"

        button = ctk.CTkButton(
            parent,
            text=f"  {icon}     {label}",
            anchor="w",
            height=44,
            corner_radius=9,
            fg_color=color,
            hover_color="#E8F5F3" if not active else "#11877D",
            text_color=text_color,
            font=ctk.CTkFont(
                size=13,
                weight="bold" if active else "normal"
            ),
            command=lambda: self._navegar(label)
        )

        button.pack(
            fill="x",
            padx=12,
            pady=4
        )

    def _aviso_secao(self, secao):

        self.status_label.configure(
            text=f"Módulo '{secao}' será desenvolvido."
        )

    def _navegar(self, secao):

        if secao == "Vendas" and self.navigation is not None:
            self.navigation.mostrar_tela("vendas")
        else:
            self._aviso_secao(secao)

    # CONTEÚDO PRINCIPAL
    def _criar_conteudo(self):

        content = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=27,
            pady=22
        )

        content.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1
        )

        content.grid_rowconfigure(3, weight=1)

        # CABEÇALHO
        header = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="ew",
            pady=(0, 22)
        )

        header.grid_columnconfigure(0, weight=1)

        title_area = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_area.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            title_area,
            text="Visão geral",
            text_color=DARK,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_area,
            text="Acompanhe o desempenho comercial da sua empresa.",
            text_color=MUTED,
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(4, 0))

        right = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        right.grid(
            row=0,
            column=1,
            sticky="e"
        )

        search = ctk.CTkEntry(
            right,
            placeholder_text="⌕  Pesquisar...",
            width=210,
            height=38,
            corner_radius=9,
            border_color=BORDER,
            fg_color=WHITE,
            text_color=DARK
        )

        search.pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            right,
            text="●",
            text_color=TEAL,
            font=ctk.CTkFont(size=19)
        ).pack(side="left", padx=8)

        ctk.CTkLabel(
            right,
            text="Administrador",
            text_color=DARK,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(side="left")

        # INDICADORES
        for col, item in enumerate(
            self.model.obter_indicadores()
        ):

            self._card_indicador(
                content,
                col,
                item
            )

        # GRÁFICO DE VENDAS
        chart1 = self._painel(
            content,
            "Vendas ao longo dos meses"
        )

        chart1.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=(0, 9),
            pady=(18, 9)
        )

        self._grafico_linha(chart1)

        # GRÁFICO DE PRODUTOS
        chart2 = self._painel(
            content,
            "Produtos mais vendidos"
        )

        chart2.grid(
            row=2,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=(9, 0),
            pady=(18, 9)
        )

        self._grafico_barras(chart2)

        # VENDAS RECENTES
        recent = self._painel(
            content,
            "Vendas recentes"
        )

        recent.grid(
            row=3,
            column=0,
            columnspan=4,
            sticky="nsew",
            pady=(9, 0)
        )

        self._tabela_vendas(recent)

        self.status_label = ctk.CTkLabel(
            content,
            text="Dados demonstrativos",
            text_color="#98A2B0",
            font=ctk.CTkFont(size=10)
        )

        self.status_label.grid(
            row=4,
            column=0,
            columnspan=4,
            sticky="e",
            pady=(8, 0)
        )

    # CARTÕES DE INDICADORES
    def _card_indicador(self, parent, col, item):

        card = ctk.CTkFrame(
            parent,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        card.grid(
            row=1,
            column=col,
            sticky="nsew",
            padx=5
        )

        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text=item["titulo"],
            text_color=MUTED,
            font=ctk.CTkFont(size=11)
        ).pack(
            anchor="w",
            padx=16,
            pady=(16, 9)
        )

        ctk.CTkLabel(
            card,
            text=item["valor"],
            text_color=DARK,
            font=ctk.CTkFont(
                size=23,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=16
        )

        ctk.CTkLabel(
            card,
            text=item["variacao"],
            text_color=TEAL,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=16,
            pady=(8, 15)
        )

    # PAINÉIS
    def _painel(self, parent, titulo):

        panel = ctk.CTkFrame(
            parent,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        ctk.CTkLabel(
            panel,
            text=titulo,
            text_color=DARK,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 5)
        )

        return panel

    # GRÁFICO DE LINHA
    def _grafico_linha(self, parent):

        data = self.model.obter_vendas_mensais()

        canvas = Canvas(
            parent,
            height=230,
            bg=WHITE,
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 10)
        )

        def desenhar(event=None):

            canvas.delete("all")

            w = max(canvas.winfo_width(), 300)
            h = max(canvas.winfo_height(), 180)

            left = 38
            right = w - 18
            top = 18
            bottom = h - 32

            for value in range(0, 26, 5):

                y = bottom - (value / 25) * (
                    bottom - top
                )

                canvas.create_line(
                    left, y, right, y,
                    fill="#EDF1F5"
                )

                canvas.create_text(
                    left - 15,
                    y,
                    text=str(value),
                    fill=MUTED,
                    font=("Arial", 8)
                )

            points = []
            max_value = 25

            for i, (month, value) in enumerate(data):

                x = left + i * (
                    right - left
                ) / (len(data) - 1)

                y = bottom - (
                    value / max_value
                ) * (bottom - top)

                points.extend([x, y])

                canvas.create_text(
                    x,
                    bottom + 15,
                    text=month,
                    fill=MUTED,
                    font=("Arial", 8)
                )

            if len(points) >= 4:

                canvas.create_line(
                    *points,
                    fill=TEAL,
                    width=3,
                    smooth=True
                )

                for i in range(0, len(points), 2):

                    canvas.create_oval(
                        points[i] - 4,
                        points[i + 1] - 4,
                        points[i] + 4,
                        points[i + 1] + 4,
                        fill=TEAL,
                        outline=WHITE,
                        width=1
                    )

        canvas.bind("<Configure>", desenhar)

    # GRÁFICO DE BARRAS
    def _grafico_barras(self, parent):

        data = self.model.obter_produtos_mais_vendidos()

        canvas = Canvas(
            parent,
            height=230,
            bg=WHITE,
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 10)
        )

        def desenhar(event=None):

            canvas.delete("all")

            w = max(canvas.winfo_width(), 300)
            h = max(canvas.winfo_height(), 180)

            left = 95
            right = w - 22
            top = 18
            bottom = h - 15

            max_value = max(
                value for _, value in data
            )

            row_h = (
                bottom - top
            ) / len(data)

            for i, (name, value) in enumerate(data):

                y = top + i * row_h + row_h * 0.2

                bar_h = row_h * 0.52

                bar_w = (
                    value / max_value
                ) * (right - left)

                canvas.create_text(
                    left - 10,
                    y + bar_h / 2,
                    text=name,
                    anchor="e",
                    fill="#536174",
                    font=("Arial", 9)
                )

                canvas.create_rectangle(
                    left,
                    y,
                    left + bar_w,
                    y + bar_h,
                    fill=TEAL,
                    outline="",
                    width=0
                )

                canvas.create_text(
                    min(left + bar_w + 20, w - 12),
                    y + bar_h / 2,
                    text=str(value),
                    fill=DARK,
                    font=("Arial", 9, "bold")
                )

        canvas.bind("<Configure>", desenhar)

    # TABELA DE VENDAS
    def _tabela_vendas(self, parent):

        table = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        table.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=(8, 14)
        )

        headers = [
            "CÓDIGO",
            "CLIENTE",
            "PRODUTO",
            "VALOR",
            "STATUS"
        ]

        header_row = ctk.CTkFrame(
            table,
            fg_color="#F6F8FA",
            corner_radius=6
        )

        header_row.pack(
            fill="x",
            pady=(0, 5)
        )

        for i, header in enumerate(headers):

            header_row.grid_columnconfigure(
                i,
                weight=1
            )

            ctk.CTkLabel(
                header_row,
                text=header,
                text_color=MUTED,
                font=ctk.CTkFont(
                    size=9,
                    weight="bold"
                ),
                anchor="w"
            ).grid(
                row=0,
                column=i,
                sticky="ew",
                padx=9,
                pady=10
            )

        for sale in self.model.obter_vendas_recentes():

            row = ctk.CTkFrame(
                table,
                fg_color="transparent"
            )

            row.pack(fill="x")

            for i, value in enumerate(sale):

                if value == "Concluída":
                    color = TEAL

                elif value == "Pendente":
                    color = "#D98A28"

                else:
                    color = DARK

                row.grid_columnconfigure(
                    i,
                    weight=1
                )

                ctk.CTkLabel(
                    row,
                    text=value,
                    text_color=color,
                    font=ctk.CTkFont(size=11),
                    anchor="w"
                ).grid(
                    row=0,
                    column=i,
                    sticky="ew",
                    padx=9,
                    pady=9
                )

            ctk.CTkFrame(
                table,
                height=1,
                fg_color="#EFF2F5"
            ).pack(fill="x")
