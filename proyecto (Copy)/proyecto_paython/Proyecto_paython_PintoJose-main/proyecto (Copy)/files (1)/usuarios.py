import random
from persistencia import cargar_json, guardar_json


def generar_contrasena():
    letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numeros = "0123456789"
    especiales = "!@#$%&*"
    clave = ""
    for i in range(4):
        clave = clave + random.choice(letras)
    for i in range(4):
        clave = clave + random.choice(numeros)
    for i in range(2):
        clave = clave + random.choice(especiales)
    return clave

def iniciar_sesion():
    print("\n--- LOGIN ---")
    email = input("E-mail: ")
    clave = input("Contraseña: ")
    usuarios = cargar_json("usuarios.json")
    for u in usuarios:
        if u["email"] == email and u["clave"] == clave:
            return u
    print("Datos incorrectos.")
    return None

def registrar_usuario():
    while True:
        print("\n--- REGISTRAR USUARIO ---")
        usuarios = cargar_json("usuarios.json")
        id_nuevo = input("Identificación: ")
        if id_nuevo.isdigit():
            break
        else:
            print("Por favor dijite solo dijitos numericos")
            input("Presione enter para continuar")
            continue

    for u in usuarios:
        if u["id"] == id_nuevo:
            print("Ese usuario ya existe.")
            return

    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    while True:
        telefono = input("Teléfono: ")
        if telefono.isdigit():
            break
        else:
            print("Por favor dijite solo dijitos numericos")
            input("Presione enter para continuar")
            continue
        
    email = input("E-mail corporativo: ")
    direccion = input("Dirección: ")
    op_rol = input("Rol (1. Administrador / 2. Medico): ")
    if op_rol == "1":
        rol = "Administrador"
    else:
        rol = "Medico"

    clave = generar_contrasena()
    nuevo = {
        "id": id_nuevo,
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "email": email,
        "direccion": direccion,
        "rol": rol,
        "clave": clave
    }
    usuarios.append(nuevo)
    guardar_json("usuarios.json", usuarios)
    print("Usuario creado. CONTRASEÑA ASIGNADA:", clave)

def eliminar_usuario():
    print("\n--- ELIMINAR DOCTOR ---")
    id_borrar = input("Identificación del doctor a eliminar: ")
    if id_borrar == "0000":
        print("No se puede eliminar al Administrador principal.")
        return

    usuarios = cargar_json("usuarios.json")
    for u in usuarios:
        if u["id"] == id_borrar:
            print("Doctor:", u["nombres"], u["apellidos"], "-", u["rol"])
            confirmar = input("¿Seguro que desea eliminarlo? (s/n): ")
            if confirmar == "s":
                usuarios.remove(u)
                guardar_json("usuarios.json", usuarios)
                print("Doctor eliminado.")
            return
    print("Doctor no encontrado.")