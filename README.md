# Anonimizador Criptografico de Dados Tabulares (SHA-256 / LGPD)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/suelio/conversor_sha256/blob/main/conversor_sha256.ipynb)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Pandas](https://img.shields.io/badge/pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![PyArrow](https://img.shields.io/badge/pyarrow-12.0%2B-d22128.svg)](https://arrow.apache.org/)

O **Conversor SHA-256** e uma biblioteca e ferramenta de linha de comando em Python voltada para a **pseudonimizacao e protecao criptografica de dados pessoais (PII)** em conformidade com as diretrizes da **LGPD** (Lei Geral de Protecao de Dados) e **GDPR**.

O projeto permite transformar valores sensiveis em hashes criptograficos irreversiveis com suporte a **Salteamento (Salt)**, normalizacao previa de documentos e hashing seletivo de colunas, preservando as informacoes de negocio para analise de dados e machine learning.

---

## Principais Funcionalidades

### 1. Anonimizacao Seletiva de Colunas
- Permite selecionar quais colunas devem ser criptografadas (por exemplo, `CPF`, `Email`, `Telefone`), mantendo inalteradas as colunas analiticas e de negocio (como `Valor`, `Data`, `Regiao`, `Categoria`).
- Opcao de manter a coluna original acompanhada da versao em hash para comparacao e validacao tecnica.

### 2. Salteamento Criptografico (Salt / HMAC)
- Suporte a aplicacao de chaves secretas (*Salt*) durante o calculo do hash.
- Mitiga riscos contra ataques de forca bruta, ataques de dicionario e tabelas pre-computadas (*Rainbow Tables*), atendendo aos padroes de seguranca da informacao corporativa.

### 3. Normalizacao Previa de Dados Sensiveis (PII)
- Higienizacao automatica antes da geracao do hash:
  - **Documentos (CPF/CNPJ/RG)**: Remocao automatica de pontuacoes, barras e tracos (`123.456.789-00` e tratado identicamente a `12345678900`).
  - **E-mails**: Remocao de espacos em branco e conversao para minusculas.
  - **Telefones**: Padronizacao apenas de digitos numericos.

### 4. Impressao Digital de Linha (Record Fingerprint)
- Opcao de gerar um hash composto baseado na combinacao de todos os campos do registro, util para deduplicacao eficiente e controle de integridade em pipelines ETL.

### 5. Multiplos Algoritmos e Formatos
- **Algoritmos Criptograficos**: SHA-256 (padrao), SHA-512, SHA-384, SHA-1 e MD5.
- **Suporte Multi-Formato**: Entrada e saida compativeis com CSV, TXT, TSV, planilhas Excel (.xlsx), arquivos colunares Parquet e documentos JSON.
- **Processamento em Lote (Batch)**: Processa pastas inteiras de arquivos de forma automatizada com resumo consolidado de execucao.

---

## Estrutura do Repositorio

```text
conversor_sha256/
|-- hasher/                       # Pacote Python modular
|   |-- __init__.py               # Exports principais
|   |-- algorithms.py             # Motores criptograficos (SHA-256, 512, HMAC)
|   |-- normalizer.py             # Normalizacao e higienizacao de PII
|   |-- reader.py                 # Leitura universal com autodeteccao
|   |-- writer.py                 # Gravacao nos formatos suportados
|   `-- engine.py                 # Orquestrador central DataHasher
|
|-- data/                         # Datasets de teste
|   `-- clientes_exemplo.csv      # Amostra com campos de CPF, Email e Telefone
|
|-- notebooks/
|   `-- demonstracao_anonimizacao.ipynb # Notebook com fluxo didatico
|
|-- conversor_sha256.ipynb        # Notebook oficial pronto para o Google Colab
|-- cli.py                        # Interface de linha de comando (interativa e direta)
|-- environment.yml               # Configuracao para Anaconda/Conda
|-- requirements.txt              # Dependencias para pip
|-- .gitignore                    # Arquivos ignorados pelo Git
|-- LICENSE                       # Licenca MIT
`-- README.md                     # Documentacao tecnica oficial
```

---

## Instalacao

### Com Anaconda / Conda (Recomendado)

```bash
# Criar ambiente dedicado
conda env create -f environment.yml
conda activate conversor_sha256

# Ou instalar no ambiente atual
conda install --file requirements.txt -y
```

### Com Pip

```bash
pip install -r requirements.txt
```

---

## Exemplos de Uso

### 1. No Google Colab
Abra o notebook oficial diretamente pelo link:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/suelio/conversor_sha256/blob/main/conversor_sha256.ipynb)

---

### 2. Como Biblioteca Python em seus Pipelines

```python
from hasher import DataHasher

# 1. Anonimizar colunas especificas com Salt criptografico
resultado = DataHasher.process_file(
    source="data/clientes_exemplo.csv",
    columns=["CPF", "Email", "Telefone"],
    algorithm="sha256",
    salt="chave_secreta_lgpd",
    target_format="parquet"
)

print(f"Arquivo gerado: {resultado['arquivo_destino']}")
print(f"Linhas processadas: {resultado['linhas_processadas']}")
print(f"Taxa de velocidade: {resultado['taxa_linhas_por_segundo']} linhas/s")

# 2. Criar uma coluna de fingerprint da linha inteira
res_fingerprint = DataHasher.process_file(
    source="data/clientes_exemplo.csv",
    fingerprint_col="hash_registro",
    target_format="csv"
)
```

---

### 3. Via Linha de Comando (CLI)

#### Modo Direto por Argumentos
```bash
# Anonimizar colunas sensiveis para formato Parquet
python cli.py data/clientes_exemplo.csv --columns "CPF,Email" --salt "segredo123" -f parquet

# Anonimizar todas as colunas de texto com SHA-512
python cli.py data/clientes_exemplo.csv -a sha512 -f xlsx

# Processamento em lote de todos os arquivos de um diretorio
python cli.py data --batch --columns "CPF" -f csv
```

#### Modo Interativo
Execute sem parametros para acessar o menu guiado:
```bash
python cli.py
```
O menu interativo permite utilizar o Explorador de Arquivos do Windows para selecionar a base de dados, escolher as colunas numeradas e definir o algoritmo de forma visual.

---

## Autor

- **Suelio Lima**
  - GitHub: [@suelio](https://github.com/suelio)
  - Repositorio: [github.com/suelio/conversor_sha256](https://github.com/suelio/conversor_sha256)

---

## Licenca

Este projeto e distribuido sob os termos da licenca **MIT**. Consulte o arquivo [LICENSE](LICENSE) para obter mais informacoes.
