# Testing Observations and Challenges

### Summary

Testing was conducted on a range of notebooks with varying complexity, including:

- Simple notebooks with plain text and code.
- Notebooks with Plotly visualizations and widgets.
- Large notebooks with extensive outputs.

### Observations

1. **Plotly Visualizations**:
   - Static snapshots worked well for simple plots.
   - Large datasets caused delays during snapshot creation.

2. **Unsupported Outputs**:
   - Widgets and custom MIME types are not rendered. Fallback messages are logged and displayed in Markdown.

3. **Batch Processing**:
   - Conversion works but is slower for large batches due to redundant folder operations.

4. **Colab Rendering**:
   - Markdown outputs displayed inconsistently in Google Colab. Inline images and long text outputs required manual adjustments.

### Next Steps

- Refactor folder management logic to streamline batch processing.
- Investigate better handling of unsupported MIME types.
- Experiment with external Markdown renderers for Colab compatibility.
