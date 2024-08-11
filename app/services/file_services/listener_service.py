import os
import re
from watchdog.events import FileSystemEventHandler
from app import db
from app.services.file_services.orchestration_service import extract_and_query


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        Handles the event when a new file is created.
        Parameters:
        event (Event): The event object containing information about the created file.
        Behavior:
        - If the event is not for a directory, processes the file.
        - Checks if the file exists.
        - Extracts the file name and file type.
        - If the file has already been processed, updates it.
        - If the file is new, extracts information using extract_info and inserts it into a collection.
        - Stores the processed file path and its database ID.
        Raises:
        Exception: If there is an error processing the file.
        """
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            job_number = extract_job_number(file_name)
            job_model = db['job']
            job = job_model.get_job_by_number(job_number)
            if not job:
                print(f"No job found with job number: {job_number}")
                return "Error"
            job_id = job['_id']
            return extract_and_query(file_path, job_id)


def extract_job_number(file_name: str) -> str:
    """
    Extracts the job number from the given file name using a regular expression.
    Args:
        file_name (str): The name of the file.
    Returns:
        str: The extracted job number or an empty string if not found.
    """
    match = re.match(r'^(\d+)_', file_name)
    if match:
        return match.group(1)
    return ""