from collections.abc import Callable, Sequence
import math

from ecovision.domain.categories import (
    ClassificationResult,
    RankedPrediction,
    guide_for_label,
)


def classify_image(
    image: object,
    labels: Sequence[str],
    predict: Callable[[object], Sequence[float]],
) -> ClassificationResult:
    scores = tuple(float(score) for score in predict(image))
    if not labels or len(scores) != len(labels):
        raise ValueError(
            f"El modelo devolvió {len(scores)} puntuaciones para {len(labels)} etiquetas."
        )
    if not all(math.isfinite(score) for score in scores):
        raise ValueError("El modelo devolvió puntuaciones no válidas.")

    best_index = max(range(len(scores)), key=scores.__getitem__)
    label = labels[best_index]
    guide = guide_for_label(label)
    alternatives = tuple(
        RankedPrediction(
            label=guide_for_label(labels[index]).display_name,
            confidence=scores[index],
        )
        for index in sorted(range(len(scores)), key=scores.__getitem__, reverse=True)
        if index != best_index
    )
    return ClassificationResult(
        label=guide.display_name,
        confidence=scores[best_index],
        guide=guide,
        alternatives=alternatives,
    )
