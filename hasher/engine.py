"""
Motor Principal de Anonimizacao e Geracao de Hash
Autor: Suelio Lima
"""

import time
from pathlib import Path
from typing import Union, Optional, List, Dict, Any
import pandas as pd

from .algorithms import HashAlgorithms
from .normalizer import DataNormalizer
from .reader import FileReader
from .writer import FileWriter


class DataHasher:
    """Orquestrador para anonimizacao criptografica de dados sensiveis."""

    @classmethod
    def anonymize_dataframe(
        cls,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        algorithm: str = "sha256",
        salt: Optional[str] = None,
        keep_original: bool = False,
        normalize: bool = True,
        fingerprint_col: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Aplica hash criptografico sobre colunas selecionadas ou sobre a linha completa.
        """
        df_out = df.copy()

        # Se nenhuma coluna foi indicada e o DataFrame tiver 1 coluna, usa essa coluna (compatibilidade)
        target_cols = columns
        if target_cols is None and len(df.columns) == 1:
            target_cols = list(df.columns)

        # 1. Anonimizacao de colunas especificas
        if target_cols:
            for col in target_cols:
                if col not in df_out.columns:
                    raise KeyError(f"A coluna '{col}' nao existe no DataFrame.")

                def hash_field(val):
                    clean_val = DataNormalizer.normalize_value(val, col) if normalize else str(val)
                    return HashAlgorithms.compute(clean_val, algorithm=algorithm, salt=salt)

                hashed_series = df_out[col].apply(hash_field)
                if keep_original:
                    df_out[f"{col}_hash"] = hashed_series
                else:
                    df_out[col] = hashed_series

        # 2. Geracao opcional de fingerprint composto (hash de toda a linha)
        if fingerprint_col:
            def hash_row(row):
                row_str = "|".join([str(val) for val in row.values])
                return HashAlgorithms.compute(row_str, algorithm=algorithm, salt=salt)

            df_out[fingerprint_col] = df_out.apply(hash_row, axis=1)

        return df_out

    @classmethod
    def process_file(
        cls,
        source: Union[str, Path],
        target_format: Optional[str] = None,
        columns: Optional[List[str]] = None,
        output_path: Optional[Union[str, Path]] = None,
        algorithm: str = "sha256",
        salt: Optional[str] = None,
        keep_original: bool = False,
        normalize: bool = True,
        fingerprint_col: Optional[str] = None,
        delimiter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processa e salva arquivo com colunas anonimizadas.
        """
        start_time = time.perf_counter()
        source_path = Path(source)

        df, meta_in = FileReader.read(source_path)

        # Se columns for None e tiver mais de 1 coluna, aplica na primeira por padrao se nada informado
        selected_cols = columns
        if selected_cols is None and len(df.columns) > 1 and not fingerprint_col:
            # Por padrao, avisa ou aplica sobre todas as colunas de texto
            selected_cols = list(df.select_dtypes(include=["object"]).columns)

        df_anonymized = cls.anonymize_dataframe(
            df=df,
            columns=selected_cols,
            algorithm=algorithm,
            salt=salt,
            keep_original=keep_original,
            normalize=normalize,
            fingerprint_col=fingerprint_col
        )

        # Determina formato de saida
        clean_fmt = target_format.lower().lstrip(".") if target_format else source_path.suffix.lstrip(".").lower()
        if not clean_fmt:
            clean_fmt = "csv"

        if output_path is None:
            final_target = source_path.with_name(f"{source_path.stem}_{algorithm}.{clean_fmt}")
        else:
            p_out = Path(output_path)
            if p_out.is_dir() or not p_out.suffix:
                final_target = p_out / f"{source_path.stem}_{algorithm}.{clean_fmt}"
            else:
                final_target = p_out

        saved_path, size_out = FileWriter.write(
            df=df_anonymized,
            target_path=final_target,
            target_format=clean_fmt,
            delimiter=delimiter
        )

        elapsed = round(time.perf_counter() - start_time, 4)
        throughput = round(len(df) / elapsed, 1) if elapsed > 0 else len(df)

        return {
            "status": "Sucesso",
            "arquivo_origem": str(source_path.resolve()),
            "arquivo_destino": str(saved_path.resolve()),
            "algoritmo": algorithm.upper(),
            "salt_utilizado": bool(salt),
            "colunas_anonimizadas": selected_cols or [],
            "fingerprint_criado": fingerprint_col,
            "linhas_processadas": int(len(df)),
            "colunas_finais": int(len(df_anonymized.columns)),
            "tempo_segundos": elapsed,
            "taxa_linhas_por_segundo": throughput,
            "tamanho_saida_kb": round(size_out / 1024, 2)
        }

    @classmethod
    def process_batch(
        cls,
        source_dir: Union[str, Path],
        target_format: str = "csv",
        columns: Optional[List[str]] = None,
        output_dir: Optional[Union[str, Path]] = None,
        algorithm: str = "sha256",
        salt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Processa em lote todos os arquivos compativeis de uma pasta."""
        start_batch = time.perf_counter()
        in_dir = Path(source_dir)
        if not in_dir.is_dir():
            raise NotADirectoryError(f"Pasta nao encontrada: {source_dir}")

        out_dir = Path(output_dir) if output_dir else in_dir / "anonimizados"
        out_dir.mkdir(parents=True, exist_ok=True)

        target_exts = [".csv", ".tsv", ".txt", ".xlsx", ".parquet", ".json"]
        files = [p for p in in_dir.iterdir() if p.is_file() and p.suffix.lower() in target_exts]

        results = []
        for f in files:
            try:
                res = cls.process_file(
                    source=f,
                    target_format=target_format,
                    columns=columns,
                    output_path=out_dir,
                    algorithm=algorithm,
                    salt=salt
                )
                results.append(res)
            except Exception as e:
                results.append({"status": "Erro", "arquivo": str(f.resolve()), "erro": str(e)})

        total_elapsed = round(time.perf_counter() - start_batch, 4)

        return {
            "pasta_origem": str(in_dir.resolve()),
            "pasta_destino": str(out_dir.resolve()),
            "total_arquivos": len(files),
            "sucessos": sum(1 for r in results if r.get("status") == "Sucesso"),
            "falhas": sum(1 for r in results if r.get("status") == "Erro"),
            "tempo_total_segundos": total_elapsed,
            "arquivos": results
        }

    @staticmethod
    def select_file_gui() -> Optional[str]:
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            p = filedialog.askopenfilename(
                title="Selecione o arquivo para anonimizacao",
                filetypes=[
                    ("Arquivos Tabulares", "*.csv *.txt *.tsv *.xlsx *.parquet *.json"),
                    ("Todos os Arquivos", "*.*")
                ]
            )
            root.destroy()
            return p if p else None
        except Exception:
            return None

    @staticmethod
    def select_folder_gui() -> Optional[str]:
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            p = filedialog.askdirectory(title="Selecione a pasta para anonimizacao em lote")
            root.destroy()
            return p if p else None
        except Exception:
            return None

    @staticmethod
    def upload_via_colab() -> Optional[str]:
        try:
            from google.colab import files  # type: ignore
            print("[Hasher] Selecione o arquivo para envio:")
            uploaded = files.upload()
            if uploaded:
                return next(iter(uploaded))
            return None
        except ImportError:
            print("[Aviso] A funcao upload_via_colab deve ser executada dentro do Google Colab.")
            return None
