from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.sanitizer import mask_text
from backend.prompt_generator import generate_safe_query
from backend.ocr import extract_text_from_image


app = FastAPI(title="Secure Prompt Sanitizer API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://secureprompt.local:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def apply_manual_masks(text: str, manual_masks: str) -> str:
    manual_values = [value.strip() for value in manual_masks.splitlines() if value.strip()]

    for value in manual_values:
        text = text.replace(value, "<MANUAL_MASK>")

    return text

@app.get("/")
def root():
    return {
        "name": "Secure Prompt Sanitizer API",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/sanitize")
async def sanitize(
    text: str = Form(default=""),
    user_goal: str = Form(default=""),
    manual_masks: str = Form(default=""),
    files: List[UploadFile] = File(default=[]),
):
    image_text_blocks = []
    file_text_blocks = []

    for uploaded_file in files:
        file_name = uploaded_file.filename or "uploaded-file"
        lower_name = file_name.lower()

        if lower_name.endswith((".png", ".jpg", ".jpeg", ".webp")):
            extracted_text = extract_text_from_image(uploaded_file.file)
            image_text_blocks.append(
                f"--- OCR text from image: {file_name} ---\n{extracted_text}"
            )

        elif lower_name.endswith((".txt", ".log", ".json", ".yaml", ".yml", ".env")):
            raw_bytes = await uploaded_file.read()
            file_text = raw_bytes.decode("utf-8", errors="replace")
            file_text_blocks.append(
                f"--- Text from file: {file_name} ---\n{file_text}"
            )

        else:
            file_text_blocks.append(
                f"--- Unsupported file skipped: {file_name} ---"
            )

    combined_input = text or ""

    if file_text_blocks:
        combined_input += "\n\n" + "\n\n".join(file_text_blocks)

    if image_text_blocks:
        combined_input += "\n\n" + "\n\n".join(image_text_blocks)

    if not combined_input.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide text or upload at least one supported file."
        )

    sanitized_text, findings = mask_text(combined_input)
    sanitized_text = apply_manual_masks(sanitized_text, manual_masks)

    safe_query = generate_safe_query(sanitized_text, user_goal)

    return {
        "combined_input": combined_input,
        "sanitized_text": sanitized_text,
        "safe_query": safe_query,
        "findings": [
            {
                "type": finding.label,
                "preview": finding.value[:100],
            }
            for finding in findings
        ],
    }