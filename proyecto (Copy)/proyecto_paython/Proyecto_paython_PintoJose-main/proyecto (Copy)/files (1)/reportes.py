from collections import Counter
from datetime import datetime
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def _cargar_json_seguro(nombre_archivo, default):
    ruta = BASE_DIR / nombre_archivo
    if not ruta.exists():
        return default
    try:
        with ruta.open("r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
            return contenido if contenido is not None else default
    except (json.JSONDecodeError, OSError):
        return default


def _parsear_fecha(valor_fecha):
    if not valor_fecha or not isinstance(valor_fecha, str):
        return None
    texto = valor_fecha.strip()
    formatos = (
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
    )
    for fmt in formatos:
        try:
            return datetime.strptime(texto, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(texto)
    except ValueError:
        return None


def reporte_anual_diagnosticos():
    diagnosticos = _cargar_json_seguro("diagnosticos.json", [])
    usuarios = _cargar_json_seguro("usuarios.json", [])
    _ = _cargar_json_seguro("pacientes.json", []) 


    if isinstance(diagnosticos, dict):
        diagnosticos = diagnosticos.get("diagnosticos", [])
    if isinstance(usuarios, dict):
        usuarios = usuarios.get("usuarios", [])

    medicos_validos = set()
    if isinstance(usuarios, list):
        for u in usuarios:
            if isinstance(u, dict) and str(u.get("rol", "")).lower() in ("medico", "médico", "doctor"):
                for clave in ("id", "cedula", "documento", "usuario", "nombre"):
                    if u.get(clave) is not None:
                        medicos_validos.add(str(u[clave]).strip())

    grupos_por_anio = {}
    diagnosticos_invalidos = 0

    if not isinstance(diagnosticos, list):
        diagnosticos = []

    for idx, item in enumerate(diagnosticos):
        if not isinstance(item, dict):
            diagnosticos_invalidos += 1
            continue

        fecha_raw = (
            item.get("fecha")
            or item.get("fecha_registro")
            or item.get("fecha_diagnostico")
        )
        fecha_dt = _parsear_fecha(fecha_raw)

        if fecha_dt is None:
            diagnosticos_invalidos += 1
            print(f"[Aviso] Diagnóstico #{idx + 1} omitido por fecha inválida o ausente: {fecha_raw!r}")
            continue

        anio = fecha_dt.strftime("%Y")
        grupos_por_anio.setdefault(anio, []).append((fecha_dt, str(fecha_raw).strip(), item))

    resultado_anios = {}

    for anio in sorted(grupos_por_anio.keys()):
        registros = grupos_por_anio[anio]

        registros.sort(key=lambda tupla: tupla[0])

        total_diagnosticos = len(registros)
        medicos_anio = set()
        pacientes_anio = set()
        total_sintomas = 0
        total_medicamentos = 0
        conteo_nombres_diagnostico = Counter()

        for _, _, diag in registros:

            medico_ref = (
                diag.get("medico_id")
                or diag.get("id_medico")
                or diag.get("medico")
                or diag.get("doctor")
            )
            if medico_ref is not None and str(medico_ref).strip():
                med_str = str(medico_ref).strip()
                if not medicos_validos or med_str in medicos_validos:
                    medicos_anio.add(med_str)

            paciente_ref = (
                diag.get("paciente_id")
                or diag.get("id_paciente")
                or diag.get("paciente")
                or diag.get("cedula_paciente")
            )
            if paciente_ref is not None and str(paciente_ref).strip():
                pacientes_anio.add(str(paciente_ref).strip())


            sintomas = diag.get("sintomas", [])
            if isinstance(sintomas, list):
                total_sintomas += len(sintomas)
            elif isinstance(sintomas, str) and sintomas.strip():
                total_sintomas += len([s for s in sintomas.split(",") if s.strip()])


            medicamentos = diag.get("medicamentos", [])
            if isinstance(medicamentos, list):
                total_medicamentos += len(medicamentos)
            elif isinstance(medicamentos, str) and medicamentos.strip():
                total_medicamentos += len([m for m in medicamentos.split(",") if m.strip()])


            nombre_diag = (
                diag.get("diagnostico")
                or diag.get("nombre_diagnostico")
                or diag.get("enfermedad")
                or diag.get("titulo")
                or "Sin especificar"
            )
            conteo_nombres_diagnostico[str(nombre_diag).strip()] += 1

        diagnostico_mas_comun = (
            conteo_nombres_diagnostico.most_common(1)[0][0]
            if conteo_nombres_diagnostico
            else None
        )

        primer_raw, primer_item = registros[0][1], registros[0][2]
        ultimo_raw, ultimo_item = registros[-1][1], registros[-1][2]

        primer_texto = primer_item.get("diagnostico") or primer_item.get("enfermedad") or "Diagnóstico"
        ultimo_texto = ultimo_item.get("diagnostico") or ultimo_item.get("enfermedad") or "Diagnóstico"

        resultado_anios[anio] = {
            "total_diagnosticos": total_diagnosticos,
            "medicos_participantes": len(medicos_anio),
            "pacientes_atendidos": len(pacientes_anio),
            "promedio_sintomas": round(total_sintomas / total_diagnosticos, 1) if total_diagnosticos else 0.0,
            "promedio_medicamentos": round(total_medicamentos / total_diagnosticos, 1) if total_diagnosticos else 0.0,
            "diagnostico_mas_comun": diagnostico_mas_comun,
            "primer_diagnostico": f"{primer_texto} ({primer_raw})",
            "ultimo_diagnostico": f"{ultimo_texto} ({ultimo_raw})",
        }

    reporte_final = {"años": resultado_anios}
    ruta_salida = BASE_DIR / "reporte_anual_diagnosticos.json"

    with ruta_salida.open("w", encoding="utf-8") as f_out:
        json.dump(reporte_final, f_out, indent=2, ensure_ascii=False)

    print(f"\nReporte generado exitosamente en: {ruta_salida}")
    print(f"Años procesados: {len(resultado_anios)} | Registros omitidos por fecha inválida: {diagnosticos_invalidos}")
    return reporte_final