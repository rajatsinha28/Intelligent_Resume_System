# Utility helpers for Resume Optimizer MVP
import os
import json
from typing import Dict, Any, Optional
from config import INPUT_DIR, OUTPUT_DIR, TEMP_DIR

def ensure_dir_exists(directory: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    """Load and parse a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file {filepath}: {e}")
        return None

def save_json_file(data: Dict[str, Any], filepath: str) -> bool:
    """Save data as JSON to a file."""
    try:
        # Ensure directory exists
        ensure_dir_exists(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON file {filepath}: {e}")
        return False

def read_text_file(filepath: str) -> Optional[str]:
    """Read text content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def write_text_file(content: str, filepath: str) -> bool:
    """Write text content to a file."""
    try:
        # Ensure directory exists
        ensure_dir_exists(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file {filepath}: {e}")
        return False

def get_file_extension(filepath: str) -> str:
    """Get the file extension in lowercase."""
    return os.path.splitext(filepath)[1].lower()

def is_supported_resume_file(filepath: str) -> bool:
    """Check if file is a supported resume format."""
    from config import SUPPORTED_RESUME_TYPES
    return get_file_extension(filepath) in SUPPORTED_RESUME_TYPES

def is_supported_jd_file(filepath: str) -> bool:
    """Check if file is a supported job description format."""
    from config import SUPPORTED_JD_TYPES
    return get_file_extension(filepath) in SUPPORTED_JD_TYPES