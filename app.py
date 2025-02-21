from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Aplicação
app = Flask( __name__ )
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy( app ) # Associando o banco de dados a aplicação

@app.route( '/' )
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
