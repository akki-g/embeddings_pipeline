from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import embeddings
from app.core.logger import logger 
import uvicorn

app = FastAPI(
    title="Embeddings API",
    description="API for embeddings",
    version="0.1",
    debug=True
)
origins = [
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,            # Allow cookies and authentication headers
    allow_methods=["*"],               # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],               # Allow all headers
)

app.include_router(
    embeddings.router,
    prefix="/embeddings",
    tags=["Embeddings"],
    responses={404: {"description": "Not Found"}}
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Embeddings Pipeline API is up and running!"}

@app.on_event("startup")
async def startup_event():
    # Initialize the database
    logger.info("Embeddings API is starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    # Close the database
    logger.info("Embeddings API is shutting down...")

if __name__ == "__main__":
    import uvicorn
    if __name__ == "__main__":
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )