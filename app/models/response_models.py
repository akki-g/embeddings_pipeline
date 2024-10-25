from pydantic import BaseModel, Field

class EmbeddingResponse(BaseModel):
    id: str = Field(
        title="Unique ID",
        description="A unique identifier for the embedding",
        example="1234"
    )
    document_id: str = Field(
        title="Document ID",
        description="The identifier for the entire document",
        example="doc_5678"
    )
    document: str = Field( 
        ...,
        title="Document",
        description="The document to be embedded",
        example="This is an example document"
    )
    embedding: list = Field(
        title="Embedding",
        description="The vector representation of the text",
        example=[0.1, 0.2, 0.3]
    )
    embedding_metadata: dict = Field(
        title="Metadata",
        description="Additional metadata stored with the embedding",
        example={"key": "value"}
    )
    class Config:
        json_schema_extra = {
            "example": {
                "id": "1234",
                'document': "This is an example document",
                "document_id": "doc_5678",
                "embedding": [0.1, 0.2, 0.3],
                "embedding_metadata": {"key": "value"}
            }
        }