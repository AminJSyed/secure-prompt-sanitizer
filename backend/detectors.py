import re
from dataclasses import dataclass
from typing import List


@dataclass
class Finding:
    label: str
    value: str
    start: int
    end: int


PATTERNS = [
    ("PRIVATE_KEY_BLOCK", r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"),
    ("BEARER_TOKEN", r"(?i)\bAuthorization:\s*Bearer\s+[A-Za-z0-9._~+/=-]+"),
    ("JWT_TOKEN", r"\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b"),
    ("GITHUB_TOKEN", r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    ("OPENAI_API_KEY", r"\bsk-[A-Za-z0-9]{20,}\b"),
    ("AWS_ACCESS_KEY", r"\bAKIA[0-9A-Z]{16}\b"),
    ("DATABASE_URL", r"\b(?:postgres|postgresql|mysql|mongodb|redis)://[^\s\"']+"),
    ("PASSWORD_ASSIGNMENT", r"(?i)\b(password|passwd|pwd|secret|token|api_key|apikey)\s*[:=]\s*[^\s\"']+"),
    ("EMAIL", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    ("PRIVATE_IP", r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"),
    ("IP_ADDRESS", r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    ("LOCAL_PATH", r"(/Users/[^ \n\t]+|/home/[^ \n\t]+|C:\\\\Users\\\\[^ \n\t]+)"),
    ("COOKIE", r"(?i)\b(cookie|set-cookie):\s*[^\n]+"),
]


def detect_secrets(text: str) -> List[Finding]:
    findings: List[Finding] = []

    for label, pattern in PATTERNS:
        for match in re.finditer(pattern, text):
            findings.append(
                Finding(
                    label=label,
                    value=match.group(0),
                    start=match.start(),
                    end=match.end(),
                )
            )

    findings.sort(key=lambda x: x.start)
    return findings
