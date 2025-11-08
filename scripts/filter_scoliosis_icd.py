#!/usr/bin/env python3
"""Filter diagnoses for scoliosis-related ICD codes and report counts."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ICD10_REGEX = re.compile(r"^M41", re.IGNORECASE)
ICD9_REGEX = re.compile(r"^7373", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Filter diagnoses for scoliosis ICD codes (ICD-9 737.3*, "
            "ICD-10 M41.*) and write matches to an output CSV."
        )
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the diagnoses CSV file (e.g., data/diagnoses_icd.csv).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Destination path for the filtered CSV output.",
    )
    return parser.parse_args()


def icd_matches(code: str, version: str) -> bool:
    """Return True when the ICD code/version pair represents scoliosis."""
    if not code:
        return False

    normalized_code = code.strip().upper()
    version = (version or "").strip()

    if version == "10":
        return bool(ICD10_REGEX.match(normalized_code))

    if version == "9":
        return bool(ICD9_REGEX.match(normalized_code))

    # Unknown version: attempt best-effort match across both patterns.
    return bool(ICD9_REGEX.match(normalized_code) or ICD10_REGEX.match(normalized_code))


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    unique_patients: set[str] = set()

    with input_path.open(newline="", encoding="utf-8") as source, output_path.open(
        "w", newline="", encoding="utf-8"
    ) as destination:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError("Input CSV missing header row.")

        writer = csv.DictWriter(destination, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            code = row.get("icd_code", "")
            version = row.get("icd_version", "")

            if icd_matches(code, version):
                writer.writerow(row)
                total_rows += 1
                subject_id = row.get("subject_id")
                if subject_id:
                    unique_patients.add(subject_id)

    print(
        f"Filtered {total_rows} matching diagnoses spanning "
        f"{len(unique_patients)} unique patients.\n"
        f"Output saved to {output_path}"
    )


if __name__ == "__main__":
    main()
