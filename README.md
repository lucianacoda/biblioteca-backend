# Biblioteca Escolar - Backend

### Autora: Luciana Coda ([GitHub](https://github.com/lucianacoda) e [E-mail](mailto:lcsg23@hotmail.com))

API para cadastro de alunos, livros e controle de empréstimos.
Projeto criado para avaliação da disciplina de **Desenvolvimento Full Stack Básico (40530010058_20250_02)** do curso de **[Pós-Graduação - Especialização em Engenharia de Software da PUC-Rio](https://especializacao.ccec.puc-rio.br/especializacao/engenharia-de-software)**.

## Descrição

Este projeto fornece uma API RESTful para gerenciar alunos, livros e empréstimos numa biblioteca escolar. Utiliza Flask, SQLAlchemy e Flasgger para documentação interativa.

## Instalação

Siga os passos abaixo para configurar o ambiente local:

1. Clone o repositório do backend e acesse a pasta correspondente:

```bash
git clone <URL_DO_REPOSITORIO_BACKEND>
cd <PASTA_DO_REPOSITORIO>
```

2. (Opcional, mas fortemente recomendado) Crie e ative um ambiente virtual Python:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências listadas no arquivo de requisitos:

```bash
pip install -r requirements.txt
```

## Inicialização

1. Execute a aplicação principal do backend:
```bash
python app.py
```

2. Acesse a documentação interativa da API através do navegador, utilizando o [endereço padrão](http://127.0.0.1:5000/apidocs):

## Observações

- O banco de dados SQLite será criado automaticamente na primeira execução.
- Certifique-se de que a porta ```5000``` está livre para uso.