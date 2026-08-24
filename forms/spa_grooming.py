"""
Formulario: Consentimiento Informado sobre el Servicio Brindado a tu Mascota
(Canino Fino Spa & Grooming Boutique).

Mismo patrón que los demás módulos en forms/: una función render() que
app.py invoca según la opción de menú seleccionada.
"""

from datetime import date

import streamlit as st
from streamlit_drawable_canvas import st_canvas

from utils import canvas_to_base64_png, render_spa_grooming_pdf


def render() -> None:
    """Dibuja el formulario completo y gestiona la generación del PDF."""
    with st.form("spa_grooming_form", clear_on_submit=False):

        fecha = st.date_input("Fecha", value=date.today())

        st.subheader("Datos generales de la mascota")
        col1, col2 = st.columns(2)
        with col1:
            perrito = st.text_input("Nombre de la mascota *")
            raza = st.text_input("Raza o tipo")
            edad = st.text_input("Edad")
        with col2:
            propietario = st.text_input("Nombre del dueño *")
            telefono = st.text_input("Teléfono")
            domicilio = st.text_input("Domicilio")

        st.subheader("Antecedente de la mascota y observaciones del dueño")
        col1, col2 = st.columns(2)
        with col1:
            ansiedad = st.text_input("Ansiedad")
        with col2:
            agresividad = st.text_input("Agresividad")
        enfermedades_alergias = st.text_input("Enfermedades y/o alergias")
        observaciones = st.text_area("Observaciones")

        st.subheader("Firma — Aceptación del servicio")
        st.caption("Dibuja con el dedo (móvil/tablet) o el mouse")
        firma_aceptacion_canvas = st_canvas(
            stroke_width=3,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=150,
            width=400,
            drawing_mode="freedraw",
            key="firma_aceptacion_spa",
        )

        st.subheader("Firma — Recepción de conformidad")
        st.caption("Se firma al momento de recoger a la mascota; puede dejarse en blanco y firmarse después en físico")
        firma_recepcion_canvas = st_canvas(
            stroke_width=3,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=150,
            width=400,
            drawing_mode="freedraw",
            key="firma_recepcion_spa",
        )

        submitted = st.form_submit_button("Generar PDF")

    if submitted:
        if not propietario or not perrito:
            st.error("El nombre del dueño y de la mascota son obligatorios.")
        else:
            pdf_bytes = render_spa_grooming_pdf(
                fecha=fecha.strftime("%d/%m/%Y"),
                perrito=perrito,
                raza=raza,
                edad=edad,
                propietario=propietario,
                domicilio=domicilio,
                telefono=telefono,
                ansiedad=ansiedad,
                agresividad=agresividad,
                enfermedades_alergias=enfermedades_alergias,
                observaciones=observaciones,
                firma_aceptacion=canvas_to_base64_png(firma_aceptacion_canvas),
                firma_recepcion=canvas_to_base64_png(firma_recepcion_canvas),
            )

            st.success("PDF generado correctamente.")
            st.download_button(
                label="⬇️ Descargar consentimiento en PDF",
                data=pdf_bytes,
                file_name=f"consentimiento_spa_{perrito.replace(' ', '_').lower()}.pdf",
                mime="application/pdf",
            )