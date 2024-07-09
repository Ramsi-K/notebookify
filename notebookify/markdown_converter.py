import os
import shutil
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import nbconvert
import nbformat
from jinja2 import Environment, FileSystemLoader
import plotly.io as pio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("notebookify.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

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
    logger.info(f"Starting Markdown conversion for {notebook_path}")
    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        exporter = nbconvert.MarkdownExporter()
        body, _ = exporter.from_notebook_node(notebook)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")

        output_file = os.path.join(
            output_dir,
            os.path.basename(notebook_path).replace(".ipynb", ".md"),
        )
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(body)

        logger.info(f"Markdown file saved to: {output_file}")
        return output_file

    except Exception as e:
        logger.error(f"Error during Markdown conversion: {e}")
        raise


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
    logger.info(
        f"Uploaded file {file_path} to Google Drive with ID: {uploaded_file.get('id')}"
    )


def save_plotly_snapshot(data, output_dir, filename="plotly_snapshot.png"):
    """
    Save Plotly visualizations as static images.
    Args:
        data (dict): Plotly data from the notebook cell.
        output_dir (str): Directory where the snapshot will be saved.
        filename (str): Name of the snapshot file.
    """
    try:
        fig = pio.from_json(data)
        snapshot_path = os.path.join(output_dir, filename)
        fig.write_image(snapshot_path)
        logger.info(f"Saved Plotly snapshot to {snapshot_path}")
        return snapshot_path
    except Exception as e:
        logger.error(f"Error saving Plotly snapshot: {e}")
        placeholder_path = os.path.join(output_dir, "plotly_snapshot_error.md")
        with open(placeholder_path, "w") as f:
            f.write(f"# Plotly Snapshot Error\n\nError: {e}")
        return placeholder_path


def convert_to_markdown_with_template(
    notebook_path, output_path, template_path
):
    logger.info(f"Starting Markdown conversion for {notebook_path}")
    # Load the Jupyter notebook
    with open(notebook_path, "r") as f:
        notebook = nbformat.read(f, as_version=4)

    # Load the Jinja2 environment and template
    env = Environment(loader=FileSystemLoader("/path/to/templates"))
    template = env.get_template(template_path)

    # Prepare the cells for rendering
    for cell in notebook["cells"]:
        if "outputs" in cell:
            for output in cell["outputs"]:
                if "application/vnd.plotly.v1+json" in output.get("data", {}):
                    logger.info("Plotly visualization found.")
                    plotly_snapshot_path = save_plotly_snapshot(
                        output["data"]["application/vnd.plotly.v1+json"],
                        os.path.dirname(output_path),
                        f"{os.path.basename(output_path).replace('.md', '')}_plotly.png",
                    )
                    output["plotly_snapshot"] = plotly_snapshot_path

    # Render the Markdown output
    markdown_output = template.render(
        cells=notebook["cells"],
        repo_name="Ramsi-K/notebookify",
        notebook_name=os.path.basename(notebook_path),
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
    logger.info(f"Converted notebook saved to: {markdown_file}")

    # Authenticate and upload to Google Drive
    try:
        service = authenticate_google_drive()
        upload_to_google_drive(service, markdown_file)
    except Exception as e:
        logger.error(f"Error during Google Drive upload: {e}")
