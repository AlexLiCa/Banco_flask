from flask import Flask, request, jsonify
from db import db
from cuenta import Cuenta, deposito, transferencia, retiro, crea_cuenta
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://banquitobd_distribuidos_user:WyBjSnJcaqpYP6OKNtq7bX2UBz9XYoD6@dpg-cn52q5f109ks73f0qjc0-a.oregon-postgres.render.com/banquitobd_distribuidos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()  # Crea las tablas si no existen

# Tus rutas y lógica de la aplicación aquí



@app.route('/deposito', methods=['POST'])
def handle_deposito():
    data = request.json
    resultado = deposito(data.get('no_cuenta'), data.get('monto'))
    if resultado['success']:
        return jsonify(resultado)
    else:
        return jsonify(resultado), 400


@app.route('/transferencia', methods=['POST'])
def handle_transferencia():
    data = request.json
    resultado = transferencia(data.get('no_origen'),
                              data.get('no_destino'), data.get('monto'))
    if resultado['success']:
        return jsonify(resultado)
    else:
        return jsonify(resultado), 400


@app.route('/retiro', methods=['POST'])
def handle_retiro():
    data = request.json
    resultado = retiro(data.get('no_cuenta'),
                       data.get('monto'), data.get('nip'))
    if resultado['success']:
        return jsonify(resultado)
    else:
        return jsonify(resultado), 400


@app.route('/crear_cuenta', methods=['POST'])
def handle_crear_cuenta():
    data = request.json
    try:
        cuenta = crea_cuenta(data.get('titular'),
                             data.get('nip'), data.get('saldo', 0))
        return jsonify(success=True, no_cuenta=cuenta.id, saldo=cuenta.saldo)
    except:
        return jsonify(success=False, message="Error al crear la cuenta"), 400


@app.route('/cuentas', methods=['GET'])
def obtener_cuentas():
    cuentas_lista = Cuenta.query.all()  # Consulta todas las cuentas
    cuentas = []
    for cuenta in cuentas_lista:
        cuentas.append({
            'id': cuenta.id,
            'titular': cuenta.titular,
            'nip': cuenta.nip,  # Ten cuidado con exponer datos sensibles como el NIP
            'saldo': cuenta.saldo
        })
    return jsonify(cuentas)


if __name__ == '__main__':
    app.run(debug=True)
