
"""Calculate job match scores using a fixed rubric."""

from resume_parser import ask_llm

SCORE_SCHEMA = {
    "name": "match_scores",
    "schema": {
        "type": "object",
        "properties": {
            "skills": {"type": "integer", "minimum": 0, "maximum": 40},
            "experience": {"type": "integer", "minimum": 0, "maximum": 30},
            "education": {"type": "integer", "minimum": 0, "maximum": 20},
            "other": {"type": "integer", "minimum": 0, "maximum": 10},
            "evidence": {
                "type": "array",
                "items": {"type": "string"}
            },
        },
        "required": [
            "skills", "experience", "education", "other", "evidence"
        ],
        "additionalProperties": False,
    },
}


def score_candidate(resume, job, config):
    prompt = f"""
Compare the resume with the job description using only written evidence.
Score relevant skills out of 40, experience out of 30, education out of 20,
and other explicit job requirements out of 10. Do not double-count evidence.
Do not use protected or irrelevant personal characteristics. Do not guess.
Give short reasons in the evidence list. Scores are for human review only.

JOB DESCRIPTION:
{job}

RESUME:
{resume}
"""

    result = ask_llm(
        config["client"],
        config,
        "You compare resumes carefully and only use job-related evidence.",
        prompt,
        SCORE_SCHEMA,
    )

    result["total"] = (
        result["skills"]
        + result["experience"]
        + result["education"]
        + result["other"]
    )

    return result
