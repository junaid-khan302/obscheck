import re
from datetime import datetime

from reader import read_lines

ALLOWED_ACTIVITIES = ["Passive", "Active", "Constructive", "Interactive"]


def is_valid_time(text):
    """Return True if text is a real time like 09:00:05."""
    if not re.fullmatch(r"\d{2}:\d{2}:\d{2}", text):
        return False
    try:
        datetime.strptime(text, "%H:%M:%S")
        return True
    except ValueError:
        return False


def validate_line(line):
    """Check one line and return a dict with its status and messages."""
    errors = []
    warnings = []

    parts = line.split(";")

    if len(parts) == 3:
        parts.append("")  # observer missing: add an empty one
    elif len(parts) != 4:
        return {
            "status": "Error",
            "messages": [f"Expected 4 fields, found {len(parts)}"],
        }

    cleaned = [part.strip() for part in parts]
    if cleaned != parts:
        warnings.append("Extra spaces removed")

    time_text, student, activity, observer = cleaned

    if not is_valid_time(time_text):
        errors.append(f"Invalid time: '{time_text}'")

    if student == "":
        errors.append("Student ID is empty")
    elif not re.fullmatch(r"S\d+", student):
        errors.append(f"Student ID looks wrong: '{student}'")

    matched = None
    for allowed in ALLOWED_ACTIVITIES:
        if activity.lower() == allowed.lower():
            matched = allowed
    if matched is None:
        errors.append(f"Unknown activity: '{activity}'")
    elif matched != activity:
        warnings.append(f"Capitalisation fixed: '{activity}' -> '{matched}'")

    if observer == "":
        warnings.append("Observer is missing")

    if errors:
        status = "Error"
    elif warnings:
        status = "Warning"
    else:
        status = "Valid"

    return {"status": status, "messages": errors + warnings}


if __name__ == "__main__":
    encoding, lines = read_lines("data/sample_messy.txt")
    counts = {"Valid": 0, "Warning": 0, "Error": 0}

    for number, line in enumerate(lines, start=1):
        result = validate_line(line)
        counts[result["status"]] += 1
        print(f"Line {number}: {result['status']} {result['messages']}")

    print()
    print(counts)