import customtkinter as ctk
from tkinter import messagebox
from view.sidebar import Sidebar

BG, WHITE, DARK = "#141820", "#1D2430", "#F0F3F8"
MUTED, TEAL, BORDER = "#9AA6B5", "#20B8A8", "#303A49"


class ClientesView(ctk.CTkFrame):
    PAGE_NAME, MENU_LABEL, MENU_ICON, MENU_ORDER, SHOW_IN_MENU = "clientes", "Clientes", "♙", 3, True

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
        ctk.CTkLabel(header, text="Clientes", text_color=DARK, font=ctk.CTkFont(size=26, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="+ Novo cliente", fg_color="#167F76", hover_color="#126D66", height=40, command=lambda: self.abrir_formulario()).grid(row=0, column=1, sticky="e")
        ctk.CTkLabel(content, text="Cadastre, consulte e gerencie os clientes da empresa.", text_color=MUTED, font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", pady=(0, 18))
        painel = ctk.CTkFrame(content, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        painel.grid(row=2, column=0, sticky="nsew")
        painel.grid_columnconfigure(0, weight=1)
        painel.grid_rowconfigure(1, weight=1)
        self.pesquisa = ctk.CTkEntry(painel, placeholder_text="Pesquisar por nome, telefone ou e-mail...", height=40, fg_color=BG, border_color=BORDER, text_color=DARK)
        self.pesquisa.grid(row=0, column=0, sticky="ew", padx=18, pady=18)
        self.pesquisa.bind("<KeyRelease>", lambda e: self.atualizar_lista())
        self.lista_clientes = ctk.CTkScrollableFrame(painel, fg_color="transparent")
        self.lista_clientes.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.atualizar_lista()

    def abrir_formulario(self, cliente=None):
        janela = ctk.CTkToplevel(self)
        janela.title("Editar cliente" if cliente else "Novo cliente")
        janela.geometry("430x390")
        janela.resizable(False, False)
        janela.configure(fg_color=BG)
        janela.transient(self.winfo_toplevel())
        janela.grab_set()
        ctk.CTkLabel(janela, text="Editar cliente" if cliente else "Cadastrar cliente", text_color=DARK, font=ctk.CTkFont(size=21, weight="bold")).pack(anchor="w", padx=25, pady=(25, 20))
        campos = {}
        for chave, rotulo in (("nome", "Nome completo"), ("telefone", "Telefone"), ("email", "E-mail")):
            ctk.CTkLabel(janela, text=rotulo, text_color=MUTED).pack(anchor="w", padx=25, pady=(8, 4))
            entrada = ctk.CTkEntry(janela, height=38, fg_color=WHITE, border_color=BORDER, text_color=DARK)
            entrada.pack(fill="x", padx=25)
            if cliente:
                entrada.insert(0, cliente.get(chave, ""))
            campos[chave] = entrada

        def salvar():
            try:
                valores = [campos[k].get().strip() for k in ("nome", "telefone", "email")]
                if not valores[0] or not valores[1]:
                    raise ValueError("Informe o nome e o telefone do cliente.")
                if cliente:
                    self.navigation.sistema.editar_cliente(cliente["id"], *valores)
                else:
                    self.navigation.sistema.cadastrar_cliente(*valores)
                janela.destroy()
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!", parent=self)
            except Exception as erro:
                messagebox.showerror("Não foi possível salvar", str(erro), parent=janela)

        ctk.CTkButton(janela, text="Salvar cliente", height=40, fg_color="#167F76", hover_color="#126D66", command=salvar).pack(fill="x", padx=25, pady=25)

    def excluir_cliente(self, cliente):
        if not messagebox.askyesno("Excluir cliente", f"Deseja excluir {cliente['nome']}?", parent=self):
            return
        try:
            self.navigation.sistema.excluir_cliente(cliente["id"])
            self.atualizar_lista()
        except Exception as erro:
            messagebox.showerror("Não foi possível excluir", str(erro), parent=self)

    def atualizar_lista(self):
        for widget in self.lista_clientes.winfo_children():
            widget.destroy()
        busca = self.pesquisa.get().strip().lower()
        clientes = [c for c in self.navigation.sistema.listar_clientes() if busca in c["nome"].lower() or busca in c["telefone"].lower() or busca in c["email"].lower()]
        if not clientes:
            ctk.CTkLabel(self.lista_clientes, text="Nenhum cliente encontrado." if busca else "Nenhum cliente cadastrado.", text_color=MUTED).pack(pady=35)
            return
        header = ctk.CTkFrame(self.lista_clientes, fg_color="#28313E", corner_radius=6)
        header.pack(fill="x", pady=(0, 8))
        for i, titulo in enumerate(("CÓDIGO", "NOME", "TELEFONE", "E-MAIL", "AÇÕES")):
            header.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(header, text=titulo, text_color="#AEB9C8", font=ctk.CTkFont(size=10, weight="bold"), anchor="w").grid(row=0, column=i, sticky="ew", padx=8, pady=12)
        for cliente in clientes:
            row = ctk.CTkFrame(self.lista_clientes, fg_color="transparent")
            row.pack(fill="x", pady=2)
            vals = (f"#{cliente['id']}", cliente["nome"], cliente["telefone"], cliente["email"] or "-")
            for i, val in enumerate(vals):
                row.grid_columnconfigure(i, weight=1)
                ctk.CTkLabel(row, text=val, text_color=DARK, font=ctk.CTkFont(size=11), anchor="w").grid(row=0, column=i, sticky="ew", padx=8, pady=10)
            acoes = ctk.CTkFrame(row, fg_color="transparent")
            acoes.grid(row=0, column=4, padx=4)
            ctk.CTkButton(acoes, text="Editar", width=58, height=28, command=lambda c=cliente: self.abrir_formulario(c)).pack(side="left", padx=2)
            ctk.CTkButton(acoes, text="Excluir", width=58, height=28, fg_color="#8B3942", hover_color="#702D35", command=lambda c=cliente: self.excluir_cliente(c)).pack(side="left", padx=2)
            ctk.CTkFrame(self.lista_clientes, height=1, fg_color=BORDER).pack(fill="x")
