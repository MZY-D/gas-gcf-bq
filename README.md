# GAS-GCF-BQ



## Introduction

Easy to kick APIs regulary and store the data to BQ. 

- GAS = Google App Script. Javascript basis. One of the Google Drive tool.
- GCF = Google Cloud Functions. Python, Javascript and Go basis. One of the GCP tool.
- GCS = Google Cloud Storage. File storage service. One of the GCP tool.
- BQ = Google BigQuery. Fully-managed serverless data warehouse. One of the GCP tool.

Leverging the tools, you can kick API and save the data regulary.

1. Spreadsheet : API credentials and parameters
2. GAS : GCF Kicking with the credentials and parameters
3. GCF-1
   1. API calling
   2. Save data to GCS
   3. Return data to GAS
4. GAS : Write returned data to Spreadsheet
5. GCF-2 : Add GCS data to BQ data table.

*Scheduling : GAS schedular

