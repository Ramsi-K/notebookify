from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os
import logging

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
logger = logging.getLogger(__name__)


def authenticate_google_drive():
    creds = None
    token_path = "token.json"
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        raise FileNotFoundError(
            "token.json file not found. Authenticate using OAuth."
        )
    return build("drive", "v3", credentials=creds)


def upload_to_google_drive(service, file_path):
    file_metadata = {"name": os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype="text/markdown")
    uploaded_file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    logger.info(
        f"Uploaded {file_path} to Google Drive. ID: {uploaded_file.get('id')}"
    )


def process_batch_notebooks(service, notebook_paths, output_dir):
    for notebook_path in notebook_paths:
        try:
            logger.info(f"Processing notebook: {notebook_path}")
            # Assuming convert_to_markdown is implemented in markdown_converter
            markdown_file = convert_to_markdown(notebook_path, output_dir)
            upload_to_google_drive(service, markdown_file)
        except Exception as e:
            logger.error(f"Error processing {notebook_path}: {e}")
