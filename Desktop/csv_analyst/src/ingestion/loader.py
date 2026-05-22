# src/ingestion/loader.py
# Lecture de fichiers CSV/Excel vers DataFrame pandas

import pandas as pd
from pathlib import Path


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def load_file(path: str | Path) -> pd.DataFrame:
    """
    Charge un CSV ou Excel en DataFrame.
    Détecte automatiquement le séparateur CSV (, ou ;).
    """
    path = Path(path)

    if path.suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Format non supporté : {path.suffix}. Acceptés : {SUPPORTED_EXTENSIONS}")

    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    if path.suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    # Détection auto du séparateur
    sample = path.read_text(encoding="utf-8", errors="replace")[:2048]
    sep = ";" if sample.count(";") > sample.count(",") else ","

    return pd.read_csv(path, sep=sep)