from persistencia import cargar_json, guardar_json

def buscar_paciente(id_buscar):
    pacientes = cargar_json("pacientes.json")
    for p in pacientes:
        if p["id"] == id_buscar:
            return p
    return None

def registrar_paciente():
    print("\n--- REGISTRAR PACIENTE ---")
    id_nuevo = input("Identificación: ")
    if buscar_paciente(id_nuevo) != None:
        print("El paciente ya está registrado.")
        return

    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    while True:
        telefono = input("Teléfono: ")
        if telefono.isdigit():
            break
        else:
            print("El numero telefonico deben ser solo dijitos numericos")
            input("Presione enter para continuar")
            continue
    email = input("E-mail: ")
    direccion = input("Dirección: ")
    genero = input("Género: ")
    estado_civil = input("Estado civil: ")

    nuevo = {
        "id": id_nuevo,
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "email": email,
        "direccion": direccion,
        "genero": genero,
        "estado_civil": estado_civil
    }
    pacientes = cargar_json("pacientes.json")
    pacientes.append(nuevo)
    guardar_json("pacientes.json", pacientes)
    print("Paciente registrado con éxito.")

