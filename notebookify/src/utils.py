import os
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


def cleanup_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        logger.info(f"Cleaned up folder: {folder_path}")
