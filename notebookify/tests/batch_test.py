import logging
from notebookify.src.markdown_converter import (
    process_batch_notebooks,
    authenticate_google_drive,
)

# Configure logging for batch tests
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    notebook_paths = [
        "notebooks/example1.ipynb",
        "notebooks/example2.ipynb",
        "notebooks/example3.ipynb",
    ]
    output_dir = "markdown_outputs"

    # Authenticate with Google Drive
    try:
        service = authenticate_google_drive()
    except Exception as e:
        logging.error(f"Google Drive authentication failed: {e}")
        service = None

    # Process the batch
    process_batch_notebooks(notebook_paths, output_dir, service)


if __name__ == "__main__":
    main()
