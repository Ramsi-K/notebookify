from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os
import logging

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
TOKEN_PATH = "token.json"
logger = logging.getLogger(__name__)


def authenticate_google_drive():
    """
    Authenticate with Google Drive API using credentials.
    """
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    else:
        logger.error("Token file not found. Please authenticate using OAuth.")
        raise FileNotFoundError(
            f"{TOKEN_PATH} not found. Generate it by completing the OAuth process."
        )
    return build("drive", "v3", credentials=creds)


def upload_to_google_drive(service, file_path):
    """
    Upload a file to Google Drive.
    """
    try:
        file_metadata = {"name": os.path.basename(file_path)}
        media = MediaFileUpload(file_path, mimetype="text/markdown")
        uploaded_file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        logger.info(
            f"Uploaded {file_path} to Google Drive. File ID: {uploaded_file.get('id')}"
        )
    except Exception as e:
        logger.error(f"Failed to upload {file_path} to Google Drive: {e}")
        raise


def process_batch_notebooks(
    service, notebook_paths, output_dir, convert_to_markdown
):
    """
    Process a batch of notebooks, convert them to Markdown, and upload to Google Drive.
    """
    for notebook_path in notebook_paths:
        try:
            if not os.path.isfile(notebook_path):
                logger.warning(f"Skipping invalid file: {notebook_path}")
                continue
            logger.info(f"Processing notebook: {notebook_path}")
            markdown_file = convert_to_markdown(notebook_path, output_dir)
            upload_to_google_drive(service, markdown_file)
        except Exception as e:
            logger.error(f"Error processing {notebook_path}: {e}")
