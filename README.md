# Analytics API

==============================

Essa API tem como o objetivo servir o time de analytics da AMMO.

KPI -> O relatório KPI é enviado diariamente para o time de operações

    ├── Fluxo 
    │   ├── Dados extraídos do BQ 
    │   ├── Parse dos dados
    │   ├── Formatação dos resultados 
    │   ├── Envio por email


Instagram monitor -> O monitor de contas do Instagram. Tem como objetivo saber seguidores e postagens dos usuários.

    ├── Fluxo 
    │   ├── Usando a API do RapidApi busca os dados das contas 
    │   ├── Parse dos dados
    │   ├── Salva os dados no BQ
    │   ├── Envio por email


Login Artex -> Checa se o login está correto. Função não usada.

    ├── Fluxo 

Whatsapp service -> Estudo sobre disparo de mensagens pelo whats app
    
    ├── Recomendação -> Usar alguma API diferente da botmaker.


## Instalação das ferramentas necessárias

Instale o [Homebrew](https://brew.sh/)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Instale o [Poetry](https://python-poetry.org/) utilizando o brew

```bash
brew install poetry
```

Instale o [Pyenv](https://github.com/pyenv/pyenv) utilizando o brew

```bash
brew install pyenv
```

## Para MacOs - Catalina ou superior

Rode os seguintes comandos, na ordem, para que o pyenv seja adicionado ao Shell

```bash
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
```

```bash
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

```bash
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
```

```bash
source ~/.zshrc
```

Para verificar se tudo foi adicionado corretamente, use o seguinte comando

```bash
pyenv --help
```

[Referência](https://medium.com/@miqui.ferrer/the-ultimate-guide-to-managing-python-virtual-environments-in-macos-c8cb49bf0a3c)

## Para Windows

....

## Instalando a versão correta do [Python](https://www.python.org/)

Para o projeto do **Ammo Analytics** utilizamos a versão 3.10.14

Veja as versões do python instaladas
```bash
pyenv versions
```

Utilize o *pyenv* para instalar a versão correta (caso ainda não esteja instalada)

```bash
pyenv install 3.10.14
```

Adicione a versão ao escopo global

```bash
pyenv global 3.10.14
```

## Instalando as dependências do projeto

Para as próximas etapas é necessário que o seja feito o clone do projeto [*Analytics API*](https://github.com/Ammo-BI/analytics-api/tree/main).

Dentro da pasta raiz do repositório:

```bash
poetry install
```

Após a instalação dos pacotes

```bash
poetry shell
```

## Rodando o projeto

Se tudo foi feito corretamente o seguinte comando deve fazer a API rodar localmente (Ambos os comandos fazem a mesma coisa.):

```bash
task start
```

OU

```bash
poetry run task start
```

OU

```bash
uvicorn src.analytics_api.api.main:fast_api --port 8080 --host 0.0.0.0 --reload
```
OU

```bash
poetry run uvicorn src.analytics_api.api.main:fast_api --port 8080 --host 0.0.0.0 --reload
```

Project Organization
------------

    ├── .github
    ├── docs               <- Not used
    ├── notebooks          <- Python notebooks used for discovery
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── commom         <- Arquivos comuns aos endpoints
    │   │
    │   ├── innovation_api <- Arquivos principais dos endpoints
    │   │
    │   ├── innovation_messenger <- Arquivos relacionados ao disparador de email
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
