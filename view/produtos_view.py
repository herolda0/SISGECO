import customtkinter as ctk
from tkinter import messagebox
from view.sidebar import Sidebar

BG, WHITE, DARK = "#141820", "#1D2430", "#F0F3F8"
MUTED, TEAL, BORDER = "#9AA6B5", "#20B8A8", "#303A49"


class ProdutosView(ctk.CTkFrame):
    PAGE_NAME, MENU_LABEL, MENU_ICON, MENU_ORDER, SHOW_IN_MENU = "produtos", "Produtos", "▦", 4, True

    def __init__(self, master, navigation):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self.navigation = navigation
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        Sidebar(self, navigation, self.PAGE_NAME).grid(row=0, column=0, sticky="nsew")
        self.criar_conteudo()

    def criar_conteudo(self):
        content = ctk.CTkFrame(self, fg_color=BG)
        content.grid(row=0, column=1, sticky="nsew", padx=30, pady=25)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(2, weight=1)
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Produtos", text_color=DARK, font=ctk.CTkFont(size=26, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="+ Novo produto", fg_color="#167F76", hover_color="#126D66", height=40, command=lambda: self.abrir_formulario()).grid(row=0, column=1, sticky="e")
        ctk.CTkLabel(content, text="Cadastre e gerencie os produtos comercializados.", text_color=MUTED, font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", pady=(0, 18))
        painel = ctk.CTkFrame(content, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        painel.grid(row=2, column=0, sticky="nsew")
        painel.grid_columnconfigure(0, weight=1)
        painel.grid_rowconfigure(1, weight=1)
        self.pesquisa = ctk.CTkEntry(painel, placeholder_text="Pesquisar produto ou categoria...", height=40, fg_color=BG, border_color=BORDER, text_color=DARK)
        self.pesquisa.grid(row=0, column=0, sticky="ew", padx=18, pady=18)
        self.pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_lista())
        self.lista_produtos = ctk.CTkScrollableFrame(painel, fg_color="transparent")
        self.lista_produtos.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.atualizar_lista()

    def abrir_formulario(self, produto=None):
        janela = ctk.CTkToplevel(self)
        janela.title("Editar produto" if produto else "Novo produto")
        janela.geometry("430x450")
        janela.resizable(False, False)
        janela.configure(fg_color=BG)
        janela.transient(self.winfo_toplevel())
        janela.grab_set()
        ctk.CTkLabel(janela, text="Editar produto" if produto else "Cadastrar produto", text_color=DARK, font=ctk.CTkFont(size=21, weight="bold")).pack(anchor="w", padx=25, pady=(25, 20))
        campos = {}
        for chave, rotulo in (("nome", "Nome do produto"), ("categoria", "Categoria"), ("preco", "Preço de venda"), ("quantidade", "Quantidade inicial")):
            ctk.CTkLabel(janela, text=rotulo, text_color=MUTED).pack(anchor="w", padx=25, pady=(8, 4))
            entrada = ctk.CTkEntry(janela, height=38, fg_color=WHITE, border_color=BORDER, text_color=DARK)
            entrada.pack(fill="x", padx=25)
            if produto:
                entrada.insert(0, str(produto.get(chave, "")))
            campos[chave] = entrada
        if produto:
            campos["quantidade"].configure(state="disabled")
        def salvar():
            try:
                nome, categoria = campos["nome"].get().strip(), campos["categoria"].get().strip()
                preco = float(campos["preco"].get().replace(",", "."))
                if produto:
                    self.navigation.sistema.editar_produto(produto["id"], nome, categoria, preco)
                else:
                    quantidade = int(campos["quantidade"].get())
                    self.navigation.sistema.cadastrar_produto(nome, categoria, preco, quantidade)
                janela.destroy()
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Produto salvo com sucesso!", parent=self)
            except Exception as erro:
                messagebox.showerror("Dados inválidos", str(erro), parent=janela)
        ctk.CTkButton(janela, text="Salvar produto", height=40, fg_color="#167F76", hover_color="#126D66", command=salvar).pack(fill="x", padx=25, pady=25)

    def excluir_produto(self, produto):
        if not messagebox.askyesno("Excluir produto", f"Deseja excluir {produto['nome']}?", parent=self):
            return
        try:
            self.navigation.sistema.excluir_produto(produto["id"])
            self.atualizar_lista()
        except Exception as erro:
            messagebox.showerror("Não foi possível excluir", str(erro), parent=self)

    def atualizar_lista(self):
        for widget in self.lista_produtos.winfo_children():
            widget.destroy()
        busca = self.pesquisa.get().strip().lower()
        produtos = [p for p in self.navigation.sistema.listar_produtos() if busca in p["nome"].lower() or busca in p["categoria"].lower()]
        if not produtos:
            ctk.CTkLabel(self.lista_produtos, text="Nenhum produto encontrado." if busca else "Nenhum produto cadastrado.", text_color=MUTED).pack(pady=35)
            return
        header = ctk.CTkFrame(self.lista_produtos, fg_color="#28313E", corner_radius=6)
        header.pack(fill="x", pady=(0, 8))
        for i, titulo in enumerate(("CÓDIGO", "PRODUTO", "CATEGORIA", "PREÇO", "ESTOQUE", "AÇÕES")):
            header.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(header, text=titulo, text_color="#AEB9C8", font=ctk.CTkFont(size=10, weight="bold"), anchor="w").grid(row=0, column=i, sticky="ew", padx=7, pady=12)
        for produto in produtos:
            row = ctk.CTkFrame(self.lista_produtos, fg_color="transparent")
            row.pack(fill="x", pady=2)
            vals = (f"#{produto['id']}", produto["nome"], produto["categoria"], f"R$ {produto['preco']:.2f}", str(produto["quantidade"]))
            for i, val in enumerate(vals):
                row.grid_columnconfigure(i, weight=1)
                ctk.CTkLabel(row, text=val, text_color=TEAL if i == 3 else DARK, font=ctk.CTkFont(size=11), anchor="w").grid(row=0, column=i, sticky="ew", padx=7, pady=10)
            acoes = ctk.CTkFrame(row, fg_color="transparent")
            acoes.grid(row=0, column=5, padx=2)
            ctk.CTkButton(acoes, text="Editar", width=55, height=28, command=lambda p=produto: self.abrir_formulario(p)).pack(side="left", padx=2)
            ctk.CTkButton(acoes, text="Excluir", width=55, height=28, fg_color="#8B3942", hover_color="#702D35", command=lambda p=produto: self.excluir_produto(p)).pack(side="left", padx=2)
            ctk.CTkFrame(self.lista_produtos, height=1, fg_color=BORDER).pack(fill="x")
