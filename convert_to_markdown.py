import os
from nbconvert import MarkdownExporter
import subprocess


def convert_notebook_to_markdown(notebook_path):
    if not os.path.exists(notebook_path):
        print(f"Error: Notebook {notebook_path} does not exist.")
        return None

    output_file = notebook_path.replace(".ipynb", ".md")
    try:
        subprocess.run(
            ["jupyter", "nbconvert", "--to", "markdown", notebook_path],
            check=True,
        )
        print(f"Converted {notebook_path} to {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error converting {notebook_path} to Markdown: {e}")
        return None


if __name__ == "__main__":
    notebook_path = input("Enter the path to the notebook: ").strip()
    convert_notebook_to_markdown(notebook_path)
