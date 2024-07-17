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

### Features

- Plotly visualizations are now saved as static PNG snapshots using `plotly.io.write_image`.
- **Detailed Logging**: Logs all major actions and errors during notebook conversion, uploads, and rendering.
  - Logs are stored in `notebookify.log`.
- **Automatic Folder Cleanup**: Ensures temporary files and folders are cleaned up after processing.
- **Modular Folder Management**: Handles folder creation and resource management efficiently for batch processing.
- **Batch Processing**: Convert and upload multiple notebooks in a single execution, streamlining the workflow for large-scale projects.
- **Enhanced Output Formatting**: The Jinja2 templates now handle Markdown, code, text streams, and static images with appropriate formatting.

### Known Issues

- If `kaleido` is not installed, Plotly snapshots may not work. Install it with `pip install -U kaleido`.

### Known Issues with Large Notebooks

- **Interactive Visualizations**: Some Plotly and widget outputs are not fully rendered.
- **Conversion Time**: Processing large notebooks can take several minutes.
- **Missing Outputs**: Certain edge-case outputs may not appear due to Jinja2 or nbconvert limitations.

### Colab-Specific Rendering Quirks

While testing Markdown outputs in Google Colab, the following issues were identified:

1. **Inline Images**:
   - Markdown rendering in Colab often fails for inline images using `data:image/png;base64`.
   - Temporary Solution: Save images as separate files and link them using relative paths.

2. **Interactive Outputs (Plotly)**:
   - Interactive outputs like Plotly are not supported directly in Colab Markdown.
   - Temporary Solution: Export Plotly visualizations as static images and include links or snapshots in the Markdown.

3. **Text Wrapping**:
   - Long lines of text in code cells may not wrap properly, causing layout issues.
   - Temporary Solution: Use `pre-wrap` CSS styling for better handling.

### Future Improvements

- Explore rendering workarounds using custom Colab scripts or external Markdown previewers.
- Investigate using nbconvert extensions for enhanced compatibility.
