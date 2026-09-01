"""
Formulario: Carta de Aceptación del Servicio de Estancia Diurna (Guardería Boutique).

Mismo patrón que forms/carta_aceptacion.py: un módulo por formulario, con
una función render() que app.py invoca según la opción de menú seleccionada.
"""
from datetime import date
from datetime import time

import streamlit as st
from streamlit_drawable_canvas import st_canvas

from utils import canvas_to_base64_png, render_estancia_diurna_pdf


def render() -> None:
    """Dibuja el formulario completo y gestiona la generación del PDF."""
    with st.form("estancia_diurna_form", clear_on_submit=False):
        st.title("Carta de Aceptación del Servicio de Estancia Diurna")

        st.subheader("Datos del propietario o tutor")
        col1, col2 = st.columns(2)
        with col1:
            propietario = st.text_input("Nombre del propietario/tutor *")
            correo_propietario = st.text_input("Correo", placeholder="john@gmail.com")
        with col2:
            telefono_propietario = st.text_input("Teléfono", placeholder="55 1234 5678", key="nombre_tutor")
            identificacion_oficial = st.text_input("Identificación oficial")

        st.subheader("Datos del perrito")
        col1, col2 = st.columns(2)
        with col1:
            perrito = st.text_input("Nombre del perrito *")
            raza = st.text_input("Raza")
            edad = st.number_input("Edad", min_value=1, max_value=100, step=1, format="%d")
        with col2:
            sexo = st.radio("Sexo", ["Macho", "Hembra"], horizontal=True, index=None)
            peso = st.number_input("Peso aproximado (kg)", min_value=0.0, step=0.5, format="%.1f")
            color = st.text_input("Color")

        st.subheader("Datos veterinarios")
        col1, col2 = st.columns(2)
        with col1:
            mvz_habitual = st.text_input("Médico Veterinario")
        with col2:
            tel_mvz = st.text_input("Teléfono MVZ", placeholder="55 1234 5678", key="nombre_mvz")

        st.subheader("Autorización de imagen")
        autoriza_imagen = st.radio(
            "¿Autoriza el uso de fotografías y/o videos de su perro con fines "
            "informativos, promocionales y publicitarios del Club?",
            ["Sí", "No"],
            horizontal=True,
        )

        st.subheader("Horario de la visita")
        col1, col2, col3 = st.columns(3)
        with col1:
            dia_visita = st.date_input("Día", value=date.today())
        with col2:
            hora_ingreso = st.time_input("Hora de ingreso", value=time(9, 0), step=1800)
        with col3:
            hora_salida = st.time_input("Hora de salida", value=time(18, 0), step=1800)

        observaciones = st.text_area("Observaciones")

        st.subheader("Firma del propietario o tutor")
        st.caption("Dibuja con el dedo (móvil/tablet) o el mouse")
        firma_propietario_canvas = st_canvas(
            stroke_width=3,
            stroke_color="#0000A0",
            background_color="#FFFFFF",
            height=150,
            width=400,
            drawing_mode="freedraw",
            key="firma_propietario_diurna",
        )

        st.subheader("Firma del responsable que recibe")
        st.caption("Dibuja con el dedo (móvil/tablet) o el mouse")
        firma_responsable_canvas = st_canvas(
            stroke_width=3,
            stroke_color="#0000A0",
            background_color="#FFFFFF",
            height=150,
            width=400,
            drawing_mode="freedraw",
            key="firma_responsable_diurna",
        )

        submitted = st.form_submit_button("Generar PDF")

    if submitted:
        pdf_bytes = render_estancia_diurna_pdf(
            propietario=propietario,
            telefono_propietario=telefono_propietario,
            correo_propietario=correo_propietario,
            identificacion_oficial=identificacion_oficial,
            perrito=perrito,
            raza=raza,
            edad=edad,
            sexo=sexo,
            peso=peso,
            color=color,
            mvz_habitual=mvz_habitual,
            tel_mvz=tel_mvz,
            autoriza_imagen=autoriza_imagen,
            dia_visita=dia_visita.strftime("%d/%m/%Y"),
            hora_ingreso=hora_ingreso.strftime("%H:%M"),
            hora_salida=hora_salida.strftime("%H:%M"),
            observaciones=observaciones or "",
            firma_propietario=canvas_to_base64_png(firma_propietario_canvas),
            firma_responsable=canvas_to_base64_png(firma_responsable_canvas),
        )

        st.success("PDF generado correctamente.")
        st.download_button(
            label="⬇️ Descargar PDF",
            data=pdf_bytes,
            file_name=f"guarderia_{perrito.replace(' ', '_').lower()}_{date.today().strftime('%d_%m_%y')}.pdf",
            mime="application/pdf",
        )