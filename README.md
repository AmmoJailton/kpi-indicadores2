# Analytics API

==============================

Essa API tem como o objetivo servir o time de analytics da AMMO.

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

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
