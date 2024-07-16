import nbformat
from jinja2 import Environment, FileSystemLoader
import os
import logging
import plotly.io as pio


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
                if cell["cell_type"] == "code" and "outputs" in cell:
                    for output in cell["outputs"]:
                        if "application/vnd.plotly.v1+json" in output.get(
                            "data", {}
                        ):
                            self.logger.info(
                                "Found Plotly visualization. Saving snapshot."
                            )
                            plotly_data = output["data"][
                                "application/vnd.plotly.v1+json"
                            ]
                            snapshot_path = self.save_plotly_snapshot(
                                plotly_data,
                                os.path.dirname(output_path),
                                f"{os.path.basename(output_path).replace('.md', '')}_plotly.png",
                            )
                            output["plotly_snapshot"] = snapshot_path

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
