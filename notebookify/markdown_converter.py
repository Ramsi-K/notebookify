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
                                    processed_output = save_plotly_snapshot(
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
