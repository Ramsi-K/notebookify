# Notebookify: Current Features

- Convert Jupyter Notebooks to Markdown format using `convert_to_markdown.py`.
- Basic handling for text and plots.
- Simplifies sharing via Markdown while retaining the ability to regenerate outputs if required.

## Rebranding to Notebookify

Notebookify is the next evolution of the initial convert_to_markdown.py script. What started as a simple tool to convert Jupyter notebooks into Markdown files has grown into a more comprehensive and modular project.

### Key Changes

- **Project Name:** The tool has been rebranded to Notebookify to reflect its broader scope and purpose.
- Modular Design: The codebase has been refactored into a structured package to improve scalability and maintainability.
- Folder Cleanup Logic: Added functionality to manage and delete temporary folders, ensuring efficient resource handling.
- End-to-End Workflow: Initial end-to-end tests for converting, managing, and cleaning outputs have been implemented.

## Why Notebookify?

The project’s new name represents its goal: to simplify and streamline the process of converting, managing, and sharing notebooks in a flexible and user-friendly manner. Whether for Markdown conversion, cloud integration, or custom templates, Notebookify is designed to adapt to diverse workflows.

### New Feature

- Plotly visualizations are now saved as static PNG snapshots using `plotly.io.write_image`.
- **Detailed Logging**: Logs all major actions and errors during notebook conversion, uploads, and rendering.
  - Logs are stored in `notebookify.log`.

### Known Issues

- If `kaleido` is not installed, Plotly snapshots may not work. Install it with `pip install -U kaleido`.


