"""Camada de regras e persistência do SISGECO.

Os dados são armazenados em JSON para permanecerem disponíveis após fechar
 o programa. As Views não devem manter listas próprias: devem chamar SistemaModel.
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


class SistemaModel:
    def __init__(self, caminho_dados=None):
        raiz_projeto = Path(__file__).resolve().parents[2]
        self.caminho_dados = Path(caminho_dados) if caminho_dados else raiz_projeto / "data" / "sisgeco.json"
        self.caminho_dados.parent.mkdir(parents=True, exist_ok=True)
        self.dados = {
            "clientes": [],
            "produtos": [],
            "vendas": [],
            "proximos_ids": {"cliente": 1, "produto": 1, "venda": 1},
        }
        self._carregar()

    def _carregar(self):
        if not self.caminho_dados.exists():
            
            
            arquivo_legado = self.caminho_dados.parent / "clientes.json"
            if arquivo_legado.exists():
                try:
                    with arquivo_legado.open("r", encoding="utf-8") as arquivo:
                        clientes_legados = json.load(arquivo)
                    if isinstance(clientes_legados, list):
                        for item in clientes_legados:
                            self.dados["clientes"].append({
                                "id": int(item.get("id", len(self.dados["clientes"]) + 1)),
                                "nome": str(item.get("nome", "")).strip(),
                                "telefone": str(item.get("telefone", "")).strip(),
                                "email": str(item.get("email", "")).strip(),
                            })
                        maior_id = max((c["id"] for c in self.dados["clientes"]), default=0)
                        self.dados["proximos_ids"]["cliente"] = maior_id + 1
                except (json.JSONDecodeError, OSError, TypeError, ValueError):
                    raise RuntimeError(f"Não foi possível migrar os clientes de {arquivo_legado}.")
            self._salvar()
            return
        try:
            with self.caminho_dados.open("r", encoding="utf-8") as arquivo:
                carregado = json.load(arquivo)
            for chave in ("clientes", "produtos", "vendas"):
                if isinstance(carregado.get(chave), list):
                    self.dados[chave] = carregado[chave]
            proximos = carregado.get("proximos_ids", {})
            for tipo, chave in (("cliente", "clientes"), ("produto", "produtos"), ("venda", "vendas")):
                maior_id = max((item.get("id", 0) for item in self.dados[chave]), default=0)
                self.dados["proximos_ids"][tipo] = max(int(proximos.get(tipo, maior_id + 1)), maior_id + 1)
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            
            raise RuntimeError(f"Não foi possível ler os dados em {self.caminho_dados}.")

    def _salvar(self):
        temporario = self.caminho_dados.with_suffix(".tmp")
        with temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(self.dados, arquivo, ensure_ascii=False, indent=4)
        temporario.replace(self.caminho_dados)

    @staticmethod
    def _texto_obrigatorio(valor, campo):
        texto = str(valor or "").strip()
        if not texto:
            raise ValueError(f"Informe {campo}.")
        return texto

    
    def listar_clientes(self):
        return [dict(item) for item in self.dados["clientes"]]

    def buscar_cliente(self, cliente_id):
        return next((dict(c) for c in self.dados["clientes"] if c["id"] == int(cliente_id)), None)

    def cadastrar_cliente(self, nome, telefone="", email=""):
        cliente = {
            "id": self.dados["proximos_ids"]["cliente"],
            "nome": self._texto_obrigatorio(nome, "o nome do cliente"),
            "telefone": str(telefone or "").strip(),
            "email": str(email or "").strip(),
        }
        self.dados["clientes"].append(cliente)
        self.dados["proximos_ids"]["cliente"] += 1
        self._salvar()
        return dict(cliente)

    def editar_cliente(self, cliente_id, nome, telefone="", email=""):
        cliente = next((c for c in self.dados["clientes"] if c["id"] == int(cliente_id)), None)
        if cliente is None:
            return False
        cliente.update({
            "nome": self._texto_obrigatorio(nome, "o nome do cliente"),
            "telefone": str(telefone or "").strip(),
            "email": str(email or "").strip(),
        })
        self._salvar()
        return True

    def excluir_cliente(self, cliente_id):
        cliente_id = int(cliente_id)
        if any(v["cliente_id"] == cliente_id for v in self.dados["vendas"]):
            raise ValueError("Este cliente possui vendas registradas e não pode ser excluído.")
        antes = len(self.dados["clientes"])
        self.dados["clientes"] = [c for c in self.dados["clientes"] if c["id"] != cliente_id]
        if len(self.dados["clientes"]) == antes:
            return False
        self._salvar()
        return True

    
    def listar_produtos(self):
        return [dict(item) for item in self.dados["produtos"]]

    def buscar_produto(self, produto_id):
        return next((dict(p) for p in self.dados["produtos"] if p["id"] == int(produto_id)), None)

    def cadastrar_produto(self, nome, categoria, preco, quantidade=0):
        nome = self._texto_obrigatorio(nome, "o nome do produto")
        categoria = self._texto_obrigatorio(categoria, "a categoria")
        preco = float(preco)
        quantidade = int(quantidade)
        if preco <= 0 or quantidade < 0:
            raise ValueError("O preço deve ser maior que zero e a quantidade não pode ser negativa.")
        produto = {
            "id": self.dados["proximos_ids"]["produto"],
            "nome": nome,
            "categoria": categoria,
            "preco": round(preco, 2),
            "quantidade": quantidade,
        }
        self.dados["produtos"].append(produto)
        self.dados["proximos_ids"]["produto"] += 1
        self._salvar()
        return dict(produto)

    def editar_produto(self, produto_id, nome, categoria, preco):
        produto = next((p for p in self.dados["produtos"] if p["id"] == int(produto_id)), None)
        if produto is None:
            return False
        preco = float(preco)
        if preco <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        produto.update({
            "nome": self._texto_obrigatorio(nome, "o nome do produto"),
            "categoria": self._texto_obrigatorio(categoria, "a categoria"),
            "preco": round(preco, 2),
        })
        self._salvar()
        return True

    def excluir_produto(self, produto_id):
        produto_id = int(produto_id)
        if any(v["produto_id"] == produto_id for v in self.dados["vendas"]):
            raise ValueError("Este produto possui vendas registradas e não pode ser excluído.")
        antes = len(self.dados["produtos"])
        self.dados["produtos"] = [p for p in self.dados["produtos"] if p["id"] != produto_id]
        if len(self.dados["produtos"]) == antes:
            return False
        self._salvar()
        return True

    
    def listar_estoque(self):
        return self.listar_produtos()

    def movimentar_estoque(self, produto_id, quantidade, tipo):
        produto = next((p for p in self.dados["produtos"] if p["id"] == int(produto_id)), None)
        if produto is None:
            raise ValueError("Produto não encontrado.")
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if tipo == "entrada":
            produto["quantidade"] += quantidade
        elif tipo == "saida":
            if produto["quantidade"] < quantidade:
                raise ValueError("Estoque insuficiente para essa saída.")
            produto["quantidade"] -= quantidade
        else:
            raise ValueError("Tipo de movimentação inválido.")
        self._salvar()
        return dict(produto)

    
    def listar_vendas(self):
        return [dict(item) for item in sorted(self.dados["vendas"], key=lambda v: v["id"], reverse=True)]

    def registrar_venda(self, cliente_id, produto_id, quantidade):
        cliente = next((c for c in self.dados["clientes"] if c["id"] == int(cliente_id)), None)
        produto = next((p for p in self.dados["produtos"] if p["id"] == int(produto_id)), None)
        if cliente is None:
            raise ValueError("Selecione um cliente cadastrado.")
        if produto is None:
            raise ValueError("Selecione um produto cadastrado.")
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if produto["quantidade"] < quantidade:
            raise ValueError("Não há quantidade suficiente desse produto no estoque.")

        total = round(produto["preco"] * quantidade, 2)
        venda = {
            "id": self.dados["proximos_ids"]["venda"],
            "cliente_id": cliente["id"],
            "cliente": cliente["nome"],
            "produto_id": produto["id"],
            "produto": produto["nome"],
            "quantidade": quantidade,
            "preco_unitario": produto["preco"],
            "total": total,
            "data": datetime.now().isoformat(timespec="seconds"),
            "status": "Concluída",
        }
        produto["quantidade"] -= quantidade
        self.dados["vendas"].append(venda)
        self.dados["proximos_ids"]["venda"] += 1
        self._salvar()
        return dict(venda)

    
    def obter_resumo(self):
        vendas = self.dados["vendas"]
        faturamento = sum(v["total"] for v in vendas)
        return {
            "faturamento": round(faturamento, 2),
            "total_vendas": len(vendas),
            "total_clientes": len(self.dados["clientes"]),
            "total_produtos": len(self.dados["produtos"]),
            "ticket_medio": round(faturamento / len(vendas), 2) if vendas else 0.0,
        }

    def obter_vendas_mensais(self):
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        totais = {i: 0 for i in range(1, 13)}
        for venda in self.dados["vendas"]:
            try:
                mes = datetime.fromisoformat(venda["data"]).month
                totais[mes] += 1
            except (KeyError, ValueError):
                continue
        return [(meses[i - 1], totais[i]) for i in range(1, 13)]

    def obter_produtos_mais_vendidos(self):
        totais = {}
        for venda in self.dados["vendas"]:
            nome = venda["produto"]
            totais[nome] = totais.get(nome, 0) + venda["quantidade"]
        return sorted(totais.items(), key=lambda item: item[1], reverse=True)[:5]

    def obter_vendas_recentes(self, limite=5):
        resultado = []
        for venda in self.listar_vendas()[:limite]:
            resultado.append((
                f"#{venda['id']:06d}", venda["cliente"], venda["produto"],
                f"R$ {venda['total']:.2f}", venda["status"]
            ))
        return resultado



class Registro(ABC):
    @abstractmethod
    def registrar(self):
        pass

    def editar(self):
        pass

    def deletar(self):
        pass


class Cliente(Registro):
    def __init__(self, nome, uid):
        self.nome = nome
        self.uid = uid

    def get_nome(self):
        return self.nome

    def get_uid(self):
        return self.uid

    def registrar(self):
        return self


class Produto(Registro):
    def __init__(self, nome, idd, val, categoria="", quantidade=0):
        self.nome = nome
        self.idd = idd
        self.val = val
        self.categoria = categoria
        self.quantidade = quantidade

    def get_nome(self):
        return self.nome

    def get_idd(self):
        return self.idd

    def get_val(self):
        return self.val

    def registrar(self):
        return self


class Venda(Registro):
    def __init__(self, idd, prod, val, cli, quantidade=1, data=None):
        self.idd = idd
        self.prod = prod
        self.val = val
        self.cli = cli
        self.quantidade = quantidade
        self.data = data or datetime.now().isoformat(timespec="seconds")

    def get_idd(self):
        return self.idd

    def get_prod(self):
        return self.prod

    def get_val(self):
        return self.val

    def get_cli(self):
        return self.cli

    def registrar(self):
        return self


class Historico_Vendas:
    def __init__(self, data=None, vendas=None):
        self.data = data or datetime.now().isoformat(timespec="seconds")
        self.vendas = list(vendas or [])


class Estoque:
    def __init__(self, item=None, quantidade=0, estoque=None):
        self.item = item
        self.quantidade = quantidade
        self.estoque = list(estoque or [])

    def get_item(self):
        return self.item

    def get_quantidade(self):
        return self.quantidade

    def adicionar_estoque(self, quantidade):
        quantidade = int(quantidade)
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser positiva.")
        self.quantidade += quantidade

    def remover_estoque(self, quantidade):
        quantidade = int(quantidade)
        if quantidade <= 0 or quantidade > self.quantidade:
            raise ValueError("Quantidade de saída inválida.")
        self.quantidade -= quantidade


class Relatorio:
    def __init__(self, sistema=None):
        self.sistema = sistema

    def gerar(self):
        return self.sistema.obter_resumo() if self.sistema else {}
