"""
Modulo de Exportacao de Arquivos Anonimizados
Autor: Suelio Lima
"""

from pathlib import Path
from typing import Tuple, Optional
import pandas as pd


class FileWriter:
    """Classe responsavel por exportar DataFrames anonimizados."""

    SUPPORTED_FORMATS = ["csv", "txt", "xlsx", "parquet", "json", "tsv"]

    @classmethod
    def write(
        cls,
        df: pd.DataFrame,
        target_path: Path,
        target_format: str,
        delimiter: Optional[str] = None
    ) -> Tuple[Path, int]:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        fmt = target_format.lower().lstrip(".")

        if fmt == "csv":
            sep = delimiter if delimiter else ","
            df.to_csv(target_path, sep=sep, index=False, encoding="utf-8")
        elif fmt == "txt":
            sep = delimiter if delimiter else "\t"
            df.to_csv(target_path, sep=sep, index=False, encoding="utf-8")
        elif fmt == "tsv":
            df.to_csv(target_path, sep="\t", index=False, encoding="utf-8")
        elif fmt == "xlsx":
            df.to_excel(target_path, index=False, engine="openpyxl")
        elif fmt == "parquet":
            df.to_parquet(target_path, index=False, engine="pyarrow", compression="snappy")
        elif fmt == "json":
            df.to_json(target_path, orient="records", indent=2, force_ascii=False)
        else:
            raise ValueError(f"Formato '{fmt}' nao suportado.")

        return target_path, target_path.stat().st_size
