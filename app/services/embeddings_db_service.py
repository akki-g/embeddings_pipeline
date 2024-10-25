from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy import func
from app.models.models import Embedding
from app.core.database import get_session
from app.core.logger import logger
from typing import List, Dict
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends

async def store_embeddings(base_id: str, document_id: str, embeddings: List[Dict], session: AsyncSession) -> List[str]:

    try:
        stored_ids = []
        for emb in embeddings:
            start = emb['embedding_metadata']['start']
            end = emb['embedding_metadata']['end']
            emb_id = f"{base_id}-{document_id}-{start}-{end}"
            embedding_entry = Embedding(
                id=emb_id,
                document_id=document_id,
                embedding=emb['embedding'],
                embedding_metadata=emb.get('embedding_metadata', {}),
                document = emb['document']
            )
            session.add(embedding_entry)
            stored_ids.append(emb_id)

        await session.commit()
        logger.info(f"Stored embedding: {emb_id}")
        return stored_ids
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Error storing embeddings in PostgreSQL: {e}")
        raise

async def query_embeddings(query_embedding: List[float], top_k: int = 10, session: AsyncSession = Depends(get_session)) -> List[Embedding]:

    try:
        stmt = (
            select(Embedding)
            .order_by(func.similarity(Embedding.embedding, query_embedding).desc())
            .limit(top_k)
        )
        result = await session.execute(stmt)
        embeddings = result.scalars().all()
        logger.info(f"Query embeddings: {embeddings}")
        return embeddings
    except SQLAlchemyError as e:
        logger.error(f"Error querying embeddings in PostgreSQL: {e}")
        raise

async def delete_embeddings(document_id: str, session: AsyncSession = Depends(get_session)) -> None:

    try: 
        stmt = delete(Embedding).where(Embedding.document_id == document_id)
        await session.execute(stmt)
        await session.commit()
        logger.info(f"Deleted embeddings for document: {document_id}")
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Error deleting embeddings in PostgreSQL: {e}")
        raise

async def list_embeddings(session: AsyncSession)-> List[Embedding]:

    try:
        stmt = select(Embedding)
        result = await session.execute(stmt)
        embeddings = result.scalars().all()
        logger.info(f"List embeddings: {embeddings}")
        return embeddings
    except SQLAlchemyError as e:
        logger.error(f"Error listing embeddings in PostgreSQL: {e}")
        raise