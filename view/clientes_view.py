
import customtkinter as ctk
from tkinter import messagebox

from view.sidebar import Sidebar


BG = "#141820"
WHITE = "#1D2430"
DARK = "#F0F3F8"
MUTED = "#9AA6B5"
TEAL = "#20B8A8"
BORDER = "#303A49"


class ClientesView(ctk.CTkFrame):

    PAGE_NAME = "clientes"
    MENU_LABEL = "Clientes"
    MENU_ICON = "♙"
    MENU_ORDER = 3
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
            text="Clientes",
            text_color=DARK,
            font=ctk.CTkFont(size=26, weight="bold")
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            header,
            text="+ Novo cliente",
            fg_color="#167F76",
            hover_color="#126D66",
            height=40,
            corner_radius=9,
            command=self.novo_cliente
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        ctk.CTkLabel(
            content,
            text="Cadastre e consulte os clientes da empresa.",
            text_color=MUTED,
            font=ctk.CTkFont(size=12)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 18)
        )

        # PAINEL PRINCIPAL
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

        # PESQUISA
        self.pesquisa = ctk.CTkEntry(
            painel,
            placeholder_text="Pesquisar por nome, telefone ou e-mail...",
            height=40,
            fg_color="#141820",
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

        self.lista_clientes = ctk.CTkScrollableFrame(
            painel,
            fg_color="transparent"
        )

        self.lista_clientes.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

        self.atualizar_lista()

    # NOVO CLIENTE
    def novo_cliente(self):

        janela = ctk.CTkToplevel(self)

        janela.title("Novo cliente")
        janela.geometry("430x390")
        janela.resizable(False, False)
        janela.configure(fg_color=BG)

        janela.transient(self.winfo_toplevel())
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text="Cadastrar cliente",
            text_color=DARK,
            font=ctk.CTkFont(size=21, weight="bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        campos = {}

        dados = [
            ("nome", "Nome completo"),
            ("telefone", "Telefone"),
            ("email", "E-mail")
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
            telefone = campos["telefone"].get().strip()
            email = campos["email"].get().strip()

            if not nome or not telefone:

                messagebox.showwarning(
                    "Campos obrigatórios",
                    "Informe o nome e o telefone do cliente.",
                    parent=janela
                )

                return

            numero = len(self.navigation.clientes) + 1

            cliente = {
                "id": numero,
                "nome": nome,
                "telefone": telefone,
                "email": email
            }

            self.navigation.clientes.append(cliente)

            janela.destroy()
            self.atualizar_lista()

            messagebox.showinfo(
                "Sucesso",
                "Cliente cadastrado com sucesso!"
            )

        ctk.CTkButton(
            janela,
            text="Salvar cliente",
            height=40,
            fg_color="#167F76",
            hover_color="#126D66",
            command=salvar
        ).pack(
            fill="x",
            padx=25,
            pady=25
        )

    # LISTAGEM DE CLIENTES
    def atualizar_lista(self):

        for widget in self.lista_clientes.winfo_children():
            widget.destroy()

        busca = self.pesquisa.get().strip().lower()

        clientes = [
            cliente
            for cliente in self.navigation.clientes
            if busca in cliente["nome"].lower()
            or busca in cliente["telefone"].lower()
            or busca in cliente["email"].lower()
        ]

        if not clientes:

            mensagem = (
                "Nenhum cliente encontrado."
                if busca else
                "Nenhum cliente cadastrado."
            )

            ctk.CTkLabel(
                self.lista_clientes,
                text=mensagem,
                text_color=MUTED
            ).pack(pady=35)

            return

        # CABEÇALHO DA LISTA
        cabecalho = ctk.CTkFrame(
            self.lista_clientes,
            fg_color="#28313E",
            corner_radius=6
        )

        cabecalho.pack(
            fill="x",
            pady=(0, 8)
        )

        colunas = [
            ("CÓDIGO", 0),
            ("NOME", 1),
            ("TELEFONE", 2),
            ("E-MAIL", 3)
        ]

        for titulo, coluna in colunas:

            cabecalho.grid_columnconfigure(
                coluna,
                weight=1
            )

            ctk.CTkLabel(
                cabecalho,
                text=titulo,
                text_color="#AEB9C8",
                font=ctk.CTkFont(size=10, weight="bold"),
                anchor="w"
            ).grid(
                row=0,
                column=coluna,
                sticky="ew",
                padx=10,
                pady=12
            )

        for cliente in clientes:

            linha = ctk.CTkFrame(
                self.lista_clientes,
                fg_color="transparent"
            )

            linha.pack(
                fill="x",
                pady=2
            )

            valores = [
                f"#{cliente['id']}",
                cliente["nome"],
                cliente["telefone"],
                cliente["email"] or "-"
            ]

            for coluna, valor in enumerate(valores):

                linha.grid_columnconfigure(
                    coluna,
                    weight=1
                )

                ctk.CTkLabel(
                    linha,
                    text=valor,
                    text_color=DARK,
                    font=ctk.CTkFont(size=11),
                    anchor="w"
                ).grid(
                    row=0,
                    column=coluna,
                    sticky="ew",
                    padx=10,
                    pady=12
                )

            ctk.CTkFrame(
                self.lista_clientes,
                height=1,
                fg_color=BORDER
            ).pack(fill="x")
