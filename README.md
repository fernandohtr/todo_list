# TODO LIST

Programa de todo list no navegador local.

## Começando

O presente projeto foi desenvolvido em Linux/Ubuntu, e todas as suas instruções serão baseadas nesses sistema operacional. Siga as descrições para rodar o programa.

### Pré-requisitos

Primeiramente será necessário ter instalado em sua máquina:
- Python 3.7+
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

### Instalando

Crie um ambiente virtual:
```python
virtualenv -p python3.7 env
```

Entre no ambiente virtual:
```python
source env/bin/activate
```

Dentro do ambiente virtual, instale as dependências:
```python
pip install -r requirements/base.txt
```

### Rodando o programa

Com o ambiente preparado, execute o código principal:
```python
gunicorn todo_list:app
```

Assim que executar o comando, o terminal retornará uma mensagem equivalente a essa:
```bash
[2019-10-25 08:55:42 -0300] [20484] [INFO] Starting gunicorn 19.9.0
[2019-10-25 08:55:42 -0300] [20484] [INFO] Listening at: http://127.0.0.1:8000 (20484)
[2019-10-25 08:55:42 -0300] [20484] [INFO] Using worker: sync
[2019-10-25 08:55:42 -0300] [20487] [INFO] Booting worker with pid: 20487
```

Essa é a mensagem indicando que o programa está rodando localmente.

Agora, basta acessar o navegador no endereço `http://127.0.0.1:8000` ou `localhost:8000`.
