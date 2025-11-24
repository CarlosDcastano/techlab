import csv
import os
import tempfile
from datetime import datetime, date
from typing import List, Dict, Optional
import equipos


PRESTAMOS_CSV = "data/prestamos.csv"




TIPOS_MAX = {
    'ESTUDIANTE': 3,
    'INSTRUCTOR': 7,
    'ADMINISTRATIVO': 10
}




def leer_prestamos(path: str = PRESTAMOS_CSV) -> List[Dict]:
    prestamos = []
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalizar y convertir tipos numéricos donde aplique
                prestamos.append({
                'prestamo_id': int(row['prestamo_id']),
                'equipo_id': int(row['equipo_id']),
                'nombre_equipo': row['nombre_equipo'],
                'usuario_prestatario': row['usuario_prestatario'],
                'tipo_usuario': row['tipo_usuario'].upper(),
                'fecha_solicitud': row['fecha_solicitud'],
                'fecha_prestamo': row.get('fecha_prestamo',''),
                'fecha_devolucion': row.get('fecha_devolucion',''),
                'dias_autorizados': int(row['dias_autorizados']) if row.get('dias_autorizados') else 0,
                'dias_reales_usados': int(row['dias_reales_usados']) if row.get('dias_reales_usados') else 0,
                'retraso': row.get('retraso','').upper(),
                'estado': row['estado'].upper(),
                'mes': int(row['mes']) if row.get('mes') else 0,
                'anio': int(row['anio']) if row.get('anio') else 0
                })
    except FileNotFoundError:
        guardar_prestamos([], path)
    return prestamos




def guardar_prestamos(prestamos: List[Dict], path: str = PRESTAMOS_CSV) -> None:
    fieldnames = ['prestamo_id','equipo_id','nombre_equipo','usuario_prestatario','tipo_usuario','fecha_solicitud','fecha_prestamo','fecha_devolucion','dias_autorizados','dias_reales_usados','retraso','estado','mes','anio']
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp()
    with os.fdopen(fd, 'w', encoding='utf-8', newline='') as tmpf:
        writer = csv.DictWriter(tmpf, fieldnames=fieldnames)
        writer.writeheader()
        for p in prestamos:
            writer.writerow({
                'prestamo_id': p['prestamo_id'],
                'equipo_id': p['equipo_id'],
                'nombre_equipo': p['nombre_equipo'],
                'usuario_prestatario': p['usuario_prestatario'],
                'tipo_usuario': p['tipo_usuario'],
                'fecha_solicitud': p['fecha_solicitud'],
                'fecha_prestamo': p.get('fecha_prestamo',''),
                'fecha_devolucion': p.get('fecha_devolucion',''),
                'dias_autorizados': p.get('dias_autorizados',0),
                'dias_reales_usados': p.get('dias_reales_usados',0),
                'retraso': p.get('retraso',''),
                'estado': p['estado'],
                'mes': p.get('mes',0),
                'anio': p.get('anio',0)
            })
    os.replace(tmp, path)




def gen_id(path: str = PRESTAMOS_CSV) -> int:
    prestamos = leer_prestamos(path)
    if not prestamos:
        return 1
    return max(p['prestamo_id'] for p in prestamos) + 1




def parsear_fecha(texto: str) -> date:
    # formato esperado YYYY-MM-DD
    return datetime.strptime(texto, '%Y-%m-%d').date()




def dias_max(tipo_usuario: str) -> int:
    return TIPOS_MAX.get(tipo_usuario.upper(), 0)




def equipo_disponible_para_prestar(equipo_id: int) -> tuple[bool, str]:
    e = equipos.buscar_equipo_por_id(equipo_id)
    if e is None:
        return False, 'Equipo no encontrado.'
    if e['estado_actual'] != 'DISPONIBLE':
        return False, f"Equipo no está DISPONIBLE (estado_actual={e['estado_actual']})."
    # Verificar que no haya préstamos APROBADOS sin devolver
    prestamos = leer_prestamos()
    for p in prestamos:
        if p['equipo_id'] == equipo_id and p['estado'] == 'APROBADO':
            return False, 'El equipo tiene un préstamo APROBADO sin devolución.'
    return True, ''




def registrar_solicitud(equipo_id: int, nombre_prestatario: str, tipo_usuario: str,
                        fecha_prestamo_text: str, dias_solicitados: int) -> tuple[bool, str]:

    tipo_usuario = tipo_usuario.upper()

    # Validar tipo de usuario
    if tipo_usuario not in TIPOS_MAX:
        return False, 'Tipo de usuario inválido.'

    # Validar días
    if dias_solicitados > dias_max(tipo_usuario):
        return False, (
            f"Solicitud rechazada: días solicitados ({dias_solicitados}) exceden "
            f"máximo permitido para {tipo_usuario} ({dias_max(tipo_usuario)})."
        )

    # Validar fecha
    try:
        fecha_prestamo = parsear_fecha(fecha_prestamo_text)
    except Exception:
        return False, 'Fecha inválida. Use formato YYYY-MM-DD.'

    # Validar disponibilidad del equipo
    disponible, msg = equipo_disponible_para_prestar(equipo_id)
    if not disponible:
        return False, msg

    # Obtener nombre del equipo
    equipo = equipos.buscar_equipo_por_id(equipo_id)
    if equipo is None:
        return False, "Equipo no encontrado."

    # Crear registro de préstamo
    prestamo_id = gen_id()

    registro = {
        'prestamo_id': prestamo_id,
        'equipo_id': equipo_id,
        'nombre_equipo': equipo["nombre_equipo"],
        'usuario_prestatario': nombre_prestatario,
        'tipo_usuario': tipo_usuario,
        'fecha_solicitud': fecha_prestamo_text,
        'fecha_prestamo': fecha_prestamo_text,
        'fecha_devolucion': "",
        'dias_autorizados': dias_solicitados,
        'dias_reales_usados': 0,
        'retraso': "",
        'estado': 'PENDIENTE',
        'mes': fecha_prestamo.month,
        'anio': fecha_prestamo.year
    }

    # Guardar
    prestamos = leer_prestamos()
    prestamos.append(registro)
    guardar_prestamos(prestamos)

    return True, f"Solicitud registrada con ID {prestamo_id}."
