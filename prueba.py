from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABESE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo Cuenta
class Cuenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titular = db.Column(db.String(80), nullable=False)
    nip = db.Column(db.Integer, nullable=False)
    saldo = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Cuenta {self.id}>'

# Creación de la tabla e inserción de datos

def setup_database():
    with app.app_context():
        db.create_all()  # Crea las tablas
        nueva_cuenta = Cuenta(titular='Alejandro', nip=123,
                              saldo=1000)  # Crea una nueva cuenta
        # Agrega la cuenta a la sesión de la base de datos
        db.session.add(nueva_cuenta)
        db.session.commit()  # Guarda los cambios en la base de datos

# Verificación de la inserción


def verificar_cuenta():
    with app.app_context():
        cuenta = Cuenta.query.filter_by(titular='Alejandro').first()
        if cuenta:
            print(
                f'Cuenta encontrada: {cuenta.titular}, NIP: {cuenta.nip}, Saldo: {cuenta.saldo}')
        else:
            print('La cuenta no fue encontrada.')


if __name__ == '__main__':
    setup_database()
    verificar_cuenta()
