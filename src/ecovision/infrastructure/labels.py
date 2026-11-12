from pathlib import Path
import re


_LABEL_PATTERN = re.compile(r"^\s*(\d+)\s+(.+?)\s*$")


def read_labels(path: Path) -> tuple[str, ...]:
    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de etiquetas: {path}")

    indexed_labels: dict[int, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        if not line.strip():
            continue
        match = _LABEL_PATTERN.fullmatch(line)
        if match is None:
            raise ValueError(f"Formato de etiqueta inválido en la línea {line_number}: {line!r}")

        index = int(match.group(1))
        if index in indexed_labels:
            raise ValueError(f"El índice de etiqueta {index} está repetido.")
        indexed_labels[index] = match.group(2).strip()

    expected_indices = list(range(len(indexed_labels)))
    if sorted(indexed_labels) != expected_indices:
        raise ValueError("Los índices de labels.txt deben iniciar en 0 y ser consecutivos.")
    if any(not label for label in indexed_labels.values()):
        raise ValueError("labels.txt contiene una etiqueta vacía.")

    return tuple(indexed_labels[index] for index in expected_indices)
