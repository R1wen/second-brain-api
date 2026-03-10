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


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks


if __name__ == "__main__":
    path = "./test.pdf"
    print("extraction...")
    result = extract_text_from_pdf(path)
    print(f"total characters length: {len(result)}")

    print("chunking...")
    chunks = chunk_text(result)
    print(f"number of chunks : {len(chunks)}")

    if len(chunks) >= 2:
        print(chunks[0][-200:])
        print("----2eme-----\n")
        print(chunks[1][:200])
