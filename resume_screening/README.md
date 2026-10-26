# Resume Screening System

A simple Python terminal project that reads resume PDFs, extracts
candidate details with an LLM, compares each resume with a job
description, scores candidates out of 100, ranks them, and exports CSV
files.

## Folder structure

``` text
resume_screening/
├── app.py
├── config.py
├── resume_parser.py
├── matching.py
├── ranking.py
├── utils.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── resumes/
├── job_description/
├── output/
└── tests/
    └── test_resume_screening.py
```

## How it works

``` text
Resume PDFs + Job Description PDF
             |
             v
       Extract PDF text
             |
             v
   LLM extracts candidate details
             |
             v
     LLM scores job-related fit
             |
             v
       Rank candidates
             |
        +----+----+
        |         |
        v         v
    Results CSV  Error CSV
```

## Setup in Windows and VS Code

1.  Extract the ZIP and open its folder in VS Code.

2.  Open Terminal \> New Terminal.

3.  Create a virtual environment:

    ``` powershell
    py -3.11 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

    For Command Prompt, use `.venv\Scripts\activate.bat` after creating
    the environment.

4.  Install packages:

    ``` bash
    pip install -r requirements.txt
    ```

5.  Copy `.env.example` to `.env`:

    ``` powershell
    Copy-Item .env.example .env
    ```

6.  Put your API key in `.env`. Never share this file.

7.  Put resume PDFs in `resumes/`.

8.  Put the job description at `job_description/job_description.pdf`.

9.  Run:

    ``` bash
    python app.py
    ```

10. Check `output/resume_screening_results.csv` and
    `output/resume_screening_errors.csv`.

## Scoring

  Category                           Maximum points
  -------------------------------- ----------------
  Relevant skills                                40
  Relevant experience                            30
  Education and qualifications                   20
  Other job-related requirements                 10
  Total                                         100

Candidates are sorted by score, then alphabetically by name
(case-insensitive), then by source filename. Scores support human
review; they must not be used as the sole basis for hiring decisions.

## CSV columns

`Name, Email, Phone, Skills, Education, Location, Experience, Match Score, Ranking`

Lists are separated with semicolons. Phone numbers are prefixed with an
apostrophe so Excel preserves leading zeros. Missing details are blank.
Failed resumes are not scored or ranked.

## Limitations and troubleshooting

-   Scanned PDFs are not supported; OCR is not included. Use searchable
    PDFs.
-   Password-protected or encrypted PDFs may fail during text extraction
    if they require a password.
-   Resume and job-description text has no custom character limit; very
    long documents may increase API usage and cost.
-   The configured model must support structured JSON Schema responses.
-   API usage may cost money. Resume text is sent to your configured
    provider.
-   If a resume fails, its filename and reason are written to the error
    CSV and other resumes continue.
-   If the API key is missing, add it to `.env`.
-   If a package is missing, activate `.venv` and run
    `pip install -r requirements.txt`.

## Tests

Run:

``` bash
python -m pytest -v
```

The included tests cover ranking tie-breaks and CSV/error output. They
do not test a live API call. Run the project with your own API key and
sample PDFs to verify the full workflow.
