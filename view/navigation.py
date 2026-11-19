
import importlib
import inspect
import pkgutil

import view
from models.models_backend.modelos import SistemaModel
from models.dashboard_model import DashboardModel


class Navigation:

    def __init__(self, container):

        self.container = container
        self.tela_atual = None
        self.pagina_atual = None

        
        
        self.sistema = SistemaModel()
        self.dashboard_model = DashboardModel(self.sistema)

        self.paginas = {}

        self.descobrir_paginas()

    def descobrir_paginas(self):

        self.paginas.clear()

        for _, module_name, _ in pkgutil.iter_modules(view.__path__):

            if module_name in ("navigation", "sidebar", "__init__"):
                continue

            try:
                modulo = importlib.import_module(
                    f"view.{module_name}"
                )

                for _, classe in inspect.getmembers(
                    modulo,
                    inspect.isclass
                ):

                    if classe.__module__ != modulo.__name__:
                        continue

                    nome_pagina = getattr(
                        classe,
                        "PAGE_NAME",
                        None
                    )

                    if nome_pagina:
                        self.paginas[nome_pagina] = classe

            except Exception as erro:
                print(
                    f"Erro ao carregar {module_name}: {erro}"
                )

    def obter_menu(self):

        menu = []

        for nome, classe in self.paginas.items():

            if not getattr(classe, "SHOW_IN_MENU", True):
                continue

            menu.append({
                "nome": nome,
                "titulo": getattr(
                    classe,
                    "MENU_LABEL",
                    nome.capitalize()
                ),
                "icone": getattr(
                    classe,
                    "MENU_ICON",
                    "▣"
                ),
                "ordem": getattr(
                    classe,
                    "MENU_ORDER",
                    99
                )
            })

        return sorted(
            menu,
            key=lambda item: item["ordem"]
        )

    def mostrar_tela(self, nome):

        classe_pagina = self.paginas.get(nome)

        if classe_pagina is None:
            print(f"Página não encontrada: {nome}")
            return

        if self.tela_atual is not None:
            self.tela_atual.destroy()
            self.tela_atual = None

        self.pagina_atual = nome

        self.tela_atual = classe_pagina(
            self.container,
            self
        )

        self.tela_atual.pack(
            fill="both",
            expand=True
        )
