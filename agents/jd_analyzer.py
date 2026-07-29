"""
JD Analyzer Agent for Resume Optimizer MVP.

Analyzes job description files (TXT/PDF) and extracts structured data
matching the job description schema.
"""

import re
from typing import Dict, Any, List


def extract_job_title(text: str) -> str:
    """Extract job title from the beginning of the job description."""
    lines = text.strip().split('\n')
    if lines:
        # Usually the first non-empty line contains the job title
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('-', '•', '*')) and len(line) < 100:
                # Skip lines that look like bullet points or are too long
                if not any(keyword in line.lower() for keyword in ['company:', 'location:', 'about', 'we are']):
                    return line
    return ""


def extract_company(text: str) -> str:
    """Extract company name from the job description."""
    # Look for patterns like "at [Company]" or "[Company] is"
    patterns = [
        r'at\s+([A-Z][A-Za-z0-9\s&\.]+?)(?:\s+is|\s+has|\s+was|\s+seeks|\s+looks|\s*$)',
        r'^([A-Z][A-Za-z0-9\s&\.]+?)\s+is\s+(?:hiring|looking|seeking)',
        r'([A-Z][A-Za-z0-9\s&\.]+?)\s+(?:is|are)\s+(?:hiring|looking|seeking)'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            company = match.group(1).strip()
            # Clean up common suffixes
            company = re.sub(r'\s+(Inc\.?|LLC\.?|Ltd\.?|Corp\.?|Corporation|Company|Co\.?)$', '', company, flags=re.IGNORECASE)
            return company

    # Fallback: look for company-like patterns
    lines = text.split('\n')
    for line in lines[:5]:  # Check first few lines
        line = line.strip()
        if ('company' in line.lower() or 'at' in line.lower()) and len(line) < 100:
            # Extract potential company name
            match = re.search(r'(?:at|@|company:?\s*)([A-Z][A-Za-z0-9\s&\.]+)', line, re.IGNORECASE)
            if match:
                return match.group(1).strip()

    return ""


def extract_location(text: str) -> str:
    """Extract job location from the job description."""
    # Common location patterns
    location_patterns = [
        r'location[:\s]*([^,\n]+?)(?:,|\n|$)',
        r'based\s+in[:\s]*([^,\n]+?)(?:,|\n|$)',
        r'ubicado\s*en[:\s]*([^,\n]+?)(?:,|\n|$)',
        r'location:?\s*([^,\n]{2,50}?)(?:,|\n|$)',
    ]

    for pattern in location_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            location = match.group(1).strip()
            if len(location) < 100:  # Reasonable location length
                return location

    # Look for common location keywords
    location_keywords = ['remote', 'hybrid', 'on-site', 'onsite', 'new york', 'san francisco',
                        'london', 'bangalore', 'hyderabad', 'pune', 'chennai', 'mumbai',
                        'delhi', 'gurgaon', 'noida', 'boston', 'seattle', 'austin']

    text_lower = text.lower()
    for keyword in location_keywords:
        if keyword in text_lower:
            # Try to extract surrounding context
            pattern = rf'.{{0,50}}{keyword}.{{0,50}}'
            match = re.search(pattern, text_lower)
            if match:
                context = match.group(0)
                # Extract the actual location part
                loc_match = re.search(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', context)
                if loc_match:
                    return loc_match.group(0)
                return keyword.title()

    return ""


def extract_employment_type(text: str) -> str:
    """Extract employment type from the job description."""
    employment_types = {
        'full-time': ['full-time', 'full time', 'fulltime'],
        'part-time': ['part-time', 'part time', 'parttime'],
        'contract': ['contract', 'contractor', 'consulting'],
        'temporary': ['temporary', 'temp', 'interim'],
        'internship': ['internship', 'intern', 'summer intern'],
        'freelance': ['freelance', 'freelancer']
    }

    text_lower = text.lower()
    for emp_type, keywords in employment_types.items():
        if any(keyword in text_lower for keyword in keywords):
            return emp_type

    return ""


def extract_experience_level(text: str) -> str:
    """Extract experience level from the job description."""
    experience_patterns = {
        'entry-level': ['entry.level', 'entry level', 'junior', 'jr.', 'associate', 'assistant'],
        'mid-level': ['mid.level', 'mid level', 'intermediate', 'experienced'],
        'senior': ['senior', 'sr.', 'lead', 'principal', 'staff'],
        'executive': ['executive', 'director', 'vp', 'vice president', 'cto', 'cfo', 'ceo']
    }

    text_lower = text.lower()
    for level, keywords in experience_patterns.items():
        if any(keyword in text_lower for keyword in keywords):
            return level

    # Look for years of experience patterns
    year_patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)'
    ]

    for pattern in year_patterns:
        match = re.search(pattern, text_lower)
        if match:
            years = int(match.group(1))
            if years <= 2:
                return "entry-level"
            elif years <= 5:
                return "mid-level"
            elif years <= 10:
                return "senior"
            else:
                return "executive"

    return ""


def extract_remote_option(text: str) -> bool:
    """Extract if remote work is an option from the job description."""
    remote_indicators = [
        'remote', 'work from home', 'wfh', 'telecommute', 'teleworking',
        'virtual', 'distributed', 'flexible location', 'location independent'
    ]

    text_lower = text.lower()
    return any(indicator in text_lower for indicator in remote_indicators)


