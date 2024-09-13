import pickle

import pandas as pd
from google.cloud import bigquery

from commom.config import config


class DataRead:
    @classmethod
    def from_bigquery(cls, query: str) -> pd.DataFrame:
        client = bigquery.Client(project=config.credentials.project_id, credentials=config.credentials)
        dataframe = client.query(query).to_dataframe()
        return dataframe

    @classmethod
    def from_local_pickle(cls, file_path: str) -> pd.DataFrame:
        with open(file_path, "rb") as file:
            objeto_lido = pickle.load(file)

        return objeto_lido
