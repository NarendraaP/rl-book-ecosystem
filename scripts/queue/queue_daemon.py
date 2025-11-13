#!/usr/bin/env python3
# scripts/queue/queue_daemon.py
# Minimal queue daemon stub for local testing (no Drive)
import time, json, shutil, pathlib
ROOT = pathlib.Path('data/jobs')
INBOX = ROOT/'inbox'
WORK = ROOT/'work'
OUT = ROOT/'outbox'
LOCKS = ROOT/'locks'
for d in [INBOX, WORK, OUT, LOCKS]:
    d.mkdir(parents=True, exist_ok=True)

def pick_job():
    jobs = list(INBOX.glob('*.json'))
    if not jobs:
        return None
    job = jobs[0]
    dest = WORK/job.name
    shutil.move(str(job), str(dest))
    lock = LOCKS/f"{job.stem}.lock"
    lock.write_text('LOCK')
    return dest

def process_job(path):
    data = json.loads(path.read_text())
    # simple noop processor
    result = {'job_id': data.get('job_id','unknown'), 'status':'done'}
    out = OUT/path.name
    out.write_text(json.dumps(result))
    # cleanup lock
    lock = LOCKS/f"{path.stem}.lock"
    if lock.exists(): lock.unlink()

if __name__ == '__main__':
    while True:
        job = pick_job()
        if job:
            process_job(job)
        time.sleep(1)
