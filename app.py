from flask import Flask, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

from database import db
from models.user import User
from login_manager import login_manager

# Aplicação
app = Flask( __name__ )

# Configurando a aplicação (obrigatório)
app.config[ "SECRET_KEY" ] = "your_secret_key"
app.config[ "SQLALCHEMY_DATABASE_URI" ] = "sqlite:///database.db"

# Após a criação da instância do banco, é necessário iniciar as instâncias criadas com a aplicação
db.init_app( app )
login_manager.init_app( app )

login_manager.login_view = "login"


# Quando um usuário faz login no sistema, o Flask-Login armazena seu ID na sessão.
# Sempre que for necessário recuperar esse usuário (por exemplo, para verificar
# permissões ou exibir informações), o Flask-Login chamará automaticamente essa
# função load_user para carregar o objeto do usuário correspondente no banco de dados.
@login_manager.user_loader
def load_user( user_id: int ):
    return User.query.get( int( user_id ) )


@app.route( '/login', methods = [ 'POST' ] )  # Enviando dados
def login():
    # Recuperando as informações enviadas na requisição
    data = request.json

    username: str = data.get( 'username' )
    password: str = data.get( 'password' )

    # Se existir...
    if username and password:

        # O filter_by retorna uma lista. Uso first para retornar um registro.
        user = User.query.filter_by( username = username ).first()

        if user and user.password == password:
            # Username existe no banco e a senha digitada está certa

            # Autenticação do usuário logado
            login_user( user )
            return jsonify( { "message": "Autenticação realizada com sucesso!" } ), 200

    return jsonify( { "message": "Credenciais inválidas!" } ), 400


@app.route( '/logout', methods = [ 'GET' ] )
@login_required  # Necessário usuário autenticado
def logout():
    # Mét[odo próprio para logout
    logout_user()
    return jsonify( { "message": "Logout realizada com sucesso!" } ), 200


@app.route( '/user', methods = [ "POST" ] )
def create_user():
    # Recuperando as informações enviadas na requisição
    data = request.json

    username: str = data.get( 'username' )
    password: str = data.get( 'password' )

    # Se existir...
    if username and password:

        # Verificar se o username já existe
        if User.query.filter_by( username = username ).first():
            return jsonify( { "message": "Usuário já existe no sistema!" } ), 400

        # Adicionando o novo usuário
        user = User( username = username, password = password )
        db.session.add( user )
        db.session.commit()

        return jsonify( { "message": "Usuário cadastrado com sucesso!" } ), 200

    return jsonify( { "message": "Dados inválidas!" } ), 400


@app.route( '/user/<int:id_user>', methods = [ "GET" ] )
@login_required
def read_user( id_user: int ):

    # Busca a instância daquele usuário
    user = User.query.get( id_user )
    if user:
        return jsonify( { "message": user.username } ), 200

    return jsonify( { "message": "Usuário não encontrado!" } ), 404


@app.route( '/user/<int:id_user>', methods = [ "PUT" ] )
@login_required
def update_user( id_user: int ):
    # Busca a instância daquele usuário
    user = User.query.get( id_user )
    if not user:
        return jsonify( { "message": "Usuário não encontrado!" } ), 404

    data = request.json
    new_name = data.get( "username" )
    new_password = data.get( "password" )

    # Verifica se nenhum dos dados foi informado
    if not new_name and not new_password:
        return jsonify( { "message": "Nenhuma atualização informada!" } ), 400

    # Se username for informado, verifica se já não existe
    if new_name:
        other_user = User.query.filter_by( username = new_name ).first()
        if other_user and other_user.id != id_user:
            return jsonify( { "message": "Username não válido!" } ), 400
        user.username = new_name

    # Atualiza a senha, se informado
    if new_password:
        user.password = new_password

    db.session.commit()
    return jsonify( { "message": f"Usuário {id_user} atualizado com sucesso!" } ), 200


@app.route( '/user/<int:id_user>', methods = [ "DELETE" ] )
@login_required
def delete_user( id_user: int ):

    # Usuário não pode se autodeletar
    if id_user == current_user.id:
        return jsonify( { "message": "Deleção não permitida!" } ), 403

    # Busca a instância daquele usuário
    user = User.query.get( id_user )
    if user:

        db.session.delete( user )
        db.session.commit()

        return jsonify( { "message": f"Usuário {id_user} deletado com sucesso!" } ), 200

    return jsonify( { "message": "Usuário não encontrado!" } ), 404


if __name__ == '__main__':
    app.run()
