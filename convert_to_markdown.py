import os
from nbconvert import MarkdownExporter
import subprocess
import nbformat


def convert_to_markdown(notebook_path, output_dir):
    """Converts a Jupyter Notebook to a Markdown file."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    exporter = MarkdownExporter()
    body, resources = exporter.from_notebook_node(notebook)

    markdown_path = os.path.join(output_dir, "converted_notebook.md")
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(body)

    return markdown_path


if __name__ == "__main__":
    notebook_path = "example_notebook.ipynb"
    output_dir = "output"
    markdown_file = convert_to_markdown(notebook_path, output_dir)
    print(f"Markdown file created at: {markdown_file}")
