import csv
from typing import Optional


USUARIOS_CSV = "data/usuarios.csv"




def leer_usuarios(path: str = USUARIOS_CSV) -> list:
    usuarios = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                usuarios.append({
                'usuario': row.get('usuario','').strip(),
                'contrasena': row.get('contrasena',''),
                'rol': row.get('rol','').strip().upper()
                })
    except FileNotFoundError:
        pass
    return usuarios




def validar_credenciales(usuario: str, contrasena: str, path: str = USUARIOS_CSV) -> bool:
    usuarios = leer_usuarios(path)
    for u in usuarios:
        if u['usuario'] == usuario and u['contrasena'] == contrasena and u['rol'] == 'ADMIN':
            return True
    return False




if __name__ == '__main__':
    print("Módulo usuarios. Prueba rápida:")
    print(leer_usuarios())