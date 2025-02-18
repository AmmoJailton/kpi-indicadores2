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

Obs: o fluxo de deploy está descrito no github/workflows. A pipeline é montada com a arquivo yaml. Os serviços usados são do gcp.

O deploy é feito via cli pelo github actions. O projeto é inserido dentro de uma imagem docker com o entrypoint visível, é feito o upload da imagem para o artifact registry, a partir daí o cloud run é atualizado para ler a docker e disponibilizar os serviços.

As variáveis de ambiente foram compartilhadas com o Chiesa e estão no backup do drive.

EMAIL_PASSWORDS -> senhas do time de inovação
EMAIL_SENDER_ACCOUNT -> email do time de inovação
GCLOUD_RUN_REGION -> a região do google cloud onde o projeto está online
GCP_APP_NAME_BASE -> app base name
GCP_ARTIFACT_REGISTRY_REGION -> região do artifact registry onde a imagem docker está
GCP_CREDENTIALS_SECRET -> secret da gpc em base64
GCP_CREDENTIALS_SECRET_DECODED -> secret da gpc em json
GCP_CREDENTIALS_SECRET_ENCODED -> secret da gpc em base64
GCP_IMAGE_NAME -> nome da imagem docker do projeto
GCP_PROJECT_ID -> id do projeto no gcp
GOOGLE_CREDENTIALS_FILEPATH -> endereço virtual de um arquivo (não sei pq mas funciona)
INSTAGRAM_SCRAPPER_API_HOST -> host do scrapper api
INSTAGRAM_SCRAPPER_API_TOKEN -> token da scrapper api


Para obter algumas envs é interessante ter acesso ao gcp [gcp](https://console.cloud.google.com/artifacts?referrer=search&hl=pt&project=projetoomni) . Encontre o nome do projeto GCP_APP_NAME, região GCP_ARTIFACT_REGISTRY_REGION, nome da imagem GCP_IMAGE_NAME, e id do projeto GCP_PROJECT_ID.

O cloud run [cloud run](https://console.cloud.google.com/run?referrer=search&hl=pt&project=projetoomni) serve para armazenar sites estáticos ou imagens docker ou apis. Para encontrar as envs relacionadas ao cloud run basta acessar e encontrar o nome do projeto. 

O padrão é que dentro da gcp tudo siga a nomenclatura do time "innovation_alguma_coisa" ou "alguma_coisa_innovation" etc , e para os serviços seguimos com o mesmo nome do repositório.
