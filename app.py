import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime, time
from pathlib import Path

st.set_page_config(
    page_title="Generador RCA",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Generador de Informe de Incidente / RCA")

# ==================================================
# DATOS GENERALES
# ==================================================

st.header("Información General")

incidente = st.text_input("Número de Incidente")
reportado_por = st.text_input("Reportado por")
responsable = st.text_input("Responsable")

col1, col2 = st.columns(2)

with col1:
    fecha_inicio = st.date_input("Fecha Inicio")
    hora_inicio = st.time_input(
        "Hora Inicio",
        value=time(0, 0)
    )

with col2:
    fecha_fin = st.date_input("Fecha Fin")
    hora_fin = st.time_input(
        "Hora Fin",
        value=time(0, 0)
    )

forma_detectar = st.text_area(
    "Forma de detección"
)

procesos_impactados = st.text_area(
    "Procesos impactados"
)

tipo_incidente = st.selectbox(
    "Tipo de incidente",
    [
        "Disponibilidad",
        "Aplicación",
        "Infraestructura",
        "Base de Datos",
        "Red",
        "Seguridad"
    ]
)

estado = st.selectbox(
    "Estado",
    ["Abierto", "Cerrado"]
)

# ==================================================
# RESUMEN
# ==================================================

st.header("Resumen")

resumen = st.text_area(
    "Resumen del incidente",
    height=200
)

# ==================================================
# CAUSA
# ==================================================

st.header("Causa Raíz")

causa = st.text_area(
    "Causa identificada",
    height=200
)

# ==================================================
# ACCIONES
# ==================================================

st.header("Acciones Ejecutadas")

acciones = []

cantidad_acciones = st.number_input(
    "Número de acciones",
    min_value=1,
    max_value=20,
    value=3
)

for i in range(cantidad_acciones):

    st.subheader(f"Acción {i+1}")

    col1, col2 = st.columns(2)

    with col1:
        fecha_accion = st.date_input(
            "Fecha",
            key=f"fecha_accion_{i}"
        )

    with col2:
        hora_accion = st.time_input(
            "Hora",
            key=f"hora_accion_{i}"
        )

    detalle = st.text_input(
        "Detalle",
        key=f"detalle_accion_{i}"
    )

    if detalle:

        acciones.append({
            "fecha": fecha_accion.strftime("%d/%m/%Y"),
            "hora": hora_accion.strftime("%H:%M"),
            "detalle": detalle
        })

# ==================================================
# PLANES DE ACCIÓN
# ==================================================

st.header("Plan de Acción")

planes = []

cantidad_planes = st.number_input(
    "Cantidad de actividades",
    min_value=1,
    max_value=20,
    value=3
)

for i in range(cantidad_planes):

    actividad = st.text_input(
        f"Actividad {i+1}",
        key=f"actividad_{i}"
    )

    responsable_plan = st.text_input(
        "Responsable",
        key=f"resp_{i}"
    )

    fecha_inicio_plan = st.date_input(
        "Inicio",
        key=f"inicio_{i}"
    )

    fecha_fin_plan = st.date_input(
        "Fin",
        key=f"fin_{i}"
    )

    estado_plan = st.selectbox(
        "Estado",
        [
            "Pendiente",
            "En Progreso",
            "Completado"
        ],
        key=f"estado_{i}"
    )

    if actividad:

        planes.append({
            "numero": i + 1,
            "actividad": actividad,
            "responsable": responsable_plan,
            "fecha_inicio": fecha_inicio_plan.strftime("%d/%m/%Y"),
            "fecha_fin": fecha_fin_plan.strftime("%d/%m/%Y"),
            "estado": estado_plan
        })

# ==================================================
# RCA
# ==================================================

tipo_rca = st.radio(
    "Tipo RCA",
    [
        "DEFINITIVA",
        "TEMPORAL"
    ]
)

# ==================================================
# EQUIPO
# ==================================================

st.header("Equipo Investigador")

departamento = st.text_input("Departamento")
investigador = st.text_input("Investigador")
cargo = st.text_input("Cargo")

# ==================================================
# GENERAR
# ==================================================

if st.button("Generar Informe"):

    campos = [
        incidente,
        reportado_por,
        responsable,
        resumen,
        causa
    ]

    if not all(campos):
        st.error(
            "Complete los campos obligatorios."
        )
        st.stop()

    if not Path(
        "template_incidente.docx"
    ).exists():

        st.error(
            "No existe template_incidente.docx"
        )
        st.stop()

    try:

        doc = DocxTemplate(
            "template_incidente.docx"
        )

        context = {

            "codigo": incidente,
            "fecha": datetime.now().strftime("%d/%m/%Y"),

            "incidente": incidente,
            "reportado_por": reportado_por,
            "responsable": responsable,

            "fecha_inicio": datetime.combine(
                fecha_inicio,
                hora_inicio
            ).strftime("%d/%m/%Y %H:%M"),

            "fecha_fin": datetime.combine(
                fecha_fin,
                hora_fin
            ).strftime("%d/%m/%Y %H:%M"),

            "forma_detectar": forma_detectar,
            "procesos_impactados": procesos_impactados,
            "tipo_incidente": tipo_incidente,
            "estado": estado,

            "resumen": resumen,
            "causa": causa,

            "acciones": acciones,
            "planes": planes,

            "rca_definitiva":
                "X" if tipo_rca == "DEFINITIVA" else "",

            "rca_temporal":
                "X" if tipo_rca == "TEMPORAL" else "",

            "departamento": departamento,
            "nombre_investigador": investigador,
            "cargo_investigador": cargo
        }

        doc.render(context)

        archivo_seguro = (
            incidente
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
            .replace("*", "_")
            .replace("?", "_")
            .replace("\"", "_")
            .replace("<", "_")
            .replace(">", "_")
            .replace("|", "_")
        )

        nombre_archivo = (
            f"Incidente_{archivo_seguro}.docx"
        )

        doc.save(nombre_archivo)

        with open(
            nombre_archivo,
            "rb"
        ) as archivo:

            st.download_button(
                label="📥 Descargar Informe",
                data=archivo.read(),
                file_name=nombre_archivo,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        st.success(
            "✅ Informe generado correctamente"
        )

    except Exception as e:
        st.exception(e)
