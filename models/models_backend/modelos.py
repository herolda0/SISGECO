class Cliente:
    def __init__(self, nome, uid):
        self.__nome = nome
        self.__uid = uid

    def get_nome(self):
        return self.__nome

    def get_uid(self):
        return self.__uid

    def registrar_cliente(self, nome):
        return Cliente(nome, 0)

    def deletar_cliente(self):
        del(self)

class Produto:
    def __init__(self, nome, idd, val):
        self.__nome = nome
        self.__idd = idd
        self.__val = val

    def get_nome(self):
        return self.__nome

    def get_idd(self):
        return self.__idd

    def get_val(self):
        return self.__val
    
    def registrar_produto(nome, val):
        return Produto(nome, 0, val)

class Venda:
    def __init__(self, idd, prod, val, cli):
        self.__cli = cli
        self.__idd = idd
        self.__prod = prod
        self.__val = val

    def get_idd(self):
        return self.__idd
    
    def get_prod(self):
        return self.__prod
    
    def get_val(self):
        return self.__val

    def get_cli(self):
        return self.__cli

    def registrar_venda(self, prod, cli):
        return Venda(0, prod, prod.get_val(), cli)

    def deletar_venda(self):
        del(self)

class Historico_Vendas:
    def __init__(self, data, vendas):
        pass

class Estoque:
    def __init__(self, item, quantidade, estoque):
        self.__item = item
        self.__quantidade = quantidade
        self.__estoque = []

    def get_item(self):
        return self.__item

    def get_quantidade(self):
        return self.__quantidade

    def adicionar_estoque(self, item):
        self.__estoque.append(item)

    def remover_estoque(self, item):
        self.__estoque.remove(item)

class Relatorio:
    def __init__(self):
        pass