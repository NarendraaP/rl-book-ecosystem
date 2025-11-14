# gdrive_utils.py
import os, json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]

def creds_from_service_account_info(info_json: dict):
    return service_account.Credentials.from_service_account_info(info_json, scopes=SCOPES)

def drive_service_from_creds(creds):
    return build("drive", "v3", credentials=creds, cache_discovery=False)

def load_service_account_info_from_env(envvar="GDRIVE_SERVICE_ACCOUNT_JSON"):
    raw = os.environ.get(envvar)
    if not raw:
        raise RuntimeError(f"Service account JSON not found in env {envvar}")
    try:
        return json.loads(raw)
    except Exception as e:
        raise RuntimeError("Failed to parse service account JSON from env") from e
