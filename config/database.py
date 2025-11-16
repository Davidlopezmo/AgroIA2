import cx_Oracle

def get_connection():
    return cx_Oracle.connect(
        user="AgroIA",
        password="AgroIA123",
        dsn="localhost:1521/freepdb1"
    )