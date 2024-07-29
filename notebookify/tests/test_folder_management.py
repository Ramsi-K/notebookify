import os
import pytest
from notebookify.src.markdown_converter import (
    ensure_folder_exists,
    MarkdownConverter,
)


def test_ensure_folder_exists():
    test_folder = "test_outputs"
    try:
        # Test folder creation
        ensure_folder_exists(test_folder)
        assert os.path.exists(test_folder)
    finally:
        # Cleanup
        if os.path.exists(test_folder):
            os.rmdir(test_folder)


def test_cleanup_folder():
    test_folder = "test_cleanup"
    os.makedirs(test_folder, exist_ok=True)
    assert os.path.exists(test_folder)

    # Test cleanup
    MarkdownConverter.cleanup_folder(test_folder)
    assert not os.path.exists(test_folder)
