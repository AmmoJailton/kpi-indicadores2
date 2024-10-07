import pickle
from typing import Any, Dict, List, Optional
from commom.database.bigquery_functions.create_table_if_not_exists import create_table_if_not_exists
from commom.database.bigquery_functions.write_dataframe_to_bigquery import write_dataframe_to_bigquery
from commom.logger import logger

import pandas as pd
from google.cloud import bigquery

from commom.config import config

class DataHandler:
    @classmethod
    def read_from_bigquery(cls, query: str) -> pd.DataFrame:
        client = bigquery.Client(project=config.credentials.project_id, credentials=config.credentials)
        dataframe = client.query(query).to_dataframe()
        return dataframe

    @classmethod
    def read_from_local_pickle(cls, file_path: str) -> pd.DataFrame:
        with open(file_path, "rb") as file:
            objeto_lido = pickle.load(file)

        return objeto_lido

    @classmethod
    def write_to_bigquery(cls, dataset_id:str, table_id:str, dataframe:pd.DataFrame, schema: Optional[List[bigquery.SchemaField]] = None, **kwargs):
        client = bigquery.Client(project=config.credentials.project_id, credentials=config.credentials)
        logger.info("Connection to BigQuery successful")
        table_id = create_table_if_not_exists(client=client, dataset_id=dataset_id, table_id=table_id, schema=schema)
        
        
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            write_disposition="WRITE_TRUNCATE"
        )
        
        write_dataframe_to_bigquery(client=client, dataframe=dataframe, table_id=table_id, job_config=job_config)
        logger.info('write done')

        return dataframe
    
    @classmethod
    def write_to_pickle(cls, data, path:str, **kwargs) -> bool:
        pickle.dump(data, open(path, "wb"))
        return True
    
    @classmethod
    def write_to_s3(cls, data: str, s3_bucket: str, s3_key: str, **kwargs) -> bool:
        raise NotImplementedError("Method write_to_s3 hasn't been implemented yet.")
    
    @classmethod
    def write_to_json(cls, data, path, **kwargs) -> bool:
        raise NotImplementedError("Method write_to_json hasn't been implemented yet.")

    