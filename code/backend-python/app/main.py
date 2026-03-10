import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

app = FastAPI(
    title="TechWatch AI - Worker Service",
    description="Python microservice handling web scraping and RAG/AI processing",
    version="1.0.0"
)

# CORS Configuration
# TODO: Restrict allowed origins for production deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    """Health check endpoint to verify service status."""
    return {
        "status": "online",
        "service": "techwatch-ai-worker",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)