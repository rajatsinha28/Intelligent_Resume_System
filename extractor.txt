#!/usr/bin/env python
"""
Resume Extraction Agent (Agent‑1)

Extracts structured data from a resume PDF and outputs a JSON object
ready for consumption by downstream agents.
"""

import os
import re
import json
import sys
from typing import Dict, List, Any, Optional, Tuple

import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI
from openai import APIStatusError, APIConnectionError, RateLimitError, AuthenticationError

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    sys.exit("Error: OPENAI_API_KEY environment variable not set. "
             "Create a .env file or export the variable before running.")
client = OpenAI(api_key=api_key)

# ----------------------------------------------------------------------
# Constants – known resume headings and their canonical types
# ----------------------------------------------------------------------
KNOWN_HEADINGS = [
    "personal information", "contact information", "contact",
    "summary", "professional summary", "profile",
    "skills", "technical skills",
    "experience", "work experience", "employment",
    "projects", "academic projects",
    "education",
    "certifications",
    "achievements", "awards",
    "internships",
    "publications",
    "leadership",
    "extracurricular activities", "positions of responsibility", "volunteering",
    "languages",
    "interests", "hobbies"
]

HEADING_TO_TYPE = {
    "personal information": "personal_information",
    "contact information": "personal_information",
    "contact": "personal_information",
    "summary": "summary",
    "professional summary": "summary",
    "profile": "summary",
    "skills": "skills",
    "technical skills": "skills",
    "experience": "experience",
    "work experience": "experience",
    "employment": "experience",
    "projects": "projects",
    "academic projects": "projects",
    "education": "education",
    "certifications": "certifications",
    "achievements": "achievements",
    "awards": "achievements",
    "internships": "experience",          # treat internships as experience
    "publications": "publications",
    # Leadership, extracurricular, etc. → other_sections
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    """Return plain‑text from all pages of the PDF."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def preprocess_text(text: str) -> str:
    """Normalize whitespace while preserving paragraph breaks."""
    # Collapse horizontal whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    # Collapse multiple blank lines to at most two newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def split_into_sections(text: str) -> List[Tuple[Optional[str], str]]:
    """
    Split the resume text into sections.
    Returns a list of (heading_or_None, section_content).
    The first block (before any known heading) is treated as personal information.
    """
    lines = text.splitlines()
    sections: List[Tuple[Optional[str], str]] = []
    current_heading: Optional[str] = None
    current_content: List[str] = []

    # Pattern matches a known heading (case‑insensitive, optional trailing colon)
    heading_pat = re.compile(
        r'^\s*(' + '|'.join(map(re.escape, KNOWN_HEADINGS)) + r')\s*:?\s*$',
        re.IGNORECASE
    )

    for line in lines:
        if heading_pat.match(line):
            # Flush previous section
            if current_heading is not None or current_content:
                sections.append((current_heading, "\n".join(current_content)))
            current_heading = heading_pat.match(line).group(1).strip()
            current_content = []
        else:
            current_content.append(line)

    # Append the final section
    if current_heading is not None or current_content:
        sections.append((current_heading, "\n".join(current_content)))

    return sections


def map_heading_to_type(heading: Optional[str]) -> Optional[str]:
    """Map a raw heading to the canonical section type."""
    if heading is None:
        return None
    h = heading.lower().strip()
    if h.endswith(':'):
        h = h[:-1]
    return HEADING_TO_TYPE.get(h)


def extract_section_data_with_openai(section_type: str, section_text: str) -> Dict[str, Any]:
    """
    Ask GPT‑3.5‑turbo to extract structured fields for a given section.
    Returns a dict matching the expected structure for that section.
    On any API error, returns an empty structure (so the pipeline can continue).
    """
    prompts = {
        "personal_information": f"""
        Extract the following personal information from the given text:
        - Name
        - Email
        - Phone
        - LinkedIn
        - GitHub
        - Portfolio
        - Website
        - Location

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return JSON with exactly these keys (null if missing):
        name, email, phone, linkedin, github, portfolio, website, location.
        """,

        "summary": f"""
        Extract the professional summary or profile section from the given text.
        Return the summary as a string, or null if none exists.

        Text:
        \"\"\"
        {section_text}
        \"\"\"
        """,

        "skills": f"""
        Extract and categorize skills into these buckets:
        Programming Languages, Frameworks, Databases, Cloud, Tools,
        Libraries, Testing, AI/ML, DevOps, Others.

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return JSON with keys (arrays of strings):
        programming_languages, frameworks, databases, cloud, tools,
        libraries, testing, ai_ml, devops, others.
        Empty array if a category has no entries.
        """,

        "experience": f"""
        Extract all work experiences. For each experience return:
        - Company
        - Role
        - Employment Type (Full‑time, Part‑time, Contract, Internship, …)
        - Location
        - Start Date (YYYY‑MM or MM/YYYY)
        - End Date (YYYY‑MM, MM/YYYY, or "Present")
        - Duration (if present, e.g. "2 years 3 months")
        - Bullet points (array of strings)
        - Technologies Used (array of strings)
        - Achievements (array of strings)

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return JSON: {{ "experience": [ {{ ... }}, ... ] }}
        Return {{"experience": []}} if none found.
        """,

        "projects": f"""
        Extract all projects. For each project return:
        - Title
        - Description
        - Technologies (array of strings)
        - Features (array of strings)
        - Contributions (array of strings)
        - GitHub Link
        - Live Link

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return JSON: {{ "projects": [ {{ ... }}, ... ] }}
        Return {{"projects": []}} if none found.
        """,

        "education": f"""
        Extract all education entries. For each entry return:
        - Degree
        - Branch (e.g., Computer Science)
        - Institution
        - CGPA/Percentage
        - Start Year
        - End Year

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return JSON: {{ "education": [ {{ ... }}, ... ] }}
        Return {{"education": []}} if none found.
        """,

        "certifications": f"""
        Extract all certifications. For each certification return:
        - Name
        - Issuing Organization
        - Year
        - Credential ID (if present)

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return JSON: {{ "certifications": [ {{ ... }}, ... ] }}
        Return {{"certifications": []}} if none found.
        """,

        "achievements": f"""
        Extract all achievements (each as a plain string).

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return JSON: {{ "achievements": [ "…", "…", ... ] }}
        Return {{"achievements": []}} if none found.
        """,

        "publications": f"""
        Extract all publications. For each publication return:
        - Title
        - Publisher
        - Date
        - Link

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return JSON: {{ "publications": [ {{ ... }}, ... ] }}
        Return {{"publications": []}} if none found.
        """
    }

    if section_type not in prompts:
        # Unknown section type → no structured extraction
        return {}

    prompt = prompts[section_type]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an expert resume parser. Extract information accurately and return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=2000
        )

        # Extract JSON from the model's reply
        reply = response.choices[0].message.content.strip()
        json_match = re.search(r'\{.*\}', reply, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        # Fallback – try to parse the whole response as JSON
        return json.loads(reply)

    except (AuthenticationError, APIStatusError, APIConnectionError, RateLimitError) as e:
        # Graceful degradation – return empty structure for this section
        print(f"[WARN] OpenAI API error while processing '{section_type}': {e}")
        return _empty_structure_for(section_type)
    except Exception as e:  # Catch‑all for unexpected issues
        print(f"[WARN] Unexpected error while processing '{section_type}': {e}")
        return _empty_structure_for(section_type)


def _empty_structure_for(section_type: str) -> Dict[str, Any]:
    """Return a suitable empty/default structure for a given section type."""
    if section_type == "personal_information":
        return {
            "name": None, "email": None, "phone": None, "linkedin": None,
            "github": None, "portfolio": None, "website": None, "location": None
        }
    if section_type == "summary":
        return {"summary": None}
    if section_type == "skills":
        return {
            "programming_languages": [], "frameworks": [], "databases": [],
            "cloud": [], "tools": [], "libraries": [], "testing": [],
            "ai_ml": [], "devops": [], "others": []
        }
    if section_type == "experience":
        return {"experience": []}
    if section_type == "projects":
        return {"projects": []}
    if section_type == "education":
        return {"education": []}
    if section_type == "certifications":
        return {"certifications": []}
    if section_type == "achievements":
        return {"achievements": []}
    if section_type == "publications":
        return {"publications": []}
    return {}  # fallback for unknown types


def build_result_json(sections: List[Tuple[Optional[str], str]]) -> Dict[str, Any]:
    """Assemble the final JSON from the parsed sections."""
    result = {
        "personal_information": {
            "name": None, "email": None, "phone": None, "linkedin": None,
            "github": None, "portfolio": None, "website": None, "location": None
        },
        "summary": None,
        "skills": {
            "programming_languages": [], "frameworks": [], "databases": [],
            "cloud": [], "tools": [], "libraries": [], "testing": [],
            "ai_ml": [], "devops": [], "others": []
        },
        "experience": [],
        "projects": [],
        "education": [],
        "certifications": [],
        "achievements": [],
        "publications": [],
        "other_sections": {}
    }

    for heading, content in sections:
        if not content.strip():
            continue

        # Determine section type
        if heading is None:
            section_type = "personal_information"   # leading block without a heading
        else:
            section_type = map_heading_to_type(heading)
            if section_type is None:
                # Unknown heading → store as-is under other_sections
                if heading is not None:
                    result["other_sections"][heading] = content
                continue  # skip extraction for this section

        if section_type is not None:
            extracted = extract_section_data_with_openai(section_type, content)

            # Merge extracted data into the result structure
            if section_type == "personal_information":
                for key in result["personal_information"]:
                    if key in extracted and extracted[key] is not None:
                        result["personal_information"][key] = extracted[key]
            elif section_type == "summary":
                if "summary" in extracted and extracted["summary"] is not None:
                    result["summary"] = extracted["summary"]
            elif section_type == "skills":
                for key in result["skills"]:
                    if key in extracted:
                        result["skills"][key] = extracted[key]
            elif section_type == "experience":
                if "experience" in extracted:
                    result["experience"].extend(extracted["experience"])
            elif section_type == "projects":
                if "projects" in extracted:
                    result["projects"].extend(extracted["projects"])
            elif section_type == "education":
                if "education" in extracted:
                    result["education"].extend(extracted["education"])
            elif section_type == "certifications":
                if "certifications" in extracted:
                    result["certifications"].extend(extracted["certifications"])
            elif section_type == "achievements":
                if "achievements" in extracted:
                    result["achievements"].extend(extracted["achievements"])
            elif section_type == "publications":
                if "publications" in extracted:
                    result["publications"].extend(extracted["publications"])

    return result


def extract_resume(pdf_path: str) -> Dict[str, Any]:
    """Main entry point: PDF → JSON."""
    raw_text = extract_text_from_pdf(pdf_path)
    clean_text = preprocess_text(raw_text)
    sections = split_into_sections(clean_text)
    return build_result_json(sections)


# ----------------------------------------------------------------------
# Command‑line interface
# ----------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python extractor.py <path_to_resume.pdf>")

    pdf_path = sys.argv[1]
    if not os.path.isfile(pdf_path):
        sys.exit(f"Error: File not found: {pdf_path}")

    try:
        json_data = extract_resume(pdf_path)
        print(json.dumps(json_data, indent=2))
    except Exception as exc:
        sys.exit(f"Error processing resume: {exc}")