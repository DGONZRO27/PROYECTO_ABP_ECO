from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = PROJECT_ROOT / "models" / "keras_model.h5"
LABELS_PATH = PROJECT_ROOT / "models" / "labels.txt"
DEFAULT_IMAGE_SIZE = 224


def load_model() -> Any:
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"No se encontró el modelo Keras: {MODEL_PATH}")

    import tensorflow as tf

    return tf.keras.models.load_model(MODEL_PATH, compile=False)


def predict_probabilities(model: Any, image: Any) -> tuple[float, ...]:
    import numpy as np
    from PIL import Image, ImageOps

    input_shape = model.input_shape
    if isinstance(input_shape, list):
        if len(input_shape) != 1:
            raise ValueError("El modelo debe tener exactamente una entrada de imagen.")
        input_shape = input_shape[0]
    if len(input_shape) != 4 or input_shape[-1] != 3:
        raise ValueError(f"Se esperaba una entrada RGB de cuatro dimensiones; se recibió {input_shape}.")

    height = int(input_shape[1] or DEFAULT_IMAGE_SIZE)
    width = int(input_shape[2] or DEFAULT_IMAGE_SIZE)
    rgb_image = ImageOps.exif_transpose(image).convert("RGB")
    resized_image = rgb_image.resize((width, height), Image.Resampling.BILINEAR)
    pixels = np.asarray(resized_image, dtype=np.float32)
    normalized_pixels = (pixels / 127.5) - 1.0

    predictions = np.asarray(model.predict(normalized_pixels[np.newaxis, ...], verbose=0))
    if predictions.ndim == 2 and predictions.shape[0] == 1:
        predictions = predictions[0]
    if predictions.ndim != 1:
        raise ValueError(f"Se esperaba una predicción por imagen; se recibió {predictions.shape}.")
    return tuple(float(score) for score in predictions)
