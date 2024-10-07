from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from commom.logger import logger
import pandas as pd
from google.cloud import bigquery
from datetime import datetime

def create_table_if_not_exists(client, dataset_id, table_id, schema=None):
   table_ref = client.dataset(dataset_id).table(table_id)
   
   try:
       table = client.get_table(table_ref)
   except NotFound:
       logger.info(f'The table does not exist. Creating the table...')
       table = bigquery.Table(table_ref, schema=schema)
       table = client.create_table(table)
       logger.info(f'Table created successfully.')
   except Exception as e:
       
       logger.error(f'An error occurred while checking the table: {e}')
       return None

   return table
