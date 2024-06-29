### Day 2: Basic nbconvert Demonstration

This script demonstrates the use of `nbconvert` to convert a Jupyter notebook into a Markdown file. While functional for simple notebooks, it highlights key limitations:

- Interactive outputs (e.g., Plotly) are not preserved.
- Embedded images or large outputs may not render correctly.

These findings motivated the development of Notebookify to address such challenges.

### Day 3: Git LFS Exploration

Git LFS was explored as a potential solution for handling large notebooks in this project. However, it was deemed unsuitable due to:

- Rapid quota consumption caused by frequent updates.
- Lack of support for interactive outputs.
- Increased complexity in collaboration.

For more details, see [`Git_LFS_Findings.md`](Git_LFS_Findings.md).

### Day 4: Google Drive API Integration

Integrated Google Drive API to simplify file sharing for large notebooks. The initial script includes:

- Authentication using Google Drive API.
- File upload functionality to a specified folder.

To test the integration:

1. Install the required dependencies: `pip install -r requirements.txt`.
2. Run `google_drive_integration.py` to authenticate and upload a file to your Drive.
