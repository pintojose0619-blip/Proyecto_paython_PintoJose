from persistencia import inicializar_archivos
from usuarios import iniciar_sesion, registrar_usuario, eliminar_usuario
from pacientes import registrar_paciente
from reportes import reporte_anual_diagnosticos

from diagnosticos import diagnosticar_paciente, consultar_historia_clinica

def menu_admin():
    while True:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Registrar doctor")
        print("2. Registrar paciente")
        print("3. Consultar historia clínica")
        print("4. Eliminar doctor")
        print("5. Cerrar sesión")
        print("6.reporte anual de disgnosticos")
        op = input("Opción: ")

        if op == "1":
            registrar_usuario()
        elif op == "2":
            registrar_paciente()
        elif op == "3":
            consultar_historia_clinica()
        elif op == "4":
            eliminar_usuario()
        elif op == "5":
            break
        elif op == "6":
            reporte_anual_diagnosticos()

def menu_medico(usuario):
    while True:
        print("\n--- MENÚ MÉDICO ---")
        print("1. Registrar paciente")
        print("2. Diagnosticar paciente")
        print("3. Consultar historia clínica")
        print("4. Cerrar sesión")
        op = input("Opción: ")

        if op == "1":
            registrar_paciente()
        elif op == "2":
            diagnosticar_paciente(usuario)
        elif op == "3":
            consultar_historia_clinica()
        elif op == "4":
            break

def main():
    inicializar_archivos()
    while True:
        print("\n=== CLÍNICA ACME ===")
        print("1. Iniciar sesión")
        print("2. Salir")
        op = input("Opción: ")

        if op == "1":
            usuario = iniciar_sesion()
            if usuario != None:
                if usuario["rol"] == "Administrador":
                    menu_admin()
                else:
                    menu_medico(usuario)
        elif op == "2":
            break

main()