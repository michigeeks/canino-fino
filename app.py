"""
Demo: Ficha de paciente con foto, dos firmas digitales y exportación a PDF.

Ejecutar con:
    streamlit run app.py

Estructura del proyecto:
    app.py              -> UI de Streamlit (este archivo)
    utils.py            -> lógica: conversión de imágenes y render de PDF
    templates/ficha.html-> plantilla Jinja2 del PDF (el "diseño" en HTML)
    static/style.css    -> estilos del PDF (el "diseño" en CSS)

Dependencias: ver requirements.txt
"""

from datetime import date

import streamlit as st
from streamlit_drawable_canvas import st_canvas

from utils import canvas_to_base64_png, uploaded_file_to_base64, render_ficha_pdf

st.set_page_config(page_title="Ficha de Paciente", page_icon="📋", layout="centered")

st.title("📋 Ficha de Paciente")
st.caption("Demo — completa los datos, sube una foto, firma y descarga el PDF.")

# ---------------------------------------------------------------------------
# FORMULARIO
# ---------------------------------------------------------------------------
with st.form("ficha_form", clear_on_submit=False):
    st.subheader("Datos generales")
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre completo *")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
        telefono = st.text_input("Teléfono")
    with col2:
        fecha = st.date_input("Fecha", value=date.today())
        documento = st.text_input("Documento de identidad")
        email = st.text_input("Correo electrónico")

    motivo = st.text_area("Motivo de consulta / observaciones")

    st.subheader("Foto del paciente")
    foto_file = st.file_uploader(
        "Sube una foto (jpg, png)", type=["jpg", "jpeg", "png"]
    )

    st.subheader("Firma del cliente / paciente")
    st.caption("Dibuja con el dedo (móvil/tablet) o el mouse")
    firma_cliente_canvas = st_canvas(
        stroke_width=3,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=150,
        width=400,
        drawing_mode="freedraw",
        key="firma_cliente",
    )

    st.subheader("Firma del encargado / responsable")
    firma_encargado_canvas = st_canvas(
        stroke_width=3,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=150,
        width=400,
        drawing_mode="freedraw",
        key="firma_encargado",
    )

    submitted = st.form_submit_button("Generar PDF")

# ---------------------------------------------------------------------------
# GENERAR PDF AL ENVIAR
# ---------------------------------------------------------------------------
if submitted:
    if not nombre:
        st.error("El nombre es obligatorio.")
    else:
        pdf_bytes = render_ficha_pdf(
            nombre=nombre,
            edad=edad,
            documento=documento,
            telefono=telefono,
            email=email,
            fecha=fecha.strftime("%d/%m/%Y"),
            motivo=motivo or "—",
            foto=uploaded_file_to_base64(foto_file),
            firma_cliente=canvas_to_base64_png(firma_cliente_canvas),
            firma_encargado=canvas_to_base64_png(firma_encargado_canvas),
        )

        st.success("PDF generado correctamente.")
        st.download_button(
            label="⬇️ Descargar ficha en PDF",
            data=pdf_bytes,
            file_name=f"ficha_{nombre.replace(' ', '_').lower()}.pdf",
            mime="application/pdf",
        )