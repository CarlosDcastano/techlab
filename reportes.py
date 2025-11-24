import csv
import os
from typing import List
import prestamos

def exportar_reporte(mes: int, anio: int, destino_folder: str = '.', prefix: str = 'reporte_prestamos') -> tuple[bool, str]:
    # Filtrar prestamos DEVUELTOS por mes y año
    datos = [p for p in prestamos.leer_prestamos() if p['estado'] == 'DEVUELTO' and p['mes'] == mes and p['anio'] == anio]
    if not datos:
        return False, f'No se encontraron préstamos DEVUELTOS para mes={mes} año={anio}.'
    os.makedirs(destino_folder, exist_ok=True)
    filename = f"{prefix}_{anio:04d}_{mes:02d}.csv"
    path = os.path.join(destino_folder, filename)
    fieldnames = ['prestamo_id','equipo_id','nombre_equipo','usuario_prestatario','tipo_usuario','dias_autorizados','dias_reales_usados','retraso','estado','mes','anio']
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in datos:
            writer.writerow({k: p[k] for k in fieldnames})
    return True, f'Reporte exportado en: {path}'

if __name__ == '__main__':
    ok, msg = exportar_reporte(3,2025, destino_folder='.')
    print(ok, msg)
