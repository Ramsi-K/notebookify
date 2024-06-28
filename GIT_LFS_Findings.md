# Git LFS Exploration: Findings and Limitations

## Why Git LFS?

Git Large File Storage (LFS) is a version control solution for large files. Given the size of some Jupyter notebooks in my portfolio, Git LFS was explored as a potential solution to:

- Avoid GitHub's rendering limitations for large notebooks.
- Reduce repository size by separating notebook storage.

## Key Findings

1. **Frequent Updates Cause Bloat**: Jupyter notebooks frequently change due to embedded outputs, leading to rapid Git LFS quota consumption.
2. **Interactive Outputs Are Unsupported**: Git LFS does not address issues with interactive content (e.g., Plotly, HTML).
3. **Complexity in Collaboration**: Collaborators must configure Git LFS locally, adding friction.

## Conclusion

While Git LFS works well for static large files (e.g., videos, datasets), it is unsuitable for Jupyter notebooks with frequent updates and interactive content. A more dynamic solution, such as Notebookify, is needed.
