import os
import tensorflow as tf
import numpy as np
import gradio as gr
from services.productor_service import ProductorService
from services.finca_service import FincaService
from services.lote_service import LoteService

from ai.model_loader import load_model
from ai.predictor import process_prediction
from utils.recommendations import RECOMENDACIONES
from utils.background_loader import load_background

import numpy as np

# ============================
# 🔥 CARGAR MODELO CNN
# ============================
model = load_model()
classes = ["cordonata", "pestalotiopsis", "healthy", "sigatoka"]

# ============================
# 🧠 FUNCIÓN DE PREDICCIÓN
# ============================


# ============================
# 🖼 FONDO
# ============================
bg = load_background()

# ============================
# 🌐 INTERFAZ VISUAL GRADIO
# ============================
with gr.Blocks(css=f"""
    body {{
        background-image: {bg};
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }}

    .gradio-container {{
        background-color: rgba(255,255,255,0.92);
        border-radius: 18px;
        padding: 2rem;
        max-width: 900px;
        margin: auto;
        margin-top: 40px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.2);
    }}
""") as demo:

    # ============================
    # TÍTULO
    # ============================
    gr.HTML("""
        <div style="text-align:center; margin-bottom:30px;">
            <h1 style="color:#1b5e20; font-size:3rem; font-weight:600;">
                🌿 AgroIA
            </h1>
            <p style="font-size:1.2rem; color:#388e3c;">
                Sistema de diagnóstico para hojas de plátano con Inteligencia Artificial 🍌
            </p>
        </div>
    """)

    # ============================
    # PANEL: REGISTRO AGRICULTOR
    # ============================
    with gr.Accordion("👨‍🌾 Registrar Agricultor", open=False):
        nombre = gr.Textbox(label="Nombre")
        contacto = gr.Textbox(label="Contacto")
        municipio = gr.Textbox(label="Municipio")
        btn_reg_agricultor = gr.Button("Registrar Agricultor")
        salida_agricultor = gr.Markdown()

        btn_reg_agricultor.click(
            ProductorService.registrar,
            inputs=[nombre, contacto, municipio],
            outputs=salida_agricultor
        )

    # ============================
    # PANEL: REGISTRO FINCA
    # ============================
    with gr.Accordion("🏡 Registrar Finca", open=False):
        productor_dropdown = gr.Dropdown(
            label="Seleccione Agricultor",
            choices=list(ProductorService.listar_dropdown().keys()),
            value=None
        )

        productor_id_state = gr.State()

        def actualizar_id(nombre_select):
            return ProductorService.listar_dropdown().get(nombre_select, None)

        productor_dropdown.change(
            actualizar_id,
            inputs=productor_dropdown,
            outputs=productor_id_state
        )

        nombre_finca = gr.Textbox(label="Nombre de Finca")
        vereda = gr.Textbox(label="Vereda")
        municipio_finca = gr.Textbox(label="Municipio")

        btn_reg_finca = gr.Button("Registrar Finca")
        salida_finca = gr.Markdown()

        btn_reg_finca.click(
            FincaService.registrar,
            inputs=[productor_id_state, nombre_finca, vereda, municipio_finca],
            outputs=salida_finca
        )

    # ============================
    # PANEL: REGISTRO LOTE
    # ============================
    with gr.Accordion("🟩 Registrar Lote", open=False):
        finca_dropdown = gr.Dropdown(
            label="Seleccione Finca",
            choices=list(FincaService.listar_dropdown().keys()),
            value=None
        )

        finca_id_state = gr.State()

        def actualizar_finca_id(nombre_finca_select):
            return FincaService.listar_dropdown().get(nombre_finca_select, None)

        finca_dropdown.change(
            actualizar_finca_id,
            inputs=finca_dropdown,
            outputs=finca_id_state
        )

        nombre_lote = gr.Textbox(label="Nombre del Lote")

        btn_reg_lote = gr.Button("Registrar Lote")
        salida_lote = gr.Markdown()

        btn_reg_lote.click(
            LoteService.registrar,
            inputs=[finca_id_state, nombre_lote],
            outputs=salida_lote
        )

    # ============================
    # PANEL: DIAGNÓSTICO IA
    # ============================
    gr.Markdown("---")
    gr.Markdown("## 🔍 Diagnóstico de Enfermedades")

    with gr.Row():

        with gr.Column():
            img_input = gr.Image(type="pil", label="Suba una imagen de hoja")
            btn_pred = gr.Button("Detectar enfermedad")

        with gr.Column():
            salida_pred = gr.Markdown()
            barra_conf = gr.HTML()

    btn_pred.click(
        fn=lambda img: process_prediction(model, img),
        inputs=img_input,
        outputs=[salida_pred, barra_conf]
    )

# ============================
# ▶ EJECUTAR APP
# ============================
demo.launch()