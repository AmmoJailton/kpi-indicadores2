from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from commom.logger import logger
import pandas as pd
from google.cloud import bigquery
from datetime import datetime

def create_table_if_not_exists(client, dataset_id, table_id, schema=None):
   table_ref = client.dataset(dataset_id).table(table_id)
   try:
       # Try to get the table, if it doesn't exist, create it
       table = client.get_table(table_ref)
   except NotFound:
       logger.info(f'The table does not exist. Creating the table...')
       table = bigquery.Table(table_ref, schema=schema)
       table = client.create_table(table)
       logger.info(f'Table created successfully.')
   except Exception as e:
       # Handle other exceptions if necessary
    #    logger.error(f'An error occurred while checking the table: {e}')
       return None

   return table


def generate_bigquery_schema(df_source):
   """
   Gera um esquema de tabela BigQuery a partir de um DataFrame.


   Parâmetros:
   - df_source: O DataFrame a partir do qual o esquema será gerado.


   Imprime:
   - O esquema da tabela no formato desejado.
   """
   for column_name, dtype in df_source.dtypes.iteritems():
       bq_type = "STRING"  # Tipo padrão é STRING
       
       # Mapeie os tipos do DataFrame para os tipos do BigQuery
       if pd.api.types.is_integer_dtype(dtype):
           bq_type = "INTEGER"
       elif pd.api.types.is_float_dtype(dtype):
           bq_type = "FLOAT"
       elif pd.api.types.is_bool_dtype(dtype):
           bq_type = "BOOLEAN"
       elif pd.api.types.is_datetime64_any_dtype(dtype):
           bq_type = "DATETIME"


       # Imprima a linha correspondente ao esquema
       print(f"bigquery.SchemaField('{column_name}', '{bq_type}'),")
       
def write_dataframe_to_bigquery(client, dataframe, table_id, job_config):
    """Writes a DataFrame to BigQuery and waits for the job to complete."""
    try:
        job = client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)
        job.result()  # Waits for the job to complete
        # logger.info(f'Job ID: {job.job_id}')
    #    logger.info(f'Records inserted: {job.output_rows}')
    except Exception as e:
    #    logger.error(f'An error occurred during data insertion in BigQuery: {e}')
        print(e)