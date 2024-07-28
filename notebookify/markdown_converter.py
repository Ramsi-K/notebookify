import nbformat
from jinja2 import Environment, FileSystemLoader
import os
import logging
import plotly.io as pio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import nbconvert
import shutil
from google_drive_uploader import upload_to_google_drive

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MarkdownConverter:
    def __init__(self, template_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.logger = logging.getLogger(__name__)

    def convert(
        self, notebook_path, output_path, template_name="template.jinja2"
    ):
        try:
            self.logger.info(f"Converting notebook: {notebook_path}")
            with open(notebook_path, "r") as f:
                notebook = nbformat.read(f, as_version=4)

            # Process Plotly outputs and save snapshots
            for cell in notebook["cells"]:
                if "outputs" in cell:
                    for output in cell["outputs"]:
                        try:
                            if output["output_type"] == "execute_result":
                                if "text/plain" in output.data:
                                    processed_output = output.data[
                                        "text/plain"
                                    ]
                                elif "image/png" in output.data:
                                    processed_output = f"![Image](data:image/png;base64,{output.data['image/png']})"
                                elif (
                                    "application/vnd.plotly.v1+json"
                                    in output.data
                                ):
                                    # Handle Plotly outputs
                                    processed_output = self.save_plotly_snapshot(
                                        output["data"][
                                            "application/vnd.plotly.v1+json"
                                        ],
                                        output_dir=os.path.dirname(
                                            output_path
                                        ),
                                    )
                                else:
                                    # Unsupported output
                                    processed_output = (
                                        handle_unsupported_output(output)
                                    )
                            else:
                                # Skip non-execute outputs for now
                                processed_output = handle_unsupported_output(
                                    output
                                )

                            # Write the processed_output to the Markdown file here
                        except Exception as e:
                            logger.error(f"Error processing output: {e}")
                            processed_output = handle_unsupported_output(
                                output
                            )

            template = self.env.get_template(template_name)
            markdown_output = template.render(
                cells=notebook["cells"],
                notebook_name=os.path.basename(notebook_path),
            )

            with open(output_path, "w") as f:
                f.write(markdown_output)

            self.logger.info(
                f"Conversion complete. Output saved to: {output_path}"
            )
        except Exception as e:
            self.logger.error(f"Error converting notebook: {e}")

    @staticmethod
    def save_plotly_snapshot(
        plotly_data, output_dir, filename="plotly_snapshot.png"
    ):
        """
        Save Plotly visualizations as static images.
        """
        try:
            fig = pio.from_json(plotly_data)
            snapshot_path = os.path.join(output_dir, filename)
            logger.info(f"Saved Plotly snapshot to {snapshot_path}")
            return snapshot_path
        except Exception as e:
            logger.error(f"Error saving Plotly snapshot: {e}")
            placeholder_path = os.path.join(
                output_dir, "plotly_snapshot_error.md"
            )
            with open(placeholder_path, "w") as f:
                f.write(f"# Plotly Snapshot Error\n\nError: {e}")
            return placeholder_path

    @staticmethod
    def cleanup_folder(folder_path):
        """
        Remove a folder and its contents if it exists.
        Ensures cleanup happens after all processing is completed.
        """
        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                logger.info(f"Successfully cleaned up folder: {folder_path}")
            else:
                logger.warning(
                    f"Folder does not exist and cannot be cleaned: {folder_path}"
                )
        except Exception as e:
            logger.error(f"Error during folder cleanup: {e}")


def capture_iframe_snapshot(url, output_path):
    """
    Capture a snapshot of an iframe from a given URL using Selenium.

    Args:
        url (str): The URL containing the iframe.
        output_path (str): Path to save the snapshot image.

    Returns:
        None
    """
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        service = Service(
            "path/to/chromedriver"
        )  # Update with the path to chromedriver

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(3)  # Wait for the iframe to load

        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        driver.save_screenshot(output_path)
        print(f"Snapshot saved to {output_path}")

        driver.quit()
    except Exception as e:
        print(f"Error capturing iframe snapshot: {e}")


def handle_unsupported_output(output):
    """
    Logs unsupported output types and skips processing.
    """
    logger.warning(f"Unsupported output type encountered: {output}")
    # Optionally write a placeholder message to the Markdown output
    return f"<!-- Unsupported output type: {output} -->"


def safe_create_folder(folder_path):
    """
    Ensures the folder exists, creating it if necessary. Logs the action.
    """
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.info(f"Created folder: {folder_path}")
        else:
            logger.info(f"Folder already exists: {folder_path}")
    except Exception as e:
        logger.error(f"Error creating folder {folder_path}: {e}")
        raise


def convert_notebook_to_markdown(notebook_path, output_dir):
    """
    Converts a notebook file to a Markdown file and saves it to the output directory.
    """
    logger.info(f"Starting Markdown conversion for {notebook_path}")
    safe_create_folder(output_dir)

    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        exporter = nbconvert.MarkdownExporter()
        body, _ = exporter.from_notebook_node(notebook)

        output_file = os.path.join(
            output_dir,
            os.path.basename(notebook_path).replace(".ipynb", ".md"),
        )
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(body)

        logger.info(f"Markdown file saved to: {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Error during Markdown conversion: {e}")
        raise


def process_batch_notebooks(notebook_paths, output_dir, service):
    """
    Converts a batch of notebooks to Markdown and uploads them to Google Drive.
    """
    safe_create_folder(output_dir)
    logger.info("Starting batch processing of notebooks.")

    for notebook_path in notebook_paths:
        try:
            logger.info(f"Processing notebook: {notebook_path}")
            markdown_file = convert_notebook_to_markdown(
                notebook_path, output_dir
            )
            if service:
                upload_to_google_drive(service, markdown_file)
        except Exception as e:
            logger.error(f"Error processing notebook {notebook_path}: {e}")
            continue

    logger.info("Batch processing completed.")


def convert_to_markdown_with_template(
    notebook_path, output_path, template_path
):
    """
    Converts a notebook to Markdown using a Jinja2 template and processes outputs.
    """
    try:
        # Load the notebook
        with open(notebook_path, "r") as f:
            notebook = nbformat.read(f, as_version=4)

        # Load Jinja2 environment and template
        env = Environment(loader=FileSystemLoader("/path/to/templates"))
        template = env.get_template(template_path)

        # Process outputs for rendering
        for cell in notebook["cells"]:
            if "outputs" in cell:
                for output in cell["outputs"]:
                    # Handle image/png outputs (base64 encoding)
                    if "image/png" in output.get("data", {}):
                        logger.info(
                            f"Encoding image/png for cell in {notebook_path}"
                        )
                        output["data"]["image/png"] = output["data"][
                            "image/png"
                        ].replace("\n", "")

        # Render Markdown
        markdown_output = template.render(cells=notebook["cells"])

        # Save output
        with open(output_path, "w") as f:
            f.write(markdown_output)

        logger.info(f"Converted notebook saved to {output_path}")
    except Exception as e:
        logger.error(f"Error during Markdown conversion: {e}")
        raise

    # Save to output path
    with open(output_path, "w") as f:
        f.write(markdown_output)
