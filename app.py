import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
from pathlib import Path

# ==================================
# CONFIGURACION
# ==================================

st.set_page_config(
    page_title="Generador Informe de Incidente",
    layout="wide"
)

st.title("📄 Generador Informe de Incidente / RCA")

# ==================================
# DATOS GENERALES
# ==================================

st.header("Información General")

incidente = st.text_input(
    "N° Incidente *"
)

reportado_por = st.text_input(
    "Reportado por *"
)

responsable = st.text_input(
    "Responsable del incidente *"
)

# ==================================
# FECHAS CON SELECTOR
# ==================================

st.subheader("Fechas del Incidente")

col1, col2 = st.columns(2)

with col1:

    fecha_inicio = st.date_input(
        "Fecha Inicio *",
        value=datetime.today()
    )

    hora_inicio = st.time_input(
        "Hora Inicio *",
        value=datetime.now().time()
    )

with col2:

    fecha_fin = st.date_input(
        "Fecha Fin *",
        value=datetime.today()
    )

    hora_fin = st.time_input(
        "Hora Fin *",
        value=datetime.now().time()
    )

forma_detectar = st.text_area(
    "Forma de detectar *",
    height=100
)

procesos_impactados = st.text_area(
    "Procesos impactados *",
    height=100
)

tipo_incidente = st.selectbox(
    "Tipo de Incidente *",
    [
        "Disponibilidad",
        "Aplicación",
        "Infraestructura",
        "Base de Datos",
        "Seguridad",
        "Red",
        "Servicio"
    ]
)

estado = st.selectbox(
    "Estado *",
    [
        "Abierto",
        "Cerrado"
    ]
)

# ==================================
# RESUMEN
# ==================================

st.header("Resumen del Incidente")

resumen = st.text_area(
    "Resumen del incidente *",
    height=200
)

# ==================================
# ACCIONES TOMADAS
# ==================================

st.header("Acciones Tomadas")

acciones = []

cantidad_acciones = st.number_input(
    "Cantidad de acciones realizadas",
    min_value=1,
    max_value=20,
    value=3
)

for i in range(cantidad_acciones):

    st.subheader(f"Acción {i + 1}")

    col1, col2, col3 = st.columns([2, 2, 6])

    with col1:

        fecha_accion = st.text_input(
            "Fecha",
            key=f"fecha_accion_{i}"
        )

    with col2:

        hora_accion = st.text_input(
            "Hora",
            key=f"hora_accion_{i}"
        )

    with col3:

        detalle_accion = st.text_input(
            "Detalle",
            key=f"detalle_accion_{i}"
        )

    if detalle_accion.strip():

        acciones.append({
            "fecha": fecha_accion,
            "hora": hora_accion,
            "detalle": detalle_accion
        })

# ==================================
# CAUSA
# ==================================

st.header("Causa del Problema")

causa = st.text_area(
    "Causa identificada *",
    height=200
)

# ==================================
# PLAN DE ACCION
# ==================================

st.header("Plan de Acción")

planes = []

cantidad_planes = st.number_input(
    "Cantidad de actividades",
    min_value=1,
    max_value=20,
    value=3
)

for i in range(cantidad_planes):

    st.subheader(f"Actividad {i + 1}")

    actividad = st.text_input(
        "Actividad",
        key=f"actividad_{i}"
    )

    responsable_plan = st.text_input(
        "Responsable",
        key=f"responsable_plan_{i}"
    )

    col1, col2 = st.columns(2)

    with col1:

        fecha_inicio_plan = st.date_input(
            "Fecha Inicio",
            key=f"inicio_plan_{i}"
        )

    with col2:

        fecha_fin_plan = st.date_input(
            "Fecha Fin",
            key=f"fin_plan_{i}"
        )

    estado_plan = st.selectbox(
        "Estado",
        [
            "Pendiente",
            "En Progreso",
            "Completado"
        ],
        key=f"estado_plan_{i}"
    )

    if actividad.strip():

        planes.append({

            "numero": i + 1,
            "actividad": actividad,
            "responsable": responsable_plan,

            "fecha_inicio": fecha_inicio_plan.strftime(
                "%d/%m/%Y"
            ),

            "fecha_fin": fecha_fin_plan.strftime(
                "%d/%m/%Y"
            ),

            "estado": estado_plan
        })

# ==================================
# RCA
# ==================================

st.header("Tipo de RCA")

tipo_rca = st.radio(
    "Seleccione una opción",
    [
        "DEFINITIVA",
        "TEMPORAL"
    ]
)

# ==================================
# EQUIPO INVESTIGADOR
# ==================================

st.header("Equipo de Investigación")

departamento = st.text_input(
    "Departamento"
)

nombre_investigador = st.text_input(
    "Investigador"
)

cargo_investigador = st.text_input(
    "Cargo"
)

# ==================================
# GENERAR DOCUMENTO
# ==================================

if st.button("🚀 Generar Informe"):

    if not all([
        incidente,
        reportado_por,
        responsable,
        forma_detectar,
        procesos_impactados,
        resumen,
        causa
    ]):

        st.error(
            "⚠️ Complete todos los campos obligatorios."
        )
        st.stop()

    if not Path(
        "template_incidente.docx"
    ).exists():

        st.error(
            "⚠️ No se encontró el archivo template_incidente.docx"
        )
        st.stop()

    try:

        fecha_inicio_str = datetime.combine(
            fecha_inicio,
            hora_inicio
        ).strftime("%d/%m/%Y %H:%M")

        fecha_fin_str = datetime.combine(
            fecha_fin,
            hora_fin
        ).strftime("%d/%m/%Y %H:%M")

        doc = DocxTemplate(
            "template_incidente.docx"
        )

        context = {

            # ENCABEZADO

            "codigo": incidente,
            "fecha": datetime.now().strftime(
                "%d/%m/%Y"
            ),

            # DATOS GENERALES

            "incidente": incidente,
            "reportado_por": reportado_por,
            "responsable": responsable,

            "fecha_inicio": fecha_inicio_str,
            "fecha_fin": fecha_fin_str,

            "forma_detectar": forma_detectar,
            "procesos_impactados": procesos_impactados,
            "tipo_incidente": tipo_incidente,
            "estado": estado,

            # RESUMEN

            "resumen": resumen,

            # ACCIONES

            "acciones": acciones,

            # CAUSA

            "causa": causa,

            # PLAN DE ACCIÓN

            "planes": planes,

            # RCA

            "rca_definitiva":
                "X"
                if tipo_rca == "DEFINITIVA"
                else "",

            "rca_temporal":
                "X"
                if tipo_rca == "TEMPORAL"
                else "",

            # EQUIPO

            "departamento": departamento,
            "nombre_investigador": nombre_investigador,
            "cargo_investigador": cargo_investigador
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

        nombre_archivo = f"Incidente_{archivo_seguro}.docx"

        doc.save(nombre_archivo)

        with open(
            nombre_archivo,
            "rb"
        ) as archivo:

            st.download_button(
                label="📥 Descargar Informe",
                data=archivo,
                file_name=nombre_archivo,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        st.success(
            "✅ Informe generado correctamente"
        )

    except Exception as e:

        st.error(
            f"❌ Error generando documento: {str(e)}"
        )
