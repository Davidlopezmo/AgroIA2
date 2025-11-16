from config.database import get_connection
from models.finca import Finca

class FincaRepository:

    @staticmethod
    def crear(finca: Finca):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO FINCA (PRODUCTOR_ID, NOMBRE, VEREDA, MUNICIPIO)
            VALUES (:1, :2, :3, :4)
        """, [finca.productor_id, finca.nombre, finca.vereda, finca.municipio])

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def obtener_todas():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT ID, NOMBRE FROM FINCA ORDER BY NOMBRE")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {nombre: id_ for id_, nombre in rows}