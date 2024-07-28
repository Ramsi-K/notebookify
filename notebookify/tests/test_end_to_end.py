import os
import shutil
from markdown_converter import (
    convert_to_markdown_with_template,
    ensure_folder_exists,
)


def test_end_to_end():
    """
    End-to-end test for notebook-to-Markdown conversion with folder management.
    """
    notebook_path = "example_notebook.ipynb"
    output_dir = "test_outputs"
    template_path = "template.jinja2"
    output_file = os.path.join(output_dir, "example_output.md")

    try:
        # Ensure output directory exists
        ensure_folder_exists(output_dir)

        # Convert notebook
        convert_to_markdown_with_template(
            notebook_path, output_file, template_path
        )
        assert os.path.exists(output_file)
        print(f"Test passed: {output_file} created successfully.")
    finally:
        # Cleanup test directory
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
