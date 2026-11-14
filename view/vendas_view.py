
import customtkinter as ctk
from tkinter import messagebox


BG = "#F5F7FA"
WHITE = "#FFFFFF"
DARK = "#172B4D"
MUTED = "#7B8798"
TEAL = "#159B8E"


class VendasView(ctk.CTkFrame):

    def __init__(self, master, navigation):
        super().__init__(
            master,
            fg_color=BG,
            corner_radius=0
        )

        self.navigation = navigation

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_sidebar()
        self.criar_conteudo()

    def criar_sidebar(self):

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
            ("⌂", "Visão geral", False),
            ("▣", "Vendas", True),
            ("♙", "Clientes", False),
            ("▦", "Produtos", False),
            ("▤", "Estoque", False),
            ("▥", "Relatórios", False),
            ("⚙", "Configurações", False)
        ]

        for icon, label, active in menu:

            ctk.CTkButton(
                sidebar,
                text=f"  {icon}     {label}",
                anchor="w",
                height=44,
                corner_radius=9,
                fg_color=TEAL if active else WHITE,
                hover_color="#11877D" if active else "#E8F5F3",
                text_color=WHITE if active else "#425166",
                font=ctk.CTkFont(
                    size=13,
                    weight="bold" if active else "normal"
                ),
                command=lambda l=label: self.navegar(l)
            ).pack(
                fill="x",
                padx=12,
                pady=4
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

    def navegar(self, secao):

        if secao == "Visão geral":
            self.navigation.mostrar_tela("dashboard")

        elif secao == "Vendas":
            self.navigation.mostrar_tela("vendas")

        else:
            messagebox.showinfo(
                "SISGECO",
                f"Módulo '{secao}' será desenvolvido."
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

        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            content,
            text="Vendas",
            text_color=DARK,
            font=ctk.CTkFont(size=25, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            content,
            text="Registre e acompanhe as vendas realizadas.",
            text_color=MUTED,
            font=ctk.CTkFont(size=12)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(4, 22)
        )

        area = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )
        area.grid(row=2, column=0, sticky="nsew")
        area.grid_columnconfigure(0, weight=1)
        area.grid_rowconfigure(1, weight=1)

        topo = ctk.CTkFrame(
            area,
            fg_color="transparent"
        )
        topo.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        ctk.CTkButton(
            topo,
            text="+ Nova venda",
            fg_color=TEAL,
            hover_color="#11877D",
            height=38,
            command=self.nova_venda
        ).pack(side="right")

        self.painel = ctk.CTkFrame(
            area,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color="#E8EDF2"
        )
        self.painel.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.atualizar_lista()

    def nova_venda(self):

        janela = ctk.CTkToplevel(self)
        janela.title("Nova venda")
        janela.geometry("400x390")
        janela.resizable(False, False)
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text="Registrar nova venda",
            text_color=DARK,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(22, 15))

        cliente = ctk.CTkEntry(
            janela,
            placeholder_text="Nome do cliente",
            width=300,
            height=38
        )
        cliente.pack(pady=8)

        produto = ctk.CTkEntry(
            janela,
            placeholder_text="Nome do produto",
            width=300,
            height=38
        )
        produto.pack(pady=8)

        quantidade = ctk.CTkEntry(
            janela,
            placeholder_text="Quantidade",
            width=300,
            height=38
        )
        quantidade.pack(pady=8)

        valor = ctk.CTkEntry(
            janela,
            placeholder_text="Preço unitário (ex.: 50.00)",
            width=300,
            height=38
        )
        valor.pack(pady=8)

        def salvar():

            try:
                nome_cliente = cliente.get().strip()
                nome_produto = produto.get().strip()
                qtd = int(quantidade.get())
                preco = float(valor.get().replace(",", "."))

                if not nome_cliente or not nome_produto:
                    raise ValueError

                if qtd <= 0 or preco <= 0:
                    raise ValueError

                total = qtd * preco

                venda = {
                    "id": len(self.navigation.vendas) + 1,
                    "cliente": nome_cliente,
                    "produto": nome_produto,
                    "quantidade": qtd,
                    "total": total,
                    "status": "Concluída"
                }

                self.navigation.vendas.append(venda)

                janela.destroy()
                self.atualizar_lista()

                messagebox.showinfo(
                    "Venda registrada",
                    f"Venda registrada com sucesso!\nTotal: R$ {total:.2f}"
                )

            except ValueError:
                messagebox.showerror(
                    "Dados inválidos",
                    "Preencha os campos corretamente."
                )

        ctk.CTkButton(
            janela,
            text="Registrar venda",
            fg_color=TEAL,
            hover_color="#11877D",
            width=180,
            height=38,
            command=salvar
        ).pack(pady=18)

    def atualizar_lista(self):

        for widget in self.painel.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.painel,
            text="Histórico de vendas",
            text_color=DARK,
            font=ctk.CTkFont(size=17, weight="bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=18
        )

        if not self.navigation.vendas:

            ctk.CTkLabel(
                self.painel,
                text="Nenhuma venda registrada.",
                text_color=MUTED
            ).pack(anchor="w", padx=18, pady=8)

            return

        for venda in self.navigation.vendas:

            linha = ctk.CTkFrame(
                self.painel,
                fg_color="#F6F8FA",
                corner_radius=8
            )
            linha.pack(
                fill="x",
                padx=15,
                pady=5
            )

            texto = (
                f"#{venda['id']}   "
                f"{venda['cliente']}   |   "
                f"{venda['produto']}   |   "
                f"{venda['quantidade']} un.   |   "
                f"R$ {venda['total']:.2f}   |   "
                f"{venda['status']}"
            )

            ctk.CTkLabel(
                linha,
                text=texto,
                text_color="#425166",
                anchor="w"
            ).pack(
                fill="x",
                padx=12,
                pady=12
            )
