import os

import pymupdf
from dotenv import load_dotenv

load_dotenv()


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    doc = pymupdf.open(file_path)
    for page in doc:
        text += page.get_text()
    return text


if __name__ == "__main__":
    path = "./test.pdf"
    result = extract_text_from_pdf(path)
    print(result)
