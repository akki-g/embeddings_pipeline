from sqlalchemy import Column, String, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Embedding(Base):
    __tablename__ = 'embeddings'

    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, nullable=False, index=True)  # Added 'document_id
    embedding = Column(Vector(1536))  # Renamed from 'vector' to 'embedding'
    embedding_metadata = Column(JSON)
    document = Column(Text)  # Added 'document' column

    def __repr__(self):
        return f"<Embedding(id={self.id})>"