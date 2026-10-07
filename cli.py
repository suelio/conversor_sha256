#!/usr/bin/env python3
"""
Interface de Linha de Comando (CLI) para Anonimizacao Criptografica (SHA-256 e outros)
Autor: Suelio Lima
"""

import sys
import argparse
from pathlib import Path
from hasher import DataHasher, FileReader

# Garante compatibilidade de saida com terminais Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def run_interactive():
    print("=" * 65)
    print("       ANONIMIZADOR CRIPTOGRAFICO DE DADOS (LGPD / GDPR)")
    print("                    Autor: Suelio Lima")
    print("=" * 65)

    print("\nModo de Operacao:")
    print("1. Anonimizar um arquivo individual")
    print("2. Anonimizar todos os arquivos de uma pasta (Em Lote)")
    print("3. Sair")
    mode = input("Escolha uma opcao (1, 2 ou 3) [padrao: 1]: ").strip()

    if mode == "3":
        print("Encerrando.")
        return

    if mode == "2":
        # Processamento em lote
        print("\nComo deseja selecionar a pasta de origem?")
        print("1. Abrir explorador de pastas do Windows")
        print("2. Digitar o caminho da pasta")
        f_choice = input("Opcao (1 ou 2) [padrao: 1]: ").strip()

        if f_choice == "2":
            source_dir = input("Digite o caminho da pasta de origem: ").strip()
        else:
            print("[*] Abrindo janela de selecao de pasta...")
            source_dir = DataHasher.select_folder_gui()

        if not source_dir or not Path(source_dir).is_dir():
            print("[!] Pasta invalida ou operacao cancelada.")
            return

        cols_str = input("\nColunas para anonimizar separadas por virgula (deixe vazio para todas de texto): ").strip()
        cols = [c.strip() for c in cols_str.split(",") if c.strip()] if cols_str else None

        algo = input("Algoritmo (sha256, sha512, md5) [padrao: sha256]: ").strip() or "sha256"
        salt = input("Chave secreta / Salt (opcional para protecao contra Rainbow Tables): ").strip() or None
        target_fmt = input("Formato de saida (csv, parquet, xlsx) [padrao: csv]: ").strip() or "csv"

        print(f"\n[*] Iniciando processamento em lote com {algo.upper()}...")
        batch_res = DataHasher.process_batch(
            source_dir=source_dir,
            target_format=target_fmt,
            columns=cols,
            algorithm=algo,
            salt=salt
        )
        print("\n[+] Resumo do Lote:")
        print(f"Total de arquivos: {batch_res['total_arquivos']}")
        print(f"Sucessos: {batch_res['sucessos']} | Falhas: {batch_res['falhas']}")
        print(f"Tempo total: {batch_res['tempo_total_segundos']}s")
        print(f"Pasta destino: {batch_res['pasta_destino']}")
        return

    # Arquivo individual
    print("\nComo deseja selecionar o arquivo?")
    print("1. Abrir explorador de arquivos do Windows")
    print("2. Digitar o caminho do arquivo")
    f_choice = input("Opcao (1 ou 2) [padrao: 1]: ").strip()

    if f_choice == "2":
        source_file = input("Digite o caminho do arquivo: ").strip()
    else:
        print("[*] Abrindo janela de selecao de arquivo...")
        source_file = DataHasher.select_file_gui()

    if not source_file or not Path(source_file).is_file():
        default_file = Path(__file__).parent / "data" / "clientes_exemplo.csv"
        if default_file.is_file():
            print(f"[*] Usando arquivo de exemplo: {default_file}")
            source_file = default_file
        else:
            print("[!] Arquivo nao encontrado ou cancelado.")
            return

    # Carrega colunas disponiveis
    try:
        df, _ = FileReader.read(source_file)
        print(f"\nColunas detectadas no arquivo ({len(df.columns)}):")
        for idx, c in enumerate(df.columns, start=1):
            print(f"  {idx}. {c}")
    except Exception as e:
        print(f"[!] Erro ao inspecionar arquivo: {e}")
        return

    print("\nComo deseja aplicar o hash?")
    print("1. Escolher colunas especificas (ex: CPF, Email)")
    print("2. Criar uma coluna de impressao digital (hash da linha inteira)")
    print("3. Anonimizar todas as colunas de texto")
    opt_modo = input("Opcao (1-3) [padrao: 1]: ").strip()

    cols_to_hash = None
    fingerprint = None

    if opt_modo == "2":
        fingerprint = input("Nome da nova coluna de hash [padrao: hash_registro]: ").strip() or "hash_registro"
    elif opt_modo == "3":
        cols_to_hash = list(df.select_dtypes(include=["object"]).columns)
    else:
        sel_cols = input("Digite os nomes ou numeros das colunas (separados por virgula): ").strip()
        parsed_cols = []
        for item in sel_cols.split(","):
            item = item.strip()
            if item.isdigit() and 1 <= int(item) <= len(df.columns):
                parsed_cols.append(df.columns[int(item) - 1])
            elif item in df.columns:
                parsed_cols.append(item)
        cols_to_hash = parsed_cols if parsed_cols else [df.columns[0]]

    keep_orig = input("\nDeseja manter as colunas originais junto com o hash? (s/n) [padrao: n]: ").strip().lower() == "s"

    print("\nEscolha o algoritmo de hash:")
    print("1. SHA-256 (Padrao de Seguranca)")
    print("2. SHA-512 (Alta complexidade)")
    print("3. MD5 (Legado / Compatibilidade)")
    algo_map = {"1": "sha256", "2": "sha512", "3": "md5"}
    algo = algo_map.get(input("Opcao (1-3) [padrao: 1]: ").strip(), "sha256")

    salt = input("\nAdicionar Salt / Chave secreta de seguranca? (deixe em branco para hash puro): ").strip() or None

    print("\nFormato de saida desejado:")
    print("1. CSV (.csv)")
    print("2. Parquet (.parquet)")
    print("3. Excel (.xlsx)")
    print("4. JSON (.json)")
    fmt_map = {"1": "csv", "2": "parquet", "3": "xlsx", "4": "json"}
    target_fmt = fmt_map.get(input("Opcao (1-4) [padrao: 1]: ").strip(), "csv")

    print("\n[*] Processando anonimizacao...")
    res = DataHasher.process_file(
        source=source_file,
        target_format=target_fmt,
        columns=cols_to_hash,
        algorithm=algo,
        salt=salt,
        keep_original=keep_orig,
        fingerprint_col=fingerprint
    )

    print("\n[+] Processamento concluido!")
    print(f"Origem            : {res['arquivo_origem']}")
    print(f"Destino           : {res['arquivo_destino']}")
    print(f"Algoritmo         : {res['algoritmo']} {'(com Salt)' if res['salt_utilizado'] else '(puro)'}")
    print(f"Colunas tratadas  : {res['colunas_anonimizadas']}")
    print(f"Linhas processadas: {res['linhas_processadas']}")
    print(f"Velocidade        : {res['taxa_linhas_por_segundo']} linhas/segundo")
    print(f"Tempo total       : {res['tempo_segundos']}s")


