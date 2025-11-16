from models.finca import Finca
from repositories.finca_repo import FincaRepository

class FincaService:

    @staticmethod
    def registrar(productor_id, nombre, vereda, municipio):
        if not productor_id:
            return "❌ Seleccione un agricultor."
        if not nombre.strip():
            return "❌ El nombre de la finca es obligatorio."

        finca = Finca(productor_id=productor_id, nombre=nombre, vereda=vereda, municipio=municipio)
        FincaRepository.crear(finca)

        return "✅ Finca registrada."

    @staticmethod
    def listar_dropdown():
        return FincaRepository.obtener_todas()