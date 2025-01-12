# Conversor de Arquivos para SHA-256

Este script converte arquivos **TXT**, **CSV** ou **XLSX** em **SHA-256**. Ele lê o conteúdo do arquivo, calcula o hash SHA-256 de cada linha e salva o resultado em um novo arquivo no formato desejado (TXT, CSV ou XLSX). O projeto foi desenvolvido para ser simples, mas altamente personalizável.

---

## Funcionalidades

- **Conversão de arquivos**: Converte arquivos TXT, CSV ou XLSX em SHA-256.
- **Formato de saída**: Permite salvar o resultado em TXT, CSV ou XLSX.
- **Delimitadores personalizados**: Para arquivos CSV, é possível escolher entre diferentes delimitadores (vírgula, ponto e vírgula, tabulação, pipe).
- **Manutenção da coluna original**: O usuário pode optar por manter ou remover a coluna original no arquivo de saída.
- **Cabeçalho personalizado**: Permite incluir ou excluir cabeçalho no arquivo de saída.

---

## Como Usar

### 1. Instalação das Dependências

Antes de executar o script, certifique-se de que as bibliotecas necessárias estão instaladas. Você pode instalá-las usando o seguinte comando:

```bash
pip install pandas openpyxl
```

### 2. Executando o Script

- Execute o script `conversor_sha256.ipynb` no **Jupyter Notebook** ou **Google Colab**.
- Siga as instruções fornecidas pelo script:

  1. **Digite o nome do arquivo** (com extensão).
  2. **Informe se o arquivo original tem cabeçalho** (s/n).
  3. **Escolha o delimitador** (se o arquivo for CSV).
  4. **Decida se deseja manter a coluna original** (s/n).
  5. **Escolha o formato de saída** (TXT, CSV ou XLSX).
  6. **Informe se deseja incluir cabeçalho no arquivo de saída** (s/n).
  7. **Digite o caminho onde deseja salvar o arquivo** (deixe em branco para salvar no diretório atual).

---

### 3. Exemplo de Uso

#### Arquivo de Entrada (`exemplo.csv`):

```csv
Nome
Alice
Bob
Charlie
```

#### Execução do Script:

1. Digite o nome do arquivo: `exemplo.csv`
2. O arquivo original tem cabeçalho? (s/n): `s`
3. Escolha o delimitador do arquivo CSV: `1` (vírgula)
4. Deseja manter a coluna original? (s/n): `n`
5. Escolha o formato de saída: `2` (CSV)
6. Deseja incluir cabeçalho no arquivo de saída? (s/n): `s`
7. Digite o caminho onde deseja salvar o arquivo: (deixe em branco)

#### Arquivo de Saída (`exemplo_sha256.csv`):

```csv
SHA256
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb
2e7d2c03a9507ae265ecf5b5356885a53393a2029d241394997265a1a25aefc6
```

---

## Personalização e Alterações

O script foi projetado para ser flexível e permitir alterações conforme necessário. Abaixo estão algumas sugestões de personalização:

### 1. Adicionar Novos Formatos de Entrada

Se você deseja adicionar suporte a outros formatos de arquivo (por exemplo, JSON), siga estas etapas:

- Adicione a extensão na função `verificar_arquivo`.
- Implemente a lógica de leitura do novo formato na função `main`.

Exemplo:

```python
if nome_arquivo.endswith('.json'):
    df = pd.read_json(nome_arquivo)
```

### 2. Alterar o Algoritmo de Hash

Se você quiser usar outro algoritmo de hash (por exemplo, MD5 ou SHA-1), basta modificar a função `calcular_sha256`:

```python
def calcular_md5(texto):
    return hashlib.md5(texto.encode()).hexdigest()
```

### 3. Adicionar Novos Delimitadores

Para adicionar novos delimitadores ao processamento de arquivos CSV, basta atualizar o dicionário `delimitadores` na função `main`.

Exemplo:

```python
delimitadores = {'1': ',', '2': ';', '3': '\t', '4': '|', '5': ':'}
```

### 4. Modificar o Formato de Saída

Se você deseja adicionar novos formatos de saída (por exemplo, JSON), siga estas etapas:

- Adicione a extensão no dicionário `extensoes`.
- Implemente a lógica de salvamento do novo formato na função `main`.

Exemplo:

```python
if extensao_saida == '.json':
    df.to_json(nome_saida, orient='records')
```

---

## Informações Técnicas

### Dependências

O script utiliza as seguintes bibliotecas:

- **pandas**: Para manipulação de dados (leitura e escrita de arquivos CSV, XLSX, etc.).
- **openpyxl**: Para leitura e escrita de arquivos XLSX.
- **hashlib**: Para cálculo de hashes SHA-256.

Certifique-se de que essas bibliotecas estejam instaladas antes de executar o script.

### Estrutura do Código

- **Função `calcular_sha256`**: Calcula o hash SHA-256 de um texto.
- **Função `verificar_arquivo`**: Verifica se o arquivo tem uma extensão válida.
- **Função `verificar_coluna_unica`**: Verifica se o arquivo contém apenas uma coluna.
- **Função `main`**: Função principal que gerencia a execução do script.

---

## Licença

Este projeto está licenciado sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

### Condições da Licença

- **Atribuição**: Se você usar ou modificar este projeto, deve creditar o autor original (Suelio Lima).
- **Uso Comercial**: O projeto pode ser usado para fins comerciais.
- **Modificações**: Você pode alterar o código, mas deve incluir a licença original.

---

## Autor

- **Suelio Lima**
  - Email: suelio@gmail.com
  - GitHub: [suelio](https://github.com/suelio)

---

## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar este projeto, siga estas etapas:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas alterações (`git commit -m 'Adicionando nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

---

## Problemas Conhecidos

- O script não suporta arquivos com múltiplas colunas. Se você precisar processar arquivos com mais de uma coluna, considere modificar a função `verificar_coluna_unica`.

---
