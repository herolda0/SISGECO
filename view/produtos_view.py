
import customtkinter as ctk
from tkinter import messagebox

from view.sidebar import Sidebar


BG = "#141820"
WHITE = "#1D2430"
DARK = "#F0F3F8"
MUTED = "#9AA6B5"
TEAL = "#20B8A8"
BORDER = "#303A49"


class ProdutosView(ctk.CTkFrame):

    # IDENTIFICAÇÃO AUTOMÁTICA DA PÁGINA
    PAGE_NAME = "produtos"
    MENU_LABEL = "Produtos"
    MENU_ICON = "▦"
    MENU_ORDER = 4
    SHOW_IN_MENU = True

    def __init__(self, master, navigation):

        super().__init__(
            master,
            fg_color=BG,
            corner_radius=0
        )

        self.navigation = navigation
        self.produtos = []

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_sidebar()
        self.criar_conteudo()

    # MENU LATERAL
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

    # CONTEÚDO PRINCIPAL
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

        # CABEÇALHO
        header = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 20)
        )

        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Produtos",
            text_color=DARK,
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            header,
            text="+ Novo produto",
            fg_color="#167F76",
            hover_color="#126D66",
            height=40,
            corner_radius=9,
            command=self.novo_produto
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        ctk.CTkLabel(
            content,
            text="Cadastre e gerencie os produtos comercializados.",
            text_color=MUTED,
            font=ctk.CTkFont(size=12)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 18)
        )

        # PAINEL DE PRODUTOS
        painel = ctk.CTkFrame(
            content,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        painel.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        painel.grid_columnconfigure(0, weight=1)
        painel.grid_rowconfigure(1, weight=1)

        self.pesquisa = ctk.CTkEntry(
            painel,
            placeholder_text="Pesquisar produto...",
            height=40,
            fg_color=BG,
            border_color=BORDER,
            text_color=DARK
        )

        self.pesquisa.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=18
        )

        self.pesquisa.bind(
            "<KeyRelease>",
            lambda event: self.atualizar_lista()
        )

        self.lista_produtos = ctk.CTkScrollableFrame(
            painel,
            fg_color="transparent"
        )

        self.lista_produtos.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

        self.atualizar_lista()

    # CADASTRAR PRODUTO
    def novo_produto(self):

        janela = ctk.CTkToplevel(self)

        janela.title("Novo produto")
        janela.geometry("430x450")
        janela.resizable(False, False)
        janela.configure(fg_color=BG)

        janela.transient(self.winfo_toplevel())
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text="Cadastrar produto",
            text_color=DARK,
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        campos = {}

        dados = [
            ("nome", "Nome do produto"),
            ("categoria", "Categoria"),
            ("preco", "Preço de venda"),
            ("quantidade", "Quantidade inicial")
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

            nome = campos["nome"].get().strip()
            categoria = campos["categoria"].get().strip()

            try:

                preco = float(
                    campos["preco"].get().replace(",", ".")
                )

                quantidade = int(
                    campos["quantidade"].get()
                )

                if not nome or not categoria:
                    raise ValueError

                if preco <= 0 or quantidade < 0:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Dados inválidos",
                    "Preencha os campos corretamente.",
                    parent=janela
                )

                return

            produto = {
                "id": len(self.produtos) + 1,
                "nome": nome,
                "categoria": categoria,
                "preco": preco,
                "quantidade": quantidade
            }

            self.produtos.append(produto)

            janela.destroy()
            self.atualizar_lista()

            messagebox.showinfo(
                "Sucesso",
                "Produto cadastrado com sucesso!"
            )

        ctk.CTkButton(
            janela,
            text="Salvar produto",
            height=40,
            fg_color="#167F76",
            hover_color="#126D66",
            command=salvar
        ).pack(
            fill="x",
            padx=25,
            pady=25
        )

    # ATUALIZAR LISTAGEM
    def atualizar_lista(self):

        for widget in self.lista_produtos.winfo_children():
            widget.destroy()

        busca = self.pesquisa.get().strip().lower()

        produtos = [
            produto
            for produto in self.produtos
            if busca in produto["nome"].lower()
            or busca in produto["categoria"].lower()
        ]

        if not produtos:

            ctk.CTkLabel(
                self.lista_produtos,
                text="Nenhum produto encontrado.",
                text_color=MUTED
            ).pack(pady=35)

            return

        cabecalho = ctk.CTkFrame(
            self.lista_produtos,
            fg_color="#28313E",
            corner_radius=6
        )

        cabecalho.pack(
            fill="x",
            pady=(0, 8)
        )

        colunas = [
            "CÓDIGO",
            "PRODUTO",
            "CATEGORIA",
            "PREÇO",
            "QUANTIDADE"
        ]

        for i, titulo in enumerate(colunas):

            cabecalho.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(
                cabecalho,
                text=titulo,
                text_color="#AEB9C8",
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                ),
                anchor="w"
            ).grid(
                row=0,
                column=i,
                sticky="ew",
                padx=8,
                pady=12
            )

        for produto in produtos:

            linha = ctk.CTkFrame(
                self.lista_produtos,
                fg_color="transparent"
            )

            linha.pack(
                fill="x",
                pady=2
            )

            valores = [
                f"#{produto['id']}",
                produto["nome"],
                produto["categoria"],
                f"R$ {produto['preco']:.2f}",
                str(produto["quantidade"])
            ]

            for i, valor in enumerate(valores):

                linha.grid_columnconfigure(i, weight=1)

                ctk.CTkLabel(
                    linha,
                    text=valor,
                    text_color=(
                        TEAL
                        if i == 3
                        else DARK
                    ),
                    font=ctk.CTkFont(size=11),
                    anchor="w"
                ).grid(
                    row=0,
                    column=i,
                    sticky="ew",
                    padx=8,
                    pady=12
                )

            ctk.CTkFrame(
                self.lista_produtos,
                height=1,
                fg_color=BORDER
            ).pack(fill="x")
