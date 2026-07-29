#!/usr/bin/env python
"""
Resume Extraction Agent (Agent-1) - MVP Version

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

# Load environment variables
load_dotenv()


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract plain text from all pages of the PDF."""
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

    # Common resume section headers (case-insensitive)
    heading_patterns = [
        r'^\s*summary\s*:?\s*$',
        r'^\s*professional\s+professional\s*:?\s*summary\s*:?\s*$',
        r'^\s*profile\s*:?\s*$',
        r'^\s*experience\s*:?\s*$',
        r'^\s*work\s+experience\s*:?\s*$',
        r'^\s*employment\s*:?\s*$',
        r'^\s*projects\s*:?\s*$',
        r'^\s*academic\s+projects\s*:?\s*$',
        r'^\s*education\s*:?\s*$',
        r'^\s*skills\s*:?\s*$',
        r'^\s*technical\s+skills\s*:?\s*$',
        r'^\s*certifications\s*:?\s*$',
        r'^\s*achievements\s*:?\s*$',
        r'^\s*awards\s*:?\s*$',
        r'^\s*publications\s*:?\s*$',
        r'^\s*languages\s*:?\s*$',
        r'^\s*interests\s*:?\s*$',
        r'^\s*hobbies\s*:?\s*$'
    ]

    # Combined pattern for matching section headers
    header_pattern = re.compile('|'.join(heading_patterns), re.IGNORECASE)

    for line in lines:
        if header_pattern.match(line.strip()):
            # Save previous section
            if current_heading is not None or current_content:
                sections.append((current_heading, "\n".join(current_content)))

            # Extract clean heading name (remove trailing colon and extra spaces)
            matched = header_pattern.match(line.strip())
            if matched:
                heading_text = matched.group(0).strip().rstrip(':')
                current_heading = heading_text.lower()
            else:
                current_heading = line.strip().lower().rstrip(':')

            current_content = []
        else:
            current_content.append(line)

    # Add the last section
    if current_heading is not None or current_content:
        sections.append((current_heading, "\n".join(current_content)))

    return sections


def extract_personal_info(text: str) -> Dict[str, Any]:
    """Extract personal information from text."""
    result = {
        "name": None,
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "portfolio": None,
        "website": None,
        "location": None
    }

    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        result["email"] = email_match.group(0)

    # Extract phone number (various formats)
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
        r'\(\d{3}\)\s*\d{3}[-.\s]??\d{4}',
        r'\d{3}[-.\s]??\d{3}[-.\s]??\d{4}'
    ]
    for pattern in phone_patterns:
        phone_match = re.search(pattern, text)
        if phone_match:
            result["phone"] = phone_match.group(0)
            break

    # Extract LinkedIn URL
    linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[^\s]+'
    linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
    if linkedin_match:
        result["linkedin"] = linkedin_match.group(0)

    # Extract GitHub URL
    github_pattern = r'https?://(?:www\.)?github\.com/[^\s]+'
    github_match = re.search(github_pattern, text, re.IGNORECASE)
    if github_match:
        result["github"] = github_match.group(0)

    # Extract name (usually at the beginning, in larger font or all caps)
    lines = text.split('\n')
    if lines:
        # First non-empty line is often the name
        for line in lines:
            if line.strip() and not re.search(r'@|\+|http|\d{3,}', line):
                # Simple heuristic: if it looks like a name (not email, phone, url)
                if len(line.split()) <= 4 and len(line.strip()) > 2:
                    result["name"] = line.strip()
                    break

    # Extract location (look for city, state patterns)
    location_patterns = [
        r'[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}',  # City, State ZIP
        r'[A-Za-z\s]+,\s*[A-Z]{2}',           # City, State
        r'[A-Za-z\s]+,\s*[A-Za-z\s]+'         # City, Country
    ]
    for pattern in location_patterns:
        loc_match = re.search(pattern, text)
        if loc_match:
            result["location"] = loc_match.group(0)
            break

    return result


