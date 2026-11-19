import customtkinter as ctk
from tkinter import messagebox
from view.sidebar import Sidebar

BG, WHITE, DARK = "#141820", "#1D2430", "#F0F3F8"
MUTED, TEAL, BORDER = "#9AA6B5", "#20B8A8", "#303A49"


class VendasView(ctk.CTkFrame):
    PAGE_NAME, MENU_LABEL, MENU_ICON, MENU_ORDER, SHOW_IN_MENU = "vendas", "Vendas", "▣", 2, True

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
        ctk.CTkLabel(header, text="Vendas", text_color=DARK, font=ctk.CTkFont(size=26, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="+ Nova venda", fg_color="#167F76", hover_color="#126D66", height=40, command=self.nova_venda).grid(row=0, column=1, sticky="e")
        ctk.CTkLabel(content, text="Registre vendas utilizando os clientes e produtos cadastrados.", text_color=MUTED, font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", pady=(0, 20))
        self.painel = ctk.CTkFrame(content, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        self.painel.grid(row=2, column=0, sticky="nsew")
        ctk.CTkLabel(self.painel, text="Histórico de vendas", text_color=DARK, font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=20, pady=(18, 12))
        self.lista_vendas = ctk.CTkScrollableFrame(self.painel, fg_color="transparent")
        self.lista_vendas.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.atualizar_lista()

    def nova_venda(self):
        clientes = self.navigation.sistema.listar_clientes()
        produtos = [p for p in self.navigation.sistema.listar_produtos() if p["quantidade"] > 0]
        if not clientes:
            messagebox.showwarning("Cadastro necessário", "Cadastre pelo menos um cliente antes de registrar uma venda.", parent=self)
            return
        if not produtos:
            messagebox.showwarning("Estoque indisponível", "Cadastre um produto e informe uma quantidade em estoque antes de vender.", parent=self)
            return

        janela = ctk.CTkToplevel(self)
        janela.title("Nova venda")
        janela.geometry("440x390")
        janela.resizable(False, False)
        janela.configure(fg_color=BG)
        janela.transient(self.winfo_toplevel())
        janela.grab_set()
        ctk.CTkLabel(janela, text="Registrar venda", text_color=DARK, font=ctk.CTkFont(size=21, weight="bold")).pack(anchor="w", padx=25, pady=(25, 18))

        cliente_opcoes = {f"#{c['id']} - {c['nome']}": c["id"] for c in clientes}
        produto_opcoes = {f"#{p['id']} - {p['nome']} (estoque: {p['quantidade']})": p["id"] for p in produtos}
        ctk.CTkLabel(janela, text="Cliente", text_color=MUTED).pack(anchor="w", padx=25, pady=(7, 4))
        cliente_box = ctk.CTkComboBox(janela, values=list(cliente_opcoes), width=385, height=38)
        cliente_box.pack(padx=25)
        cliente_box.set(list(cliente_opcoes)[0])
        ctk.CTkLabel(janela, text="Produto", text_color=MUTED).pack(anchor="w", padx=25, pady=(12, 4))
        produto_box = ctk.CTkComboBox(janela, values=list(produto_opcoes), width=385, height=38)
        produto_box.pack(padx=25)
        produto_box.set(list(produto_opcoes)[0])
        ctk.CTkLabel(janela, text="Quantidade", text_color=MUTED).pack(anchor="w", padx=25, pady=(12, 4))
        quantidade = ctk.CTkEntry(janela, height=38, fg_color=WHITE, border_color=BORDER, text_color=DARK)
        quantidade.pack(fill="x", padx=25)
        quantidade.insert(0, "1")

        def salvar():
            try:
                cliente_id = cliente_opcoes[cliente_box.get()]
                produto_id = produto_opcoes[produto_box.get()]
                venda = self.navigation.sistema.registrar_venda(cliente_id, produto_id, int(quantidade.get()))
                janela.destroy()
                self.atualizar_lista()
                messagebox.showinfo("Venda registrada", f"Venda #{venda['id']} registrada.\nTotal: R$ {venda['total']:.2f}", parent=self)
            except Exception as erro:
                messagebox.showerror("Não foi possível registrar", str(erro), parent=janela)

        ctk.CTkButton(janela, text="Confirmar venda", height=40, fg_color="#167F76", hover_color="#126D66", command=salvar).pack(fill="x", padx=25, pady=22)

    def atualizar_lista(self):
        for widget in self.lista_vendas.winfo_children():
            widget.destroy()
        vendas = self.navigation.sistema.listar_vendas()
        if not vendas:
            ctk.CTkLabel(self.lista_vendas, text="Nenhuma venda cadastrada.", text_color=MUTED).pack(pady=35)
            return
        for venda in vendas:
            linha = ctk.CTkFrame(self.lista_vendas, fg_color="#28313E", corner_radius=8)
            linha.pack(fill="x", pady=5)
            linha.grid_columnconfigure(0, weight=1)
            data = venda.get("data", "")[:16].replace("T", " ")
            ctk.CTkLabel(linha, text=f"Venda #{venda['id']}  •  {venda['cliente']}  •  {venda['produto']}  •  Qtd: {venda['quantidade']}  •  {data}", text_color=DARK, anchor="w").grid(row=0, column=0, sticky="ew", padx=15, pady=15)
            ctk.CTkLabel(linha, text=f"R$ {venda['total']:.2f}", text_color=TEAL, font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=15)
