from app import db, app
from cuenta import Cuenta  # Importa todos los modelos que necesites

with app.app_context():
    db.create_all()  # Crea las tablas según los modelos definidos
    print("Tablas creadas con éxito.")
