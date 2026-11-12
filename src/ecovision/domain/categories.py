from dataclasses import dataclass
import re


@dataclass(frozen=True)
class WasteGuide:
    display_name: str
    bin_name: str
    bin_color: str
    bin_hex: str
    instruction: str


@dataclass(frozen=True)
class RankedPrediction:
    label: str
    confidence: float


@dataclass(frozen=True)
class ClassificationResult:
    label: str
    confidence: float
    guide: WasteGuide
    alternatives: tuple[RankedPrediction, ...]


_GUIDES = {
    "plastico": WasteGuide(
        display_name="Plástico",
        bin_name="Caneca blanca",
        bin_color="blanca",
        bin_hex="#F4F5F0",
        instruction="Enjuaga el envase, déjalo secar y aplástalo si es posible.",
    ),
    "papel_carton": WasteGuide(
        display_name="Papel y cartón",
        bin_name="Caneca blanca",
        bin_color="blanca",
        bin_hex="#F4F5F0",
        instruction="Deposítalos secos y sin grasa. Pliega las cajas para ahorrar espacio.",
    ),
    "metal": WasteGuide(
        display_name="Metal",
        bin_name="Caneca blanca",
        bin_color="blanca",
        bin_hex="#F4F5F0",
        instruction="Vacía y enjuaga latas y envases antes de separarlos.",
    ),
    "vidrio": WasteGuide(
        display_name="Vidrio",
        bin_name="Caneca blanca",
        bin_color="blanca",
        bin_hex="#F4F5F0",
        instruction="Separa botellas y frascos limpios; manipúlalos con cuidado.",
    ),
}


def guide_for_label(label: str) -> WasteGuide:
    normalized_label = re.sub(r"[\s-]+", "_", label.strip().casefold())
    try:
        return _GUIDES[normalized_label]
    except KeyError as error:
        raise ValueError(f"La etiqueta '{label}' no tiene una guía de reciclaje configurada.") from error
