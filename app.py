from datetime import datetime as dt
from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import db, Aluno, Livro, Emprestimo, AlunoSchema, LivroSchema, EmprestimoSchema, APIReturn

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
CORS(app)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Biblioteca Escolar API",
        "description": "API para cadastro de alunos, livros e controle de empréstimos.",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "tags": [
        {"name": "Alunos", "description": "Operações relacionadas a alunos"},
        {"name": "Livros", "description": "Operações relacionadas a livros"},
        {"name": "Empréstimos", "description": "Operações de empréstimo e devolução"}
    ]
}
swagger = Swagger(app, template=swagger_template)

with app.app_context():
    db.create_all()

## Endpoints de alunos
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    """
    Cadastra um novo aluno
    ---
    tags:
        - Alunos
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            properties:
              nome:
                type: string
              matricula:
                type: string
              email:
                type: string
              telefone:
                type: string
    responses:
        200:
          description: Aluno cadastrado com sucesso
    """
    try:
        data = request.json
        aluno = Aluno(
            nome=data['nome'],
            matricula=data['matricula'],
            email=data['email'],
            telefone=data['telefone']
        )
        db.session.add(aluno)
        db.session.commit()
        return jsonify(APIReturn(_id=aluno.id, _message="Aluno cadastrado com sucesso").to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(e), 500

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    """
    Lista todos os alunos matriculados
    ---
    tags:
        - Alunos
    responses:
        200:
          description: Lista de alunos matriculados
    """
    try:
        return jsonify(AlunoSchema(many=True).dump(Aluno.query.all()))
    except Exception as e:
        return jsonify(e), 500

## Endpoints de livros
@app.route('/livros', methods=['POST'])
def cadastrar_livro():
    """
    Cadastra um novo livro
    ---
    tags:
        - Livros
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            properties:
              titulo:
                type: string
              autor:
                type: string
              editora:
                type: string
              edicao:
                type: integer
              ano_publicacao:
                type: integer
    responses:
        200:
          description: Livro cadastrado com sucesso
    """
    try:
        data = request.json
        livro = Livro(
            titulo=data['titulo'],
            autor=data['autor'],
            editora=data['editora'],
            edicao=data['edicao'],
            ano_publicacao=data['ano_publicacao']
        )
        db.session.add(livro)
        db.session.commit()
        return jsonify(APIReturn(_id=livro.id, _message="Livro cadastrado com sucesso").to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(e), 500

@app.route('/livros', methods=['GET'])
def listar_livros():
    """
    Lista todos os livros cadastrados
    ---
    tags:
        - Livros
    responses:
        200:
          description: Lista de livros cadastrados
    """
    try:
        return jsonify(LivroSchema(many=True).dump(Livro.query.all()))
    except Exception as e:
        return jsonify(e), 500

## Endpoints de empréstimos
@app.route('/emprestimos', methods=['POST'])
def emprestar():
    """
    Realiza empréstimo de livro
    ---
    tags:
        - Empréstimos
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            properties:
              aluno_id:
                type: integer
              livro_id:
                type: integer
    responses:
        200:
          description: Empréstimo de livro realizado com sucesso
    """
    try:
        data = request.json
        livro = Livro.query.get_or_404(data['livro_id'])
        if not livro or not livro.disponivel:
            return jsonify(APIReturn(_message= 'Erro: Livro não disponível.')), 400
        emprestimo = Emprestimo(
            aluno_id=data['aluno_id'],
            livro_id=data['livro_id']
        )
        db.session.add(emprestimo)
        db.session.commit()
        livro.disponivel = False
        db.session.add(emprestimo)
        db.session.commit()
        message = (f"Empréstimo realizado com sucesso para livro {emprestimo.livro_id} - {emprestimo.livro.titulo} "
                   f"e aluno {emprestimo.aluno.matricula} - {emprestimo.aluno.nome}")
        return jsonify(APIReturn(_id=emprestimo.id, _message=message).to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(e), 500

@app.route('/emprestimos', methods=['PUT'])
def devolver():
    """
    Devolve livro emprestado
    ---
    tags:
        - Empréstimos
    parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            properties:
              emprestimo_id:
                type: integer
    responses:
        200:
          description: Livro devolvido com sucesso
    """
    try:
        data = request.json
        emprestimo = Emprestimo.query.get_or_404(data['emprestimo_id'])
        if not emprestimo or emprestimo.data_devolucao:
            return jsonify({'error': 'Empréstimo inválido'}), 400
        emprestimo.data_devolucao = dt.fromisoformat(dt.now().isoformat())
        db.session.add(emprestimo)
        emprestimo.livro.disponivel = True
        emprestimo.devolvido_em_atraso = emprestimo.data_limite_devolucao < emprestimo.data_devolucao
        suffix = ", porém em atraso." if emprestimo.devolvido_em_atraso == True else "."
        db.session.commit()
        return jsonify(APIReturn(_id=emprestimo.id, _message=f"Livro devolvido com sucesso{suffix}").to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(e), 500

@app.route('/emprestimos', methods=['GET'])
def listar_emprestimos():
    """
    Lista todos os emprestimos feitos
    ---
    tags:
        - Empréstimos
    responses:
        200:
          description: Lista de empréstimos
    """
    try:
        return jsonify(EmprestimoSchema(many=True).dump(Emprestimo.query.all()))
    except Exception as e:
        return jsonify(e), 500

if __name__ == '__main__':
    app.run(debug=True)