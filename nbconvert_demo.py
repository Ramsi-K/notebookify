import os
from nbconvert import MarkdownExporter
import nbformat

def convert_notebook_to_markdown(notebook_path):
    """Converts a Jupyter notebook to a Markdown file."""
    if not os.path.exists(notebook_path):
        print(f"Error: File {notebook_path} does not exist.")
        return

    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    # Export to Markdown
    exporter = MarkdownExporter()
    markdown_output, _ = exporter.from_notebook_node(notebook_content)

    # Save the Markdown file
    markdown_file_path = os.path.splitext(notebook_path)[0] + ".md"
    with open(markdown_file_path, 'w', encoding='utf-8') as markdown_file:
        markdown_file.write(markdown_output)

    print(f"Markdown file saved at: {markdown_file_path}")

if __name__ == "__main__":
    notebook_path = input("Enter the path to the notebook: ").strip()
    convert_notebook_to_markdown(notebook_path)
