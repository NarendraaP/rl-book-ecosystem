# colab_worker.py
import os, time, uuid
from datetime import datetime
from scripts.queue.gdrive_queue import GDriveQueue

WORKER_ID = f"colab-{uuid.uuid4().hex[:8]}"

def process_job(payload):
    return {"job_id": payload.get("job_id"), "status": "done", "processed_at": datetime.utcnow().isoformat() + "Z"}

def main_loop(drive_folder_id_env="GDRIVE_QUEUE_FOLDER_ID"):
    folder_id = os.environ.get(drive_folder_id_env)
    if not folder_id:
        raise RuntimeError("Set env GDRIVE_QUEUE_FOLDER_ID to the Drive folder id")
    q = GDriveQueue(folder_id)
    print("Worker starting", WORKER_ID)
    while True:
        job = q.claim_next_job(WORKER_ID)
        if not job:
            time.sleep(2)
            continue
        print("Claimed job:", job["job_name"])
        try:
            res = process_job(job["payload"])
            q.finish_job(job["job_name"], job["job_id"], res, job["lock_id"])
            print("Finished job:", job["job_name"])
        except Exception as e:
            print("Processing failed", e)
            try:
                q.delete_file(job["lock_id"])
            except Exception:
                pass
        time.sleep(0.5)

if __name__ == "__main__":
    main_loop()
