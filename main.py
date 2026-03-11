import os

import google.genai as genai
import psycopg2
import pymupdf
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
DB_URL = os.getenv("DATABASE_URL")

client = genai.Client(
    api_key=API_KEY
)


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
    result = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text,
        config={
            "task_type": "RETRIEVAL_DOCUMENT"
        }
    )

    return result.embeddings[0].values


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


def search_similar_chunks(query: str) -> list[str]:

    query_vector = get_embedding(query)

    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    sql = "SELECT content, similarity FROM match_document_chunks(%s,%s,%s);"

    cursor.execute(sql, (str(query_vector), 0.7, 3))
    chunks = cursor.fetchall()

    cursor.close()
    conn.close()

    best_chunks = []
    for chunk in chunks:
        best_chunks.append(chunk[0])

    return best_chunks


if __name__ == "__main__":

    question = "Quel est le sujet principal de ce document?"
    print(f"Searching for answers to: '{question}'...\n")

    results = search_similar_chunks(question)

    if len(results) == 0:
        print("No matches found. Try lowering your 0.7 threshold to 0.5!")
    else:
        print(f"Found {len(results)} highly relevant chunks!")
        for i, text in enumerate(results):
            print(f"\n--- TOP MATCH {i+1} ---")
            print(text[:300] + "...")
