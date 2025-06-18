# detection/regex_detector.py
import re
from config import SECRET_PATTERNS

compiled = [re.compile(p) for p in SECRET_PATTERNS]

def find_with_regex(text):
    findings = []
    for patt in compiled:
        for match in patt.finditer(text):
            findings.append((patt.pattern, match.group(0)))
    return findings
