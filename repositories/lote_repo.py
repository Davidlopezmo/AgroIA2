from config.database import get_connection
from models.lote import Lote

class LoteRepository:

    @staticmethod
    def crear(lote: Lote):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO LOTE (FINCA_ID, NOMBRE)
            VALUES (:1, :2)
        """, [lote.finca_id, lote.nombre])

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def obtener_por_finca(finca_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT ID, NOMBRE FROM LOTE WHERE FINCA_ID = :1", [finca_id])
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return {nombre: id_ for id_, nombre in rows}