from flask import Flask, request, jsonify
from cuenta import deposito, transferencia, retiro, cargar_datos,crea_cuenta 

app = Flask(__name__)


@app.route('/deposito', methods=['POST'])
def handle_deposito():
    data = request.json
    no_cuenta = data.get('no_cuenta')
    monto = data.get('monto')
    if deposito(no_cuenta, monto):
        saldo = cargar_datos().get(str(no_cuenta)).get('saldo')
        return jsonify(success=True, saldo=saldo)
    else:
        return jsonify(success=False), 400


@app.route('/transferencia', methods=['POST'])
def handle_transferencia():
    data = request.json
    no_origen = data.get('no_origen')
    no_destino = data.get('no_destino')
    monto = data.get('monto')
    if transferencia(no_origen, no_destino, monto):
        datos = cargar_datos()
        saldo_origen = datos.get(str(no_origen)).get('saldo')
        saldo_destino = datos.get(str(no_destino)).get('saldo')
        return jsonify(success=True, saldo_origen=saldo_origen, saldo_destino=saldo_destino)
    else:
        return jsonify(success=False), 400


@app.route('/retiro', methods=['POST'])
def handle_retiro():
    data = request.json
    no_cuenta = data.get('no_cuenta')
    monto = data.get('monto')
    nip = data.get('nip')
    if retiro(no_cuenta, monto, nip):
        saldo = cargar_datos().get(str(no_cuenta)).get('saldo')
        return jsonify(success=True, saldo=saldo)
    else:
        return jsonify(success=False), 400


@app.route('/crear_cuenta', methods=['POST'])
def handle_crear_cuenta():
    data = request.json
    titular = data.get('titular')
    nip = data.get('nip')
    saldo = data.get('saldo', 0)

    try:
        crea_cuenta(titular, nip, saldo)
        datos = cargar_datos()
        no_cuenta = max(datos.keys(), key=int)
        saldo = datos[no_cuenta]['saldo']
        return jsonify(success=True, no_cuenta=no_cuenta, saldo=saldo)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 400



if __name__ == '__main__':
    app.run(debug=True)
