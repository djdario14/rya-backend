import psycopg2
import sys

if len(sys.argv) < 2:
    print("Uso: python consultar_fecha_prestamo.py <cedula_cliente>")
    sys.exit(1)

cedula_cliente = sys.argv[1]

# Configura tus datos de conexión
conn = psycopg2.connect(
    dbname="TU_DB",
    user="TU_USUARIO",
    password="TU_PASSWORD",
    host="TU_HOST",
    port="TU_PORT"
)

with conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.fecha
            FROM prestamos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE c.cedula = %s AND p.estado = 'activo'
            ORDER BY p.id DESC
            LIMIT 1
        """, (cedula_cliente,))
        row = cur.fetchone()
        if row:
            print("Fecha del préstamo activo:", row[0])
        else:
            print("No se encontró préstamo activo para ese cliente.")

conn.close()
