import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NotebookHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".ipynb"):
            print(f"Changement détecté : {event.src_path}")
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "auto: sauvegarde notebook"])
            subprocess.run(["git", "push", "origin", "main"])

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(NotebookHandler(), path=".", recursive=False)
    observer.start()
    print("Surveillance active... (Ctrl+C pour arrêter)")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
