from models.productor import Productor
from repositories.productor_repo import ProductorRepository

class ProductorService:

    @staticmethod
    def registrar(nombre, contacto, municipio):
        if not nombre.strip():
            return "❌ El nombre es obligatorio."

        productor = Productor(nombre=nombre, contacto=contacto, municipio=municipio)
        ProductorRepository.crear(productor)

        return "✅ Agricultor registrado exitosamente."

    @staticmethod
    def listar_dropdown():
        return ProductorRepository.obtener_todos()