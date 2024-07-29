#!/usr/bin/env python

import os
import argparse
from colorama import Fore
import sys

from src.drive import (
    authenticate_drive,
    get_or_create_drive_folder,
    upload_to_drive,
)
from src.markdown_converter import MarkdownConverter, clear_outputs
from src.utils import print_help, safe_create_folder
from src.logger import INFO, WARNING, ERROR


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


def process_notebook(notebook_path, args):
    """Process a single notebook."""
    if not os.path.isfile(notebook_path) or not notebook_path.endswith(
        ".ipynb"
    ):
        print(f"{ERROR} Invalid notebook path: {notebook_path}")
        return

    clear_output = (
        args.clean
        or input(f"{Fore.YELLOW}Clear outputs after conversion? (y/n)[y]: ")
        .strip()
        .lower()
        != "n"
    )
    share_with_link = (
        not args.no_drive
        and input(f"{Fore.YELLOW}Make file public (y/n)[y]: ").strip().lower()
        != "n"
    )

    # Conversion and upload
    output_dir = args.output_dir or os.path.join(os.getcwd(), "output")
    safe_create_folder(output_dir)
    print(f"{INFO} Created output directory: {output_dir}")

    converter = MarkdownConverter(template_dir="templates/")
    md_file_path = converter.convert(notebook_path, output_dir)

    if clear_output:
        clear_outputs(notebook_path)

    if not args.no_drive:
        drive_service = authenticate_drive()
        colab_link = upload_to_drive(
            drive_service, notebook_path, share_with_link=share_with_link
        )
        if colab_link:
            print(f"{INFO} Colab link: {colab_link}")
        else:
            print(f"{WARNING} Colab link not found.")


def batch_process(directory, args):
    """Process all notebooks in a directory recursively."""
    print(f"{INFO} Batch processing notebooks in directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ipynb"):
                notebook_path = os.path.join(root, file)
                print(f"{INFO} Processing notebook: {notebook_path}")
                try:
                    process_notebook(notebook_path, args)
                except Exception as e:
                    print(
                        f"{ERROR} Failed to process {notebook_path}: {str(e)}"
                    )


def main():
    args = parse_args()
    last_notebook_path = None  # To store the last processed notebook path

    if args.help:
        print_help()
        return

    if args.batch:
        batch_process(args.batch, args)
        return

    if args.notebook_path:
        process_notebook(args.notebook_path, args)
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
            print(f"{INFO} Retrying the last notebook: {notebook_path}")

        try:
            process_notebook(notebook_path, args)
            last_notebook_path = (
                notebook_path  # Update the last notebook path after processing
            )
        except Exception as e:
            print(f"{ERROR} {str(e)}")

        print("\nOptions:")
        print("1. Retry the same notebook.")
        print("2. Process another notebook.")
        print("3. Exit.")

        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            continue
        elif choice == "2":
            print(f"{INFO} Starting a new notebook process...")
        elif choice == "3":
            print(f"{INFO} Exiting the script.")
            break
        else:
            print(f"{ERROR} Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{INFO} Script interrupted by user.")
    finally:
        print(f"{INFO} Execution complete. Closing environment.")
        sys.exit(0)
