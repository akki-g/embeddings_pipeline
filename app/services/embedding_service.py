import openai
from app.core.config import settings
from app.core.logger import logger
from typing import List
import uuid
import asyncio


client = openai.Client(api_key = settings.OPENAI_API_KEY)

def split_text_into_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:

    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        if end > text_len:
            end = text_len
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

async def generate_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    try:
        text = text.replace("\n", " ")
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: client.embeddings.create(input=text, model=model)
        )
        embedding = response.data[0].embedding
        logger.info(f"Generated embedding for text: {text}")
        return embedding
    except Exception as e:
        logger.error(f"Failed to generate embedding for text: {text}")
        logger.error(e)
        raise


async def generate_embeddings(text: str, chunk_size: int, overlap: int) -> List[dict]:
    document_id = str(uuid.uuid4())
    embeddings = []
    text_len = len(text)
    start = 0

    while start < text_len:
        end = start + chunk_size
        if end > text_len:
            end = text_len
        chunk = text[start:end] 
        chunk_id = f"{start+1}/{len(chunk)}"
        embedding = await generate_embedding(chunk)
        embeddings.append({
            "id": chunk_id,
            "embedding": embedding,
            "document": chunk,
            "document_id": document_id,
            "embedding_metadata": {
                "chunk_id": chunk_id,
                "start": start,
                "end": end,
                "text_len": len(chunk)
            }
        })
        start += chunk_size - overlap
    return document_id, embeddings