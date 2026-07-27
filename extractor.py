import os
import re
import json
import pdfplumber
from typing import Dict, List, Any, Optional, Tuple
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Constants for section headings and their mapping to section types
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

# Mapping from heading variations to section types
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
    "internships": "experience",  # Treat internships as experience
    "publications": "publications",
    # Leadership, extracurricular, etc. will go to other_sections
}

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def preprocess_text(text: str) -> str:
    """Clean and normalize text while preserving line breaks."""
    # Replace multiple spaces/tabs with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Replace multiple newlines with at most two newlines (to keep paragraph breaks)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Remove leading/trailing whitespace
    return text.strip()

def split_into_sections(text: str) -> List[Tuple[Optional[str], str]]:
    """Split text into sections based on known headings."""
    lines = text.splitlines()
    sections = []
    current_heading = None
    current_content = []

    # Pattern to match section headings (case insensitive, optional colon)
    pattern = re.compile(r'^\s*(' + '|'.join(re.escape(h) for h in KNOWN_HEADINGS) + r')\s*:?\s*$', re.IGNORECASE)

    for line in lines:
        # Check if line matches a section heading
        match = pattern.match(line)
        if match:
            # Save previous section
            if current_heading is not None or current_content:
                sections.append((current_heading, '\n'.join(current_content)))
            current_heading = match.group(1).strip()
            current_content = []
        else:
            current_content.append(line)

    # Add last section
    if current_heading is not None or current_content:
        sections.append((current_heading, '\n'.join(current_content)))

    return sections

def map_heading_to_type(heading: Optional[str]) -> Optional[str]:
    """Map a section heading to a standard section type."""
    if heading is None:
        return None
    heading_lower = heading.lower().strip()
    # Remove trailing colon if present
    if heading_lower.endswith(':'):
        heading_lower = heading_lower[:-1]
    return HEADING_TO_TYPE.get(heading_lower)

