# Teste Técnico

Este repositório foi criado para a implementação do teste técnico.

## Pré-requisitos

Antes de começar, garanta que você tenha instalado em sua máquina:

- Python 3.x
- `pip`
- `venv` ou `conda`

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2. Adicione os dados do case

Com os dados passados no case, coloque dentro do diretório:

`mr_health/data`

### 3. Crie um ambiente virtual

Use um ambiente virtual ou conda para instalar as dependências.

Exemplo com `venv`:

```bash
python3 -m venv env
```

### 4. Ative o ambiente virtual

No Linux/macOS:

```bash
source env/bin/activate
```

No Windows:

```bash
env\Scripts\activate
```

### 5. Instale as dependências

Depois, faça a instalação das dependências com:

```bash
pip3 install -r requirements.txt
```

### 6. Execute os arquivos

Na pasta `mr_health/src/`, você pode executar os arquivos `eda.py` e `main.py` usando:

```bash
python3 main.py
```

ou

```bash
python3 eda.py
```

## Saída

Ao executar os scripts, será exibido um log no terminal com todas as informações.

E também será criado um arquivo `.csv` no caminho `mr_health/output/` com o resultado.
