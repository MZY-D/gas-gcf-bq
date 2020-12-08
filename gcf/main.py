import urllib.request as urllib
import urllib.parse as parse
import base64
import requests
import json
import pandas as pd
from google.cloud import storage


# example : call API
def call_api(API_URL, API_KEY, PASSWORS, data=None, method=None):
    req = urllib.Request(url)
    base64string = base64.encodebytes(('%s:%s' % (API_KEY, PASSWORS)).encode()).decode().replace('\n', '')
    req.add_header("Authorization", "Basic %s" % base64string)
    req.add_header('Content-Type', 'application/json')

    if method != None:
      req.get_method = lambda: method

    if data == None:
      result = urllib.urlopen(req)
    else:
      result = urllib.urlopen(req, data=json.dumps(data).encode())

    return pd.DataFrame(json.loads(result.read()))

# Slack notifying
def slack_send(body):
    WEB_HOOK_URL = "https://hooks.slack.com/services/xxx/xxx"
    requests.post(WEB_HOOK_URL,
        data = json.dumps({
            'text': body,
            'channel':'@xxx',
            'link_names': 1,
            }))

# Save data to GCS
def save_gcs(df, folder):
    client = storage.Client()
    bucket_name = 'bucket_name'
    bucket = client.get_bucket(bucket_name)

    # split data by date for table partitioning in BigQuery
    for d in set(df["date"]):
      temp_df = df[df["date"] == d]
      file_name = '{}/{}.csv'.format(folder, d)
      file_d = bucket.blob(file_name)
      file_d.upload_from_string(data=temp_df.to_csv(index=False, encoding="utf-8"), content_type='text/csv')

# main
def execute(req):
    req_json = req.get_json(force=True)
    parameters = req_json['parameters']

    # if you have slack WEB_HOOK_URL, you can notify via Slack
    slack_send("Start GCF - xxx API kick : " + str(parameters))

    # please modify along your params
    API_URL = "http://xxx.xxx/xxx"
    API_KEY = str(parameters[1][1])
    PASSWORS = str(parameters[2][1])

    df = call_api(API_URL, API_KEY, PASSWORS)
    if df.shape[0] > 0:
      save_gcs(df, "bucket_name")
      return json.dumps([list(df.columns)] + df.values.tolist())
    else:
      return json.dumps([["-"]] + [["-"]])
