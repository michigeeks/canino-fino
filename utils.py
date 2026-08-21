"""
Funciones auxiliares para la ficha de paciente.

Separado de app.py para que la lógica de negocio (conversión de imágenes,
render de PDF) no esté mezclada con el código de la interfaz de Streamlit.
"""

import base64
import io
from pathlib import Path

from PIL import Image
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

_jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def canvas_to_base64_png(canvas_result) -> str | None:
    """Convierte el resultado de st_canvas (array RGBA) a un data-URI base64 PNG.

    Devuelve None si el canvas está vacío (nadie firmó), para no meter
    una firma en blanco en el PDF.
    """
    if canvas_result is None or canvas_result.image_data is None:
        return None

    img_array = canvas_result.image_data.astype("uint8")
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


def render_ficha_pdf(**context) -> bytes:
    """Renderiza templates/ficha.html con el contexto dado y devuelve los bytes del PDF.

    El CSS de static/style.css se inyecta directamente dentro de un <style>
    en el HTML (en vez de enlazarlo como archivo externo) para que WeasyPrint
    no necesite resolver rutas relativas — útil también cuando se despliega
    en Streamlit Community Cloud.
    """
    css = (STATIC_DIR / "style.css").read_text(encoding="utf-8")
    template = _jinja_env.get_template("ficha.html")
    html_final = template.render(css=css, **context)
    return HTML(string=html_final).write_pdf()