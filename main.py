import os

import google.generativeai as genai
import psycopg2
import pymupdf
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
DB_URL = os.getenv("DATABASE_URL")

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


def save_to_database(content: str, embedding: list[float]):

    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    sql = """
        INSERT INTO document_chunks (content, embedding)
        VALUES (%s, %s);
    """

    cursor.execute(sql, (content, str(embedding)))

    conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    path = "./test.pdf"
    print("extraction...")
    result = extract_text_from_pdf(path)
    print(f"total characters length: {len(result)}")

    print("chunking...")
    chunks = chunk_text(result)
    print(f"number of chunks : {len(chunks)}")

    if len(chunks) > 0:
        print(f"Preparing to process {len(chunks)} chunks...")
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i + 1}/{len(chunks)}...")

            vector = get_embedding(chunk)
            save_to_database(chunk, vector)

        print("Success! All chunks are securely stored in the Supabase vector database.")
