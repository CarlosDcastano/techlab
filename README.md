1. Contexto general
El Laboratorio de Innovación Tecnológica (TechLab) necesita una herramienta de consola para gestionar el inventario de equipos tecnológicos y los préstamos que realizan estudiantes, instructores o personal interno.
 Actualmente todo se hace en papel o Excel, lo que genera errores al calcular:
●	Qué equipos están disponibles o prestados.

●	Cuánto tiempo puede prestar un dispositivo cada usuario según su tipo (estudiante, instructor, administrativo).

●	Quién ha devuelto tarde un equipo.

●	Historial de préstamos por mes y año.

Tu misión es construir una aplicación de consola en Python para TechLab que permita:
●	Iniciar sesión con un usuario administrador.

●	Gestionar equipos (registro, actualización y consulta).

●	Registrar solicitudes de préstamo y su aprobación o rechazo.

●	Controlar el tiempo máximo permitido según el tipo de usuario.

●	Registrar devoluciones y calcular retrasos.

●	Exportar reportes en CSV por mes y año.

________________________________________
2. Inicio de sesión (obligatorio)
2.1 Archivo de usuarios
Debe existir un archivo usuarios.csv con un único administrador.
Campos mínimos:
●	usuario

●	contrasena

●	rol (solo ADMIN)

No se permiten nuevos registros.
 El inicio de sesión se valida solo contra este archivo.
2.2 Reglas de sesión
●	Solicitar usuario y contraseña.

●	Validar contra el CSV.

●	Si las credenciales no coinciden:

○	Mostrar error claro.

○	Máximo 3 intentos → si falla, cerrar el programa.

●	Solo si el login es correcto se muestra el menú principal.

________________________________________
3. Persistencia de datos en CSV
Toda la aplicación se basa en persistencia en CSV.
Archivos obligatorios:
usuarios.csv
Usuario administrador.
equipos.csv
Campos mínimos:
●	equipo_id

●	nombre_equipo (ej: “Laptop Dell XPS”)

●	categoria (drones, laptops, tablets, cámaras, herramientas, etc.)

●	estado_actual (DISPONIBLE, PRESTADO, MANTENIMIENTO)

●	fecha_registro

●	descripcion (opcional)

prestamos.csv
Campos mínimos:
●	prestamo_id

●	equipo_id

●	nombre_equipo

●	usuario_prestatario

●	tipo_usuario (ESTUDIANTE, INSTRUCTOR, ADMINISTRATIVO)

●	fecha_solicitud

●	fecha_prestamo

●	fecha_devolucion

●	dias_autorizados

●	dias_reales_usados

●	retraso (SI/NO)

●	estado (PENDIENTE, APROBADO, RECHAZADO, DEVUELTO)

●	mes

●	anio

La aplicación debe:
●	Leer los CSV al iniciar.

●	Actualizarlos al registrar cambios.

________________________________________
4. Reglas de préstamos (TechLab)
4.1 Tiempo máximo por tipo de usuario
Cada tipo de usuario tiene un límite máximo de préstamo:
●	Estudiante: 3 días.

●	Instructor: 7 días.

●	Administrativo: 10 días.

El sistema debe garantizar que:
dias_solicitados <= dias_max_por_tipo_usuario

Si se excede → rechazar la solicitud automáticamente.
________________________________________
4.2 Estado de equipos
Un equipo solo puede prestarse si:
●	Está marcado como DISPONIBLE.

●	No tiene préstamos pendientes sin devolver.

Si el equipo no está disponible:
●	Bloquear el préstamo y mostrar mensaje claro.

________________________________________
4.3 Conteo de días reales de préstamo
Al registrar la devolución se calcula:
dias_reales_usados = diferencia entre fecha_prestamo y fecha_devolucion

Si dias_reales_usados > dias_autorizados → marcar retraso = SI.
También se actualiza el estado del equipo a DISPONIBLE.
________________________________________
5. Requerimientos funcionales
5.1 Gestión de equipos
Debe permitir:
Registrar equipo
Datos:
●	ID único

●	Nombre de equipo

●	Categoría

●	Estado inicial (por defecto: DISPONIBLE)

●	Fecha de registro

●	Descripción opcional

Guardar en equipos.csv.
Listar equipos
Mostrar:
●	ID

●	Nombre

●	Categoría

●	Estado

Consultar equipo específico
Buscar por ID y mostrar toda la información.
________________________________________
5.2 Gestión de préstamos
Registrar solicitud de préstamo
El flujo es:
●	Seleccionar equipo por ID.

●	Validar que esté DISPONIBLE.

●	Ingresar datos del solicitante:

○	nombre

○	tipo_usuario

●	Ingresar:

○	fecha_prestamo

○	dias_solicitados

Validar:
●	Que días solicitados no excedan límites según tipo.

●	Que la fecha tenga formato correcto.

Si todo es válido:
●	Guardar préstamo con estado PENDIENTE.

________________________________________
Aprobar o rechazar préstamo
●	Listar solicitudes PENDIENTES.

●	Elegir una.

●	Si se aprueba:

○	Cambiar estado a APROBADO.

○	Cambiar estado del equipo a PRESTADO.

●	Si se rechaza:

○	Cambiar estado a RECHAZADO.

Actualizar CSV.
________________________________________
Registrar devolución de equipo
●	Listar préstamos APROBADOS sin devolución.

●	Solicitar fecha_devolucion.

Calcular:

 dias_reales_usados
retraso = SI o NO
●	
●	Cambiar estado del préstamo a DEVUELTO.

●	Cambiar estado del equipo a DISPONIBLE.

________________________________________
5.3 Historial
Consultar historial por equipo o por usuario:
●	Fechas.

●	Estado.

●	Días autorizados.

●	Retraso.

●	Mes y año.

________________________________________
5.4 Exportar reporte CSV
Datos requeridos:
●	Mes

●	Año

Generar archivo:
reporte_prestamos_2025_03.csv

Debe incluir solo préstamos DEVUELTOS del mes y año seleccionados.
Columnas recomendadas:
●	prestamo_id

●	equipo_id

●	nombre_equipo

●	usuario_prestatario

●	tipo_usuario

●	dias_autorizados

●	dias_reales_usados

●	retraso

●	estado

●	mes

●	anio

Si no hay datos → mensaje claro.
________________________________________
6. Requerimientos técnicos

●	Lenguaje: Python.

●	Interfaz: consola.

●	Uso de múltiples archivos .py:

○	main.py

○	usuarios.py

○	equipos.py

○	prestamos.py

○	reportes.py

●	Uso obligatorio de funciones.

●	Uso de estructuras de control.

________________________________________
7. README.md (obligatorio)
Debe incluir:
●	Título del proyecto

○	Ej: TechLab Inventory Console – Gestión de equipos tecnológicos

●	Datos de la persona

●	Descripción general

●	Cómo ejecutar el programa

●	CSV necesarios

●	Explicación de las reglas de préstamo

●	Estructura del proyecto

●	Limitaciones

●	Mejoras futuras

________________________________________
8. Diagrama de flujo
Debe representar uno de los siguientes:
●	Inicio de sesión + menú principal

●	Flujo de solicitud de préstamo:

○	Validación límites por tipo de usuario

○	Validación disponibilidad del equipo

○	Registro de préstamo

○	Estado (pendiente → aprobado/rechazado → devuelto)

Formato: PNG, JPG o PDF.

________________________________________

9.  Restricciones
●	- Prohibido usar IA
●	- Prohibido Copilot o autocompletados
●	- Solo documentación oficial de Python
