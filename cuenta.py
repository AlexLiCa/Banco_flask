
import json
import threading
import os

# Definir la ruta del archivo JSON
json_db_path = 'Cuentas.json'

# Función para leer los datos de las cuentas desde el archivo JSON


def cargar_datos():
    if not os.path.exists(json_db_path):
        return {}
    with open(json_db_path, 'r') as file:
        return json.load(file)

# Función para guardar los datos de las cuentas en el archivo JSON


def guardar_datos(datos):
    with open(json_db_path, 'w') as file:
        json.dump(datos, file, indent=4)


class Cuenta:
    def __init__(self, titular: str, no_cuenta: int, nip: int, saldo: float) -> None:
        self.nip = nip
        self.saldo = saldo
        self.no_cuenta = no_cuenta
        self.titular = titular
        self.lock_saldo = threading.Lock()

    def retira(self, cantidad: float, nip_recibido: int):
        if nip_recibido != self.nip:
            return False

        if cantidad > 0 and self.saldo >= cantidad:
            self.saldo -= cantidad
            self.actualiza_saldo_en_archivo()
            return True
        else:
            return False

    def deposita(self, cantidad: float):
        if cantidad > 0:
            self.saldo += cantidad
            self.actualiza_saldo_en_archivo()
            return True
        else:
            return False

    def actualiza_saldo_en_archivo(self):
        with self.lock_saldo:
            datos = cargar_datos()
            datos[str(self.no_cuenta)] = {
                "titular": self.titular, "no_cuenta": self.no_cuenta, "nip": self.nip, "saldo": self.saldo}
            guardar_datos(datos)

    def transfiere(self, cuenta_destino, monto: float):
        if self.no_cuenta == cuenta_destino.no_cuenta:
            return False

        elif self.retira(monto, self.nip):
            if cuenta_destino.deposita(monto):
                return True

        return False


def transferencia(no_origen : int, no_destino: int , monto: int):
    cuenta_origen = buscar_cuenta(no_origen)
    cuenta_destino = buscar_cuenta(no_destino)
    if cuenta_origen and cuenta_destino:
        return cuenta_origen.transfiere(cuenta_destino, monto)
    else: 
        return False

def retiro(no_cuenta: int, monto : float, nip: int):
    cuenta = buscar_cuenta(no_cuenta)
    if no_cuenta:
        return cuenta.retira(monto, nip)
    else:
        return False

def deposito(no_cuenta: int, monto: float):
    cuenta = buscar_cuenta(no_cuenta)
    if no_cuenta:
        return cuenta.deposita(monto)
    else:
        return False

def crea_cuenta(titular: str, nip: int, saldo: float = 0):
    datos = cargar_datos()
    no_cuenta = len(datos) + 1
    nueva_cuenta = Cuenta(titular, no_cuenta, nip, saldo)
    datos[str(no_cuenta)] = {"titular": titular,
                             "no_cuenta": no_cuenta, "nip": nip, "saldo": saldo}
    guardar_datos(datos)


def buscar_cuenta(no_cuenta: int):
    datos = cargar_datos()
    cuenta_data = datos.get(str(no_cuenta))
    if cuenta_data is not None:
        return Cuenta(titular=cuenta_data["titular"], no_cuenta=cuenta_data["no_cuenta"], nip=cuenta_data["nip"], saldo=cuenta_data["saldo"])
    else:
        return None


if __name__ == "__main__":
    print("esta bien")
