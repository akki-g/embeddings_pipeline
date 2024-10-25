from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.request_models import EmbeddingRequest
from app.models.response_models import EmbeddingResponse
from app.services.embedding_service import generate_embeddings
from app.services.embeddings_db_service import store_embeddings, query_embeddings, delete_embeddings, list_embeddings
from app.core.logger import logger  
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/embeddings",
    tags=["embeddings"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=List[EmbeddingResponse], summary="Generate Embedding")
async def generate_embedding(request: EmbeddingRequest, session: AsyncSession = Depends(get_session)):  
    logger.info(f"Received request: {request.id}")
    try:
        document_id, embeddings = await generate_embeddings(
            request.text, 
            request.chunk_size, 
            request.overlap
        )
        logger.info(f"Generated embeddings for request: {request.id}")

        stored_ids = await store_embeddings(
            base_id=request.id,
            document_id=document_id,
            embeddings=embeddings,
            session=session
        )
        logger.info(f"Stored embeddings for request: {request.id}")

        response = [
            EmbeddingResponse(
                id=stored_id,
                document_id=document_id,
                embedding=emb['embedding'],
                document=emb['document'],
                embedding_metadata=emb['embedding_metadata']
            )
            for stored_id, emb in zip(stored_ids, embeddings)
        ]
        logger.info(f"Returning response for request: {request.id}")
        return response
    except Exception as e:
        logger.error(f"Failed to generate embeddings for request: {request.id}")
        print(e)
        logger.error(e)
        raise HTTPException(status_code=500, detail="Failed to generate embeddings")
        
@router.post("/search", response_model=List[EmbeddingResponse], summary="Search Embeddings")
async def search_embeddings(query_embedding: List[float], top_k: int = 10, session: AsyncSession = Depends(get_session)):
    logger.info(f"Received search request")

    try:
        similar_embeddings = await query_embeddings(
            query_embedding=query_embedding,
            top_k=top_k,
            session=session
        )
        response = [
            EmbeddingResponse(
                id=emb.id,
                document_id=emb.document_id,
                embedding=emb.embedding,
                document=emb.document,
                embedding_metadata=emb.embedding_metadata
            )
            for emb in similar_embeddings
        ]
        logger.info(f"Returning response for search request")
        return response
    except Exception as e:
        logger.error(f"Failed to search embeddings")
        logger.error(e)
        raise HTTPException(status_code=500, detail="Failed to search embeddings")