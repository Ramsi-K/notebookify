import nbformat
from jinja2 import Environment, FileSystemLoader
import os
import logging

logger = logging.getLogger(__name__)


class MarkdownConverter:
    def __init__(self, template_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def convert(
        self, notebook_path, output_path, template_name="template.jinja2"
    ):
        try:
            logger.info(f"Converting notebook: {notebook_path}")
            with open(notebook_path, "r") as f:
                notebook = nbformat.read(f, as_version=4)

            template = self.env.get_template(template_name)
            markdown_output = template.render(
                cells=notebook["cells"],
                notebook_name=os.path.basename(notebook_path),
            )

            with open(output_path, "w") as f:
                f.write(markdown_output)

            logger.info(f"Conversion complete. Output saved to: {output_path}")
        except Exception as e:
            logger.error(f"Error converting notebook: {e}")
