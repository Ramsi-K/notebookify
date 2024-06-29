import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# Authenticate Google Drive API
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)


# Upload a file to Google Drive
def upload_file_to_drive(drive, file_path, folder_id=None):
    file = drive.CreateFile(
        {
            "title": os.path.basename(file_path),
            "parents": [{"id": folder_id}] if folder_id else None,
        }
    )
    file.SetContentFile(file_path)
    file.Upload()
    print(f"Uploaded {file_path} to Google Drive with ID: {file['id']}")


if __name__ == "__main__":
    # Example usage
    drive = authenticate_drive()
    file_path = "example_file.txt"  # Replace with a test file path
    folder_id = None  # Replace with Google Drive folder ID if needed
    upload_file_to_drive(drive, file_path, folder_id)
