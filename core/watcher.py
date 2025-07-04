import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

WATCH_PATHS = [
    "data/raw/git_repos",
    "data/raw/policies",
    "data/raw/infra_configs"
]

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"[!] Change detected: {event.src_path}")
            trigger_compliance_pipeline()

    def on_created(self, event):
        if not event.is_directory:
            print(f"[+] New file: {event.src_path}")
            trigger_compliance_pipeline()

def trigger_compliance_pipeline():
    print("Re-running compliance pipeline...")
    subprocess.call(["python", "run_phase1.py"])
    subprocess.call(["python", "run_phase2.py"])
    subprocess.call(["python", "run_phase3.py"])
    subprocess.call(["python", "run_phase4.py"])
    print("Updated compliance report generated.\n")

def start_watchdog():
    observer = Observer()
    handler = ChangeHandler()

    for path in WATCH_PATHS:
        abs_path = os.path.abspath(path)
        observer.schedule(handler, path=abs_path, recursive=True)
        print(f"Watching: {abs_path}")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
