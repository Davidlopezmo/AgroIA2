from models.lote import Lote
from repositories.lote_repo import LoteRepository

class LoteService:

    @staticmethod
    def registrar(finca_id, nombre):
        if not finca_id:
            return "❌ Seleccione una finca."
        if not nombre.strip():
            return "❌ El nombre del lote es obligatorio."

        lote = Lote(finca_id=finca_id, nombre=nombre)
        LoteRepository.crear(lote)

        return "✅ Lote registrado."

    @staticmethod
    def listar_por_finca(finca_id):
        return LoteRepository.obtener_por_finca(finca_id)