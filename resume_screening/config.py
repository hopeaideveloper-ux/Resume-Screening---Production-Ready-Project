
"""Load settings from the .env file."""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent


def load_config():
    load_dotenv(BASE_DIR / ".env")
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise ValueError("Add OPENAI_API_KEY to your .env file.")

    def path_setting(name, default):
        path = Path(os.getenv(name, default)).expanduser()
        return path if path.is_absolute() else BASE_DIR / path

    config = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "resumes_dir": path_setting("RESUMES_DIR", "resumes"),
        "job_pdf": path_setting(
            "JOB_DESCRIPTION_PDF",
            "job_description/job_description.pdf"
        ),
        "output_csv": path_setting(
            "OUTPUT_CSV",
            "output/resume_screening_results.csv"
        ),
        "error_csv": path_setting(
            "ERROR_REPORT_CSV",
            "output/resume_screening_errors.csv"
        ),
    }

    config["client"] = OpenAI(api_key=key)

    return config
