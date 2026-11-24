from persistencia import cargar_json, guardar_json
from pacientes import buscar_paciente

def diagnosticar_paciente(medico):
    print("\n--- DIAGNOSTICAR PACIENTE ---")
    id_paciente = input("Identificación del paciente: ")
    paciente = buscar_paciente(id_paciente)
    if paciente == None:
        print("El paciente no existe. Debe registrarlo primero.")
        return

    fecha = input("Fecha de la consulta (DD/MM/AAAA): ")

    sintomas = []
    seguir = "s"
    while seguir == "s":
        s = input("Ingrese síntoma: ")
        sintomas.append(s)
        seguir = input("¿Agregar otro síntoma? (s/n): ")

    diagnostico = input("Diagnóstico (patología): ")

    medicamentos = []
    seguir = "s"
    while seguir == "s":
        nombre = input("Medicamento: ")
        cantidad = input("Cantidad: ")
        dosis = input("Dosis diaria: ")
        tiempo = input("Tiempo de aplicación (días): ")
        med = {
            "medicamento": nombre,
            "cantidad": cantidad,
            "dosis": dosis,
            "tiempo": tiempo
        }
        medicamentos.append(med)
        seguir = input("¿Agregar otro medicamento? (s/n): ")

    consulta = {
        "id_paciente": id_paciente,
        "fecha": fecha,
        "medico": medico["nombres"] + " " + medico["apellidos"],
        "sintomas": sintomas,
        "diagnostico": diagnostico,
        "medicamentos": medicamentos
    }
    prescripciones = cargar_json("prescripciones.json")
    prescripciones.append(consulta)
    guardar_json("prescripciones.json", prescripciones)
    print("Diagnóstico guardado en JSON correctamente.")

def consultar_historia_clinica():
    print("\n--- HISTORIA CLÍNICA ---")
    id_paciente = input("Identificación del paciente: ")
    paciente = buscar_paciente(id_paciente)
    if paciente == None:
        print("El paciente no existe.")
        return

    print("\n=== ENCABEZADO: DATOS DEL PACIENTE ===")
    print("ID:", paciente["id"])
    print("Nombre:", paciente["nombres"], paciente["apellidos"])
    print("Teléfono:", paciente["telefono"])
    print("Email:", paciente["email"])
    print("Dirección:", paciente["direccion"])
    print("Género:", paciente["genero"])
    print("Estado Civil:", paciente["estado_civil"])

    print("\n=== CUERPO: HISTORIAL DE CONSULTAS ===")
    prescripciones = cargar_json("prescripciones.json")
    while True:
        for c in prescripciones:
            if c["id_paciente"] == id_paciente:
                print("--------------------------------------")
                print("Fecha:", c["fecha"])
                print("Médico que atendió:", c["medico"])
                print("Síntomas:", c["sintomas"])
                print("Diagnóstico:", c["diagnostico"])
                print("Medicamentos prescritos:")
                for m in c["medicamentos"]:
                    print(" -", m["medicamento"], "| Cant:", m["cantidad"], "| Dosis:", m["dosis"], "| Días:", m["tiempo"])
        input("Presione enter para continuar")
        break