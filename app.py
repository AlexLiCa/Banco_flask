from flask import Flask, request, jsonify
from db import db
from cuenta import Cuenta, deposito, transferencia, retiro, crea_cuenta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABESE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Config JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()  

@app.route('/deposito', methods=['POST'])
def handle_deposito():
    data = request.json
    resultado = deposito(data.get('no_cuenta'), float(data.get('monto')))
    if resultado['success']:
        return jsonify(resultado)
    else:
        return jsonify(resultado), 400


@app.route('/transferencia', methods=['POST'])
def handle_transferencia():
    data = request.json
    resultado = transferencia(int(data.get('no_origen')),
                              int(data.get('no_destino')), float(data.get('monto')))
    if resultado['success']:
        return jsonify(resultado)
    else:
        return jsonify(resultado), 400


@app.route('/retiro', methods=['POST'])
def handle_retiro():
    data = request.json
    resultado = retiro(data.get('no_cuenta'),
                       float(data.get('monto')), int(data.get('nip')))
    if resultado['success']:
        return jsonify(resultado)
    else:
        return jsonify(resultado), 400


@app.route('/crear_cuenta', methods=['POST'])
def handle_crear_cuenta():
    data = request.json
    try:
        cuenta = crea_cuenta(data.get('titular'),
                             int(data.get('nip')),
                             data.get('password'),
                             float(data.get('saldo', 0)))
        return jsonify(success=True, no_cuenta=cuenta.id, saldo=cuenta.saldo)
    except Exception as e:
        return jsonify(success=False, message=f"Error al crear la cuenta: {e}"), 400

@app.route('/cuentas', methods=['GET'])
#@jwt_required
def obtener_cuentas():
    cuentas_lista = Cuenta.query.all()
    cuentas = []
    for cuenta in cuentas_lista:
        cuentas.append({
            'id': cuenta.id,
            'titular': cuenta.titular,
            'nip': cuenta.nip,  
            'saldo': cuenta.saldo
        })
    return jsonify(cuentas)

def validar_usuario(username, password):
    user = Cuenta.query.filter_by(titular=username).first()
    if user and check_password_hash(user.password, password):
        return True
    else :
        return False

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        username = data.get("titular")
        password = data.get("password")
        if validar_usuario(username, password):
            acces_token = create_access_token(identity=username)
            return jsonify(succes = True , JWT =acces_token, message="Login exitoso"), 200
        else:
            return jsonify(success=False, message="Usuario o Contraseña incorrectos"), 401
    except:
        return jsonify(success=False, message="Credenciales incorrectas"), 401

if __name__ == '__main__':
    app.run(debug=True)