def extract_summary(text: str) -> Optional[str]:
    """Extract professional summary."""
    # Look for common summary indicators
    lines = text.split('\n')
    summary_lines = []
    in_summary = False

    for line in lines:
        line_lower = line.lower().strip()
        if any(keyword in line_lower for keyword in ['summary', 'professional summary', 'profile']):
            in_summary = True
            continue
        elif in_summary and line.strip() and not any(keyword in line_lower for keyword in
                                                    ['experience', 'education', 'skills', 'projects']):
            # Stop when we hit another section header
            if line.isupper() and len(line.split()) > 3:  # Likely a new section header
                break
            summary_lines.append(line)
        elif in_summary and not line.strip():
            # Empty line might indicate end of summary
            if summary_lines:  # Only add if we have content
                break

    if summary_lines:
        return ' '.join(summary_lines).strip()
    return None


def extract_skills(text: str) -> Dict[str, List[str]]:
    """Extract and categorize skills."""
    # Initialize all skill categories with empty lists
    skills = {
        "programming_languages": [],
        "frameworks": [],
        "databases": [],
        "cloud": [],
        "tools": [],
        "libraries": [],
        "testing": [],
        "ai_ml": [],
        "devops": [],
        "others": []
    }

    # Common skill keywords by category
    skill_keywords = {
        "programming_languages": ["python", "java", "javascript", "typescript", "c\\+\\+", "c#", "ruby", "php", "swift", "kotlin", "go", "rust", "scala", "r", "matlab"],
        "frameworks": ["react", "angular", "vue", "django", "flask", "spring", "laravel", "express", ".net", "rails"],
        "databases": ["mysql", "postgresql", "mongodb", "redis", "oracle", "sql server", "sqlite", "cassandra", "dynamodb"],
        "cloud": ["aws", "azure", "gcp", "google cloud", "heroku", "digitalocean", "linode", "cloudflare"],
        "tools": ["git", "docker", "kubernetes", "jenkins", "jira", "confluence", "slack", "trello", "notion"],
        "libraries": ["numpy", "pandas", "tensorflow", "pytorch", "keras", "scikit-learn", "matplotlib", "seaborn"],
        "testing": ["junit", "pytest", "selenium", "jest", "mocha", "chai", "cypress", "testng"],
        "ai_ml": ["machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "scikit-learn"],
        "devops": ["ci/cd", "jenkins", "travis", "circleci", "github actions", "gitlab ci", "ansible", "terraform", "docker", "kubernetes"]
    }

    text_lower = text.lower()

    # Extract skills from common patterns
    # Look for skills section content
    lines = text.split('\n')
    skills_section = []
    in_skills = False

    for line in lines:
        line_lower = line.lower().strip()
        if any(keyword in line_lower for keyword in ['skills', 'technical skills']):
            in_skills = True
            continue
        elif in_skills:
            # Stop at next section
            if any(keyword in line_lower for keyword in ['experience', 'education', 'projects', 'certifications']):
                if line.isupper() and len(line.split()) > 2:  # Likely a new section
                    break
            if line.strip():
                line

    skills_text = ' '.join(skills_section) if skills_section else text

    # Extract individual skills (words or phrases)
    # Simple approach: split by common delimiters
    potential_skills = re.split(r'[,•·▪▫‣⁃\-–—\|\n\r\t]', skills_text)

    for skill in potential_skills:
        skill = skill.strip()
        if not skill or len(skill) < 2:
            continue

        # Check if it matches any category
        categorized = False
        for category, keywords in skill_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', skill, re.IGNORECASE):
                    skills[category].append(skill)
                    categorized = True
                    break
            if categorized:
                break

        # If not categorized, put in others
        if not categorized and skill:
            # Avoid duplicates
            if skill not in skills["others"]:
                skills["others"].append(skill)

    # Remove duplicates from each category
    for category in skills:
        skills[category] = list(dict.fromkeys(skills[category]))

    return skills


def extract_experience(text: str) -> List[Dict[str, Any]]:
    """Extract work experience."""
    # This is a simplified version - for MVP we'll extract basic structure
    experience = []

    # Look for experience section
    lines = text.split('\n')
    exp_section = []
    in_experience = False

    for line in lines:
        line_lower = line.lower().strip()
        if any(keyword in line_lower for keyword in ['experience', 'work experience', 'employment']):
            in_experience = True
            continue
        elif in_experience:
            # Stop at next major section
            if any(keyword in line_lower for keyword in ['education', 'projects', 'skills', 'certifications']):
                if line.isupper() and len(line.split()) > 2:
                    break
            if line.strip():
                exp_section.append(line)

    exp_text = '\n'.join(exp_section) if exp_section else text

    # Simple entry extraction (this is basic - real implementation would be more sophisticated)
    # Look for patterns like: Company Name, Location | Dates
    # or Company Name | Title | Dates

    # Split by double newline or clear section breaks
    potential_entries = re.split(r'\n\s*\n|\n{2,}', exp_text)

    for entry in potential_entries:
        if not entry.strip() or len(entry.strip()) < 10:
            continue

        exp_entry = {
            "company": None,
            "role": None,
            "employment_type": None,
            "location": None,
            "start_date": None,
            "end_date": None,
            "duration": None,
            "bullet_points": [],
            "technologies_used": [],
            "achievements": []
        }

        lines_in_entry = [line.strip() for line in entry.split('\n') if line.strip()]
        if not lines_in_entry:
            continue

        # First line often contains company and role
        first_line = lines_in_entry[0]

        # Try to extract company and role from first line
        # Pattern: "Company Name - Position" or "Company Name | Position"
        if ' - ' in first_line:
            parts = first_line.split(' - ', 1)
            if len(parts) == 2:
                exp_entry["company"] = parts[0].strip()
                exp_entry["role"] = parts[1].strip()
        elif ' | ' in first_line:
            parts = first_line.split(' | ', 1)
            if len(parts) == 2:
                exp_entry["company"] = parts[0].strip()
                exp_entry["role"] = parts[1].strip()
        else:
            # Assume first line is company, second might be role
            if len(lines_in_entry) >= 2:
                # Check if second line looks like a job title
                second_line = lines_in_entry[1]
                if any(title_word in second_line.lower() for title_word in
                      ['engineer', 'developer', 'manager', 'analyst', 'consultant', 'specialist',
                       'coordinator', 'assistant', 'director', 'lead', 'senior', 'junior']):
                    exp_entry["company"] = first_line
                    exp_entry["role"] = second_line
                else:
                    # Both might be part of company name
                    exp_entry["company"] = first_line + " " + second_line
            else:
                exp_entry["company"] = first_line

        # Look for date patterns
        date_patterns = [
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*[-–]\s*(Present|Current|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b',
            r'\b\d{1,2}/\d{4}\s*[-–]\s*(Present|Current|\d{1,2}/\d{4})\b',
            r'\b\d{4}\s*[-–]\s*(Present|Current|\d{4})\b'
        ]

        for pattern in date_patterns:
            date_match = re.search(pattern, entry, re.IGNORECASE)
            if date_match:
                date_text = date_match.group(0)
                # Try to parse start and end dates
                if ' - ' in date_text or ' – ' in date_text:
                    separator = ' - ' if ' - ' in date_text else ' – '
                    date_parts = date_text.split(separator)
                    if len(date_parts) == 2:
                        start_date = date_parts[0].strip()
                        end_date = date_parts[1].strip()
                        # Clean up
                        end_date = None if re.search(r'(?i)present|current', end_date) else end_date
                        exp_entry["start_date"] = start_date
                        exp_entry["end_date"] = end_date

                        # Calculate duration if possible
                        try:
                            # This is simplified - real implementation would parse dates properly
                            if start_date and end_date and not re.search(r'(?i)present|current', end_date):
                                # Very basic duration calculation
                                exp_entry["duration"] = "See dates"
                        except:
                            pass
                break

        # Extract bullet points (lines starting with •, *, -, –, or numbers like 1. )
        bullet_lines = []
        for line in lines_in_entry:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            # Check for bullet points: •, *, -, –
            if stripped_line.startswith(('•', '*', '-', '–')):
                # Remove the bullet character and any following whitespace
                bullet = stripped_line[1:].lstrip()
                bullet_lines.append(bullet)
            # Check for numbered list: 1. , 2. , etc.
            elif re.match(r'^\d+\.\s*', stripped_line):
                # Remove the number, dot, and following whitespace
                bullet = re.sub(r'^\d+\.\s*', '', stripped_line)
                bullet_lines.append(bullet)

        if bullet_lines:
            exp_entry["bullet_points"] = bullet_lines

        # Only add if we found meaningful content
        if exp_entry["company"] or exp_entry["role"]:
            experience.append(exp_entry)

    return experience


def extract_projects(text: str) -> List[Dict[str, Any]]:
    """Extract projects information."""
    projects = []

    # Look for projects section
    lines = text.split('\n')
    proj_section = []
    in_projects = False

    for line in lines:
        line_lower = line.lower().strip()
        if any(keyword in line_lower for keyword in ['projects', 'academic projects']):
            in_projects = True
            continue
        elif in_projects:
            # Stop at next section
            if any(keyword in line_lower for keyword in ['experience', 'education', 'skills', 'certifications']):
                if line.isupper() and len(line.split()) > 2:
                    break
            if line.strip():
                proj_section.append(line)

    proj_text = '\n'.join(proj_section) if proj_section else text

    # Split into potential project entries
    # Look for lines that might be project titles (often shorter, maybe with links)
    potential_entries = re.split(r'\n\s*\n|\n{2,}', proj_text)

    for entry in potential_entries:
        if not entry.strip() or len(entry.strip()) < 5:
            continue

        project = {
            "title": None,
            "description": None,
            "technologies": [],
            "features": [],
            "contributions": [],
            "github_link": None,
            "live_link": None
        }

        lines_in_entry = [line.strip() for line in entry.split('\n') if line.strip()]
        if not lines_in_entry:
            continue

        # First line is often the project title
        project["title"] = lines_in_entry[0]

        # Look for URLs
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, entry)
        for url in urls:
            if 'github.com' in url.lower():
                project["github_link"] = url
            elif any(domain in url.lower() for domain in ['.com', '.org', '.net', '.io', '.dev']):
                # Could be a live demo or deployment link
                if not project["live_link"]:  # Take first non-GitHub URL as live link
                    project["live_link"] = url

        # Combine remaining lines as description
        if len(lines_in_entry) > 1:
            project["description"] = ' '.join(lines_in_entry[1:])

        # Extract technologies (look for common tech names in description)
        tech_keywords = ["python", "java", "javascript", "react", "node", "sql", "html", "css",
                        "aws", "docker", "kubernetes", "mongodb", "postgresql", "git"]
        desc_lower = (project["description"] or "").lower()
        for tech in tech_keywords:
            if tech in desc_lower:
                project["technologies"].append(tech)

        # Only add if we have a title
        if project["title"]:
            projects.append(project)

    return projects


def extract_education(text: str) -> List[Dict[str, Any]]:
    """Extract education information."""
    education = []

    # Look for education section
    lines = text.split('\n')
    edu_section = []
    in_education = False

    for line in lines:
        line_lower = line.lower().strip()
        if any(keyword in line_lower for keyword in ['education', 'academic background']):
            in_education = True
            continue
        elif in_education:
            # Stop at next section
            if any(keyword in line_lower for keyword in ['experience', 'projects', 'skills', 'certifications']):
                if line.isupper() and len(line.split()) > 2:
                    break
            if line.strip():
                edu_section.append(line)

    edu_text = '\n'.join(edu_section) if edu_section else text

    # Simple entry extraction
    potential_entries = re.split(r'\n\s*\n|\n{2,}', edu_text)

    for entry in potential_entries:
        if not entry.strip() or len(entry.strip()) < 5:
            continue

        edu_entry = {
            "degree": None,
            "branch": None,
            "institution": None,
            "cgpa_percentage": None,
            "start_year": None,
            "end_year": None
        }

        lines_in_entry = [line.strip() for line in entry.split('\n') if line.strip()]
        if not lines_in_entry:
            continue

        # Often format is: Degree, Institution | Location | Dates

        # Look for degree patterns
        degree_patterns = [
            r'\b(bachelor|master|phd|doctorate|b\.|associate|diploma|high school|ssc|hsc)\b.*',
            r'\b(b\.?tech|m\.?tech|b\.?e|m\.?e|b\.?sc|m\.?sc|b\.?a|m\.?a)\b.*'
        ]

        degree_found = False
        for pattern in degree_patterns:
            degree_match = re.search(pattern, ' '.join(lines_in_entry), re.IGNORECASE)
            if degree_match:
                edu_entry["degree"] = degree_match.group(0).strip()
                degree_found = True
                break

        # Look for year patterns
        year_pattern = r'\b(19|20)\d{2}\s*[-–]\s*(19|20)\d{2}|present|current\b'
        year_matches = re.findall(year_pattern, ' '.join(lines_in_entry), re.IGNORECASE)
        if year_matches:
            # Take first match
            year_str = year_matches[0] if isinstance(year_matches[0], str) else ''.join(year_matches[0])
            if ' - ' in year_str or ' – ' in year_str:
                separator = ' - ' if ' - ' in year_str else ' – '
                years = year_str.split(separator)
                if len(years) == 2:
                    edu_entry["start_year"] = years[0].strip()
                    end_year = years[1].strip()
                    edu_entry["end_year"] = None if re.search(r'(?i)present|current', end_year) else end_year
            else:
                # Single year might be graduation year
                edu_entry["end_year"] = year_str

        # Institution often appears before or after degree
        for line in lines_in_entry:
            if any(indicator in line.lower() for indicator in ['university', 'college', 'institute', 'school']):
                if not edu_entry["institution"]:
                    edu_entry["institution"] = line.strip()
                    break

        # Look for GPA/CGPA percentage
        gpa_pattern = r'\b(cgpa|gpa|percentage)\s*:?\s*(\d+\.?\d*)\s*(/|out of)?\s*(\d+)?\s*%?\b'
        gpa_match = re.search(gpa_pattern, ' '.join(lines_in_entry), re.IGNORECASE)
        if gpa_match:
            # Extract the numeric value
            num_str = gpa_match.group(2)
            try:
                num_val = float(num_str)
                if gpa_match.group(4):  # Has "out of" part
                    scale = float(gpa_match.group(4))
                    # Convert to percentage if on 4.0 or 10.0 scale
                    if scale == 4.0:
                        edu_entry["cgpa_percentage"] = f"{min(100, (num_val/4.0)*100):.1f}%"
                    elif scale == 10.0:
                        edu_entry["cgpa_percentage"] = f"{num_val*10:.1f}%"
                    else:
                        edu_entry["cgpa_percentage"] = f"{num_val}%"
                else:
                    # Assume it's already a percentage or CGPA
                    if '.' in num_str and float(num_str) <= 4.0:
                        # Likely CGPA out of 4.0
                        edu_entry["cgpa_percentage"] = f"{float(num_str)/4.0*100:.1f}%"
                    elif '.' in num_str and float(num_str) <= 10.0:
                        # Likely CGPA out of 10.0
                        edu_entry["cgpa_percentage"] = f"{float(num_str)*10:.1f}%"
                    else:
                        # Assume percentage
                        edu_entry["cgpa_percentage"] = f"{num_str}%"
            except:
                pass

        # Only add if we have meaningful data
        if edu_entry["degree"] or edu_entry["institution"]:
            education.append(edu_entry)

    return education


# Stub functions for other sections (they would return empty structures)
def extract_certifications(text: str) -> List[Dict[str, Any]]:
    """Extract certifications - stub for MVP."""
    return []


def extract_achievements(text: str) -> List[str]:
    """Extract achievements - stub for MVP."""
    return []


def extract_publications(text: str) -> List[Dict[str, Any]]:
    """Extract publications - stub for MVP."""
    return []


def map_heading_to_type(heading: Optional[str]) -> Optional[str]:
    """Map a raw heading to the canonical section type."""
    if heading is None:
        return None
    h = heading.lower().strip()
    if h.endswith(':'):
        h = h[:-1]

    # Map common variations to standard types
    if h in ["personal information", "contact information", "contact"]:
        return "personal_information"
    elif h in ["summary", "professional summary", "profile"]:
        return "summary"
    elif h in ["skills", "technical skills"]:
        return "skills"
    elif h in ["experience", "work experience", "employment"]:
        return "experience"
    elif h in ["projects", "academic projects"]:
        return "projects"
    elif h == "education":
        return "education"
    elif h == "certifications":
        return "certifications"
    elif h in ["achievements", "awards"]:
        return "achievements"
    elif h == "publications":
        return "publications"
    else:
        return None  # Will go to other_sections


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
            extracted = None
            if section_type == "personal_information":
                extracted = extract_personal_info(content)
            elif section_type == "summary":
                extracted = {"summary": extract_summary(content)}
            elif section_type == "skills":
                extracted = extract_skills(content)
            elif section_type == "experience":
                extracted = {"experience": extract_experience(content)}
            elif section_type == "projects":
                extracted = {"projects": extract_projects(content)}
            elif section_type == "education":
                extracted = {"education": extract_education(content)}
            elif section_type == "certifications":
                extracted = {"certifications": extract_certifications(content)}
            elif section_type == "achievements":
                extracted = {"achievements": extract_achievements(content)}
            elif section_type == "publications":
                extracted = {"publications": extract_publications(content)}

            # Merge extracted data into result structure
            if extracted:
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
# Command-line interface
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