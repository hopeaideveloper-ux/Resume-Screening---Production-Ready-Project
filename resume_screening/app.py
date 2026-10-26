"""Start the resume screening program."""
from config import load_config
from resume_parser import extract_pdf_text, extract_candidate_details
from matching import score_candidate
from ranking import rank_candidates
from utils import log_errors, validate_inputs, find_resumes, save_results


def main():
    config = load_config()
    validate_inputs(config)

    job_text = extract_pdf_text(config["job_pdf"])
    if not job_text.strip():
        raise ValueError("The job PDF has no readable text. OCR is not included.")

    candidates, errors = [], []

    for pdf in find_resumes(config["resumes_dir"]):
        print(f"Reading {pdf.name}...")
        try:
            resume_text = extract_pdf_text(pdf)
            if not resume_text.strip():
                raise ValueError("No readable text; this may be a scanned PDF.")

            candidate = extract_candidate_details(resume_text, config)
            candidate["Source Filename"] = pdf.name
            candidate["Score Breakdown"] = score_candidate(
                resume_text, job_text, config
            )
            candidates.append(candidate)
        except Exception as error:
            errors.append({"Filename": pdf.name, "Failure Reason": str(error)[:200]})
            print(f"Skipped {pdf.name}: {type(error).__name__}")

    save_results(rank_candidates(candidates), errors, config)
    print(f"Finished: {len(candidates)} successful, {len(errors)} failed.")
    print(f"Results: {config['output_csv']}")
    print(f"Errors: {config['error_csv']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        log_errors(error)
        print(f"Cannot start: {error}")
