from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os
from src.utils import load_metadata, save_metadata, detect_github_root
from src.logger import log_message, INFO, ERROR, WARNING

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
TOKEN_PATH = "token.json"


def authenticate_google_drive():
    """
    Authenticate with Google Drive API using credentials.
    """
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    else:
        log_message(
            ERROR, "Token file not found. Please authenticate using OAuth."
        )
        raise FileNotFoundError(
            f"{TOKEN_PATH} not found. Generate it by completing the OAuth process."
        )
    return build("drive", "v3", credentials=creds)


def get_or_create_drive_folder(service, folder_name, parent_id=None):
    """
    Retrieves or creates a Google Drive folder and updates metadata.
    """
    try:
        metadata = load_metadata()

        # Check if folder exists in metadata
        folder_key = f"{parent_id}/{folder_name}" if parent_id else folder_name
        folder_id = metadata.get(folder_key)
        if folder_id:
            log_message(
                INFO,
                f"Folder '{folder_name}' already exists in metadata. ID: {folder_id}",
            )
            return folder_id

        # Create folder in Drive
        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            folder_metadata["parents"] = [parent_id]

        created_folder = (
            service.files().create(body=folder_metadata, fields="id").execute()
        )
        folder_id = created_folder.get("id")

        # Update metadata
        metadata[folder_key] = folder_id
        save_metadata(metadata)

        log_message(
            INFO,
            f"Created folder '{folder_name}' in Google Drive. ID: {folder_id}",
        )
        return folder_id
    except Exception as e:
        log_message(ERROR, f"Error creating folder '{folder_name}': {e}")
        raise


def upload_to_google_drive(service, file_path):
    """
    Uploads a file to Google Drive, organizing it using metadata and GitHub root context.
    """
    try:
        metadata = load_metadata()
        github_root = detect_github_root(file_path)

        # Determine relative path within GitHub repo
        relative_path = (
            os.path.relpath(file_path, github_root)
            if github_root
            else os.path.basename(file_path)
        )

        # Create folder structure in Drive
        parent_folder_id = metadata.get(
            "root_folder_id"
        )  # Example: A predefined root folder ID
        if not parent_folder_id:
            raise ValueError("Root folder ID not found in metadata.")

        # Create or fetch nested folders
        for folder in os.path.dirname(relative_path).split(os.sep):
            parent_folder_id = get_or_create_drive_folder(
                service, folder, parent_id=parent_folder_id
            )

        # Upload file to the appropriate folder
        file_metadata = {
            "name": os.path.basename(file_path),
            "parents": [parent_folder_id],
        }
        media = MediaFileUpload(file_path, mimetype="text/markdown")
        uploaded_file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        log_message(
            INFO,
            f"Uploaded {file_path} to Google Drive. ID: {uploaded_file.get('id')}",
        )
        return uploaded_file.get("id")
    except Exception as e:
        log_message(ERROR, f"Error uploading {file_path} to Google Drive: {e}")
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
                log_message.warning(f"Skipping invalid file: {notebook_path}")
                continue
            log_message(INFO, f"Processing notebook: {notebook_path}")
            markdown_file = convert_to_markdown(notebook_path, output_dir)
            upload_to_google_drive(service, markdown_file)
        except Exception as e:
            log_message(ERROR, f"Error processing {notebook_path}: {e}")
