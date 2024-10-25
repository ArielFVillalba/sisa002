import psycopg2
def conexion(db, usuario, contraseña):
    if db == 1:
        conn = psycopg2.connect(
            host = "localhost",
            database = "sisa",
            user = "postgres",
            password = "sisa",
            port=5432)
        print("todo salio bien")
    if db == 2:
        conn = "Conexion a base de datos 2"
    return conn