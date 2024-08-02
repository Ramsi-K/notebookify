import nbformat
from jinja2 import Environment, FileSystemLoader
from utils import (
    safe_create_folder,
    handle_unsupported_output,
    get_template_path,
)
import os
from logger import log_message, INFO, WARNING, ERROR
from utils import (
    load_metadata,
    save_metadata,
    detect_github_root,
    get_metadata_path,
)
from drive import upload_to_google_drive


class MarkdownConverter:
    """
    A class for converting Jupyter notebooks to Markdown using Jinja2 templates.
    """

    def __init__(self, template_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def convert(
        self, notebook_path, output_path, template_name="template.jinja2"
    ):
        """
        Converts a notebook to Markdown using a Jinja2 template.
        """
        try:
            log_message(INFO, f"Converting notebook: {notebook_path}")
            notebook = self._load_notebook(notebook_path)
            processed_cells = self._process_cells(notebook["cells"])

            template = self.env.get_template(template_name)
            markdown_output = template.render(cells=processed_cells)

            self._save_markdown(output_path, markdown_output)
            log_message(
                INFO, f"Conversion complete. Output saved to: {output_path}"
            )
        except Exception as e:
            log_message(ERROR, f"Error converting notebook: {e}")
            raise

    @staticmethod
    def _load_notebook(notebook_path):
        """
        Loads a Jupyter notebook file.
        """
        try:
            with open(notebook_path, "r", encoding="utf-8") as f:
                return nbformat.read(f, as_version=4)
        except Exception as e:
            log_message(
                ERROR, f"Failed to load notebook: {notebook_path}. Error: {e}"
            )
            raise

    @staticmethod
    def _process_cells(cells):
        """
        Processes notebook cells and extracts their outputs.
        """
        for cell in cells:
            if "outputs" in cell:
                cell["processed_outputs"] = [
                    MarkdownConverter._process_output(output)
                    for output in cell["outputs"]
                ]
        return cells

    @staticmethod
    def _process_output(output):
        """
        Processes individual cell outputs based on their types.
        """
        try:
            if output["output_type"] == "execute_result":
                if "text/plain" in output.data:
                    return output.data["text/plain"]
                elif "image/png" in output.data:
                    return f"![Image](data:image/png;base64,{output.data['image/png']})"
                elif "application/vnd.plotly.v1+json" in output.data:
                    return MarkdownConverter._process_plotly_output(
                        output.data["application/vnd.plotly.v1+json"]
                    )
            return handle_unsupported_output(output)
        except Exception as e:
            log_message(ERROR, f"Error processing output: {e}")
            return handle_unsupported_output(output)

    @staticmethod
    def _process_plotly_output(plotly_data):
        """
        Processes Plotly outputs.
        Currently a placeholder; add functionality as needed.
        """
        log_message(
            INFO, "Processing Plotly output. Placeholder logic in place."
        )
        return "<!-- Plotly output placeholder -->"

    @staticmethod
    def _save_markdown(output_path, markdown_output):
        """
        Saves the generated Markdown content to the specified path.
        """
        safe_create_folder(os.path.dirname(output_path))
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_output)
        except Exception as e:
            log_message(ERROR, f"Error saving Markdown file: {e}")
            raise


def process_batch_notebooks(
    notebook_paths, output_dir, template_dir, drive_service=None, refresh=False
):
    """
    Processes a batch of notebooks, converts them to Markdown, and optionally uploads them to Google Drive.

    Args:
        notebook_paths (list): Paths to Jupyter notebooks to process.
        output_dir (str): Directory to save converted Markdown files.
        template_dir (str): Directory containing Jinja2 templates.
        drive_service (object, optional): Google Drive service object for uploading files.
        refresh (bool): Whether to refresh metadata for uploads.
    """
    converter = MarkdownConverter(template_dir)

    for notebook_path in notebook_paths:
        try:
            log_message(INFO, f"Processing notebook: {notebook_path}")
            output_file = os.path.join(
                output_dir,
                os.path.basename(notebook_path).replace(".ipynb", ".md"),
            )
            # Convert the notebook to Markdown
            converter.convert(notebook_path, output_file)

            # Upload to Google Drive if service is provided
            if drive_service:
                upload_to_google_drive(
                    drive_service, output_file, refresh=refresh
                )
        except Exception as e:
            log_message(
                ERROR, f"Error processing notebook {notebook_path}: {e}"
            )


def update_markdown_with_colab_link(md_file_path, colab_link):
    """
    Adds a Colab link to the top of the Markdown file.
    """
    try:
        with open(md_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        colab_header = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_link})\n\n"
        updated_content = colab_header + content

        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        log_message(INFO, f"Colab link added to Markdown file: {md_file_path}")
    except Exception as e:
        log_message(ERROR, f"Error updating Markdown with Colab link: {e}")
