import usuarios
import equipos
import prestamos
import reportes

def solicitar_input_fecha(prompt: str) -> str:
    texto = input(prompt).strip()
    return texto

def menu_gestion_equipos():
    while True:
        print('\n--- GESTIÓN DE EQUIPOS ---')
        print('1. Registrar equipo')
        print('2. Listar equipos')
        print('3. Consultar equipo por ID')
        print('4. Volver')
        opcion = input('Elija opción: ').strip()
        if opcion == '1':
            nombre = input('Nombre del equipo: ').strip()
            categoria = input('Categoría: ').strip()
            descripcion = input('Descripción (opcional): ').strip()
            equipo = equipos.agregar_equipo(nombre, categoria, descripcion)
            print('Equipo registrado:', equipo)
        elif opcion == '2':
            lista = equipos.listar_equipos()
            print('\nID | Nombre | Categoría | Estado')
            for e in lista:
                print(f"{e['equipo_id']} | {e['nombre_equipo']} | {e['categoria']} | {e['estado_actual']}")
        elif opcion == '3':
            try:
                id_bus = int(input('Ingrese ID del equipo: ').strip())
            except ValueError:
                print('ID inválido.')
                continue
            e = equipos.buscar_equipo_por_id(id_bus)
            if e:
                for k,v in e.items():
                    print(f"{k}: {v}")
            else:
                print('Equipo no encontrado.')
        elif opcion == '4':
            break
        else:
            print('Opción inválida.')

def menu_gestion_prestamos():
    while True:
        print('\n--- GESTIÓN DE PRÉSTAMOS ---')
        print('1. Registrar solicitud de préstamo')
        print('2. Listar solicitudes PENDIENTES')
        print('3. Aprobar solicitud')
        print('4. Rechazar solicitud')
        print('5. Registrar devolución')
        print('6. Listar préstamos APROBADOS sin devolver')
        print('7. Volver')
        opcion = input('Elija opción: ').strip()
        if opcion == '1':
            try:
                equipo_id = int(input('ID del equipo: ').strip())
            except ValueError:
                print('ID inválido.')
                continue
            nombre = input('Nombre solicitante: ').strip()
            tipo = input('Tipo usuario (ESTUDIANTE/INSTRUCTOR/ADMINISTRATIVO): ').strip().upper()
            fecha_prestamo = solicitar_input_fecha('Fecha inicio préstamo (YYYY-MM-DD): ')
            try:
                dias = int(input('Días solicitados: ').strip())
            except ValueError:
                print('Días inválidos.')
                continue
            ok, msg = prestamos.registrar_solicitud(equipo_id, nombre, tipo, fecha_prestamo, dias)
            print(msg)
        elif opcion == '2':
            pendientes = prestamos.listar_pendientes()
            if not pendientes:
                print('No hay solicitudes PENDIENTES.')
            else:
                for p in pendientes:
                    print(f"ID {p['prestamo_id']} - Equipo {p['equipo_id']} ({p['nombre_equipo']}) - Solicitante: {p['usuario_prestatario']} - Dias autorizados: {p['dias_autorizados']}")
        elif opcion == '3':
            try:
                pid = int(input('ID de solicitud a aprobar: ').strip())
            except ValueError:
                print('ID inválido.')
                continue
            ok, msg = prestamos.aprobar_prestamo(pid)
            print(msg)
        elif opcion == '4':
            try:
                pid = int(input('ID de solicitud a rechazar: ').strip())
            except ValueError:
                print('ID inválido.')
                continue
            ok, msg = prestamos.rechazar_prestamo(pid)
            print(msg)
        elif opcion == '5':
            try:
                pid = int(input('ID del préstamo (APROBADO) a devolver: ').strip())
            except ValueError:
                print('ID inválido.')
                continue
            fecha_dev = solicitar_input_fecha('Fecha de devolución (YYYY-MM-DD): ')
            ok, msg = prestamos.registrar_devolucion(pid, fecha_dev)
            print(msg)
        elif opcion == '6':
            aprobados = prestamos.listar_aprobados_sin_devolucion()
            if not aprobados:
                print('No hay préstamos APROBADOS sin devolver.')
            else:
                for p in aprobados:
                    print(f"ID {p['prestamo_id']} - Equipo {p['equipo_id']} ({p['nombre_equipo']}) - Solicitante: {p['usuario_prestatario']} - Fecha prestamo: {p['fecha_prestamo']}")
        elif opcion == '7':
            break
        else:
            print('Opción inválida.')

def menu_historial():
    while True:
        print('\n--- HISTORIAL ---')
        print('1. Historial por equipo (ID)')
        print('2. Historial por usuario (nombre)')
        print('3. Volver')
        opcion = input('Elija opción: ').strip()
        if opcion == '1':
            try:
                eid = int(input('ID equipo: ').strip())
            except ValueError:
                print('ID inválido.')
                continue
            registros = prestamos.historial_por_equipo(eid)
            if not registros:
                print('No hay registros para ese equipo.')
            else:
                for r in registros:
                    print(r)
        elif opcion == '2':
            nombre = input('Nombre usuario (exacto): ').strip()
            registros = prestamos.historial_por_usuario(nombre)
            if not registros:
                print('No hay registros para ese usuario.')
            else:
                for r in registros:
                    print(r)
        elif opcion == '3':
            break
        else:
            print('Opción inválida.')

def menu_reportes():
    print('\n--- EXPORTAR REPORTE CSV ---')
    try:
        mes = int(input('Mes (1-12): ').strip())
        anio = int(input('Año (ej. 2025): ').strip())
    except ValueError:
        print('Mes o año inválido.')
        return
    ok, msg = reportes.exportar_reporte(mes, anio, destino_folder='.')
    print(msg)

def menu_principal():
    while True:
        print('\n=== TechLab - Menú Principal ===')
        print('1. Gestión de equipos')
        print('2. Gestión de préstamos')
        print('3. Historial')
        print('4. Exportar reporte CSV (DEVUELTOS por mes/año)')
        print('5. Salir')
        opcion = input('Elija opción: ').strip()
        if opcion == '1':
            menu_gestion_equipos()
        elif opcion == '2':
            menu_gestion_prestamos()
        elif opcion == '3':
            menu_historial()
        elif opcion == '4':
            menu_reportes()
        elif opcion == '5':
            print('Saliendo. ¡Hasta luego!')
            break
        else:
            print('Opción inválida.')

def login_loop():
    intentos = 3
    while intentos > 0:
        usuario_input = input('Usuario: ').strip()
        contrasena_input = input('Contraseña: ').strip()
        if usuarios.validar_credenciales(usuario_input, contrasena_input):
            print('Login correcto. Bienvenido', usuario_input)
            return True
        else:
            intentos -= 1
            print(f'Credenciales incorrectas. Intentos restantes: {intentos}')
    print('Máximo de intentos alcanzado. Cerrando aplicación.')
    return False

if __name__ == '__main__':
    print('*** TechLab - Aplicación de Consola ***')
    if login_loop():
        menu_principal()
