from db import db
from cuenta import Cuenta
from app import app


def borrar_tabla_cuenta():
    with app.app_context():  
        try:
            db.drop_all()
            db.session.commit()  
            print("Tabla borrada exitosamente.")
        except Exception as e:
            print(f"Error al borrar la tabla: {e}")


if __name__ == "__main__":
    borrar_tabla_cuenta()
