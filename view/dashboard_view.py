
import customtkinter as ctk
from tkinter import Canvas

from models.dashboard_model import DashboardModel
from view.sidebar import Sidebar


BG = "#141820"
WHITE = "#1D2430"
DARK = "#F0F3F8"
MUTED = "#9AA6B5"
TEAL = "#20B8A8"
BORDER = "#303A49"


class DashboardView(ctk.CTkFrame):

    PAGE_NAME = "dashboard"
    MENU_LABEL = "Visão geral"
    MENU_ICON = "⌂"
    MENU_ORDER = 1
    SHOW_IN_MENU = True

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

        self.criar_sidebar()
        self.criar_conteudo()

    def criar_sidebar(self):

        sidebar = Sidebar(
            self,
            self.navigation,
            self.PAGE_NAME
        )

        sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def criar_conteudo(self):

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

        content.grid_columnconfigure((0, 1, 2, 3), weight=1)
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

        title_area.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            title_area,
            text="Visão geral",
            text_color=DARK,
            font=ctk.CTkFont(size=25, weight="bold")
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

        right.grid(row=0, column=1, sticky="e")

        ctk.CTkEntry(
            right,
            placeholder_text="⌕  Pesquisar...",
            width=210,
            height=38,
            corner_radius=9,
            border_color=BORDER,
            fg_color=WHITE,
            text_color=DARK,
            placeholder_text_color="#778496"
        ).pack(side="left", padx=(0, 12))

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
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left")

        # INDICADORES
        for col, item in enumerate(self.model.obter_indicadores()):
            self.card_indicador(content, col, item)

        # GRÁFICO DE VENDAS
        chart1 = self.painel(
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

        self.grafico_linha(chart1)

        # GRÁFICO DE PRODUTOS
        chart2 = self.painel(
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

        self.grafico_barras(chart2)

        # VENDAS RECENTES
        recent = self.painel(
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

        self.tabela_vendas(recent)

        ctk.CTkLabel(
            content,
            text="Dados demonstrativos",
            text_color="#778496",
            font=ctk.CTkFont(size=10)
        ).grid(
            row=4,
            column=0,
            columnspan=4,
            sticky="e",
            pady=(8, 0)
        )

    # CARTÕES DE INDICADORES
    def card_indicador(self, parent, col, item):

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

        ctk.CTkLabel(
            card,
            text=item["titulo"],
            text_color=MUTED,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=16, pady=(16, 9))

        ctk.CTkLabel(
            card,
            text=item["valor"],
            text_color=DARK,
            font=ctk.CTkFont(size=23, weight="bold")
        ).pack(anchor="w", padx=16)

        ctk.CTkLabel(
            card,
            text=item["variacao"],
            text_color=TEAL,
            font=ctk.CTkFont(size=11, weight="bold")
        ).pack(anchor="w", padx=16, pady=(8, 15))

    # PAINÉIS
    def painel(self, parent, titulo):

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
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=18, pady=(16, 5))

        return panel

    # GRÁFICO DE LINHA
    def grafico_linha(self, parent):

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

                y = bottom - (value / 25) * (bottom - top)

                canvas.create_line(
                    left, y, right, y,
                    fill="#354050"
                )

                canvas.create_text(
                    left - 15, y,
                    text=str(value),
                    fill=MUTED,
                    font=("Arial", 8)
                )

            points = []
            max_value = 25

            for i, (month, value) in enumerate(data):

                if len(data) == 1:
                    x = (left + right) / 2
                else:
                    x = left + i * (right - left) / (len(data) - 1)

                y = bottom - (value / max_value) * (bottom - top)

                points.extend([x, y])

                canvas.create_text(
                    x, bottom + 15,
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
    def grafico_barras(self, parent):

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
                (value for _, value in data),
                default=1
            )

            row_h = (bottom - top) / max(len(data), 1)

            for i, (name, value) in enumerate(data):

                y = top + i * row_h + row_h * 0.2
                bar_h = row_h * 0.52
                bar_w = (value / max_value) * (right - left)

                canvas.create_text(
                    left - 10,
                    y + bar_h / 2,
                    text=name,
                    anchor="e",
                    fill="#B7C1CF",
                    font=("Arial", 9)
                )

                canvas.create_rectangle(
                    left, y,
                    left + bar_w, y + bar_h,
                    fill=TEAL,
                    outline=""
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
    def tabela_vendas(self, parent):

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
            fg_color="#28313E",
            corner_radius=6
        )

        header_row.pack(fill="x", pady=(0, 5))

        for i, header in enumerate(headers):

            header_row.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(
                header_row,
                text=header,
                text_color="#AEB9C8",
                font=ctk.CTkFont(size=9, weight="bold"),
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
                    color = "#E6A34D"
                else:
                    color = DARK

                row.grid_columnconfigure(i, weight=1)

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
                fg_color="#303A49"
            ).pack(fill="x")
