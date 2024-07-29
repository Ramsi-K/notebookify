#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install Python3 to run this script."
    exit 1
fi

# Check for required arguments
if [ $# -lt 2 ]; then
    echo "Usage: convert.sh [notebook_path] [output_dir]"
    exit 1
fi

NOTEBOOK_PATH="$1"
OUTPUT_DIR="$2"

# Run the Markdown conversion
if python3 markdown_converter.py "$NOTEBOOK_PATH" "$OUTPUT_DIR"; then
    echo "Conversion successful."
else
    echo "Conversion failed."
    exit 1
fi
