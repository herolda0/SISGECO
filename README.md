# SISGECO — Sistema de Gestão Comercial

O **SISGECO** é um sistema desktop desenvolvido em Python com o objetivo de auxiliar no gerenciamento de atividades comerciais, reunindo funcionalidades de controle e organização em uma única aplicação.

O projeto utiliza uma interface gráfica moderna e uma estrutura organizada em módulos, buscando facilitar a utilização, manutenção e evolução do sistema.

## Funcionalidades

O sistema conta com os seguintes módulos:

- **Dashboard:** painel inicial com uma visão geral das informações do sistema.
- **Clientes:** gerenciamento de clientes cadastrados.
- **Produtos:** organização e gerenciamento de produtos.
- **Estoque:** acompanhamento e controle de estoque.
- **Vendas:** gerenciamento das operações de venda.
- **Relatórios:** área destinada à visualização de informações e resultados.
- **Configurações:** opções de configuração do sistema.

## Tecnologias utilizadas

- **Python:** linguagem principal de desenvolvimento.
- **CustomTkinter:** biblioteca utilizada para construção da interface gráfica.
- **Programação Orientada a Objetos (POO):** organização e estruturação do código.

## Estrutura do projeto

```text
SISGECO/
│
├── data/
│
├── models/
│   ├── models_backend/
│   └── dashboard_model.py
│
├── view/
│   ├── clientes_view.py
│   ├── configuracoes_view.py
│   ├── dashboard_view.py
│   ├── estoque_view.py
│   ├── navigation.py
│   ├── produtos_view.py
│   ├── relatorios_view.py
│   ├── sidebar.py
│   └── vendas_view.py
│
├── main.py
├── requirements.txt
└── .gitignore
```

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/herolda0/SISGECO.git
```

### 2. Acesse a pasta

```bash
cd SISGECO
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o sistema

```bash
python main.py
```

## Objetivo acadêmico

O SISGECO foi desenvolvido como projeto acadêmico, com a finalidade de aplicar conhecimentos de desenvolvimento de software, construção de interfaces gráficas, organização de código e Programação Orientada a Objetos.

---

**Projeto:** SISGECO — Sistema de Gestão Comercial
