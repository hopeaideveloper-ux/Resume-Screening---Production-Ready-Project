import csv
from unittest.mock import Mock

import pytest

from ranking import rank_candidates
from utils import save_results


def test_ranking_and_tie_break():
    candidates = [
        {"Name": "Zoe", "Source Filename": "z.pdf",
         "Score Breakdown": {"total": 90}},
        {"Name": "alice", "Source Filename": "a.pdf",
         "Score Breakdown": {"total": 90}},
    ]
    ranked = rank_candidates(candidates)
    assert [item["Name"] for item in ranked] == ["alice", "Zoe"]
    assert [item["Ranking"] for item in ranked] == [1, 2]


def test_csv_and_error_report(tmp_path):
    config = {
        "output_csv": tmp_path / "results.csv",
        "error_csv": tmp_path / "errors.csv",
    }
    save_results([{
        "Name": "Asha", "Phone": "0123", "Skills": ["Python", "SQL"],
        "Match Score": 80, "Ranking": 1,
    }], [{"Filename": "bad.pdf", "Failure Reason": "Invalid PDF"}], config)

    assert config["output_csv"].read_bytes().startswith(b"\\xef\\xbb\\xbf")
    with config["output_csv"].open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        assert reader.fieldnames == [
            "Name", "Email", "Phone", "Skills", "Education",
            "Location", "Experience", "Match Score", "Ranking",
        ]
        row = next(reader)
        assert row["Phone"] == "'0123"
        assert row["Skills"] == "Python; SQL"

    with config["error_csv"].open(encoding="utf-8-sig", newline="") as file:
        assert next(csv.DictReader(file))["Filename"] == "bad.pdf"
