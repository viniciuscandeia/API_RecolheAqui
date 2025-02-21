from app import db

class User(db.Model):
    __tablename__ = 'users'

    # Definindo as colunas da tabela
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
            db.String(80),
            unique=True,
            nullable=False,)
    password = db.Column(db.String(100), nullable=False)
