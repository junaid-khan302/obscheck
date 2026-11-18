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
    table.to_csv(output_path, index=False, encoding="utf-8-sig")
    return table
    
from openpyxl.styles import Font, PatternFill


def export_excel(conn, file_id, output_path):
    """Write all lines of one checked file to a colour-coded .xlsx report."""
    query = (
        "SELECT line_number, raw_text, status, messages "
        "FROM observations WHERE file_id = ? ORDER BY line_number"
    )
    table = pd.read_sql_query(query, conn, params=(file_id,))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        table.to_excel(writer, index=False, sheet_name="Report")
        sheet = writer.sheets["Report"]

        for cell in sheet[1]:
            cell.font = Font(bold=True)

        colours = {"Valid": "C6EFCE", "Warning": "FFEB9C", "Error": "FFC7CE"}
        for row in range(2, sheet.max_row + 1):
            status_cell = sheet.cell(row=row, column=3)
            colour = colours.get(status_cell.value)
            if colour:
                status_cell.fill = PatternFill("solid", start_color=colour, end_color=colour)

        for column, width in {"A": 12, "B": 35, "C": 10, "D": 45}.items():
            sheet.column_dimensions[column].width = width
    return table