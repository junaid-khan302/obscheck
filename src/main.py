import argparse

from reader import read_lines
from validator import validate_line
from database import connect, save_results
from exporter import export_csv, export_excel

def main():
    parser = argparse.ArgumentParser(
        description="Validate a classroom observation text file."
    )
    parser.add_argument("file", help="path to the .txt file to check")
    parser.add_argument(
        "--out", default="output/report.csv", help="where to write the CSV report"
    )
    parser.add_argument(
        "--xlsx", default="output/report.xlsx", help="where to write the Excel report"
    )
    args = parser.parse_args()

    encoding, lines = read_lines(args.file)

    results = []
    for number, line in enumerate(lines, start=1):
        results.append((number, line, validate_line(line)))

    conn = connect()
    file_id = save_results(conn, args.file, encoding, results)
    table = export_csv(conn, file_id, args.out)
    export_excel(conn, file_id, args.xlsx)
    conn.close()

    counts = table["status"].value_counts()
    print(f"File: {args.file} (encoding: {encoding})")
    print(f"Lines checked: {len(table)}")
    for status in ["Valid", "Warning", "Error"]:
        print(f"  {status}: {counts.get(status, 0)}")
    print(f"Report saved to {args.out}")
    print(f"Excel report saved to {args.xlsx}")


if __name__ == "__main__":
    main()