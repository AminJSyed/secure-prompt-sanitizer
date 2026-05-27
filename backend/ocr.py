from PIL import Image
import pytesseract


def extract_text_from_image(image_input) -> str:
    try:
        if isinstance(image_input, Image.Image):
            image = image_input
        else:
            image = Image.open(image_input)

        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as error:
        return f"OCR_ERROR: {error}"