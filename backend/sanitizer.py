from typing import List, Tuple
from backend.detectors import Finding, detect_secrets

PLACEHOLDERS = {
    "PRIVATE_KEY_BLOCK": "<PRIVATE_KEY_BLOCK>",
    "JWT_TOKEN": "<JWT_TOKEN>",
    "BEARER_TOKEN": "Authorization: Bearer <TOKEN>",
    "GITHUB_TOKEN": "<GITHUB_TOKEN>",
    "OPENAI_API_KEY": "<API_KEY>",
    "AWS_ACCESS_KEY": "<AWS_ACCESS_KEY>",
    "DATABASE_URL": "<DATABASE_URL>",
    "PASSWORD_ASSIGNMENT": "<SECRET_ASSIGNMENT>",
    "EMAIL": "<EMAIL>",
    "PRIVATE_IP": "<PRIVATE_IP>",
    "IP_ADDRESS": "<IP_ADDRESS>",
    "LOCAL_PATH": "<LOCAL_PATH>",
    "COOKIE": "<COOKIE_HEADER>",
}


def mask_text(text: str) -> Tuple[str, List[Finding]]:
    findings = detect_secrets(text)

    if not findings:
        return text, []

    filtered: List[Finding] = []
    last_end = -1

    for finding in findings:
        if finding.start >= last_end:
            filtered.append(finding)
            last_end = finding.end

    masked_parts = []
    current = 0

    for finding in filtered:
        masked_parts.append(text[current:finding.start])
        masked_parts.append(PLACEHOLDERS.get(finding.label, f"<{finding.label}>"))
        current = finding.end

    masked_parts.append(text[current:])

    return "".join(masked_parts), filtered
