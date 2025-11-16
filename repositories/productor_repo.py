from config.database import get_connection
from models.productor import Productor

class ProductorRepository:

    @staticmethod
    def crear(productor: Productor):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO PRODUCTOR (NOMBRE, CONTACTO, MUNICIPIO)
            VALUES (:1, :2, :3)
        """, [productor.nombre, productor.contacto, productor.municipio])

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT ID, NOMBRE FROM PRODUCTOR ORDER BY NOMBRE")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {nombre: id_ for id_, nombre in rows}