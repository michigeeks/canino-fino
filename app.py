"""
Carta de Aceptación de Servicios de Hotel Boutique — Club de Bienestar Canino Fino.

Ejecutar con:
    streamlit run app.py

Estructura del proyecto:
    app.py                          -> tema visual, sidebar/navegación y enrutamiento (este archivo)
    forms/                          -> un módulo por formulario del sidebar, cada uno con su función render()
        __init__.py
        carta_aceptacion.py         -> formulario "Carta de Aceptación de Servicios" (hospedaje/hotel)
        estancia_diurna.py          -> formulario "Estancia Diurna" (guardería boutique)
    utils.py                        -> lógica: conversión de imágenes y render de PDF (compartida por ambos formularios)
    templates/
        ficha.html                  -> plantilla del PDF de hospedaje
        ficha_estancia_diurna.html  -> plantilla del PDF de estancia diurna
    static/
        style.css                   -> estilos base del PDF (compartidos)
        style_estancia_diurna.css   -> estilos adicionales del PDF de estancia diurna (layout a 2 columnas)
        logo_club_canino.jpeg       -> logo fijo del club (colócalo aquí)

Para agregar un nuevo formulario al menú:
    1. Crear forms/nombre_formulario.py con una función render().
    2. Importarlo aquí arriba: from forms import nombre_formulario
    3. Agregar su etiqueta a la lista de NAV_* y su rama al enrutamiento
       al final del archivo (sección "Contenido principal").
"""

import streamlit as st

from forms import carta_aceptacion, estancia_diurna, spa_grooming

st.set_page_config(page_title="Carta de Aceptación - Club Canino Fino", page_icon="🐾", layout="centered")

# ---------------------------------------------------------------------------
# Identidad visual — Club de Bienestar Canino Fino
#
# Paleta: pino profundo (marca), oro cálido (acento), marfil (contenido).
# Tipografía: Fraunces (display), Work Sans (cuerpo), IBM Plex Mono (eyebrows).
# ---------------------------------------------------------------------------
BRAND_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Work+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

:root {
    --pine-deep: #1E3B2C;
    --pine-dark: #142A1F;
    --gold-warm: #C89A4D;
    --gold-soft: #E4C489;
    --ivory: #FAF6EE;
    --cream: #F4EDE1;
    --ink: #2B2926;
    --sand-line: #E6DFD0;
}

html, body, [class*="css"] { font-family: 'Work Sans', sans-serif; color: var(--ink); }

/* Fondo general de la app */
[data-testid="stAppViewContainer"] { background: var(--ivory); }
[data-testid="stHeader"] { background: transparent; }

/* Deja hueco abajo para nuestro footer */
[data-testid="stAppViewContainer"] > .main .block-container {
    padding-top: 2rem;
    padding-bottom: 6rem;
    max-width: 760px;
}

/* Encabezados de sección dentro del formulario */
h3 {
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    color: var(--pine-deep) !important;
    border-bottom: 1px solid var(--sand-line);
    padding-bottom: 0.4rem;
    margin-top: 1.6rem !important;
}

/* Botón principal */
.stFormSubmitButton button, .stDownloadButton button {
    background: var(--gold-warm) !important;
    color: var(--pine-dark) !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 6px !important;
}
.stFormSubmitButton button:hover, .stDownloadButton button:hover {
    background: var(--gold-soft) !important;
    color: var(--pine-dark) !important;
}

/* --- Sidebar --- */
[data-testid="stSidebar"] {
    background: var(--cream);
    border-right: 1px solid var(--sand-line);
}
[data-testid="stSidebar"] * { color: var(--ink); }
.sidebar-seal {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, var(--gold-soft), var(--gold-warm));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin: 0.5rem auto 0.75rem auto;
    box-shadow: inset 0 0 0 2px var(--pine-deep);
}
.sidebar-club-name {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    text-align: center;
    font-size: 1rem;
    color: var(--pine-deep);
    margin-bottom: 0.1rem;
}
.sidebar-tagline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-align: center;
    color: var(--gold-warm);
    margin-bottom: 1rem;
}
.sidebar-divider {
    border: none;
    border-top: 1px solid var(--sand-line);
    margin: 0.75rem 0 1rem 0;
}

/* Navegación del sidebar (radio disfrazado de lista de menú) */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent;
    border-radius: 6px;
    padding: 0.5rem 0.6rem;
    margin-bottom: 0.15rem;
    transition: background 0.15s ease;
    width: 100%;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(200, 154, 77, 0.18);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-family: 'Work Sans', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
}
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 0.1rem;
}

/* --- Footer fijo --- */
.brand-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background: var(--pine-dark);
    color: var(--ivory);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.06em;
    text-align: center;
    padding: 0.65rem 1rem;
    border-top: 2px solid var(--gold-warm);
    z-index: 999999;
}
.brand-footer span { color: var(--gold-soft); }
</style>
"""
st.markdown(BRAND_CSS, unsafe_allow_html=True)

# Header de marca — eliminado por el momento (a pedido). El CSS de
# .brand-header/.brand-seal/.brand-title queda quitado también; si se
# vuelve a activar, restaurar ambos bloques.

# ---------------------------------------------------------------------------
# Menú lateral
# ---------------------------------------------------------------------------
NAV_INICIO = "Inicio"
NAV_FICHA = "Carta de Aceptación"
NAV_ESTANCIA_DIURNA = "Estancia Diurna"
NAV_SPA_GROOMING = "Spa & Grooming"

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-seal">🐾</div>
        <div class="sidebar-club-name">Canino Fino</div>
        <div class="sidebar-tagline">Club de Bienestar & Hotel Boutique</div>
        <hr class="sidebar-divider">
        """,
        unsafe_allow_html=True,
    )
    seccion = st.radio(
        "Menú",
        [NAV_INICIO, NAV_FICHA, NAV_ESTANCIA_DIURNA, NAV_SPA_GROOMING],
        label_visibility="collapsed",
    )


# ---------------------------------------------------------------------------
# Contenido principal — según la opción elegida en el menú
# ---------------------------------------------------------------------------
if seccion == NAV_FICHA:
    carta_aceptacion.render()
elif seccion == NAV_ESTANCIA_DIURNA:
    estancia_diurna.render()
elif seccion == NAV_SPA_GROOMING:
    spa_grooming.render()
# Si es "Inicio", no se renderiza nada: pantalla principal en blanco.

# ---------------------------------------------------------------------------
# Footer de marca
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="brand-footer">
        Club de Bienestar Canino Fino <span>·</span> Hotel Boutique
        <span>·</span> © 2026 Todos los derechos reservados
    </div>
    """,
    unsafe_allow_html=True,
)