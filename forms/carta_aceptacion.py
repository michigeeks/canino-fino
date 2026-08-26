"""
Formulario: Carta de Aceptación de Servicios.

Cada formulario del sidebar vive en su propio módulo dentro de forms/,
con una función render() que app.py invoca según la opción de menú
seleccionada. Así, agregar un nuevo formulario en el futuro es: crear
forms/nuevo_formulario.py con su propio render(), e importarlo/enrutarlo
desde app.py — sin tocar este archivo.
"""

from datetime import date

import streamlit as st
from streamlit_drawable_canvas import st_canvas

from utils import canvas_to_base64_png, render_ficha_pdf


def render() -> None:
    """Dibuja el formulario completo y gestiona la generación del PDF."""
    with st.form("ficha_form", clear_on_submit=False):

        st.subheader("Datos de estancia")
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha = st.date_input("Fecha", value=date.today())
        with col2:
            ingreso = st.date_input("Ingreso")
        with col3:
            salida_estimada = st.date_input("Salida estimada")

        st.subheader("Propietario / Tutor")
        col1, col2 = st.columns(2)
        with col1:
            propietario = st.text_input("Nombre del propietario/tutor *")
        with col2:
            telefono_propietario = st.text_input("Teléfono", placeholder="55 1234 5678", key="nombre_tutor")

        st.subheader("Datos del perrito")
        col1, col2 = st.columns(2)
        with col1:
            perrito = st.text_input("Nombre del perrito *")
            raza = st.text_input("Raza")
            edad = st.number_input("Edad", min_value=1, max_value=100, step=1, format="%d")
        with col2:
            sexo = st.selectbox("Sexo", ["", "Macho", "Hembra"])
            peso = st.number_input("Peso aproximado (kg)", min_value=0.0, max_value=100.0, step=0.5)

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
            telefono_autorizada = st.text_input("Teléfono", placeholder="55 1234 5678", key="nombre_per_autorizada")

        st.subheader("Contacto de emergencia")
        col1, col2 = st.columns(2)
        with col1:
            contacto_emergencia = st.text_input("Nombre del contacto")
        with col2:
            telefono_emergencia = st.text_input("Teléfono", placeholder="55 1234 5678", key="nombre_emergencia")

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
            stroke_color="#0000A0",
            background_color="#FFFFFF",
            height=150,
            width=400,
            drawing_mode="freedraw",
            key="firma_propietario",
        )

        st.subheader("Firma del responsable del Club")
        st.caption("Dibuja con el dedo (móvil/tablet) o el mouse")
        firma_responsable_canvas = st_canvas(
            stroke_width=3,
            stroke_color="#0000A0",
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
                ingreso=ingreso.strftime("%d/%m/%Y"),
                salida_estimada=salida_estimada.strftime("%d/%m/%Y"),
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
                label="⬇️ Descargar PDF",
                data=pdf_bytes,
                file_name=f"carta_aceptacion_{perrito.replace(' ', '_').lower()}.pdf",
                mime="application/pdf",
            )