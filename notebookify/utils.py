import os
import shutil
import logging

logger = logging.getLogger(__name__)


def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info(f"Created folder: {folder_path}")


def cleanup_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        logger.info(f"Cleaned up folder: {folder_path}")