def main():
    parser = argparse.ArgumentParser(description="Anonimizador criptografico de dados tabulares (SHA-256, etc.).")
    parser.add_argument("source", nargs="?", help="Caminho do arquivo de entrada.")
    parser.add_argument("-c", "--columns", help="Colunas a anonimizar separadas por virgula (ex: 'CPF,Email').")
    parser.add_argument("-a", "--algorithm", default="sha256", help="Algoritmo de hash (sha256, sha512, md5).")
    parser.add_argument("-s", "--salt", help="Chave secreta (Salt) para protecao adicional.")
    parser.add_argument("-f", "--format", help="Formato de saida (csv, parquet, xlsx, json).")
    parser.add_argument("-o", "--output", help="Caminho ou pasta de destino.")
    parser.add_argument("--keep-original", action="store_true", help="Mantem as colunas originais junto ao hash.")
    parser.add_argument("--fingerprint", help="Gera hash composto da linha com este nome de coluna.")
    parser.add_argument("--batch", action="store_true", help="Ativa modo em lote para o diretorio informado.")

    args = parser.parse_args()

    if not args.source:
        run_interactive()
    elif args.batch:
        cols = [c.strip() for c in args.columns.split(",")] if args.columns else None
        res = DataHasher.process_batch(
            source_dir=args.source,
            target_format=args.format or "csv",
            columns=cols,
            output_dir=args.output,
            algorithm=args.algorithm,
            salt=args.salt
        )
        print(f"[+] Lote concluido: {res['sucessos']} convertidos com sucesso.")
    else:
        cols = [c.strip() for c in args.columns.split(",")] if args.columns else None
        res = DataHasher.process_file(
            source=args.source,
            target_format=args.format,
            columns=cols,
            output_path=args.output,
            algorithm=args.algorithm,
            salt=args.salt,
            keep_original=args.keep_original,
            fingerprint_col=args.fingerprint
        )
        print(f"[+] Concluido: {res['arquivo_destino']} ({res['linhas_processadas']} linhas em {res['tempo_segundos']}s).")


if __name__ == "__main__":
    main()
