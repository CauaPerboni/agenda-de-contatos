# Agenda de Contatos

Este projeto é uma aplicação de agenda de contatos desenvolvida em Python utilizando a biblioteca PyQt5. Esta aplicação permite adicionar, editar, remover e buscar contatos, além de exportar a lista de contatos para um arquivo CSV.

## Funcionalidades

- **Adicionar Contato**: Insira o nome, telefone e email do contato.
- **Editar Contato**: Selecione um contato na lista e faça alterações.
- **Remover Contato**: Exclua um contato selecionado da lista.
- **Buscar Contato**: Pesquise contatos por nome, telefone ou email.
- **Exportar Contatos**: Salve a lista de contatos em um arquivo CSV.

## Tecnologias Utilizadas

- Python
- PyQt5
- SQLite3

## Pré-requisitos

Antes de executar o projeto, você precisará ter Python e as bibliotecas necessárias instaladas. Você pode instalar o PyQt5 usando pip:

    ´´´bash
    pip install PyQt5

## Banco de Dados

O projeto utiliza SQLite para armazenar os contatos. O arquivo do banco de dados será criado automaticamente ao executar a aplicação pela primeira vez.

## Uso

1. Clone o repositório:
    ´´´bash
    git clone https://github.com/seu-usuario/agenda-contatos.git
    cd agenda-contatos

2. Execute a aplicação:
    ´´´bash
    python main.py
