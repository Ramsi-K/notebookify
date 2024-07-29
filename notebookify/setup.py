from setuptools import setup, find_packages

setup(
    name="notebookify",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,  # Ensures static files like templates are included
    install_requires=[
        "nbconvert",
        "nbformat",
        "jinja2",
        "plotly",
        "selenium",
    ],
    package_data={
        "": ["../templates/*.jinja2"],  # Ensure templates are included
    },
    entry_points={
        "console_scripts": [
            "notebookify=src.markdown_converter:main",  # Example CLI entry point
        ]
    },
)
