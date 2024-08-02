from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os
from utils import (
    load_metadata,
    save_metadata,
    detect_github_root,
    )
from logger import log_message, INFO, ERROR, WARNING

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


def get_or_create_drive_folder(
    service, folder_name, parent_id=None, refresh=False
):
    """
    Retrieves or creates a Google Drive folder, optionally refreshing metadata.
    """
    try:
        metadata = load_metadata()
        folder_key = f"{parent_id}/{folder_name}" if parent_id else folder_name
        folder_id = metadata.get(folder_key)

        # Validate existing folder ID
        if folder_id and not refresh:
            folder_info = (
                service.files().get(fileId=folder_id, fields="id").execute()
            )
            if folder_info:
                log_message(
                    INFO, f"Folder '{folder_name}' exists. ID: {folder_id}"
                )
                return folder_id
            else:
                log_message(
                    WARNING,
                    f"Folder ID '{folder_id}' is invalid. Refreshing metadata.",
                )
                folder_id = None  # Force creation

        # Create a new folder if missing or invalid
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
        log_message(INFO, f"Folder '{folder_name}' created. ID: {folder_id}")
        return folder_id
    except Exception as e:
        log_message(ERROR, f"Error creating folder '{folder_name}': {e}")
        raise


def upload_to_google_drive(service, file_path, refresh=False):
    """
    Uploads a file to Google Drive, organizing it using metadata and GitHub root context.
    Refreshes metadata if `refresh` is True.
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
        parent_folder_id = metadata.get("root_folder_id")
        if not parent_folder_id:
            raise ValueError("Root folder ID not found in metadata.")

        for folder in os.path.dirname(relative_path).split(os.sep):
            parent_folder_id = get_or_create_drive_folder(
                service, folder, parent_id=parent_folder_id
            )

        # Upload file or refresh metadata
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

        # Update metadata only if refresh is requested
        if refresh:
            metadata[file_path] = uploaded_file.get("id")
            save_metadata(metadata)

        log_message(
            INFO,
            f"Uploaded {file_path} to Google Drive. ID: {uploaded_file.get('id')}",
        )
        return uploaded_file.get("id")
    except Exception as e:
        log_message(ERROR, f"Error uploading {file_path} to Google Drive: {e}")
        raise
