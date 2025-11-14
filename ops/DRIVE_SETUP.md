# DRIVE_SETUP.md
1) Create a Google Service Account and download JSON key.
2) Create a folder in Drive. Share with the service account email.
3) Add repository secrets:
   - GDRIVE_SERVICE_ACCOUNT_JSON: paste entire JSON (single-line)
   - GDRIVE_QUEUE_FOLDER_ID: folder id
4) Local/Colab usage:
   - in Colab set os.environ['GDRIVE_SERVICE_ACCOUNT_JSON'] = <json>
   - os.environ['GDRIVE_QUEUE_FOLDER_ID'] = '<FOLDER_ID>'
