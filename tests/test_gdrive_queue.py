# tests/test_gdrive_queue.py
from scripts.queue.gdrive_queue import GDriveQueue
from scripts.queue.colab_worker import process_job

def test_imports_and_process():
    assert GDriveQueue  # module import ok
    out = process_job({"job_id":"t1"})
    assert out["status"] == "done"
