import json

def cargar_json(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except:
        return []

def guardar_json(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def inicializar_archivos():
    usuarios = cargar_json("usuarios.json")
    if len(usuarios) == 0:
        admin = {
            "id": "0000",
            "nombres": "Admin",
            "apellidos": "Administrador",
            "telefono": "555 000111",
            "email": "admin@acmeclinic.com",
            "direccion": "Cl 185 # 26 – 85",
            "rol": "Administrador",
            "clave": "admin"
        }
        guardar_json("usuarios.json", [admin])