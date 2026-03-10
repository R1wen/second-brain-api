import os

import google.generativeai as genai
import pymupdf
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)


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


def get_embedding(text: str) -> list[float]:
    result = genai.embed_content(
        model="models/gemini-embedding-001",
        content=text,
        task_type="retrieval_document"
    )

    return result['embedding']


if __name__ == "__main__":
    path = "./test.pdf"
    print("extraction...")
    result = extract_text_from_pdf(path)
    print(f"total characters length: {len(result)}")

    print("chunking...")
    chunks = chunk_text(result)
    print(f"number of chunks : {len(chunks)}")

    if len(chunks) > 0:
        print("\nSending the first chunk to Gemini to get its embedding...")
        first_chunk = chunks[0]
        vector = get_embedding(first_chunk)
        print("The first 5 numbers of that vector:")
        print(vector[:5])
