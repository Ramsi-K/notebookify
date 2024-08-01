#!/usr/bin/env python

import os
import argparse
from colorama import Fore
import sys

from src.drive import (
    authenticate_drive,
    get_or_create_drive_folder,
    upload_to_google_drive,
)
from src.markdown_converter import MarkdownConverter, process_batch_notebooks
from src.utils import (
    print_help,
    safe_create_folder,
    load_metadata,
    save_metadata,
    detect_github_root,
    get_metadata_path,
)
from src.logger import log_message, INFO, WARNING, ERROR


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        help="Show this help message and exit",
    )
    parser.add_argument(
        "-b", "--batch", type=str, help="Process all notebooks in a directory"
    )
    parser.add_argument(
        "-t",
        "--template",
        type=str,
        help="Specify a custom Jinja2 template for Markdown conversion",
    )
    parser.add_argument(
        "--refresh-metadata",
        action="store_true",
        help="Refresh Google Drive metadata",
    )
    parser.add_argument(
        "--no-drive", action="store_true", help="Skip Google Drive upload"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clear notebook outputs after Markdown conversion",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        help="Specify an output directory for Markdown and assets",
    )
    parser.add_argument(
        "notebook_path",
        nargs="?",
        help="Path to a single Jupyter notebook file",
    )
    return parser.parse_args()


def refresh_metadata(service):
    """
    Refresh Google Drive metadata.
    """
    try:
        log_message(INFO, "Refreshing Google Drive metadata...")
        metadata = {}
        root_folder_id = get_or_create_drive_folder(
            service, "Notebookify_Root"
        )
        metadata["drive_root"] = root_folder_id
        save_metadata(metadata)
        log_message(INFO, "Google Drive metadata refreshed successfully.")
    except Exception as e:
        log_message(ERROR, f"Failed to refresh metadata: {e}")


def process_notebook(notebook_path, args, metadata):
    """Process a single notebook."""
    if not os.path.isfile(notebook_path) or not notebook_path.endswith(
        ".ipynb"
    ):
        log_message(ERROR, f"Invalid notebook path: {notebook_path}")
        return

    # Detect GitHub root
    github_root = detect_github_root(notebook_path)
    if github_root:
        log_message(INFO, f"Detected GitHub root: {github_root}")
    else:
        log_message(
            WARNING,
            "GitHub root not detected. Uploads will not reflect repository structure.",
        )

    # Upload Workflow
    try:
        output_dir = args.output_dir or os.path.dirname(notebook_path)
        log_message(INFO, f"Output directory set to: {output_dir}")

        # Convert notebook to Markdown
        template_dir = args.template or "templates"
        converter = MarkdownConverter(template_dir)
        output_path = os.path.join(
            output_dir,
            os.path.basename(notebook_path).replace(".ipynb", ".md"),
        )
        converter.convert(notebook_path, output_path)

        # Upload to Google Drive
        if not args.no_drive:
            service = authenticate_drive()
            drive_folder_id = metadata.get("drive_root", None)
            if not drive_folder_id:
                drive_folder_id = get_or_create_drive_folder(
                    service,
                    (
                        os.path.basename(github_root)
                        if github_root
                        else "Notebookify"
                    ),
                )
                metadata["drive_root"] = drive_folder_id
                save_metadata(metadata)

            upload_to_google_drive(service, output_path, drive_folder_id)
        else:
            log_message(WARNING, "Google Drive upload skipped.")
    except Exception as e:
        log_message(ERROR, f"Failed to process notebook: {e}")


def batch_process(directory, args):
    """
    Recursively processes all notebooks in a directory using the MarkdownConverter.
    """
    notebook_paths = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if file.endswith(".ipynb")
    ]
    process_batch_notebooks(
        notebook_paths,
        output_dir=args.output_dir,
        template_dir=args.template,
        drive_service=None if args.no_drive else authenticate_drive(),
        refresh=args.refresh_metadata,
    )


def main():
    args = parse_args()
    metadata = load_metadata()  # Load metadata once for all operations
    last_notebook_path = None  # To store the last processed notebook path

    if args.help:
        print_help()
        sys.exit(0)  # Exit explicitly after displaying help
        return

    if args.refresh_metadata:
        try:
            service = authenticate_drive()
            log_message(INFO, "Refreshing metadata during Drive operations.")
            refresh_metadata(service)
        except Exception as e:
            log_message(ERROR, f"Failed to refresh metadata: {e}")
        return

    if args.batch:
        batch_process(args.batch, args)
        return

    if args.notebook_path:
        process_notebook(args.notebook_path, args, metadata)
        return

    # Interactive mode fallback
    while True:
        print(f"{Fore.BLUE}Interactive mode activated.")

        # If last_notebook_path exists, use it for retry
        if not last_notebook_path:
            notebook_path = (
                input(f"{Fore.YELLOW}Enter the notebook path: ")
                .strip()
                .strip('"')
                .strip("'")
            )
        else:
            notebook_path = last_notebook_path
            log_message(INFO, f"Retrying the last notebook: {notebook_path}")

        try:
            process_notebook(notebook_path, args, metadata)
            last_notebook_path = (
                notebook_path  # Update the last notebook path after processing
            )
        except Exception as e:
            log_message(ERROR, f"{str(e)}")

        print("\nOptions:")
        print("1. Retry the same notebook.")
        print("2. Process another notebook.")
        print("3. Exit.")

        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            continue
        elif choice == "2":
            log_message(INFO, "Starting a new notebook process...")
            last_notebook_path = None  # Reset last notebook path
        elif choice == "3":
            log_message(INFO, "Exiting the script.")
            break
        else:
            log_message(ERROR, "Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_message(INFO, "Script interrupted by user.")
    finally:
        log_message(INFO, "Execution complete. Closing environment.")
        sys.exit(0)
