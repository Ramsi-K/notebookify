import os
import shutil
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import nbconvert
import nbformat
from jinja2 import Environment, FileSystemLoader

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class MarkdownConverter:
    def __init__(self, template_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def convert(self, notebook_path, output_path, template_name):
        with open(notebook_path, "r") as f:
            notebook = nbformat.read(f, as_version=4)

        template = self.env.get_template(template_name)
        markdown_output = template.render(
            cells=notebook["cells"],
            notebook_name=os.path.basename(notebook_path),
        )

        with open(output_path, "w") as f:
            f.write(markdown_output)

    @staticmethod
    def cleanup_folder(folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)


# Example Usage:
# converter = MarkdownConverter(template_dir='path/to/templates')
# converter.convert('example_notebook.ipynb', 'output.md', 'template.jinja2')
# converter.cleanup_folder('path/to/temp_folder')


def convert_notebook_to_markdown(notebook_path, output_dir):
    """
    Converts a notebook file to a Markdown file and saves it to the output directory.
    """
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    exporter = nbconvert.MarkdownExporter()
    body, _ = exporter.from_notebook_node(notebook)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(
        output_dir, os.path.basename(notebook_path).replace(".ipynb", ".md")
    )
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(body)

    return output_file


def authenticate_google_drive():
    """
    Authenticate with Google Drive and return the service object.
    """
    creds = None
    token_path = "token.json"
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        raise FileNotFoundError(
            "token.json file not found. Authenticate using OAuth."
        )

    service = build("drive", "v3", credentials=creds)
    return service


def upload_to_google_drive(service, file_path):
    """
    Upload a file to Google Drive.
    """
    file_metadata = {"name": os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype="text/markdown")

    uploaded_file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print(
        f"Uploaded file {file_path} to Google Drive with ID: {uploaded_file.get('id')}"
    )


def convert_to_markdown_with_template(
    notebook_path, output_path, template_path
):
    # Load the Jupyter notebook
    with open(notebook_path, "r") as f:
        notebook = nbformat.read(f, as_version=4)

    # Load the Jinja2 environment and template
    env = Environment(loader=FileSystemLoader("/path/to/templates"))
    template = env.get_template(template_path)

    # Render the Markdown output
    markdown_output = template.render(
        cells=notebook["cells"],
        repo_name="Ramsi-K/notebookify",
        notebook_name=notebook_path.split("/")[-1],
    )

    # Save to output path
    with open(output_path, "w") as f:
        f.write(markdown_output)


# # Example usage:
# convert_to_markdown_with_template("example_notebook.ipynb", "output.md", "template.jinja2")

if __name__ == "__main__":
    notebook_path = "example_notebook.ipynb"
    output_dir = "markdown_outputs"

    # Convert the notebook
    markdown_file = convert_notebook_to_markdown(notebook_path, output_dir)
    print(f"Converted notebook saved to: {markdown_file}")

    # Authenticate and upload to Google Drive
    try:
        service = authenticate_google_drive()
        upload_to_google_drive(service, markdown_file)
    except Exception as e:
        print(f"Error during Google Drive upload: {e}")
