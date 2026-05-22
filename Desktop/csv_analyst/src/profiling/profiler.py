# src/profiling/profiler.py
# Analyse un DataFrame et produit un profil structuré
# Ce profil sera injecté comme contexte dans les prompts Claude

import pandas as pd
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ColumnProfile:
    name: str
    dtype: str
    null_count: int
    null_pct: float
    n_unique: int
    sample_values: list[Any]
    stats: dict = field(default_factory=dict)


@dataclass
class DatasetProfile:
    n_rows: int
    n_cols: int
    columns: list[ColumnProfile]

    def to_context(self) -> str:
        """
        Génère un bloc texte compact à injecter dans un prompt Claude.
        On n'envoie jamais les données brutes — juste le schéma et les stats.
        """
        lines = [f"Dataset : {self.n_rows} lignes × {self.n_cols} colonnes\n"]
        lines.append("Colonnes :")
        for col in self.columns:
            stats_str = ""
            if col.stats:
                stats_str = " | " + ", ".join(f"{k}={v}" for k, v in col.stats.items())
            samples = str(col.sample_values[:3])[1:-1]
            lines.append(
                f"  - {col.name} [{col.dtype}]"
                f" | {col.null_pct:.0f}% nulls"
                f" | {col.n_unique} valeurs uniques"
                f" | exemples : {samples}"
                f"{stats_str}"
            )
        return "\n".join(lines)


def profile_dataframe(df: pd.DataFrame) -> DatasetProfile:
    """Analyse un DataFrame et retourne son profil complet."""
    columns = []
    for col_name in df.columns:
        series = df[col_name]
        null_count = int(series.isna().sum())
        null_pct = null_count / len(df) * 100 if len(df) > 0 else 0
        n_unique = int(series.nunique())
        sample_values = series.dropna().head(5).tolist()

        stats = {}
        if pd.api.types.is_numeric_dtype(series):
            desc = series.describe()
            stats = {
                "min": round(float(desc["min"]), 2),
                "max": round(float(desc["max"]), 2),
                "mean": round(float(desc["mean"]), 2),
            }

        columns.append(ColumnProfile(
            name=col_name,
            dtype=str(series.dtype),
            null_count=null_count,
            null_pct=null_pct,
            n_unique=n_unique,
            sample_values=sample_values,
            stats=stats,
        ))

    return DatasetProfile(n_rows=len(df), n_cols=len(df.columns), columns=columns)