def extract_section_data_with_openai(section_type: str, section_text: str) -> Dict[str, Any]:
    """Extract structured data from a section using OpenAI."""
    # Define prompts for each section type
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

        Return the information in JSON format with these exact keys:
        name, email, phone, linkedin, github, portfolio, website, location.
        If a piece of information is not present, set its value to null.
        """,

        "summary": f"""
        Extract the professional summary or profile section from the given text.
        Return the summary as a string. If no summary is found, return null.

        Text:
        \"\"\"
        {section_text}
        \"\"\"
        """,

        "skills": f"""
        Extract and categorize skills from the given text into these categories:
        - Programming Languages
        - Frameworks
        - Databases
        - Cloud
        - Tools
        - Libraries
        - Testing
        - AI/ML
        - DevOps
        - Others

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return a JSON object with these keys (arrays of strings):
        programming_languages, frameworks, databases, cloud, tools, libraries, testing, ai_ml, devops, others.
        If a category has no skills, set its value to an empty array.
        """,

        "experience": f"""
        Extract all work experiences from the given text. For each experience, extract:
        - Company
        - Role
        - Employment Type (e.g., Full-time, Part-time, Contract, Internship)
        - Location
        - Start Date (format: YYYY-MM or MM/YYYY)
        - End Date (format: YYYY-MM or MM/YYYY, or "Present")
        - Duration (if available, e.g., "2 years 3 months")
        - Bullet points (array of strings)
        - Technologies Used (array of strings)
        - Achievements (array of strings)

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return a JSON object with a key "experience" containing an array of experience objects.
        If no experiences are found, return {{"experience": []}}.
        """,

        "projects": f"""
        Extract all projects from the given text. For each project, extract:
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

        Return a JSON object with a key "projects" containing an array of project objects.
        If no projects are found, return {{"projects": []}}.
        """,

        "education": f"""
        Extract all education entries from the given text. For each entry, extract:
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

        Return a JSON object with a key "education" containing an array of education objects.
        If no education entries are found, return {{"education": []}}.
        """,

        "certifications": f"""
        Extract all certifications from the given text. For each certification, extract:
        - Name
        - Issuing Organization
        - Year
        - Credential ID (if present)

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return a JSON object with a key "certifications" containing an array of certification objects.
        If no certifications are found, return {{"certifications": []}}.
        """,

        "achievements": f"""
        Extract all achievements from the given text. Each achievement should be a string.
        Return a JSON object with a key "achievements" containing an array of achievement strings.
        If no achievements are found, return {{"achievements": []}}.

        Text:
        \"\"\"
        {section_text}
        \"\"\"
        """,

        "publications": f"""
        Extract all publications from the given text. For each publication, extract:
        - Title
        - Publisher
        - Date
        - Link

        Text:
        \"\"\"
        {section_text}
        \"\"\"

        Return a JSON object with a key "publications" containing an array of publication objects.
        If no publications are found, return {{"publications": []}}.
        """
    }

    if section_type not in prompts:
        # For unknown section types, we don't extract structured data
        return {}

    prompt = prompts[section_type]

    try:
        # Check if API key is set
        if not os.getenv("OPENAI_API_KEY"):
            print("Warning: OpenAI API key not set. Skipping OpenAI extraction for section:", section_type)
            # Return empty structure based on section type
            if section_type == "personal_information":
                return {
                    "name": None, "email": None, "phone": None, "linkedin": None,
                    "github": None, "portfolio": None, "website": None, "location": None
                }
            elif section_type == "summary":
                return {"summary": None}
            elif section_type == "skills":
                return {
                    "programming_languages": [], "frameworks": [], "databases": [],
                    "cloud": [], "tools": [], "libraries": [], "testing": [],
                    "ai_ml": [], "devops": [], "others": []
                }
            elif section_type == "experience":
                return {"experience": []}
            elif section_type == "projects":
                return {"projects": []}
            elif section_type == "education":
                return {"education": []}
            elif section_type == "certifications":
                return {"certifications": []}
            elif section_type == "achievements":
                return {"achievements": []}
            elif section_type == "publications":
                return {"publications": []}
            else:
                return {}

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume parser. Extract information accurately and return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=2000
        )

        # Extract JSON from response
        response_text = response.choices[0].message.content.strip()
        # Find JSON object in response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        else:
            # Fallback: try to parse the whole response as JSON
            return json.loads(response_text)
    except Exception as e:
        print(f"Error extracting {section_type}: {e}")
        # Return empty structure based on section type
        if section_type == "personal_information":
            return {
                "name": None, "email": None, "phone": None, "linkedin": None,
                "github": None, "portfolio": None, "website": None, "location": None
            }
        elif section_type == "summary":
            return {"summary": None}
        elif section_type == "skills":
            return {
                "programming_languages": [], "frameworks": [], "databases": [],
                "cloud": [], "tools": [], "libraries": [], "testing": [],
                "ai_ml": [], "devops": [], "others": []
            }
        elif section_type == "experience":
            return {"experience": []}
        elif section_type == "projects":
            return {"projects": []}
        elif section_type == "education":
            return {"education": []}
        elif section_type == "certifications":
            return {"certifications": []}
        elif section_type == "achievements":
            return {"achievements": []}
        elif section_type == "publications":
            return {"publications": []}
        else:
            return {}

def build_result_json(sections: List[Tuple[Optional[str], str]]) -> Dict[str, Any]:
    """Build the final JSON structure from sections."""
    # Initialize result structure
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
            # No heading -> treat as personal information (headerless block at start)
            section_type = "personal_information"
        else:
            section_type = map_heading_to_type(heading)
            if section_type is None:
                # Unknown heading -> store in other_sections and skip extraction
                if heading is not None:
                    result["other_sections"][heading] = content
                continue  # skip extraction for this section

        if section_type is not None:
            # Extract structured data for known section types
            extracted = extract_section_data_with_openai(section_type, content)

            # Merge extracted data into result
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
    """Main function to extract resume data and return JSON."""
    # Extract text from PDF
    raw_text = extract_text_from_pdf(pdf_path)
    # Preprocess text
    clean_text = preprocess_text(raw_text)
    # Split into sections
    sections = split_into_sections(clean_text)
    # Build JSON structure
    json_data = build_result_json(sections)

    return json_data

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extractor.py <path_to_resume.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    try:
        json_data = extract_resume(pdf_path)
        print(json.dumps(json_data, indent=2))
    except Exception as e:
        print(f"Error processing resume: {e}")
        sys.exit(1)