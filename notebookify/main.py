from markdown_converter import MarkdownConverter
from google_drive_uploader import (
    authenticate_google_drive,
    process_batch_notebooks,
)
from utils import ensure_folder_exists
import logging
from markdown_converter import capture_iframe_snapshot

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    template_dir = "templates"
    notebook_paths = [
        "notebooks/example1.ipynb",
        "notebooks/example2.ipynb",
        "notebooks/example3.ipynb",
    ]
    output_dir = "markdown_outputs"
    ensure_folder_exists(output_dir)

    converter = MarkdownConverter(template_dir=template_dir)

    # Authenticate with Google Drive
    try:
        service = authenticate_google_drive()
        process_batch_notebooks(service, notebook_paths, output_dir)
    except Exception as e:
        logging.error(f"Failed to process notebooks: {e}")
