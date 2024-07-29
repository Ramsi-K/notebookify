import os
from notebookify.src.markdown_converter import MarkdownConverter


def test_conversion():
    converter = MarkdownConverter(template_dir="templates/")
    converter.convert("example_notebook.ipynb", "output.md", "template.jinja2")
    assert os.path.exists("output.md"), "Markdown file was not created!"


def test_cleanup():
    temp_folder = "temp_test/"
    os.makedirs(temp_folder, exist_ok=True)
    MarkdownConverter.cleanup_folder(temp_folder)
    assert not os.path.exists(temp_folder), "Temporary folder was not deleted!"


if __name__ == "__main__":
    test_conversion()
    test_cleanup()
    print("All tests passed!")
