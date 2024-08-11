import os
from threading import Thread
from watchdog.observers import Observer
from app.services.file_services.listener_service import NewFileHandler


def monitor_directory(directory_path: str):
    """
    Monitors a directory for new files and triggers events when new files are detected.

    Args:
        directory_path (str): The path of the directory to monitor.

    This function sets up an event handler using the `NewFileHandler` class and starts an observer to monitor
    the specified directory.
    The monitoring is not recursive, meaning it will only monitor the specified directory and not its subdirectories.
    """
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_path, recursive=False)
    observer.start()


def start_monitoring(folder_path):
    if not os.path.isdir(folder_path):
        return f"The specified folder path does not exist: {folder_path}", 400
    thread = Thread(target=monitor_directory, args=(folder_path,))
    thread.start()
    return "listening..."