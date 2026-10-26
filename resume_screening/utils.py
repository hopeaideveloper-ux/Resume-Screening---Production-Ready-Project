"""Small helper functions for validation, logging, and CSV output."""
import csv
import logging
from pathlib import Path

COLUMNS = [
    "Name", "Email", "Phone", "Skills", "Education",
    "Location", "Experience", "Match Score", "Ranking",
]


def log_errors(error):
    logging.basicConfig(level=logging.ERROR)
    logging.exception("Resume screening stopped: %s", type(error).__name__)


def validate_inputs(config):
    if not config["resumes_dir"].is_dir():
        raise FileNotFoundError(f"Resume folder not found: {config['resumes_dir']}")
    if not config["job_pdf"].is_file():
        raise FileNotFoundError(f"Job PDF not found: {config['job_pdf']}")
    config["output_csv"].parent.mkdir(parents=True, exist_ok=True)
    config["error_csv"].parent.mkdir(parents=True, exist_ok=True)


def find_resumes(folder):
    return sorted(
        (path for path in folder.iterdir()
         if path.is_file() and path.suffix.lower() == ".pdf"),
        key=lambda path: path.name.casefold(),
    )


def csv_value(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def save_results(candidates, errors, config):
    with config["output_csv"].open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        for candidate in candidates:
            row = {column: csv_value(candidate.get(column, "")) for column in COLUMNS}
            if row["Phone"]:
                row["Phone"] = "'" + row["Phone"].lstrip("'")
            writer.writerow(row)

    with config["error_csv"].open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["Filename", "Failure Reason"])
        writer.writeheader()
        writer.writerows(errors)
