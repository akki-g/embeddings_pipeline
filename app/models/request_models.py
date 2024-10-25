from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class EmbeddingRequest(BaseModel):

    id: str = Field(
        ...,
        title="Unique ID",
        description="A unique identifier for the embedding",
        example="1234"
    )
    document: str = Field( 
        ...,
        title="Document",
        description="The document to be embedded",
        example="This is an example document"
    )
    text: str = Field(
        ...,
        title="Text",
        description="The text to be embedded",
        example="This is an example sentence"
    )
    embedding_metadata: Optional[dict] = Field(
        None,
        title="Metadata",
        description="Additional metadata to store with the embedding",
        example={"key": "value"}
    )
    chunk_size: int = Field(
        1000,
        title="Chunk Size",
        description="The number of characters to process at a time",
        example=1000
    )
    overlap: int = Field(
        100,
        title="Overlap Size",
        description="The number of characters to overlap between chunks",
        example=100
    )
        
    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234",
                'document': "This is an example document",
                "text": "This is an example sentence",
                "embedding_metadata": {"key": "value"}
            },
            "chunk_size": 1000,
            "overlap": 100
        }