
"""PDF text extraction and candidate detail extraction."""

import json
from pypdf import PdfReader


def extract_pdf_text(pdf_path):
    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()


def ask_llm(client, config, system_message, prompt, schema):
    response = client.chat.completions.create(
        model=config["model"],
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": schema["name"],
                "strict": True,
                "schema": schema["schema"],
            },
        },
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The model returned an empty response.")

    return json.loads(content)


DETAILS_SCHEMA = {
    "name": "candidate_details",
    "schema": {
        "type": "object",
        "properties": {
            "name": {"type": ["string", "null"]},
            "email": {"type": ["string", "null"]},
            "phone": {"type": ["string", "null"]},
            "skills": {
                "type": "array",
                "items": {"type": "string"},
            },
            "education": {
                "type": "array",
                "items": {"type": "string"},
            },
            "location": {"type": ["string", "null"]},
            "experience": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": [
            "name",
            "email",
            "phone",
            "skills",
            "education",
            "location",
            "experience",
        ],
        "additionalProperties": False,
    },
}


def extract_candidate_details(text, config):
    prompt = (
        "Extract only facts explicitly stated in the resume. Do not guess. "
        "Use null for missing single values and [] for missing lists. "
        "Ignore protected or irrelevant personal characteristics such as "
        "age, gender, religion, caste, disability, and marital status.\n\n"
        "RESUME:\n" + text
    )

    data = ask_llm(
        config["client"],
        config,
        "Extract resume details accurately. Never invent missing information.",
        prompt,
        DETAILS_SCHEMA,
    )

    return {
        "Name": data.get("name") or "",
        "Email": data.get("email") or "",
        "Phone": data.get("phone") or "",
        "Skills": data.get("skills") or [],
        "Education": data.get("education") or [],
        "Location": data.get("location") or "",
        "Experience": data.get("experience") or [],
    }
