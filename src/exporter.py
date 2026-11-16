import sqlite3
from pathlib import Path

import pandas as pd


def export_csv(conn, file_id, output_path):
    """Write all lines of one checked file to a CSV report."""
    query = (
        "SELECT line_number, raw_text, status, messages "
        "FROM observations WHERE file_id = ? ORDER BY line_number"
    )
    table = pd.read_sql_query(query, conn, params=(file_id,))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")
    return table