"""
Modulo de Leitura Tabular com Deteccao Inteligente
Autor: Suelio Lima
"""

import csv
from pathlib import Path
from typing import Tuple, Dict, Any, Union
import pandas as pd


class FileReader:
    """Classe responsavel pela leitura de datasets tabulares com deteccao automatica."""

    SUPPORTED_ENCODINGS = ["utf-8", "utf-8-sig", "cp1252", "latin1", "iso-8859-1"]
    COMMON_DELIMITERS = [",", ";", "\t", "|"]

    @classmethod
    def detect_encoding(cls, file_path: Path) -> str:
        for enc in cls.SUPPORTED_ENCODINGS:
            try:
                with open(file_path, "r", encoding=enc, errors="strict") as f:
                    f.read(8192)
                return enc
            except (UnicodeDecodeError, UnicodeError):
                continue
        return "utf-8"

    @classmethod
    def detect_delimiter(cls, file_path: Path, encoding: str = "utf-8") -> str:
        try:
            with open(file_path, "r", encoding=encoding, errors="replace") as f:
                sample_lines = [f.readline() for _ in range(10)]
                sample_text = "".join([l for l in sample_lines if l.strip()])

            if sample_text:
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample_text, delimiters=cls.COMMON_DELIMITERS)
                return dialect.delimiter
        except Exception:
            pass

        try:
            with open(file_path, "r", encoding=encoding, errors="replace") as f:
                first_line = f.readline()
                counts = {d: first_line.count(d) for d in cls.COMMON_DELIMITERS}
                best = max(counts, key=counts.get)
                if counts[best] > 0:
                    return best
        except Exception:
            pass

        return ","

    @classmethod
    def read(cls, source: Union[str, Path]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        path = Path(source)
        if not path.is_file():
            raise FileNotFoundError(f"Arquivo nao encontrado: {source}")

        suffix = path.suffix.lower()
        size_bytes = path.stat().st_size
        meta = {
            "caminho_origem": str(path.resolve()),
            "nome_arquivo": path.name,
            "extensao_origem": suffix,
            "tamanho_bytes": size_bytes
        }

        if suffix in [".xlsx", ".xls"]:
            df = pd.read_excel(path)
            meta.update({"formato": "Excel", "delimitador": None, "encoding": None})
        elif suffix == ".parquet":
            df = pd.read_parquet(path)
            meta.update({"formato": "Parquet", "delimitador": None, "encoding": None})
        elif suffix == ".json":
            df = pd.read_json(path)
            meta.update({"formato": "JSON", "delimitador": None, "encoding": "utf-8"})
        else:
            encoding = cls.detect_encoding(path)
            delimiter = "\t" if suffix == ".tsv" else cls.detect_delimiter(path, encoding)
            df = pd.read_csv(path, encoding=encoding, sep=delimiter)
            meta.update({
                "formato": "Texto Delimitado" if suffix == ".txt" else "CSV",
                "delimitador": delimiter,
                "encoding": encoding
            })

        meta["linhas"] = int(len(df))
        meta["colunas"] = int(len(df.columns))
        return df, meta
