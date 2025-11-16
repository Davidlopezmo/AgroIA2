class Prediccion:
    def __init__(self, id=None, imagen_id=None, modelo_id=None, clase_id=None, score=None):
        self.id = id
        self.imagen_id = imagen_id
        self.modelo_id = modelo_id
        self.clase_id = clase_id
        self.score = score