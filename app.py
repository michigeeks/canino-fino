"""
Carta de Aceptación de Servicios de Hotel Boutique — Club de Bienestar Canino Fino.

Ejecutar con:
    streamlit run app.py

Estructura del proyecto:
    app.py                       -> UI de Streamlit (este archivo)
    utils.py                     -> lógica: conversión de imágenes y render de PDF
    templates/ficha.html         -> plantilla Jinja2 del PDF (texto legal fijo + campos dinámicos)
    static/style.css             -> estilos del PDF
    static/logo_club_canino.png  -> logo fijo del club (colócalo aquí)
"""

from datetime import date

import streamlit as st
from streamlit_drawable_canvas import st_canvas

from utils import canvas_to_base64_png, render_ficha_pdf

st.set_page_config(page_title="Carta de Aceptación - Club Canino Fino", page_icon="🐾", layout="centered")

st.title("🐾 Carta de Aceptación de Servicios")
st.caption("Club de Bienestar Canino Fino — Hotel Boutique")

with st.form("ficha_form", clear_on_submit=False):

    st.subheader("Datos de estancia")
    col1, col2, col3 = st.columns(3)
    with col1:
        fecha = st.date_input("Fecha", value=date.today())
    with col2:
        ingreso = st.text_input("Ingreso (hora/fecha)")
    with col3:
        salida_estimada = st.text_input("Salida estimada")

    st.subheader("Propietario / Tutor")
    col1, col2 = st.columns(2)
    with col1:
        propietario = st.text_input("Nombre del propietario/tutor *")
    with col2:
        telefono_propietario = st.text_input("Teléfono")

    st.subheader("Datos del perrito")
    col1, col2 = st.columns(2)
    with col1:
        perrito = st.text_input("Nombre del perrito *")
        raza = st.text_input("Raza")
        edad = st.text_input("Edad")
    with col2:
        sexo = st.selectbox("Sexo", ["", "Macho", "Hembra"])
        peso = st.text_input("Peso aproximado")

    st.subheader("Datos veterinarios")
    col1, col2 = st.columns(2)
    with col1:
        mvz_habitual = st.text_input("MVZ habitual")
        medicamentos = st.text_area("Medicamentos / horarios")
    with col2:
        tel_mvz = st.text_input("Teléfono del MVZ")
        alergias = st.text_area("Alergias o condición especial")

    st.subheader("Persona autorizada para recoger")
    col1, col2 = st.columns(2)
    with col1:
        persona_autorizada = st.text_input("Nombre")
    with col2:
        telefono_autorizada = st.text_input("Teléfono ")

    st.subheader("Contacto de emergencia")
    col1, col2 = st.columns(2)
    with col1:
        contacto_emergencia = st.text_input("Nombre del contacto")
    with col2:
        telefono_emergencia = st.text_input("Teléfono  ")

    autoriza_decisiones = st.radio(
        "¿Autoriza a esta persona para tomar decisiones si no es posible localizarlo?",
        ["Sí", "No"],
        horizontal=True,
    )

    observaciones = st.text_area("Observaciones")

    st.subheader("Firma del propietario o tutor")
    st.caption("Dibuja con el dedo (móvil/tablet) o el mouse")
    firma_propietario_canvas = st_canvas(
        stroke_width=3,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=150,
        width=400,
        drawing_mode="freedraw",
        key="firma_propietario",
    )

    st.subheader("Firma del responsable del Club")
    firma_responsable_canvas = st_canvas(
        stroke_width=3,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=150,
        width=400,
        drawing_mode="freedraw",
        key="firma_responsable",
    )

    submitted = st.form_submit_button("Generar PDF")

if submitted:
    if not propietario or not perrito:
        st.error("El nombre del propietario y del perrito son obligatorios.")
    else:
        pdf_bytes = render_ficha_pdf(
            fecha=fecha.strftime("%d/%m/%Y"),
            ingreso=ingreso,
            salida_estimada=salida_estimada,
            propietario=propietario,
            telefono_propietario=telefono_propietario,
            perrito=perrito,
            raza=raza,
            edad=edad,
            sexo=sexo,
            peso=peso,
            mvz_habitual=mvz_habitual,
            tel_mvz=tel_mvz,
            medicamentos=medicamentos or "—",
            alergias=alergias or "—",
            persona_autorizada=persona_autorizada,
            telefono_autorizada=telefono_autorizada,
            contacto_emergencia=contacto_emergencia,
            telefono_emergencia=telefono_emergencia,
            autoriza_decisiones=autoriza_decisiones,
            observaciones=observaciones or "",
            firma_propietario=canvas_to_base64_png(firma_propietario_canvas),
            firma_responsable=canvas_to_base64_png(firma_responsable_canvas),
        )

        st.success("PDF generado correctamente.")
        st.download_button(
            label="⬇️ Descargar carta en PDF",
            data=pdf_bytes,
            file_name=f"carta_aceptacion_{perrito.replace(' ', '_').lower()}.pdf",
            mime="application/pdf",
        )