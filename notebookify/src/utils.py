import os
from pathlib import Path
import shutil
import logging

logger = logging.getLogger(__name__)


def ensure_folder_exists(folder_path):
    """
    Ensure a folder exists, creating it if necessary.
    Handles nested folder creation and logs errors if creation fails.
    """
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.info(f"Created folder: {folder_path}")
        else:
            logger.info(f"Folder already exists: {folder_path}")
    except OSError as e:
        logger.error(f"Failed to create folder {folder_path}: {e}")
        raise


def safe_create_folder(folder_path):
    """
    Ensures the folder exists, creating it if necessary. Logs the action.
    """
    try:
        folder = Path(folder_path)
        folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created folder: {folder}")
    except Exception as e:
        logger.error(f"Error creating folder {folder_path}: {e}")
        raise


def cleanup_folder(folder_path):
    """
    Remove a folder and its contents if it exists.
    """
    try:
        folder = Path(folder_path)
        if folder.exists():
            shutil.rmtree(folder)
            logger.info(f"Successfully cleaned up folder: {folder}")
        else:
            logger.warning(f"Folder does not exist: {folder}")
    except Exception as e:
        logger.error(f"Error during folder cleanup: {e}")


def handle_unsupported_output(output):
    """
    Logs unsupported output types and skips processing.
    """
    logger.warning(f"Unsupported output type encountered: {output}")
    return f"<!-- Unsupported output type: {output} -->"


def get_metadata_path():
    """Centralized path for drive metadata."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # credentials_path = os.path.join(script_dir, "credentials.json")
    return os.path.join(script_dir, "drive_metadata.json")


def load_metadata():
    """Load drive metadata."""
    metadata_path = get_metadata_path()
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(
                f"{WARNING} Metadata file corrupted. Initializing new metadata."
            )
            return {}
    return {}


def save_metadata(metadata):
    """Save metadata."""
    metadata_path = get_metadata_path()
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)
