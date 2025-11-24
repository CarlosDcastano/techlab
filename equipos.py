import csv
import os
import tempfile
from datetime import date
from typing import Optional, List, Dict

EQUIPOS_CSV = "data/equipos.csv"

def leer_equipos(path: str = EQUIPOS_CSV) -> List[Dict]:
    equipos = []
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                equipos.append({
                    'equipo_id': int(row.get('equipo_id', 0)),
                    'nombre_equipo': row.get('nombre_equipo', ''),
                    'categoria': row.get('categoria', ''),
                    'estado_actual': row.get('estado_actual', '').upper(),
                    'fecha_registro': row.get('fecha_registro', ''),
                    'descripcion': row.get('descripcion', '')
                })
    except FileNotFoundError:
        # Crear archivo con cabecera si no existe
        guardar_equipos([], path)
    return equipos


def guardar_equipos(equipos: List[Dict], path: str = EQUIPOS_CSV) -> None:
    fieldnames = ['equipo_id', 'nombre_equipo', 'categoria',
                  'estado_actual', 'fecha_registro', 'descripcion']

    os.makedirs(os.path.dirname(path), exist_ok=True)

    fd, tmp = tempfile.mkstemp()
    with os.fdopen(fd, 'w', encoding='utf-8', newline='') as tmpf:
        writer = csv.DictWriter(tmpf, fieldnames=fieldnames)
        writer.writeheader()
        for e in equipos:
            writer.writerow({
                'equipo_id': e['equipo_id'],
                'nombre_equipo': e['nombre_equipo'],
                'categoria': e['categoria'],
                'estado_actual': e['estado_actual'],
                'fecha_registro': e['fecha_registro'],
                'descripcion': e.get('descripcion', '')
            })

    import shutil
    shutil.copyfile(tmp, path)
    os.remove(tmp)


def gen_id(path: str = EQUIPOS_CSV) -> int:
    equipos = leer_equipos(path)
    if not equipos:
        return 1
    return max(e['equipo_id'] for e in equipos) + 1


def agregar_equipo(nombre: str, categoria: str, descripcion: str = '',
                   estado: str = 'DISPONIBLE', path: str = EQUIPOS_CSV) -> Dict:

    equipos = leer_equipos(path)
    nuevo_id = gen_id(path)
    hoy = date.today().isoformat()

    equipo = {
        'equipo_id': nuevo_id,
        'nombre_equipo': nombre,
        'categoria': categoria,
        'estado_actual': estado.upper(),
        'fecha_registro': hoy,
        'descripcion': descripcion
    }

    equipos.append(equipo)
    guardar_equipos(equipos, path)
    return equipo


def listar_equipos(path: str = EQUIPOS_CSV) -> List[Dict]:
    return leer_equipos(path)


def buscar_equipo_por_id(equipo_id: int, path: str = EQUIPOS_CSV) -> Optional[Dict]:
    equipos = leer_equipos(path)
    for e in equipos:
        if e['equipo_id'] == equipo_id:
            return e
    return None


def actualizar_estado_equipo(equipo_id: int, nuevo_estado: str,
                             path: str = EQUIPOS_CSV) -> bool:

    equipos = leer_equipos(path)
    cambiado = False

    for e in equipos:
        if e['equipo_id'] == equipo_id:
            e['estado_actual'] = nuevo_estado.upper()
            cambiado = True
            break

    if cambiado:
        guardar_equipos(equipos, path)

    return cambiado


if __name__ == '__main__':
    print("Módulo equipos. Prueba rápida:")
    equipos = listar_equipos()
    for e in equipos:
        print(e)
