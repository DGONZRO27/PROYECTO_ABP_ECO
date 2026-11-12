from io import BytesIO

import streamlit as st
from PIL import Image

from ecovision.application.classification import classify_image
from ecovision.infrastructure.keras_model import (
    LABELS_PATH,
    load_model,
    predict_probabilities,
)
from ecovision.infrastructure.labels import read_labels


@st.cache_resource
def _cached_model():
    return load_model()


@st.cache_data
def _cached_labels() -> tuple[str, ...]:
    return read_labels(LABELS_PATH)


def _render_guide() -> None:
    st.markdown("#### Materiales que reconoce")
    columns = st.columns(4)
    for column, material in zip(columns, ("Plástico", "Papel y cartón", "Metal", "Vidrio")):
        with column:
            st.markdown(f"**{material}**")
            st.caption("Aprovechable · caneca blanca")


def _render_classification(uploaded_file) -> None:
    try:
        labels = _cached_labels()
        model = _cached_model()
        with Image.open(BytesIO(uploaded_file.getvalue())) as source_image:
            image = source_image.copy()
        result = classify_image(
            image,
            labels,
            lambda selected_image: predict_probabilities(model, selected_image),
        )
    except (FileNotFoundError, ModuleNotFoundError, OSError, ValueError) as error:
        st.error(f"No fue posible clasificar la imagen: {error}")
        if isinstance(error, ModuleNotFoundError):
            st.info("Instala las dependencias con `pip install -r requirements.txt`.")
        return

    image_column, result_column = st.columns([1, 1], gap="large")
    with image_column:
        st.image(image, caption="Imagen analizada", use_container_width=True)
    with result_column:
        st.markdown("### Resultado")
        st.success(f"Material identificado: **{result.label}**")
        st.markdown(f"### {result.guide.bin_name}")
        st.caption(f"Color de separación: {result.guide.bin_color}")
        st.write(result.guide.instruction)
        confidence_percent = round(result.confidence * 100)
        st.progress(max(0, min(confidence_percent, 100)))
        st.caption(f"Confianza del modelo: {confidence_percent}%")
        if result.confidence < 0.60:
            st.warning(
                "La confianza es baja. Revisa el material antes de separarlo; "
                "esta predicción no sustituye la clasificación manual."
            )
        if result.alternatives:
            alternative = result.alternatives[0]
            st.caption(
                f"Alternativa: {alternative.label} "
                f"({round(alternative.confidence * 100)}%)."
            )


def run_app() -> None:
    st.set_page_config(
        page_title="EcoVision | Clasificación de residuos",
        page_icon="♻️",
        layout="wide",
    )

    st.title("Dale una segunda vida a tus residuos.")
    st.write(
        "Toma una foto o carga una imagen para identificar plástico, papel y cartón, "
        "metal o vidrio y conocer cómo separarlo."
    )
    st.info(
        "En Colombia, estos materiales aprovechables van en la **caneca blanca** "
        "cuando están limpios y secos."
    )

    camera_tab, upload_tab = st.tabs(["Tomar una foto", "Subir una imagen"])
    with camera_tab:
        camera_image = st.camera_input("Enfoca un solo material y toma la foto.")
    with upload_tab:
        uploaded_image = st.file_uploader(
            "Selecciona una imagen del material",
            type=("jpg", "jpeg", "png", "webp"),
            help="Usa una foto clara, con un solo material como protagonista.",
        )

    selected_image = camera_image or uploaded_image
    if selected_image is not None:
        _render_classification(selected_image)
    else:
        _render_guide()

    st.divider()
    st.caption(
        "EcoVision es un prototipo educativo. La clasificación puede fallar, "
        "especialmente con objetos mezclados, sucios o fuera de las clases entrenadas."
    )
    st.caption(
        "Proyecto académico creado por Daniel Alejandro Gonzalez · "
        "[Código fuente en GitHub](https://github.com/DGONZRO27/PROYECTO_ABP_ECO)"
    )
