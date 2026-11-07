
import customtkinter as ctk
from tkinter import messagebox

from view.sidebar import Sidebar


BG = "#141820"
WHITE = "#1D2430"
DARK = "#F0F3F8"
MUTED = "#9AA6B5"
TEAL = "#20B8A8"
BORDER = "#303A49"


class VendasView(ctk.CTkFrame):

    PAGE_NAME = "vendas"
    MENU_LABEL = "Vendas"
    MENU_ICON = "▣"
    MENU_ORDER = 2
    SHOW_IN_MENU = True

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
            fg_color=BG
        )

        content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=30,
            pady=25
        )

        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 25)
        )

        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Vendas",
            text_color=DARK,
            font=ctk.CTkFont(size=26, weight="bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            header,
            text="+ Nova venda",
            fg_color="#167F76",
            hover_color="#126D66",
            height=40,
            corner_radius=9,
            command=self.nova_venda
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        ctk.CTkLabel(
            content,
            text="Gerencie as vendas realizadas no sistema.",
            text_color=MUTED,
            font=ctk.CTkFont(size=12)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 20)
        )

        self.painel = ctk.CTkFrame(
            content,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        self.painel.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        ctk.CTkLabel(
            self.painel,
            text="Histórico de vendas",
            text_color=DARK,
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 12)
        )

        self.lista_vendas = ctk.CTkScrollableFrame(
            self.painel,
            fg_color="transparent"
        )

        self.lista_vendas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.atualizar_lista()

    def nova_venda(self):

        janela = ctk.CTkToplevel(self)

        janela.title("Nova venda")
        janela.geometry("430x480")
        janela.resizable(False, False)
        janela.configure(fg_color=BG)

        janela.transient(self.winfo_toplevel())
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text="Cadastrar venda",
            text_color=DARK,
            font=ctk.CTkFont(size=21, weight="bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        campos = {}

        dados = [
            ("cliente", "Nome do cliente"),
            ("produto", "Nome do produto"),
            ("quantidade", "Quantidade"),
            ("preco", "Preço unitário")
        ]

        for chave, texto in dados:

            ctk.CTkLabel(
                janela,
                text=texto,
                text_color=MUTED,
                font=ctk.CTkFont(size=12)
            ).pack(
                anchor="w",
                padx=25,
                pady=(8, 4)
            )

            entrada = ctk.CTkEntry(
                janela,
                height=38,
                fg_color=WHITE,
                border_color=BORDER,
                text_color=DARK
            )

            entrada.pack(
                fill="x",
                padx=25
            )

            campos[chave] = entrada

        def salvar():

            cliente = campos["cliente"].get().strip()
            produto = campos["produto"].get().strip()

            try:
                quantidade = int(campos["quantidade"].get())
                preco = float(
                    campos["preco"].get().replace(",", ".")
                )

                if not cliente or not produto:
                    raise ValueError

                if quantidade <= 0 or preco <= 0:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Dados inválidos",
                    "Preencha todos os campos corretamente.",
                    parent=janela
                )
                return

            numero = len(self.navigation.vendas) + 1

            venda = {
                "id": numero,
                "cliente": cliente,
                "produto": produto,
                "quantidade": quantidade,
                "total": quantidade * preco,
                "status": "Concluída"
            }

            self.navigation.vendas.append(venda)

            janela.destroy()
            self.atualizar_lista()

            messagebox.showinfo(
                "Sucesso",
                "Venda cadastrada com sucesso!"
            )

        ctk.CTkButton(
            janela,
            text="Salvar venda",
            height=40,
            fg_color="#167F76",
            hover_color="#126D66",
            command=salvar
        ).pack(
            fill="x",
            padx=25,
            pady=25
        )

    def atualizar_lista(self):

        for widget in self.lista_vendas.winfo_children():
            widget.destroy()

        if not self.navigation.vendas:

            ctk.CTkLabel(
                self.lista_vendas,
                text="Nenhuma venda cadastrada.",
                text_color=MUTED
            ).pack(pady=35)

            return

        for venda in self.navigation.vendas:

            linha = ctk.CTkFrame(
                self.lista_vendas,
                fg_color="#28313E",
                corner_radius=8
            )

            linha.pack(
                fill="x",
                pady=5
            )

            linha.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                linha,
                text=(
                    f"Venda #{venda['id']}  •  "
                    f"{venda['cliente']}  •  "
                    f"{venda['produto']}  •  "
                    f"Qtd: {venda['quantidade']}"
                ),
                text_color=DARK,
                anchor="w"
            ).grid(
                row=0,
                column=0,
                sticky="ew",
                padx=15,
                pady=15
            )

            ctk.CTkLabel(
                linha,
                text=f"R$ {venda['total']:.2f}",
                text_color=TEAL,
                font=ctk.CTkFont(weight="bold")
            ).grid(
                row=0,
                column=1,
                padx=15
            )
