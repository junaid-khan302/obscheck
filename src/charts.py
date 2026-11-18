from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # draw to a file, no window needed
import matplotlib.pyplot as plt


def make_status_chart(table, output_path, title="Validation results"):
    """Draw a bar chart of Valid / Warning / Error counts and save it as PNG."""
    order = ["Valid", "Warning", "Error"]
    counts = table["status"].value_counts()
    values = [int(counts.get(status, 0)) for status in order]
    colours = ["#4CAF50", "#FFC107", "#F44336"]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(order, values, color=colours)
    ax.bar_label(bars)
    ax.set_ylabel("Number of lines")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)