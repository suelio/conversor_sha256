"""
Modulo de Normalizacao de Dados Pessoais (PII) Pre-Hash
Autor: Suelio Lima
"""

import re
from typing import Any
import pandas as pd


class DataNormalizer:
    """Classe responsavel por higienizar e padronizar dados sensiveis antes do calculo do hash."""

    @staticmethod
    def normalize_value(val: Any, column_name: str = "") -> str:
        """
        Padroniza valores de entrada para garantir hashing deterministico e consistente.
        """
        if pd.isna(val) or val is None:
            return ""

        text = str(val).strip()
        col_lower = column_name.lower().strip()

        # Normalizacao para emails: converter para minusculas e remover espacos
        if any(term in col_lower for term in ["email", "e-mail", "mail"]):
            return text.lower()

        # Normalizacao para documentos numericos (CPF, CNPJ, RG, Titulo): remover pontuacao
        if any(term in col_lower for term in ["cpf", "cnpj", "rg", "documento", "doc"]):
            return re.sub(r"[^\w]", "", text)

        # Normalizacao para telefones
        if any(term in col_lower for term in ["telefone", "celular", "phone", "tel"]):
            return re.sub(r"[^\d]", "", text)

        return text
