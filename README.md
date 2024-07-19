# Notebookify

Notebookify is a Python tool that converts Jupyter notebooks into shareable Markdown files with enhanced support for visualizations, templates, and cloud uploads.

## Features

- Converts Jupyter notebooks to Markdown using `nbconvert` or custom templates.
- Supports embedding images and interactive Plotly visualizations.
- Google Drive integration for seamless file sharing.
- Batch processing for multiple notebooks.
- Experimental Selenium support for iframe snapshot rendering.
- Plotly visualizations saved as static PNG snapshots using `plotly.io.write_image`.
- Detailed logging of all actions and errors stored in `notebookify.log`.

## Challenges Faced

1. **Handling Large Outputs**:
   - Large outputs in notebooks caused rendering and upload issues.
2. **Interactive Content**:
   - Plotly and iframe visualizations required custom handling to generate static snapshots.
3. **Dynamic Paths**:
   - Debugging path inconsistencies for local files and Google Drive uploads consumed significant time.

## Lessons Learned

1. **Iterative Development**:
   - Breaking the project into small, testable components reduced complexity.
2. **Importance of Logging**:
   - Adding detailed logs improved debugging efficiency.
3. **Flexibility in Tools**:
   - Experimenting with libraries helped identify the best solutions.

## Known Issues

1. **Interactive Outputs**:
   - Plotly and widget outputs are not fully rendered in Markdown.
2. **Conversion Time**:
   - Processing large notebooks can be slow.
3. **Colab-Specific Rendering Quirks**:
   - Inline images fail, interactive outputs are unsupported, and text wrapping issues occur.

## Future Plans

- **Enhanced Visualization Support**:
  - Explore better handling for Plotly and other 3D visualizations.
- **Cloud Integration**:
  - Add support for AWS S3 and Dropbox.
- **Improved Batch Processing**:
  - Optimize batch processing logic for large-scale notebook management.

## Selenium Setup

### Steps

1. Install Selenium:

   ```
   pip install selenium
   ```

2. Download ChromeDriver:
   - Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads).
3. Update Path:
   - Place the `chromedriver` binary in your PATH or specify its location in the script.

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
   python markdown_converter.py --input example_notebook.ipynb --output markdown_outputs/
   ```
