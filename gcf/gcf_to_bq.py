import os
from google.cloud import bigquery

PROJECT_ID = os.getenv('GCP_PROJECT')
BQ_DATASET = "DATASET_name"

def main(event, context):
     client = bigquery.Client()
     BQ_TABLE = str(event['name']).split("/")[0] + "_" + str(event['name']).split("/")[-1].replace(".csv", "").replace("-", "")

     table_ref = client.dataset(BQ_DATASET).table(BQ_TABLE)

     job_config = bigquery.LoadJobConfig()
     job_config.autodetect = True
     job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
     job_config.source_format = bigquery.SourceFormat.CSV
     job_config.skip_leading_rows = 1

     uri = 'gs://' + event['bucket'] + '/' + event['name']

     load_job = client.load_table_from_uri(
          uri,
          table_ref,
          job_config = job_config)
