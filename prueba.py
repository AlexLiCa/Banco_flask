from app import db, app
from cuenta import Cuenta  

with app.app_context():
    db.create_all() 
    print("Tablas creadas con éxito.")
