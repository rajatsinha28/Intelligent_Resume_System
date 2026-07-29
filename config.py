# Configuration for Resume Optimizer MVP
import os

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
AGENTS_DIR = os.path.join(BASE_DIR, "agents")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
SCHEMAS_DIR = os.path.join(BASE_DIR, "schemas")

# File names
RESUME_FILE = os.path.join(INPUT_DIR, "resume.pdf")
JD_FILE = os.path.join(INPUT_DIR, "jd.txt")

# Supported file types
SUPPORTED_RESUME_TYPES = [".pdf"]
SUPPORTED_JD_TYPES = [".txt", ".pdf"]

# Output settings
OUTPUT_FORMAT = "markdown"  # For MVP, output as markdown preview
OUTPUT_RESUME_NAME = "tailored_resume.md"

# Agent settings (for future use)
AGENT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3