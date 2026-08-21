"""
Demo: Ficha de paciente con foto, dos firmas digitales y exportación a PDF.

Ejecutar con:
    streamlit run app.py

Dependencias (ver requirements.txt):
    streamlit
    streamlit-drawable-canvas
    weasyprint
    jinja2
    Pillow
"""

import base64
import io
from datetime import date

import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from jinja2 import Template
from weasyprint import HTML

st.set_page_config(page_title="Ficha de Paciente", page_icon="📋", layout="centered")

st.title("📋 Ficha de Paciente")
st.caption("Demo — completa los datos, sube una foto, firma y descarga el PDF.")

# ---------------------------------------------------------------------------
# 1. DATOS DEL FORMULARIO
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
# 2. HELPERS
# ---------------------------------------------------------------------------
def canvas_to_base64_png(canvas_result) -> str | None:
    """Convierte el resultado de st_canvas (array RGBA) a un data-URI base64 PNG.
    Devuelve None si el canvas está vacío (nadie firmó)."""
    if canvas_result is None or canvas_result.image_data is None:
        return None

    img_array = canvas_result.image_data.astype("uint8")
    # Si todos los pixeles son transparentes/blancos, se considera vacío
    alpha_channel = img_array[:, :, 3]
    if alpha_channel.max() == 0:
        return None

    img = Image.fromarray(img_array, mode="RGBA")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


def uploaded_file_to_base64(uploaded_file) -> str | None:
    """Convierte un UploadedFile de Streamlit a data-URI base64."""
    if uploaded_file is None:
        return None
    bytes_data = uploaded_file.getvalue()
    b64 = base64.b64encode(bytes_data).decode()
    mime = uploaded_file.type or "image/jpeg"
    return f"data:{mime};base64,{b64}"


# ---------------------------------------------------------------------------
# 3. PLANTILLA HTML DEL PDF (edítala a gusto: colores, logo, layout, etc.)
# ---------------------------------------------------------------------------
HTML_TEMPLATE = Template(
    """
<html>
<head>
<meta charset="utf-8">
<style>
    @page {
        size: Letter;
        margin: 2cm;
    }
    body {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #222;
        font-size: 12pt;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 3px solid #2c6ecb;
        padding-bottom: 12px;
        margin-bottom: 24px;
    }
    .header h1 {
        font-size: 20pt;
        color: #2c6ecb;
        margin: 0;
    }
    .header .fecha {
        font-size: 10pt;
        color: #666;
    }
    .foto {
        width: 100px;
        height: 100px;
        object-fit: cover;
        border-radius: 6px;
        border: 1px solid #ccc;
    }
    .datos-grid {
        display: flex;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }
    .campo {
        width: 50%;
        margin-bottom: 10px;
    }
    .campo .label {
        font-size: 9pt;
        text-transform: uppercase;
        color: #888;
        letter-spacing: 0.5px;
    }
    .campo .valor {
        font-size: 12pt;
        font-weight: 600;
    }
    .observaciones {
        background: #f5f7fa;
        border-radius: 6px;
        padding: 14px;
        margin: 20px 0;
        min-height: 60px;
    }
    .firmas {
        display: flex;
        justify-content: space-between;
        margin-top: 60px;
    }
    .firma-box {
        width: 45%;
        text-align: center;
    }
    .firma-box img {
        width: 100%;
        max-height: 100px;
        object-fit: contain;
        border-bottom: 1px solid #333;
        margin-bottom: 6px;
    }
    .firma-sin-firmar {
        height: 100px;
        border-bottom: 1px solid #333;
        margin-bottom: 6px;
    }
    .firma-box .nombre {
        font-size: 10pt;
        color: #555;
    }
</style>
</head>
<body>

    <div class="header">
        <div>
            <h1>Ficha de Paciente</h1>
            <div class="fecha">Fecha: {{ fecha }}</div>
        </div>
        {% if foto %}
        <img class="foto" src="{{ foto }}">
        {% endif %}
    </div>

    <div class="datos-grid">
        <div class="campo">
            <div class="label">Nombre completo</div>
            <div class="valor">{{ nombre }}</div>
        </div>
        <div class="campo">
            <div class="label">Edad</div>
            <div class="valor">{{ edad }}</div>
        </div>
        <div class="campo">
            <div class="label">Documento</div>
            <div class="valor">{{ documento }}</div>
        </div>
        <div class="campo">
            <div class="label">Teléfono</div>
            <div class="valor">{{ telefono }}</div>
        </div>
        <div class="campo">
            <div class="label">Correo</div>
            <div class="valor">{{ email }}</div>
        </div>
    </div>

    <div class="label">Motivo / Observaciones</div>
    <div class="observaciones">{{ motivo }}</div>

    <div class="firmas">
        <div class="firma-box">
            {% if firma_cliente %}
                <img src="{{ firma_cliente }}">
            {% else %}
                <div class="firma-sin-firmar"></div>
            {% endif %}
            <div class="nombre">Firma del cliente / paciente</div>
        </div>
        <div class="firma-box">
            {% if firma_encargado %}
                <img src="{{ firma_encargado }}">
            {% else %}
                <div class="firma-sin-firmar"></div>
            {% endif %}
            <div class="nombre">Firma del encargado / responsable</div>
        </div>
    </div>

</body>
</html>
"""
)

# ---------------------------------------------------------------------------
# 4. GENERAR PDF AL ENVIAR EL FORMULARIO
# ---------------------------------------------------------------------------
if submitted:
    if not nombre:
        st.error("El nombre es obligatorio.")
    else:
        foto_b64 = uploaded_file_to_base64(foto_file)
        firma_cliente_b64 = canvas_to_base64_png(firma_cliente_canvas)
        firma_encargado_b64 = canvas_to_base64_png(firma_encargado_canvas)

        html_final = HTML_TEMPLATE.render(
            nombre=nombre,
            edad=edad,
            documento=documento,
            telefono=telefono,
            email=email,
            fecha=fecha.strftime("%d/%m/%Y"),
            motivo=motivo or "—",
            foto=foto_b64,
            firma_cliente=firma_cliente_b64,
            firma_encargado=firma_encargado_b64,
        )

        pdf_bytes = HTML(string=html_final).write_pdf()

        st.success("PDF generado correctamente.")
        st.download_button(
            label="⬇️ Descargar ficha en PDF",
            data=pdf_bytes,
            file_name=f"ficha_{nombre.replace(' ', '_').lower()}.pdf",
            mime="application/pdf",
        )

        with st.expander("Vista previa del HTML (debug)"):
            st.code(html_final, language="html")