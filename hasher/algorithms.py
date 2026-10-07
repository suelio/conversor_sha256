"""
Modulo de Algoritmos Criptograficos e Salteamento (Salt / HMAC)
Autor: Suelio Lima
"""

import hmac
import hashlib
from typing import Optional


class HashAlgorithms:
    """Classe responsavel pela geracao de hashes criptograficos com suporte a Salt e HMAC."""

    SUPPORTED_ALGORITHMS = {
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
        "sha384": hashlib.sha384,
        "sha1": hashlib.sha1,
        "md5": hashlib.md5
    }

    @classmethod
    def compute(
        cls,
        text: str,
        algorithm: str = "sha256",
        salt: Optional[str] = None,
        use_hmac: bool = False
    ) -> str:
        """
        Calcula o hash do texto utilizando o algoritmo selecionado.
        
        Args:
            text: Conteudo textual a ser anonimizado.
            algorithm: Algoritmo desejado ('sha256', 'sha512', 'sha384', 'sha1', 'md5').
            salt: Chave secreta / salteamento adicional para prevencao contra Rainbow Tables.
            use_hmac: Se True e salt for fornecido, utiliza HMAC-Hash.
            
        Returns:
            String hexadecimal contendo o hash criptografico.
        """
        algo_name = algorithm.lower().strip()
        if algo_name not in cls.SUPPORTED_ALGORITHMS:
            raise ValueError(f"Algoritmo '{algorithm}' nao suportado. Opcoes validas: {', '.join(cls.SUPPORTED_ALGORITHMS.keys())}")

        hash_func = cls.SUPPORTED_ALGORITHMS[algo_name]
        data_bytes = str(text).encode("utf-8")

        if salt:
            salt_bytes = str(salt).encode("utf-8")
            if use_hmac:
                return hmac.new(salt_bytes, data_bytes, hash_func).hexdigest()
            # Salteamento por prefixo padrao
            return hash_func(salt_bytes + data_bytes).hexdigest()

        return hash_func(data_bytes).hexdigest()
