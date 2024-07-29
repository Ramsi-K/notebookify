# Notebookify

Notebookify is a Python tool that converts Jupyter notebooks into shareable Markdown files, featuring template-based customization and seamless integration with Google Drive.

## Features

- Converts Jupyter notebooks to Markdown with support for custom templates.
- Google Drive integration for quick sharing of outputs.
- Batch processing for multiple notebooks.
- Modular design for easier maintenance and extensibility.

## Current Repository Structure

The project is being actively reorganized to improve clarity and functionality. Here’s the current structure:

```
Notebookify/
├── src/                            # Source code for Notebookify
│   ├── __init__.py                 # Makes this a package
│   ├── markdown_converter.py       # Core Markdown conversion logic
│   ├── utils.py                    # Utility functions
│   ├── drive_metadata.py           # Google Drive file handling
│   ├── credentials.json            # Google API credentials (ignored in git)
│   ├── token.json                  # OAuth token for Google Drive (ignored in git)
├── templates/                      # Templates for Markdown rendering
│   └── index.md.j2                 # Jinja2 template for Markdown conversion
├── setup/                          # Setup and execution scripts
│   ├── notebookify.bat             # Windows batch script
│   ├── notebookify.sh              # Linux/macOS shell script
├── examples/                       # Sample notebooks and expected outputs
│   ├── sample_notebook.ipynb       # Example notebook for testing
│   ├── expected_output.md          # Expected Markdown output
├── docs/                           # Documentation
│   ├── GIT_LFS_Findings.md         # Documentation on Git LFS
│   ├── README.md                   # Project documentation
├── tests/                          # Unit tests
│   ├── test_markdown_converter.py  # Tests for markdown conversion
│   ├── test_utils.py               # Tests for utility functions
├── requirements.txt                # Python dependencies
├── environment.yml                 # Conda environment configuration
├── setup.py                        # Installation script
├── .gitignore                      # Ignored files
```

## Today’s Updates

1. **Repository Structure**:
   - Reorganized the repository to separate source code, templates, and documentation.
   - Introduced a `src/` directory for all Python scripts.
   - Moved `templates/` outside `src/` to separate static assets.

2. **README Alignment**:
   - Updated the README to reflect the reorganized structure.
   - Added placeholders for upcoming updates.

## Known Issues

- Some interactive visualizations and unsupported MIME types are still under review.
- Batch processing performance optimizations are ongoing.

## Next Steps

- Integrate features like `drive_metadata.py` and finalize folder handling logic.
- Expand README to include detailed usage examples for the reorganized structure.
- Test end-to-end functionality after all components are in place.

## Get Started

1. Clone the repository:

   ```
   git clone https://github.com/Ramsi-K/notebookify.git
   cd notebookify
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Convert a notebook:

   ```
   python src/markdown_converter.py --input examples/sample_notebook.ipynb --output examples/expected_output.md
   ```
