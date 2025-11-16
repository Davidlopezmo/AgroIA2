import base64

def load_background():
    with open("Imagen.jpg", "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    return f"url('data:image/jpg;base64,{encoded}')"