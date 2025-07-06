from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt, timedelta as td
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome = db.Column(db.String(120), nullable=False)
    matricula = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefone = db.Column(db.String(120), nullable=False, unique=True)

class AlunoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Aluno
        load_instance = True

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    titulo = db.Column(db.String(120), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    editora = db.Column(db.String(120), nullable=False)
    edicao = db.Column(db.Integer, nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

class LivroSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Livro
        load_instance = True

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    data_emprestimo = db.Column(
        db.DateTime,
        default=dt.fromisoformat(dt.now().isoformat()),
        nullable=False
    )
    data_devolucao = db.Column(db.DateTime, nullable=True)
    data_limite_devolucao = db.Column(
        db.DateTime,
        default=(dt.now() + td(days=7)).replace(hour=23, minute=59, second=59),
        nullable=False
    )
    devolvido_em_atraso = db.Column(db.Boolean, nullable=True)
    aluno = db.relationship('Aluno')
    livro = db.relationship('Livro')

class EmprestimoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Emprestimo
        load_instance = True
        include_fk = True

class APIReturn:
    def __init__(self, _message: str, _id: int=None):
        self.id = _id
        self.message = _message

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message
        }