def extract_bullet_points(text: str, section_header: str) -> List[str]:
    """Extract bullet points from a specific section."""
    # Find the section
    pattern = rf'{section_header}[:\s]*\n(.*?)(?:\n[A-Z][^:\n]*:|\Z)'
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    if not match:
        # Try alternative patterns
        pattern = rf'{section_header}[:\s]*(.*?)(?:\n[A-Z][^:\n]*:|\Z)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    if not match:
        return []

    section_content = match.group(1).strip()

    # Extract bullet points (lines starting with -, *, •, or numbers)
    lines = section_content.split('\n')
    bullet_points = []

    for line in lines:
        line = line.strip()
        if line and (line.startswith('-') or line.startswith('*') or line.startswith('•') or
                     re.match(r'^\d+[\.\)]', line)):
            # Clean the bullet point
            cleaned = re.sub(r'^[-*•\d\.\)]\s*', '', line)
            if cleaned:
                bullet_points.append(cleaned)
        elif line and len(line) < 200 and not line.endswith(':'):  # Avoid section headers
            # Treat as a bullet point if it looks like one
            bullet_points.append(line)

    return bullet_points


def extract_key_responsibilities(text: str) -> List[str]:
    """Extract key responsibilities from the job description."""
    section_headers = [
        'key responsibilities', 'responsibilities', 'what you will do',
        'your responsibilities', 'role responsibilities', 'key duties',
        'job responsibilities', 'duties and responsibilities', 'what youll do'
    ]

    for header in section_headers: headers = headers = [header for header in section_headers if header in text.lower()]

    all_responsibilities = []
    for header in headers:
        responsibilities = extract_bullet_points(text, header)
        all_responsibilities.extend(responsibilities)

    # Remove duplicates while preserving order
    seen = set()
    unique_responsibilities = []
    for resp in all_responsibilities:
        if resp.lower() not in seen:
            seen.add(resp.lower())
            unique_responsibilities.append(resp)

    return unique_responsibilities[:10]  # Limit to top 10


def extract_required_qualifications(text: str) -> List[str]:
    """Extract required qualifications from the job description."""
    section_headers = [
        'required qualifications', 'requirements', 'required skills',
        'qualifications', 'what you need', 'must have', 'required experience',
        'essential requirements', 'minimum qualifications'
    ]

    all_requirements = []
    for header in section_headers:
        requirements = extract_bullet_points(text, header)
        all_requirements.extend(requirements)

    # Remove duplicates while preserving order
    seen = set()
    unique_requirements = []
    for req in all_requirements:
        if req.lower() not in seen:
            seen.add(req.lower())
            unique_requirements.append(req)

    return unique_requirements[:10]  # Limit to top 10


def extract_preferred_qualifications(text: str) -> List[str]:
    """Extract preferred qualifications from the job description."""
    section_headers = [
        'preferred qualifications', 'preferred skills', 'nice to have',
        'desired qualifications', 'preferred experience', 'bonus points',
        'plus', 'preferred', 'desirable'
    ]

    all_preferred = []
    for header in section_headers:
        preferred = extract_bullet_points(text, header)
        all_preferred.extend(preferred)

    # Remove duplicates while preserving order
    seen = set()
    unique_preferred = []
    for pref in all_preferred:
        if pref.lower() not in seen:
            seen.add(pref.lower())
            unique_preferred.append(pref)

    return unique_preferred[:10]  # Limit to top 10


def extract_what_we_offer(text: str) -> List[str]:
    """Extract what the company offers from the job description."""
    section_headers = [
        'what we offer', 'benefits', 'perks', 'compensation and benefits',
        'what youll get', 'we offer', 'our benefits', 'total rewards',
        'compensation', 'benefits package', 'perks and benefits'
    ]

    all_offerings = []
    for header in section_headers:
        offerings = extract_bullet_points(text, header)
        all_offerings.extend(offerings)

    # Remove duplicates while preserving order
    seen = set()
    unique_offerings = []
    for offer in all_offerings:
        if offer.lower() not in seen:
            seen.add(offer.lower())
            unique_offerings.append(offer)

    return unique_offerings[:10]  # Limit to top 10


def analyze_jd(file_content: str) -> dict:
    """
    Analyze a job description file.

    Args:
        file_content: Content of the job description file

    Returns:
        dict: Analyzed job description data matching the JD schema
    """
    # Clean the text
    text = file_content.strip()

    # Extract all required fields
    result = {
        "title": extract_job_title(text),
        "company": extract_company(text),
        "location": extract_location(text),
        "employment_type": extract_employment_type(text),
        "experience_level": extract_experience_level(text),
        "remote_option": extract_remote_option(text),
        "raw_text": text,
        "key_responsibilities": extract_key_responsibilities(text),
        "required_qualifications": extract_required_qualifications(text),
        "preferred_qualifications": extract_preferred_qualifications(text),
        "what_we_offer": extract_what_we_offer(text)
    }

    # Ensure we have at least some basic information
    if not result["title"]:
        # Try to extract from first line
        first_line = text.split('\n')[0].strip()
        if first_line and len(first_line) < 100:
            result["title"] = first_line

    if not result["company"]:
        # Try common patterns
        company_patterns = [
            r'([A-Z][a-zA-Z\s&\.]+(?:\s+Inc\.?|\s+LLC\.?|\s+Ltd\.?|\s+Corp\.?|\s+Corporation|\s+Company))',
            r'join\s+([A-Z][a-zA-Z\s&\.]+)',
            r'([A-Z][a-zA-Z\s&\.]+)\s+is\s+(?:hiring|looking|seeking)'
        ]

        for pattern in company_patterns:
            match = re.search(pattern, text)
            if match:
                result["company"] = match.group(1).strip()
                break

    return result


# For future use - this agent will likely be a class
class JDAnalyzerAgent:
    """JD Analyzer Agent."""

    def __init__(self):
        pass

    def analyze(self, file_content: str):
        """Analyze job description content."""
        return analyze_jd(file_content)
