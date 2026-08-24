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


def _find_logo_file() -> Path | None:
    """Busca el logo del club en static/ sin depender de acertarle al nombre exacto.

    En Linux (Streamlit Cloud) los nombres de archivo son sensibles a
    mayúsculas/minúsculas, así que si el archivo real no coincide EXACTO
    con lo que el código espera (ej. subiste "Logo_Club_Canino.PNG" en vez
    de "logo_club_canino.jpeg"), antes fallaba en silencio y el PDF salía
    sin logo. Ahora se prueban varios nombres/extensiones típicos primero,
    y si ninguno coincide, se busca cualquier archivo en static/ cuyo
    nombre empiece con "logo" (sin importar mayúsculas ni extensión).
    """
    candidatos = [
        "logo_club_canino.jpeg",
        "logo_club_canino.jpg",
        "logo_club_canino.png",
        "logo.jpeg",
        "logo.jpg",
        "logo.png",
    ]
    for nombre in candidatos:
        ruta = STATIC_DIR / nombre
        if ruta.exists():
            return ruta

    if STATIC_DIR.exists():
        for archivo in sorted(STATIC_DIR.iterdir()):
            if archivo.is_file() and archivo.stem.lower().startswith("logo") and archivo.suffix.lower() in (".png", ".jpg", ".jpeg"):
                return archivo

    return None


def _file_to_base64(path: Path | None) -> str | None:
    """Lee un archivo de imagen en disco y lo convierte a data-URI base64.

    Se usa para assets FIJOS (ej. el logo del club), que no vienen del
    formulario sino que ya viven en la carpeta static/ del proyecto.
    """
    if path is None or not path.exists():
        return None
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def _render_pdf(template_name: str, extra_css_file: str | None = None, **context) -> bytes:
    """Renderiza un template de templates/ con el contexto dado y devuelve los bytes del PDF.

    El CSS se inyecta directamente dentro de un <style> en el HTML (en vez de
    enlazarlo como archivo externo) para que WeasyPrint no necesite resolver
    rutas relativas — útil también cuando se despliega en Streamlit Community Cloud.

    static/style.css siempre se incluye como base de marca. Si el documento
    necesita reglas propias (ej. un layout a dos columnas), se pasa
    `extra_css_file` con el nombre de un segundo archivo en static/ que se
    concatena después, así puede sobreescribir puntualmente alguna regla
    del CSS base sin duplicarlo todo.

    El logo del club se busca automáticamente en static/ (ver _find_logo_file)
    y se embebe aquí, así los formularios no tienen que preocuparse por él.
    """
    css = (STATIC_DIR / "style.css").read_text(encoding="utf-8")
    if extra_css_file:
        css += "\n" + (STATIC_DIR / extra_css_file).read_text(encoding="utf-8")

    logo_b64 = _file_to_base64(_find_logo_file())
    template = _jinja_env.get_template(template_name)
    html_final = template.render(css=css, logo=logo_b64, **context)
    return HTML(string=html_final).write_pdf()


def render_ficha_pdf(**context) -> bytes:
    """Carta de Aceptación de Servicios de Hotel Boutique (hospedaje)."""
    return _render_pdf("ficha.html", **context)


def render_estancia_diurna_pdf(**context) -> bytes:
    """Carta de Aceptación del Servicio de Estancia Diurna (Guardería Boutique)."""
    return _render_pdf("ficha_estancia_diurna.html", extra_css_file="style_estancia_diurna.css", **context)


def render_spa_grooming_pdf(**context) -> bytes:
    """Consentimiento Informado — Canino Fino Spa & Grooming Boutique."""
    return _render_pdf("ficha_spa_grooming.html", extra_css_file="style_spa_grooming.css", **context)