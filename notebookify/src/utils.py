import os
from pathlib import Path
import shutil
import json
from logger import log_message, INFO, ERROR, WARNING
from colorama import Fore, Style


def ensure_folder_exists(folder_path):
    """
    Ensure a folder exists, creating it if necessary.
    Handles nested folder creation and logs errors if creation fails.
    """
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            log_message(INFO, f"Created folder: {folder_path}")
        else:
            log_message(INFO, f"Folder already exists: {folder_path}")
    except OSError as e:
        log_message(ERROR, f"Failed to create folder {folder_path}: {e}")
        raise


def safe_create_folder(folder_path):
    """
    Ensures the folder exists, creating it if necessary. Logs the action.
    """
    try:
        folder = Path(folder_path)
        folder.mkdir(parents=True, exist_ok=True)
        log_message(INFO, f"Created folder: {folder}")
    except Exception as e:
        log_message(ERROR, f"Error creating folder {folder_path}: {e}")
        raise


def cleanup_folder(folder_path):
    """
    Remove a folder and its contents if it exists.
    """
    try:
        folder = Path(folder_path)
        if folder.exists():
            shutil.rmtree(folder)
            log_message(INFO, f"Successfully cleaned up folder: {folder}")
        else:
            log_message(WARNING, f"Folder does not exist: {folder}")
    except Exception as e:
        log_message(ERROR, f"Error during folder cleanup: {e}")


def handle_unsupported_output(output):
    """
    Logs unsupported output types and skips processing.
    """
    log_message(WARNING, f"Unsupported output type encountered: {output}")
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
            log_message(
                WARNING, f"Metadata file corrupted. Initializing new metadata."
            )
            return {}
    return {}


def save_metadata(metadata):
    """Save metadata."""
    metadata_path = get_metadata_path()
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)


# Detect GitHub root directory
def detect_github_root(notebook_path):
    current_dir = os.path.dirname(notebook_path)
    while current_dir:
        if ".git" in os.listdir(current_dir):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break
        current_dir = parent_dir
    return None


def get_template_path(template_name="index.md.j2"):
    """Retrieve the path to the custom template or default to nbconvert's template."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    custom_template = os.path.join(script_dir, "../templates", template_name)
    if os.path.exists(custom_template):
        return custom_template
    log_message(WARNING, f"Custom template not found. Using default template.")
    return "markdown"  # Fallback to default template


def print_help(script_name="Notebookify"):
    """
    Display help information for the script.

    Args:
        script_name (str): The name of the script/tool being described.
    """
    help_text = f"""
    {Style.BRIGHT}{Fore.BLUE}{script_name}: Convert Jupyter notebooks to Markdown and upload to Google Drive.{Style.RESET_ALL}

    {Fore.CYAN}Usage:
        {script_name.lower()} [options] {Style.RESET_ALL}

    {Fore.YELLOW}Options:{Style.RESET_ALL}
        {Fore.GREEN}-h, --help{Style.RESET_ALL}          Show this help message and exit
        {Fore.GREEN}-b, --batch DIRECTORY{Style.RESET_ALL} Process all notebooks in a directory (recursively)
        {Fore.GREEN}-t, --template PATH{Style.RESET_ALL}  Specify a custom Jinja2 template for Markdown conversion
        {Fore.GREEN}--no-drive{Style.RESET_ALL}          Skip Google Drive upload
        {Fore.GREEN}--clean{Style.RESET_ALL}             Clear notebook outputs after Markdown conversion
        {Fore.GREEN}-o, --output-dir PATH{Style.RESET_ALL} Specify an output directory for Markdown and assets

    {Fore.MAGENTA}Examples:{Style.RESET_ALL}
        {script_name.lower()} -h
        {script_name.lower()} --clean "path/to/notebook.ipynb"
        {script_name.lower()} --batch "path/to/notebooks/" --no-drive
    """
    log_message(INFO, help_text)
