from db import db
from werkzeug.security import generate_password_hash


class Cuenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titular = db.Column(db.String(80), nullable=False)
    nip = db.Column(db.Integer, nullable=False)
    saldo = db.Column(db.Float, nullable=False)
    password = db.Column(db.String(513), nullable=False)

    def __repr__(self):
        return f'<Cuenta {self.id}>'


def crea_cuenta(titular : str, nip: int, password: str, saldo : float =0):
    nueva_cuenta = Cuenta(titular=titular, nip=nip, saldo=saldo,
                          password=generate_password_hash(password))
    db.session.add(nueva_cuenta)
    db.session.commit()
    return nueva_cuenta


def deposito(no_cuenta: int, monto: float):
    cuenta = Cuenta.query.get(no_cuenta)
    if cuenta:
        cuenta.saldo += monto
        db.session.commit()
        return {'success': True, 'saldo': cuenta.saldo, 'message': 'Deposito exitoso'}
    else:
        return {'success': False, 'message': 'Cuenta no encontrada'}


def retiro(no_cuenta: int, monto: float, nip: int):
    cuenta = Cuenta.query.get(no_cuenta)
    if cuenta and cuenta.nip == nip:
        if cuenta.saldo >= monto:
            cuenta.saldo -= monto
            db.session.commit()
            return {'success': True, 'saldo': cuenta.saldo, 'message': 'Retiro exitoso'}
        else:
            return {'success': False, 'message': 'Saldo insuficiente'}
    else:
        return {'success': False, 'message': 'Cuenta no encontrada o NIP incorrecto'}


def transferencia(no_origen: int, no_destino: int, monto: float):
    origen = Cuenta.query.get(no_origen)
    destino = Cuenta.query.get(no_destino)
    if origen and destino:
        if origen.saldo >= monto:
            origen.saldo -= monto
            destino.saldo += monto
            db.session.commit()
            return {'success': True, 'saldo_origen': origen.saldo, 'saldo_destino': destino.saldo, 'message': 'Transferencia exitosa'}
        else:
            return {'success': False, 'message': 'Saldo insuficiente en cuenta origen'}
    else:
        return {'success': False, 'message': 'Una o ambas cuentas no encontradas'}
