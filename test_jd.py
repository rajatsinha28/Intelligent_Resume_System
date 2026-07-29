#!/usr/bin/env python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agents'))

try:
    from jd_analyzer import extract_location
    print("Import successful!")

    # Test the function
    test_text = "Location: New York, USA"
    result = extract_location(test_text)
    print(f"Test result: '{result}'")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()