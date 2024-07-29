import nbformat
from jinja2 import Environment, FileSystemLoader
import os
import logging
import plotly.io as pio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import nbconvert
import shutil
from notebookify.src.google_drive_uploader import upload_to_google_drive


import nbformat
from jinja2 import Environment, FileSystemLoader
from src.utils import safe_create_folder, handle_unsupported_output
import os
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MarkdownConverter:
    def __init__(self, template_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def convert(
        self, notebook_path, output_path, template_name="template.jinja2"
    ):
        """
        Converts a notebook to Markdown using a Jinja2 template.
        """
        try:
            logger.info(f"Converting notebook: {notebook_path}")
            notebook = self._load_notebook(notebook_path)
            processed_cells = self._process_cells(notebook["cells"])

            template = self.env.get_template(template_name)
            markdown_output = template.render(cells=processed_cells)

            self._save_markdown(output_path, markdown_output)
            logger.info(f"Conversion complete. Output saved to: {output_path}")
        except Exception as e:
            logger.error(f"Error converting notebook: {e}")
            raise

    @staticmethod
    def _load_notebook(notebook_path):
        with open(notebook_path, "r", encoding="utf-8") as f:
            return nbformat.read(f, as_version=4)

    @staticmethod
    def _process_cells(cells):
        for cell in cells:
            if "outputs" in cell:
                cell["processed_outputs"] = [
                    MarkdownConverter._process_output(output)
                    for output in cell["outputs"]
                ]
        return cells

    @staticmethod
    def _process_output(output):
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
            logger.error(f"Error processing output: {e}")
            return handle_unsupported_output(output)

    @staticmethod
    def _process_plotly_output(plotly_data):
        """
        Placeholder for processing Plotly outputs.
        """
        return "<!-- Plotly output -->"

    @staticmethod
    def _save_markdown(output_path, markdown_output):
        safe_create_folder(os.path.dirname(output_path))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_output)

    def convert_to_nbconvert(self, notebook_path, output_dir):
        """
        Converts a notebook to Markdown using nbconvert and saves it to the output directory.
        """
        try:
            self.logger.info(f"Starting nbconvert for {notebook_path}")
            safe_create_folder(output_dir)

            with open(notebook_path, "r", encoding="utf-8") as f:
                notebook = nbformat.read(f, as_version=4)

            exporter = nbconvert.MarkdownExporter()
            body, _ = exporter.from_notebook_node(notebook)

            output_file = os.path.join(
                output_dir,
                os.path.basename(notebook_path).replace(".ipynb", ".md"),
            )
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(body)

            self.logger.info(f"Markdown file saved to: {output_file}")
            return output_file
        except Exception as e:
            self.logger.error(f"Error during nbconvert: {e}")
            raise

    def convert_with_custom_template(
        self, notebook_path, output_path, template_path
    ):
        """
        Converts a notebook to Markdown using a custom Jinja2 template.
        """
        try:
            logger.info(
                f"Converting notebook with custom template: {notebook_path}"
            )
            notebook = self._load_notebook(notebook_path)

            # Load Jinja2 environment and template
            template = self.env.get_template(template_path)

            # Process outputs
            processed_cells = self._process_cells(notebook["cells"])

            # Render Markdown
            markdown_output = template.render(cells=processed_cells)

            # Save output
            self._save_markdown(output_path, markdown_output)
            logger.info(f"Converted notebook saved to {output_path}")
        except Exception as e:
            logger.error(f"Error during Markdown conversion: {e}")
            raise


def process_batch_notebooks(service, notebook_paths, output_dir, template_dir):
    converter = MarkdownConverter(template_dir)

    for notebook_path in notebook_paths:
        try:
            logger.info(f"Processing notebook: {notebook_path}")
            output_file = os.path.join(
                output_dir,
                os.path.basename(notebook_path).replace(".ipynb", ".md"),
            )
            converter.convert(notebook_path, output_file)
            upload_to_google_drive(service, output_file)
        except Exception as e:
            logger.error(f"Error processing notebook {notebook_path}: {e}")
