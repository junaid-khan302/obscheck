from pathlib import Path
from charset_normalizer import from_bytes


def read_lines(file_path):
    """Read a text file and return (encoding, list_of_lines)."""
    raw = Path(file_path).read_bytes()

    if not raw:
        return "utf-8", []

    best_guess = from_bytes(raw).best()
    if best_guess is None:
        raise ValueError(f"Could not detect encoding of {file_path}")

    text = str(best_guess)
    return best_guess.encoding, text.splitlines()


if __name__ == "__main__":
    encoding, lines = read_lines("data/sample_valid.txt")
    print(f"Detected encoding: {encoding}")
    print(f"Number of lines: {len(lines)}")
    for number, line in enumerate(lines, start=1):
        print(f"{number}: {line}")