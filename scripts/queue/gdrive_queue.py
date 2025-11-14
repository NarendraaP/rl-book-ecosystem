# gdrive_queue.py (concise implementation)
import io, json, time, uuid
from datetime import datetime, timedelta
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from .gdrive_utils import load_service_account_info_from_env, creds_from_service_account_info, drive_service_from_creds

LEASE_SECONDS = 60

class GDriveQueue:
    def __init__(self, drive_folder_id: str, service_account_env="GDRIVE_SERVICE_ACCOUNT_JSON"):
        info = load_service_account_info_from_env(service_account_env)
        creds = creds_from_service_account_info(info)
        self.service = drive_service_from_creds(creds)
        self.root = drive_folder_id
        self.inbox_id = self._ensure_folder("inbox")
        self.locks_id = self._ensure_folder("locks")
        self.work_id = self._ensure_folder("work")
        self.outbox_id = self._ensure_folder("outbox")

    def _ensure_folder(self, name) -> str:
        q = f"mimeType='application/vnd.google-apps.folder' and name='{name}' and '{self.root}' in parents and trashed=false"
        res = self.service.files().list(q=q, fields="files(id,name)").execute()
        if res.get("files"):
            return res["files"][0]["id"]
        body = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents":[self.root]}
        created = self.service.files().create(body=body, fields="id").execute()
        return created["id"]

    def list_inbox(self):
        q = f"'{self.inbox_id}' in parents and trashed=false"
        res = self.service.files().list(q=q, fields="files(id,name,createdTime)", orderBy="createdTime").execute()
        return res.get("files", [])

    def download_file(self, file_id):
        fh = io.BytesIO()
        req = self.service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(fh, req)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        return fh.read().decode("utf-8")

    def upload_json(self, folder_id, filename, obj):
        data = json.dumps(obj, indent=2).encode("utf-8")
        media = MediaIoBaseUpload(io.BytesIO(data), mimetype="application/json")
        body = {"name": filename, "parents": [folder_id]}
        created = self.service.files().create(body=body, media_body=media, fields="id").execute()
        return created["id"]

    def create_lock(self, job_name, worker_id, ttl=LEASE_SECONDS):
        expires = (datetime.utcnow() + timedelta(seconds=ttl)).isoformat() + "Z"
        lock_content = {"worker_id": worker_id, "expires_at": expires}
        try:
            return self.upload_json(self.locks_id, f"{job_name}.lock", lock_content)
        except Exception:
            return None

    def delete_file(self, file_id):
        self.service.files().delete(fileId=file_id).execute()

    def move_file(self, file_id, old_parent_id, new_parent_id):
        file = self.service.files().get(fileId=file_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents", []))
        self.service.files().update(fileId=file_id, addParents=new_parent_id, removeParents=previous_parents, fields="id,parents").execute()

    def claim_next_job(self, worker_id):
        inbox = self.list_inbox()
        for f in inbox:
            job_name = f["name"]
            try:
                lock_id = self.create_lock(job_name, worker_id)
                if not lock_id:
                    continue
                self.move_file(f["id"], self.inbox_id, self.work_id)
                payload = self.download_file(f["id"])
                return {"job_name": job_name, "job_id": f["id"], "payload": json.loads(payload), "lock_id": lock_id}
            except Exception:
                continue
        return None

    def finish_job(self, job_name, job_id, result_obj, lock_id):
        self.upload_json(self.outbox_id, job_name, result_obj)
        try:
            self.delete_file(lock_id)
        except Exception:
            pass
        try:
            self.delete_file(job_id)
        except Exception:
            pass
