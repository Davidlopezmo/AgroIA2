import os
import numpy as np
from PIL import Image
from datetime import datetime
from config.database import get_connection
from utils.recommendations import RECOMENDACIONES

IMAGES_FOLDER = "Imagenes/"
os.makedirs(IMAGES_FOLDER, exist_ok=True)

classes = ["cordonata", "pestalotiopsis", "healthy", "sigatoka"]

# ---------------------------------------------------------
# GUARDAR IMAGEN EN DISCO + REGISTRO EN TABLA IMAGEN
# ---------------------------------------------------------
def save_image(img):
    filename = f"hoja_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(IMAGES_FOLDER, filename)
    img.save(filepath)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO IMAGEN (PLANTA_ID, RUTA)
        VALUES (:1, :2)
    """, (1, filepath))   # Planta_id temporal (luego lo conectamos)

    cur.execute("SELECT IMAGEN_SEQ.CURRVAL FROM dual")
    imagen_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return imagen_id, filepath

# ---------------------------------------------------------
# OBTENER O CREAR MODELO EN TABLA MODELO
# ---------------------------------------------------------
def get_or_create_model():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT ID FROM MODELO WHERE NOMBRE='CNN-AgroIA'")
    row = cur.fetchone()

    if row:
        modelo_id = row[0]
    else:
        cur.execute("""
            INSERT INTO MODELO (NOMBRE, VERSION, FRAMEWORK)
            VALUES ('CNN-AgroIA', '1.0', 'TensorFlow')
        """)

        cur.execute("SELECT MODELO_SEQ.CURRVAL FROM dual")
        modelo_id = cur.fetchone()[0]

        conn.commit()

    cur.close()
    conn.close()
    return modelo_id

# ---------------------------------------------------------
# INSERTAR PREDICCIÓN EN ORACLE
# ---------------------------------------------------------
def save_prediction(imagen_id, modelo_id, clase_id, score):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO PREDICCION (IMAGEN_ID, MODELO_ID, CLASE_ID, SCORE)
        VALUES (:1, :2, :3, :4)
    """, (imagen_id, modelo_id, clase_id, score))

    conn.commit()
    cur.close()
    conn.close()

# ---------------------------------------------------------
# PROCESAR TODO: CNN + BD
# ---------------------------------------------------------
def process_prediction(model, img):
    # Guardar la imagen
    imagen_id, ruta = save_image(img)

    # Obtener modelo
    modelo_id = get_or_create_model()

    # Procesar imagen para la IA
    img_resized = img.resize((224, 224))
    img_array = np.array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, 0)

    pred = model.predict(img_array)
    predicted_class = classes[np.argmax(pred)]
    confidence = float(np.max(pred))

    # Guardar predicción
    clase_map = {"cordonata": 1, "pestalotiopsis": 2, "healthy": 3, "sigatoka": 4}
    clase_id = clase_map[predicted_class]

    save_prediction(imagen_id, modelo_id, clase_id, confidence)

    # Obtener recomendaciones
    recomendacion = RECOMENDACIONES.get(predicted_class, "Sin datos disponibles")

    # Texto diagnóstico
    mensaje = f"""
# 🔍 Diagnóstico

## Enfermedad detectada:
*{predicted_class.upper()}*

### Confianza:
*{confidence * 100:.2f}%*

---

## Tratamiento recomendado:
{recomendacion}
"""

    barra = f"""
<div style='margin-top:1rem;'>
    <div style='font-weight:600;color:#2e7d32;'>Nivel de confianza</div>
    <div style='width:100%;background:#eee;border-radius:10px;height:25px;'>
        <div style='width:{confidence*100:.2f}%;background:#66bb6a;height:100%;border-radius:10px'></div>
    </div>
    <div style='text-align:right;'>{confidence*100:.2f}%</div>
</div>
"""

    return mensaje, barra