import customtkinter as ctk
from tkinter import messagebox
from view.sidebar import Sidebar

BG, WHITE, DARK = "#141820", "#1D2430", "#F0F3F8"
MUTED, TEAL, BORDER = "#9AA6B5", "#20B8A8", "#303A49"


class EstoqueView(ctk.CTkFrame):
    PAGE_NAME, MENU_LABEL, MENU_ICON, MENU_ORDER, SHOW_IN_MENU = "estoque", "Estoque", "▤", 5, True

    def __init__(self, master, navigation):
        super().__init__(master, fg_color=BG)
        self.navigation = navigation
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        Sidebar(self, navigation, self.PAGE_NAME).grid(row=0, column=0, sticky="ns")
        self.criar_conteudo()

    def criar_conteudo(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=0, column=1, sticky="nsew", padx=35, pady=30)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(2, weight=1)
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Estoque", font=ctk.CTkFont(size=28, weight="bold"), text_color=DARK).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="Movimentar estoque", fg_color="#167F76", hover_color="#126D66", command=self.movimentar).grid(row=0, column=1, sticky="e")
        ctk.CTkLabel(content, text="Consulte quantidades e registre entradas e saídas de produtos.", font=ctk.CTkFont(size=13), text_color=MUTED).grid(row=1, column=0, sticky="w", pady=(5, 20))
        self.tabela = ctk.CTkScrollableFrame(content, fg_color=WHITE, corner_radius=12)
        self.tabela.grid(row=2, column=0, sticky="nsew")
        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.tabela.winfo_children():
            widget.destroy()
        cabecalho = ctk.CTkFrame(self.tabela, fg_color="#252E3B", corner_radius=8)
        cabecalho.pack(fill="x", padx=15, pady=15)
        for i, titulo in enumerate(("Produto", "Categoria", "Quantidade", "Situação")):
            cabecalho.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(cabecalho, text=titulo, text_color=DARK, font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=i, sticky="ew", padx=10, pady=12)
        produtos = self.navigation.sistema.listar_estoque()
        if not produtos:
            ctk.CTkLabel(self.tabela, text="Nenhum produto cadastrado. Cadastre produtos para controlar o estoque.", text_color=MUTED).pack(pady=40)
            return
        for produto in produtos:
            row = ctk.CTkFrame(self.tabela, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=3)
            situacao = "Sem estoque" if produto["quantidade"] == 0 else "Estoque baixo" if produto["quantidade"] <= 5 else "Disponível"
            valores = (produto["nome"], produto["categoria"], str(produto["quantidade"]), situacao)
            for i, valor in enumerate(valores):
                row.grid_columnconfigure(i, weight=1)
                ctk.CTkLabel(row, text=valor, text_color="#E6A34D" if situacao != "Disponível" and i == 3 else (TEAL if i == 3 else DARK), anchor="w").grid(row=0, column=i, sticky="ew", padx=10, pady=12)
            ctk.CTkFrame(self.tabela, height=1, fg_color=BORDER).pack(fill="x", padx=15)

    def movimentar(self):
        produtos = self.navigation.sistema.listar_produtos()
        if not produtos:
            messagebox.showwarning("Sem produtos", "Cadastre um produto antes de movimentar o estoque.", parent=self)
            return
        janela = ctk.CTkToplevel(self)
        janela.title("Movimentação de estoque")
        janela.geometry("420x330")
        janela.resizable(False, False)
        janela.configure(fg_color=BG)
        janela.transient(self.winfo_toplevel())
        janela.grab_set()
        ctk.CTkLabel(janela, text="Movimentar estoque", text_color=DARK, font=ctk.CTkFont(size=21, weight="bold")).pack(anchor="w", padx=25, pady=(25, 18))
        opcoes = {f"#{p['id']} - {p['nome']} (atual: {p['quantidade']})": p["id"] for p in produtos}
        ctk.CTkLabel(janela, text="Produto", text_color=MUTED).pack(anchor="w", padx=25, pady=(5, 4))
        produto_box = ctk.CTkComboBox(janela, values=list(opcoes))
        produto_box.pack(fill="x", padx=25)
        produto_box.set(list(opcoes)[0])
        ctk.CTkLabel(janela, text="Tipo de movimentação", text_color=MUTED).pack(anchor="w", padx=25, pady=(10, 4))
        tipo_box = ctk.CTkComboBox(janela, values=["entrada", "saida"])
        tipo_box.pack(fill="x", padx=25)
        tipo_box.set("entrada")
        ctk.CTkLabel(janela, text="Quantidade", text_color=MUTED).pack(anchor="w", padx=25, pady=(10, 4))
        quantidade = ctk.CTkEntry(janela)
        quantidade.pack(fill="x", padx=25)
        quantidade.insert(0, "1")
        def salvar():
            try:
                self.navigation.sistema.movimentar_estoque(opcoes[produto_box.get()], int(quantidade.get()), tipo_box.get())
                janela.destroy()
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Estoque atualizado.", parent=self)
            except Exception as erro:
                messagebox.showerror("Movimentação não realizada", str(erro), parent=janela)
        ctk.CTkButton(janela, text="Confirmar", fg_color="#167F76", hover_color="#126D66", command=salvar).pack(fill="x", padx=25, pady=20)
